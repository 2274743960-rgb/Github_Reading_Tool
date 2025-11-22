# test_static_files.py - 测试静态文件是否可访问
import requests

def test_static_files():
    base_url = "http://localhost:5000"
    
    files_to_test = [
        "/static/css/style.css",
        "/static/js/background.js", 
        "/static/js/script.js"
    ]
    
    for file_path in files_to_test:
        url = base_url + file_path
        try:
            response = requests.get(url)
            status = "✅ 成功" if response.status_code == 200 else f"❌ 失败 ({response.status_code})"
            print(f"{file_path}: {status}")
        except Exception as e:
            print(f"{file_path}: ❌ 错误 - {e}")

if __name__ == "__main__":
    test_static_files()