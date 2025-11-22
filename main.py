from utils.github_client import GitHubClient
from utils.ai_analyzer import AIAnalyzer

def main():
    print("=== 🚀 GitHub Repo AI分析师 ===")
    print("现在我可以智能分析GitHub仓库了！")
    print("=" * 50)
    
    # 创建客户端
    github_client = GitHubClient()
    ai_analyzer = AIAnalyzer()
    
    while True:
        repo_url = input("\n📝 请输入GitHub仓库链接 (输入 'quit' 退出): ").strip()
        
        if repo_url.lower() == 'quit':
            print("👋 再见！")
            break
            
        if not repo_url.startswith('https://github.com/'):
            print("❌ 请输入正确的GitHub链接")
            continue
            
        print("\n🔍 正在分析仓库...")
        
        # 获取基本信息
        repo_info = github_client.get_repo_info(repo_url)
        if not repo_info:
            continue
            
        # 从URL提取信息
        parts = repo_url.strip('/').split('/')
        owner = parts[-2]
        repo_name = parts[-1]
        
        # 获取更多信息
        print("📖 正在获取README...")
        readme_content = github_client.get_readme(owner, repo_name)
        
        print("🤖 正在调用AI分析...")
        ai_analysis = ai_analyzer.analyze_repo(repo_info, readme_content)
        
        # 显示完整结果
        print("\n" + "🎉 分析结果：" + "="*40)
        print(f"📦 仓库: {repo_info['full_name']}")
        print(f"📝 描述: {repo_info['description']}")
        print(f"💻 语言: {repo_info['language']}")
        print(f"⭐ 星标: {repo_info['stars']}")
        print(f"🍴 Fork: {repo_info['forks']}")
        print(f"🐛 问题: {repo_info['open_issues']}")
        print(f"📅 创建: {repo_info['created_at']}")
        print(f"🔄 更新: {repo_info['updated_at']}")
        print("\n🤖 AI分析报告:")
        print("-" * 30)
        print(ai_analysis)
        print("=" * 50)

if __name__ == "__main__":
    main()