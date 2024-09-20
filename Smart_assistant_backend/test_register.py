import requests

# 服务器的 URL
url = 'http://127.0.0.1:5000/register_speaker'

# 音频文件路径
audio_file_path = '/home/ma-user/work/smart_assistant_backend/tmp_register_resource/Test_Speaker_1.m4a'

# 打开文件
with open(audio_file_path, 'rb') as audio_file:
    # 使用 POST 请求上传文件
    response = requests.post(url, files={'file': audio_file})

# 检查响应状态码
if response.status_code == 200:
    print("文件上传成功")
else:
    print(f"文件上传失败，状态码: {response.status_code}")