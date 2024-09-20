import time

from flask import Flask, request, jsonify, abort, make_response, url_for
import json
import os
import requests
from flask_cors import CORS
from gradio.themes.utils.colors import neutral

from functions import Speech_to_text_by_SenseVoice_small
from functions import Recognize_who_is_speaking
from functions.Speech_to_text_by_SenseVoice_small import stt
from functions.send_to_BERT import ask_questions_to_BERT
from functions.send_to_ChatGLM import chat_with_chatglm6b
from functions.read_json_file import read_json_file
from pydub import AudioSegment

# 配置文件路径
config_path = 'config.json'
# 检查配置文件是否存在，如果不存在则创建
if not os.path.exists(config_path):
    with open(config_path, 'w') as f:
        json.dump({"speaker_counter": 1}, f)

# 全局变量来跟踪用户编号
speaker_counter = 1
speaker_directory = "Register_Audio_Resource"
profile_json_path = os.path.join(speaker_directory, "speaker_profiles.json")

# 读取配置文件中的 speaker_counter
with open(config_path, 'r') as f:
    config_data = json.load(f)
    speaker_counter = config_data['speaker_counter']

if not os.path.exists(speaker_directory):
    os.makedirs(speaker_directory)

#全局变量跟踪是否是第一次发送prompt
#初始话一个空的字典
def initialize_json_file(file_path):
    data = {}
    with open(file_path, 'w') as file:
        json.dump(data, file)
        print("初始化 JSON 文件，现在prompt_status是一个空的字典.")

prompt_status_file_path = 'prompt_status.json'
initialize_json_file(prompt_status_file_path)
# bert和ChatGLM 的服务端的地址
bert_url = 'http://127.0.0.1:5001/receive-texts'
chat_glm_url = 'http://127.0.0.1:5004//posttext'
app = Flask(__name__)
CORS(app)

@app.route('/')
def api_root():
    return 'Welcome to the RESTful API'

@app.route('/input_audio', methods=['POST'])
def turn_audio_into_txt():
    #测试前后端交互
    # result = {'status': 'success', 'text': "TESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTESTTEST"}
    # return jsonify(result)

    #下面这段是通用文字接受段
    # 检查请求中是否包含文件部分
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    audio_file = request.files['file']

    #测试用
    # print(type(audio_file))
    # print(audio_file)

    # 如果用户没有选择文件
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    save_file_dir = "tmp_audio_resource\\turn_audio_into_text_tmp.m4a"
    audio_file.save(save_file_dir)
    #接受文件结束



    debug_mode = True
    print("Debug_Mode:{}".format(debug_mode))
    if not debug_mode:

        #接下来是对文字进行处理
        word,emo = Speech_to_text_by_SenseVoice_small.stt(save_file_dir,need_emo=True)

        speaker_id = Recognize_who_is_speaking.compare_speakers(save_file_dir)
        print("Speaker_id:{}".format(speaker_id))
    # if debug_mode:
    #     word = "我今天应该吃什么"
    #     speaker_id = 1
    #     emo = "neutral"
    if debug_mode:
        word = "我想学一首新的吉他曲目，有什么适合初学者的经典歌曲推荐吗？"
        # speaker_id = Recognize_who_is_speaking.compare_speakers(save_file_dir)
        speaker_id = 3
        print("Speaker_id:{}".format(speaker_id))
        emo = "neutral"


    #大改前最后一个版本的稳定版修改
    with open('/home/ma-user/work/smart_assistant_backend/Register_Audio_Resource/speaker_profiles.json', 'r', encoding='utf-8') as file:
        data = file.read()
    data_dict = json.loads(data)
    speaker_id_search_id = "speaker_"+str(speaker_id)
    print("Speaker_ID:{}".format(speaker_id_search_id))
    #下面这一行有speaker_profile
    speaker_profile = data_dict[speaker_id_search_id]["text"]
    print("Speaker_profile:{}".format(speaker_profile))

    prompt_status_dict = read_json_file(prompt_status_file_path)
    if speaker_id_search_id not in prompt_status_dict:

        print("第一次输入prompt分支")
        prompt_status_dict[speaker_id_search_id] = True
        with open(prompt_status_file_path, 'w', encoding='utf-8') as file:
            json.dump(prompt_status_dict, file)

        # word 是说话的文字 emo是说话时包含的感情 speaker_id_search_id 表示是谁在说话 speaker_profile 表示说话的人的描述
        # 截止到现在 有用的变量有speaker_profile word emo

        # 接下来丢给bert
        input_to_bert_cn = "一个人说了：" + str(word)
        # 先进行翻译
        # 先放一下
        print("翻译成英语")
        input_to_bert = chat_with_chatglm6b(chat_glm_url, str(input_to_bert_cn) + "\n把刚刚的这段话翻译成英语")
        # analyze_question = ("Analyze this statement. What is the purpose of the person making this statement?"+
        #                     "What are his additional conditions?")
        analyze_question = ("What is the primary purpose or intention of the speaker's statement?")

        ans_from_bert = ask_questions_to_BERT(bert_url, input_to_bert, str(analyze_question))  # 现在是英语

        # 翻译回中文
        print("翻译成中文")
        cn_analysis = chat_with_chatglm6b(chat_glm_url, ans_from_bert + "\n把刚刚的这段话翻译成简体中文")

        # bert部分结束
        ERA_frame_prompt = """
        我们希望智能家居助手能够根据说话人的当前输入、之前的自我介绍以及BERT对说话人的发言总结的内容，生成一段合适的对话内容。这段对话应该能够自然地回应说话人的问题或请求，并且展示对说话人背景的理解。

        请你担任一名智能家居助手，具备理解和回应说话人需求的能力。你需要根据提供的信息，对输入做出合适的、有人情味的回答。

        请你完成以下任务：

        根据说话人的当前输入、之前的自我介绍以及BERT推理出的内容，做出合适的、有人情味的回答，不需要说出像“根据你的自我介绍和BERT分析出的内容”这样的词。
        1.确保对话内容能够准确回应说话人的问题或请求，在回答的时候结合对于说话人背景进行回答，但是比重不要太大。
        2.对话内容应简洁明了，不超过100字。
        3.**不要说**“根据你的自我介绍和BERT分析出的内容”这样的内容。

        """
        input_to_chatglm = ERA_frame_prompt + "\n" \
                           + "说话人说的话：" + word + "\n" \
                         "说话人的意图是：" + cn_analysis + "\n" \
                        "说话人的自我介绍：" + str(
                speaker_profile)
        print("input_to_chatglm is:{}".format(input_to_chatglm))
        ans_from_chatglm = chat_with_chatglm6b(chat_glm_url, input_to_chatglm)
        print("ans_from_chatglm is:{}".format(ans_from_chatglm))

    else:
        print("直接把word给它")
        ans_from_chatglm = chat_with_chatglm6b(chat_glm_url,word)

    result = {'status': 'success', 'text': ans_from_chatglm}
    return jsonify(result)

@app.route('/register_speaker', methods=['POST'])
def register_a_person():
    global speaker_counter
    # 检查请求中是否包含文件部分
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    audio_file = request.files['file']
    # 如果用户没有选择文件
    if audio_file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # 生成有规律的文件名
    audio_file_path = os.path.join(speaker_directory, f"speaker_{speaker_counter}.m4a")
    audio_file.save(audio_file_path)

    audio = AudioSegment.from_file(audio_file_path, format="m4a")
    audio = audio.set_frame_rate(16000)

    audio_file_path = os.path.join(speaker_directory, f"speaker_{speaker_counter}.wav")

    audio.export(audio_file_path, format="wav")

    # 将处理后的音频保存为临时 wav 文件
    # temp_wav_path = "temp.wav"
    # audio.export(temp_wav_path, format="wav")


    # 转换音频文件为文本
    text,emo = Speech_to_text_by_SenseVoice_small.stt(audio_file_path,need_emo=True)

    # 存储音频文件转文字之后的内容
    speaker_profile = {
        "audio_file_path": audio_file_path,
        "text": text
    }

    # 更新用户编号
    speaker_counter += 1

    # 将更新后的 speaker_counter 写回配置文件
    with open(config_path, 'w') as f:
        json.dump({"speaker_counter": speaker_counter}, f)

    # 将角色表述和相关信息保存为 JSON 文件
    try:
        with open(profile_json_path, 'r') as f:
            profiles = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        profiles = {}
    profiles[f"speaker_{speaker_counter - 1}"] = speaker_profile
    with open(profile_json_path, 'w') as f:
        json.dump(profiles, f, indent=4)

    # 返回成功录入的响应
    return jsonify({"message": "Speaker registered successfully", "profile": speaker_profile}), 201
    #audio_file 是上传上来的音频文件 现在在内存中 还没有到存储中 想要调用Speech_to_text_by_SenseVoice只能给出音频的本地地址
    #存储音频文件，存储在Register_Audio_Resource  用来比对
    #存储音频文件转文字之后的内容 即角色表述 （id_profile）（角色表述使用Speech_to_text_by_SenseVoice转文字存储）
    #给文件合适的取名来匹配音频文件和json文件中的内容（id）  可以用字典保存 然后保存为json
    #返回成功录入
@app.route('/test-internet')
def test_internet():
    try:
        response = requests.get('http://www.google.com')
        return f"Internet access successful: {response.status_code}"
    except requests.RequestException as e:
        return f"Internet access failed: {str(e)}"
@app.route('/test', methods=['GET'])
def test():
    # 创建一个示例 JSON 响应
    response_data = {
        'message': 'Hello, World!',
        'status': 'success',
        'data': {
            'key1': 'value1',
            'key2': 'value2'
        }
    }

    # 返回 JSON 响应
    return jsonify(response_data)
if __name__ == '__main__':
    app.run(debug=True,port=5000)
