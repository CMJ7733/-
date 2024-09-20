#接受一个音频输入
#输出转成文字 文字包括文本  可选项是情感的标签 作为参数可以选择是否要情感
from models.Sense_voice_small_model import SenseVoiceSmall
from funasr.utils.postprocess_utils import rich_transcription_postprocess
# import torch
# import torch_npu
# from torch_npu.contrib import transfer_to_npu
def stt(audio_path,need_emo=True):
    print("STT function 启动")
    # 模型路径和设备配置
    model_dir = "iic/SenseVoiceSmall"
    m, kwargs = SenseVoiceSmall.from_pretrained(model=model_dir, device="cuda:0")
    m.eval()

    # 进行推理
    res = m.inference(
        data_in=audio_path,
        language="auto",  # "zh", "en", "yue", "ja", "ko", "nospeech"
        use_itn=False,
        ban_emo_unk=need_emo,
        **kwargs,
    )

    # 从推理结果中提取文本
    text = res[0][0]["text"]

    # 提取情感信息
    def extract_emotion(text):
        for emo in ["<|HAPPY|>", "<|SAD|>", "<|ANGRY|>", "<|NEUTRAL|>", "<|FEARFUL|>", "<|DISGUSTED|>",
                    "<|SURPRISED|>"]:
            if emo in text:
                return emo
        return "<|NEUTRAL|>"

    emotion = extract_emotion(text)

    # 进行后处理
    processed_text = rich_transcription_postprocess(text)

    # 打印结果
    print("Text:", processed_text)
    print("Emotion:", emotion)
    print("STT function 结束")
    return processed_text,emotion