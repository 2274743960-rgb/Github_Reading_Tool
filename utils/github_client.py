import os
import requests
import base64
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class GitHubClient:
    def __init__(self):
        # 从.env文件读取令牌
        self.token = os.getenv('GITHUB_TOKEN')
        
        # 设置请求头
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        print("✅ GitHub客户端准备就绪！")
    
    def get_repo_info(self, repo_url):
        """从GitHub URL获取仓库基本信息"""
        try:
            # 从URL中提取用户名和仓库名
            # 比如：https://github.com/vuejs/vue → vuejs/vue
            parts = repo_url.strip('/').split('/')
            owner = parts[-2]  # vuejs
            repo_name = parts[-1]  # vue
            
            api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
            
            print(f"🔍 正在获取 {owner}/{repo_name} 的信息...")
            
            # 发送请求到GitHub
            response = requests.get(api_url, headers=self.headers)
            
            # 检查响应
            if response.status_code == 200:
                repo_data = response.json()
                
                return {
                    'name': repo_data['name'],
                    'full_name': repo_data['full_name'],
                    'description': repo_data.get('description', '无描述'),
                    'html_url': repo_data['html_url'],
                    'language': repo_data.get('language', '未知'),
                    'stars': repo_data['stargazers_count'],
                    'forks': repo_data['forks_count'],
                    'open_issues': repo_data['open_issues_count'],
                    'created_at': repo_data['created_at'][:10],  # 只取前10位（年月日）
                    'updated_at': repo_data['updated_at'][:10]
                }
            else:
                print(f"❌ 出错了！错误代码: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            return None

    def get_readme(self, owner, repo_name):
        """获取仓库的README内容"""
        try:
            api_url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"
            response = requests.get(api_url, headers=self.headers)
            
            if response.status_code == 200:
                # GitHub返回的README是Base64编码的，需要解码
                content = response.json().get('content', '')
                decoded_content = base64.b64decode(content).decode('utf-8')
                return decoded_content
            else:
                print("❌ 无法获取README")
                return "无README"
        except Exception as e:
            print(f"❌ 获取README失败: {e}")
            return "无README"

    def get_languages(self, owner, repo_name):
        """获取仓库使用的编程语言"""
        try:
            api_url = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
            response = requests.get(api_url, headers=self.headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                return {"未知": 100}
        except:
            return {"未知": 100}