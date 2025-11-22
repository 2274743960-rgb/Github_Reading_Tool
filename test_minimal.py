# test_minimal.py - 最简化测试
import requests
import os
from dotenv import load_dotenv

load_dotenv()

def minimal_test():
    print("=== 最简化GitHub API测试 ===")
    
    # 直接从.env读取token
    token = os.getenv('GITHUB_TOKEN')
    if not token:
        print("❌ 没有找到GITHUB_TOKEN")
        return
    
    print(f"✅ 找到Token，长度: {len(token)}")
    
    # 设置请求头
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # 测试一个简单的API调用
    url = "https://api.github.com/repos/vuejs/vue"
    
    try:
        print("🔍 发送请求到GitHub API...")
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 响应状态码: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ 成功获取仓库信息!")
            print(f"仓库名: {data.get('name')}")
            print(f"描述: {data.get('description')}")
            print(f"星标数: {data.get('stargazers_count')}")
        else:
            print(f"❌ API请求失败: {response.status_code}")
            print(f"错误信息: {response.text}")
            
    except Exception as e:
        print(f"❌ 请求异常: {e}")

if __name__ == "__main__":
    minimal_test()