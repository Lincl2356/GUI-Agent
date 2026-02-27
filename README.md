# 电脑操作 Agent

基于视觉的电脑自动化操作 Agent，使用多模态 AI 理解屏幕内容并执行操作。

## 功能特点

- 屏幕截图理解
- AI 任务规划和决策
- 自动鼠标操作（点击、拖拽、滚动）
- 键盘输入（剪贴板注入）
- 截图 - 思考 - 操作循环

## 文件说明

| 文件 | 说明 |
|------|------|
| `agent.py` | 主程序 |
| `config.yaml` | 配置文件（需填写 API key） |
| `config.yaml.example` | 配置模板 |
| `system_prompt.txt` | 系统提示词 |
| `requirements.txt` | Python 依赖 |
| `.gitignore` | Git 忽略配置 |

## 安装

```bash
pip install -r requirements.txt
```

## 配置

复制配置模板并填写 API 信息：

```bash
copy config.yaml.example config.yaml
```

编辑 `config.yaml`：

```yaml
openai:
  base_url: "https://api.openai.com/v1"
  api_key: "your-api-key-here"
  model: "gpt-4o"
```

## 运行

```bash
python agent.py
```

输入任务指令，例如：
- "打开记事本并输入 Hello World"
- "打开浏览器访问 google.com"

## 支持的操作

| 操作 | 说明 |
|------|------|
| click | 鼠标点击 |
| double_click | 双击 |
| drag | 拖拽 |
| type | 键盘输入（剪贴板注入） |
| hotkey | 快捷键 |
| scroll | 滚动 |
| wait | 等待 |
| done | 任务完成 |


## 许可证

MIT

---

# Desktop Automation Agent

A vision-based desktop automation agent that uses multimodal AI to understand screen content and execute operations.

## Features

- Screen capture and understanding
- AI task planning and decision making
- Automatic mouse operations (click, drag, scroll)
- Keyboard input via clipboard injection
- Screenshot-think-act loop

## File Structure

| File | Description |
|------|-------------|
| `agent.py` | Main program |
| `config.yaml` | Configuration file (requires API key) |
| `config.yaml.example` | Configuration template |
| `system_prompt.txt` | System prompt |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Git ignore configuration |

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Copy the config template and fill in your API credentials:

```bash
cp config.yaml.example config.yaml
```

Edit `config.yaml`:

```yaml
openai:
  base_url: "https://api.openai.com/v1"
  api_key: "your-api-key-here"
  model: "gpt-4o"
```

## Usage

```bash
python agent.py
```

Enter task commands, for example:
- "Open Notepad and type Hello World"
- "Open browser and visit google.com"

## Supported Operations

| Operation | Description |
|-----------|-------------|
| click | Mouse click |
| double_click | Double click |
| drag | Drag operation |
| type | Keyboard input (clipboard injection) |
| hotkey | Keyboard shortcut |
| scroll | Scroll |
| wait | Wait |
| done | Task complete |


## License

MIT
