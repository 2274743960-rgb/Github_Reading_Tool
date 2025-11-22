# test_flask.py - 测试Flask是否安装成功
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "🎉 Flask安装成功！Web应用可以正常工作了！"

if __name__ == '__main__':
    print("正在启动Flask服务器...")
    app.run(debug=True, host='0.0.0.0', port=5000)