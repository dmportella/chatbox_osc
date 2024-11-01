[![coverage](https://gitlab.com/ameliend/chatbox_osc/badges/main/coverage.svg)](https://gitlab.com/ameliend/chatbox_osc/-/commits/main)
[![vscode-editor](https://badgen.net/badge/icon/visualstudio?icon=visualstudio&label)](https://code.visualstudio.com/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)
[![API Documentation](https://badgen.net/badge/icon/API%20documentation?icon=gitlab&label&color=cyan)](https://ameliend.gitlab.io/chatbox_osc/)

# Chatbox OSC

<p align="center">
  <img src="./resources/logo.png">
</p>

A python library to control your VRChat Chatbox, which can be used as a module or simply on the command line.

## ⚙️ Installation

1. Clone the repository by running the following command in your terminal:

```shell
git clone https://gitlab.com/ameliend/chatbox_osc.git
```

2. Navigate to the cloned directory using the cd command:

```shell
cd chatbox_osc
```

3. Install the package using `pip`:

```shell
pip install .
```

## 🚀 Usage

### 💻 Command Line

Use the following command-line interface syntax to run the script from the command
line:

```shell
chatbox_osc [OPTIONS]
```

* -m, --msg: Specify the message to write in the chatbox. This should be a string.

* -d, --delay: An optional delay (in seconds) before sending the message.
This will create a "writing dot" animation, giving the appearance that the message
is being written manually. If this option is not given, then the default value is 0.

* -cl, --chunk-length: Specify the chunk length for the "writing" animation.
The message will be split into chunks and written one by one, creating a ChatGPT-like
animation effect. ✨ New in version [1.4.0](https://gitlab.com/ameliend/chatbox_osc/compare/v1.3.1...v1.4.0), at the end of the typing animation, this will trigger
the Chatbox SFX. If the chunk length is set to 0, the entire message will be written
directly without any animation style. If this option is not given, then the default
chunk length is 25.

* -f, --font: Choose a font to customize the appearance of the written text.
The default font is None, which uses the default font.
Available fonts are:
- UwU
- Normal
- Wide
- SmallCaps
- Squared
- Circled
- Parenthesized
- Boxed
- Blue
- HeavyCircled
- Curly
- Currency
- Magic
- Wiry
- UpsideDown
- Superscript

Here's an example command that demonstrates the usage of chatbox_osc:

```shell
chatbox_osc --msg "Hello, world!" --delay 1 --chunk-length 25 --font Magic
```

This command will send the message "Hello, world!" to the chatbox with a delay of 1
second, using a chunk length of 25 characters per animation frame,
and using the Magic font.

### 🐍 Python Module

Import the chatbox_osc module with pythonosc's SimpleUDPClient.
This will send the message "Hello, world!" to the chatbox with a delay of 1
second, using a chunk length of 25 characters per animation frame,
and using the Magic font.

```python
from pythonosc.udp_client import SimpleUDPClient

from chatbox_osc import write_chatbox

# Create a VRChat OSC client
client = SimpleUDPClient("127.0.0.1", 9000)

# Write a message to the VRChat Chatbox with the "Magic" font
write_chatbox(client, message="Hello, world!", delay=1, chunk_length=25, font="Magic")

# You can also clear the current message in the VRChat Chatbox
write_chatbox(client, message=None)
```
