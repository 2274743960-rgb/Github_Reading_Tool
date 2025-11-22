import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI  # 确保正确导入

load_dotenv()

class AIAnalyzer:
    def __init__(self):
        # 设置智谱AI的API Key
        self.api_key = os.getenv('ZHIPUAI_API_KEY')
        
        # 使用新版本的ZhipuAI客户端
        try:
            self.client = ZhipuAI(api_key=self.api_key)
            print("✅ AI分析器准备就绪！(使用新版本SDK)")
        except ImportError:
            print("❌ 请安装zhipuai库: pip install zhipuai")
            self.client = None
        except Exception as e:
            print(f"❌ AI分析器初始化失败: {e}")
            self.client = None
    
    def analyze_repo(self, repo_info, readme_content):
        """让AI分析仓库"""
        
        if not self.client:
            return "AI分析器未正确初始化，请检查配置"
        
        # 准备要分析的信息
        repo_data = f"""
仓库名称: {repo_info['full_name']}
描述: {repo_info['description']}
主要语言: {repo_info['language']}
星标数: {repo_info['stars']}
Fork数: {repo_info['forks']}
README内容: {readme_content[:1000]}  # 只取前1000字避免太长
"""
        
        # 让AI分析
        prompt = f"""
请你作为一个资深技术专家，分析这个GitHub仓库：

{repo_data}

请用中文回答以下问题：
1. 这个项目是做什么的？（用一句话简单说明）
2. 技术栈可能包含什么？
3. 从数据看，这个项目受欢迎吗？
4. 对于初学者来说，这个项目值得学习吗？

请用通俗易懂的语言回答，不要太技术化。
"""
        
        try:
            response = self.client.chat.completions.create(
                model="glm-4",  # 更新模型名称
                messages=[{"role": "user", "content": prompt}],
                top_p=0.7,
                temperature=0.9,
            )
            
            return response.choices[0].message.content
                
        except Exception as e:
            return f"调用AI时出错: {str(e)}"
