import requests
def chat_with_chatglm6b(url):
    # print("ChatGLM init")
    #开始聊天
        # 请求头
    headers = {
        'Content-Type': 'application/json'
    }

    # 发送POST请求
    response = requests.post(url, headers=headers)

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
    chat_glm_url_clear = 'http://127.0.0.1:5004/clearhistory'
    print(chat_with_chatglm6b(chat_glm_url_clear))