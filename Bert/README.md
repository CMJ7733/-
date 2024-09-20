# Bert问答

bert.py 实现基于BERT模型的问题回答功能

utils.py 处理训练数据集

flask_app.ipynb 使用Flask框架构建应用程序，利用BERT处理和回答相关问题

#### flask_app.ipynb 

```python
#BERT
from flask import Flask, request, jsonify
from bert import QA
import torch
import torch_npu
from torch_npu.contrib import transfer_to_npu
app = Flask(__name__)
model = QA('/home/ma-user/work/Bert/model') #输入训练好的模型路径

```

```python
# 接收 POST 请求中的文字数据
@app.route('/receive-texts', methods=['POST'])
def receive_data():
    # 获取请求体中的 JSON 数据
    data = request.get_json() 
    # 获取传入的文字
    doc = data.get('text1', '')
    q = data.get('text2', '')

    answer = model.predict(doc,q)#调用BERT得到回答
    # 返回处理后的结果
    return jsonify({
        'answer': answer['answer']
    })


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False,port=5001) #设置服务器端口5001
```