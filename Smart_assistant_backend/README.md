# 声控未来家后端服务

---

## 安装环境

首先安装所需的依赖项：

```bash
pip install -r requirements.txt
```

此外，还需要安装 ffmpeg 包来处理音频文件。安装方法取决于你的操作系统：

对于Linux和MacOS:
```bash
sudo apt-get install ffmpeg # 对于Debian/Ubuntu
brew install ffmpeg  
```

打开Flask服务端
```bash
python app.py
```

项目中文件解释：
function目录中存放了各个函数
    Recognize_who_is_speaking.py  声纹识别
    send_to_BERT.py  向BERT服务端发送信息
    send_to_ChatGLM.py 向ChatGLM服务端发送信息
    Speech_to_text_by_SenseVoice_small.py 语音转文字模块
    Clear_ChatGLM_history.py 清除微调后的ChatGLM
    read_json_file.py   读取json文件

Register_Audio_Resource目录中存放已经注册了的家庭成员的声音 
    其中的speaker_profiles.json  存放了家庭成员们的自我介绍信息

tmp_audio_resource文件夹保存从前端网页端传入的临时音频文件，以便后续的处理

tmp_register_resource文件夹保存了以前测试用的文件

config.json用来跟踪已经注册的家庭成员数量

测试Flask接口的脚本。
