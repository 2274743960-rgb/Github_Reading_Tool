# test_simple.py - 简单测试脚本
import sys
import os

print("=== 开始测试 ===")

# 检查Python版本
print(f"Python版本: {sys.version}")

# 检查当前目录
print(f"当前目录: {os.getcwd()}")

# 检查文件是否存在
files_to_check = [
    'main.py',
    'utils/__init__.py', 
    'utils/github_client.py',
    'utils/ai_analyzer.py',
    '.env'
]

for file in files_to_check:
    exists = os.path.exists(file)
    print(f"{file}: {'✅ 存在' if exists else '❌ 缺失'}")

# 测试导入
try:
    from utils.github_client import GitHubClient
    print("✅ GitHubClient导入成功")
    
    # 测试初始化
    client = GitHubClient()
    print("✅ GitHubClient初始化成功")
    
except Exception as e:
    print(f"❌ 导入失败: {e}")
    import traceback
    traceback.print_exc()

print("=== 测试结束 ===")