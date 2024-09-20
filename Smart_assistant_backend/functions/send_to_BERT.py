#会返回一个BERT阅读理解的结果
#questions是定死的
import requests
def ask_questions_to_BERT(url,word,question):
    # print("BERT init")
    # 请求头
    headers = {
        'Content-Type': 'application/json'
    }
    # 请求数据
    data = {
        'text1': word,
        'text2': question  #需要预先设置好
    }
    # 发送POST请求
    response = requests.post(url, headers=headers, json=data)
    # 检查响应状态码
    if response.status_code == 200:
        # print('请求成功BERT')
        # print(response.json())  # 如果响应内容是JSON格式
        result = response.json().get('answer', '未找到文本')
        print("BERT said:{}".format(result))
        return result
    else:
        print(f'BERT请求失败，状态码：{response.status_code}')
        print(response.text)

if __name__ == "__main__":
    bert_url = 'http://127.0.0.1:5001/receive-texts'
    chat_glm_url = 'http://127.0.0.1:5002//posttext'
    doc="Artificial Intelligence (AI) has become one of the defining technologies of the 21st century, reshaping industries and daily life in ways previously unimaginable. From self-driving cars to personalized healthcare solutions, AI is transforming how we live, work, and interact with technology."
    q='What is this article mainly about?'
    # answer = model.predict(doc,q)
    # print(answer['answer'])
    ask_questions_to_BERT(bert_url,doc,q)
