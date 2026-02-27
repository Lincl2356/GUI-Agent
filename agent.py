import base64
import io
import json
import time
import yaml
import pyautogui
import pyperclip
from PIL import Image
from openai import OpenAI


class ScreenAgent:
    def __init__(self, config_path: str = "config.yaml"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)
        
        self.client = OpenAI(
            base_url=self.config["openai"]["base_url"],
            api_key=self.config["openai"]["api_key"]
        )
        self.model = self.config["openai"]["model"]
        self.max_iterations = self.config["execution"]["max_iterations"]
        self.delay = self.config["execution"]["delay_between_actions"]
        self.loop_delay = self.config["execution"]["delay_between_loops"]
        self.quality = self.config["execution"]["screenshot_quality"]
        
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.1
        
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"屏幕分辨率：{self.screen_width}x{self.screen_height}")
    
    def take_screenshot(self) -> str:
        screenshot = pyautogui.screenshot()
        buffer = io.BytesIO()
        screenshot.save(buffer, format="PNG", quality=self.quality, optimize=True)
        return base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    def normalize_coords(self, x: float, y: float) -> tuple:
        real_x = int(x * self.screen_width)
        real_y = int(y * self.screen_height)
        return real_x, real_y
    
    def execute_action(self, action: dict) -> str:
        action_type = action.get("type")
        params = action.get("params", {})
        
        print(f"执行操作：{action_type}")
        
        try:
            if action_type == "click":
                x, y = self.normalize_coords(params["x"], params["y"])
                button = params.get("button", "left")
                pyautogui.click(x, y, button=button)
                return f"点击 ({x}, {y}) {button}键"
            
            elif action_type == "double_click":
                x, y = self.normalize_coords(params["x"], params["y"])
                pyautogui.doubleClick(x, y)
                return f"双击 ({x}, {y})"
            
            elif action_type == "drag":
                start_x, start_y = self.normalize_coords(params["start_x"], params["start_y"])
                end_x, end_y = self.normalize_coords(params["end_x"], params["end_y"])
                pyautogui.moveTo(start_x, start_y)
                pyautogui.mouseDown(button="left")
                pyautogui.moveTo(end_x, end_y, duration=0.3)
                pyautogui.mouseUp(button="left")
                return f"拖拽从 ({start_x}, {start_y}) 到 ({end_x}, {end_y})"
            
            elif action_type == "type":
                text = params["text"]
                pyperclip.copy(text)
                time.sleep(0.1)
                pyautogui.hotkey("ctrl", "v")
                return f"输入文本：{text[:50]}..." if len(text) > 50 else f"输入文本：{text}"
            
            elif action_type == "hotkey":
                keys = params["keys"]
                pyautogui.hotkey(*keys)
                return f"快捷键：{'+'.join(keys)}"
            
            elif action_type == "scroll":
                x, y = self.normalize_coords(params["x"], params["y"])
                amount = params["amount"]
                pyautogui.moveTo(x, y)
                pyautogui.scroll(amount * 100)
                direction = "向上" if amount > 0 else "向下"
                return f"滚动 {direction} {abs(amount)} 格"
            
            elif action_type == "wait":
                seconds = params["seconds"]
                time.sleep(seconds)
                return f"等待 {seconds} 秒"
            
            elif action_type == "done":
                result = params.get("result", "任务完成")
                return f"任务完成：{result}"
            
            else:
                return f"未知操作类型：{action_type}"
        
        except Exception as e:
            return f"操作执行失败：{str(e)}"
    
    def run(self, user_task: str):
        messages = [
            {
                "role": "system",
                "content": open("system_prompt.txt", "r", encoding="utf-8").read()
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"请完成以下任务：{user_task}"
                    }
                ]
            }
        ]
        
        iteration = 0
        print(f"\n开始执行任务：{user_task}\n")
        
        while iteration < self.max_iterations:
            iteration += 1
            print(f"=== 第 {iteration} 次循环 ===")
            
            screenshot_base64 = self.take_screenshot()
            
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"当前截图如下。请分析屏幕内容并决定下一步操作。"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{screenshot_base64}"
                        }
                    }
                ]
            })
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1000
            )
            
            assistant_message = response.choices[0].message.content
            if assistant_message is None:
                print("AI 返回空消息，跳过本次循环")
                continue
            
            messages.append({"role": "assistant", "content": assistant_message})
            
            print(f"AI 思考：{assistant_message[:200]}...")
            
            response_json = None
            try:
                response_json = json.loads(assistant_message)
            except json.JSONDecodeError:
                start = assistant_message.find("{")
                end = assistant_message.rfind("}") + 1
                if start != -1 and end > start:
                    try:
                        response_json = json.loads(assistant_message[start:end])
                    except json.JSONDecodeError:
                        pass
            
            if response_json is None:
                print("无法解析 AI 响应，跳过本次循环")
                continue
            
            thought = response_json.get("thought", "")
            action = response_json.get("action", {})
            task_complete = response_json.get("task_complete", False)
            completion_reason = response_json.get("completion_reason", "")
            
            print(f"思考：{thought}")
            
            result = self.execute_action(action)
            print(f"结果：{result}\n")
            
            if action.get("type") == "done" or task_complete:
                print(f"\n任务已完成：{completion_reason or result}")
                break
            
            time.sleep(self.loop_delay)
        
        if iteration >= self.max_iterations:
            print(f"\n达到最大循环次数 ({self.max_iterations})，任务终止")


def main():
    print("=" * 50)
    print("电脑操作 Agent")
    print("=" * 50)
    
    agent = ScreenAgent()
    
    print("\n请输入任务（输入 'quit' 退出）：")
    
    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ["quit", "exit", "q"]:
            print("再见！")
            break
        if user_input:
            agent.run(user_input)


if __name__ == "__main__":
    main()
