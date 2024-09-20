import requests
def chat_with_chatglm6b(url,input_words):
    # print("ChatGLM init")
    #开始聊天
        # 请求头
    headers = {
        'Content-Type': 'application/json'
    }

    # 请求数据
    data = {
        'text':input_words
    }

    # 发送POST请求
    response = requests.post(url, headers=headers, json=data)

    # 检查响应状态码
    if response.status_code == 200:
        # print('请求成功ChatGLM')
        result = response.json().get('received_text', '未找到文本')
        print("ChatGLM said:{}".format(result))
        return result
    else:
        print(f'ChatGLM请求失败，状态码：{response.status_code}')
        print(response.text)
if __name__ == "__main__":
    bert_url = 'http://127.0.0.1:5001/receive-texts'
    chat_glm_url = 'http://127.0.0.1:5004/posttext'
    print(chat_with_chatglm6b(chat_glm_url,"""
        我们希望智能家居助手能够根据说话人的当前输入、之前的自我介绍以及BERT对说话人的发言总结的内容，生成一段合适的对话内容。这段对话应该能够自然地回应说话人的问题或请求，并且展示对说话人背景的理解。

        请你担任一名智能家居助手，具备理解和回应说话人需求的能力。你需要根据提供的信息，对输入做出合适的、有人情味的回答。

        请你完成以下任务：

        根据说话人的当前输入、之前的自我介绍以及BERT推理出的内容，做出合适的、有人情味的回答，不需要说出像“根据你的自我介绍和BERT分析出的内容”这样的词。
        1.确保对话内容能够准确回应说话人的问题或请求，在回答的时候结合对于说话人背景进行回答，但是比重不要太大。
        2.对话内容应简洁明了，不超过100字。
        3.**不要说**“根据你的自我介绍和BERT分析出的内容”这样的内容。

        说话人的自我介绍：我是李明，男，今年30岁，是一名在IT公司工作的程序员。我的业余生活丰富多彩，除了喜欢阅读科技类书籍和烹饪美食，我还热衷于玩桌游和扮演角色游戏。我也是一名狂热的电影爱好者，经常去电影院看最新上映的影片，尤其是科幻和悬疑类电影。同时，我也喜欢动手DIY，比如制作模型和3D打印。在节假日，我常常和朋友一起去露营，享受大自然的宁静和美好。

        说话人说的话：今天感觉胃口不是很好，有点想吃甜的，请问有什么推荐的比较方便的早饭，我赶时间。
        请你作为一名智能家居助手回答"""))
