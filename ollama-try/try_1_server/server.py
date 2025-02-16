import ollama
import time
from flask import Flask, request, jsonify, render_template


class Chat():
    """A AI chatbot, using Ollama"""
    def __init__(self, 
                model_name="deepseek-r1:1.5b", 
                model_path=None, host="localhost", 
                port=11434):
        """初始化"""
        self.model_name = model_name
        self.model_path = model_path
        self.host = host
        self.port = port
        self.history = []

    def get_answer(self, question, stream=False) -> str:
        """获取答案"""
        client = ollama.Client(host=f'http://{self.host}:{self.port}')  # 创建客户端
        res = client.chat(model=self.model_name, messages=[{"role": "user", "content" : question}], stream=stream)  # 获取答案
        answer = res.message['content']
        self.history.append((question, answer))
        return answer
    

def main(model_name="deepseek-r1:1.5b",
        model_path=None,
        host="localhost",
        port=11434):
    """主函数"""
    chat = Chat(model_name, model_path, host, port)
    while True:
        question = input("请输入问题：")
        print("thinking...")
        answer = chat.get_answer(question)
        for line in answer.split("\n"):
            for text in line:
                print(text, end="", flush=True)
                time.sleep(0.01)
            print()
        chat.history.append((question, answer))


app = Flask(__name__)

@app.route('/')
def index():
    """主页"""
    with open('./ollama-try/try_1_server/index.html', 'r', encoding='utf-8') as f:
        html_content = f.read()
    return html_content

@app.route('/ask', methods=['POST'])
def ask():
    """处理用户提问"""
    question = request.json.get('question')
    answer = Chat.get_answer(question)
    return jsonify({'answer': answer})

if __name__ == "__main__":
    try:
        app.run(host='127.0.0.1', port=8080)  # 启动 Flask 应用
    except KeyboardInterrupt:
        print("程序已退出")
        exit()
    except Exception as e:
        print("程序出错：", e)
        exit()