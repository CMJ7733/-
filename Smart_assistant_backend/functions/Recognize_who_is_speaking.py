#接受一个音频输入
#输出一个讲话人的内部id
import subprocess

from modelscope.pipelines import pipeline
from pydub import AudioSegment
import os

def compare_speakers(m4a_file_path, wav_folder_path="./Register_Audio_Resource"):
# def compare_speakers(m4a_file_path, wav_folder_path="/home/ma-user/work/smart_assistant_backend/Register_Audio_Resource"):
    # 创建一个用于说话人验证的 pipeline
    sv_pipeline = pipeline(
        task='speaker-verification',
        model='damo/speech_campplus_sv_zh-cn_16k-common',
        model_revision='v1.0.0'
    )
    # m4a_file_path = 'tmp_audio_resource/turn_audio_into_text_tmp.m4a'
    # #警告 这里使用了一个绝对路径
    # m4a_file_path = "/home/ma-user/work/smart_assistant_backend/tmp_audio_resource/turn_audio_into_text_tmp.m4a"
    wav_file_path = m4a_file_path.replace('.m4a', '.wav')
    temp_wav_path = wav_file_path
    # 使用 subprocess 直接调用 ffmpeg 命令
    try:
        command = ['ffmpeg', '-i', m4a_file_path,'-ar', '16000',  wav_file_path]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # 检查 ffmpeg 命令是否成功执行
        if result.returncode != 0:
            print("Error: ", result.stderr.decode('utf-8'))
        else:
            print("Conversion successful!")
    except Exception as e:
        print(f"An error occurred while converting m4a to wav: {e}")

    # 从 m4a 文件加载音频，并设置采样率为 16000 Hz
    # audio = AudioSegment.from_file(m4a_file_path, format="m4a")
    # audio = audio.set_frame_rate(16000)
    # # 将处理后的音频保存为临时 wav 文件
    # temp_wav_path = "temp.wav"
    # audio.export(temp_wav_path, format="wav")
    #
    #
    #
    # 列出指定文件夹中所有的 wav 文件
    wav_files = [f for f in os.listdir(wav_folder_path) if f.endswith('.wav')]
    print("检测到的wav_files:{}".format(wav_files))
    match_index = None

    print("match_initiated")
    # 遍历所有 wav 文件，与上传的音频进行比较
    for index, wav_file in enumerate(wav_files):
        wav_file_path = os.path.join(wav_folder_path, wav_file)
        # 使用 pipeline 进行说话人验证
        result = sv_pipeline([temp_wav_path, wav_file_path])
        # 如果验证结果为 'yes'，表示找到匹配的说话人
        if result['text'] == 'yes':
            print("是已知的说话人")
            match_index = index + 1
            break
        else:
            print("不是已知的说话人！")
    os.remove(temp_wav_path)
    print("Match end")
    return match_index

# 以下为测试代码

# sv_pipeline = pipeline(
#     task='speaker-verification',
#     model='damo/speech_campplus_sv_zh-cn_16k-common',
#     model_revision='v1.0.0'
# )

# speaker_crz1_wav='voice_dataset/crz1.m4a'
# speaker_crz2_wav='voice_dataset/crz2.m4a'
#
# audio1 = AudioSegment.from_file('voice_dataset/crz1.m4a', format="m4a")
# audio2 = AudioSegment.from_file('voice_dataset/crz2.m4a', format="m4a")
#
# audio1 = audio1.set_frame_rate(16000)
# audio2 = audio2.set_frame_rate(16000)
#
# audio1.export("voice_dataset/crz1.wav", format="wav")
# audio2.export("voice_dataset/crz2.wav", format="wav")
#
# result=sv_pipeline(["voice_dataset/crz1.wav", "voice_dataset/crz2.wav"])
# print(result['text'])

