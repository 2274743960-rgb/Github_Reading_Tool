# check_env.py - 检查环境变量
import os
from dotenv import load_dotenv

load_dotenv()

print("=== 环境变量检查 ===")
github_token = os.getenv('GITHUB_TOKEN')
zhipuai_key = os.getenv('ZHIPUAI_API_KEY')

print(f"GITHUB_TOKEN: {'✅ 已设置' if github_token else '❌ 未设置'}")
if github_token:
    print(f"Token长度: {len(github_token)}")
    print(f"Token前10位: {github_token[:10]}...")

print(f"ZHIPUAI_API_KEY: {'✅ 已设置' if zhipuai_key else '❌ 未设置'}")
if zhipuai_key:
    print(f"Key长度: {len(zhipuai_key)}")
    print(f"Key前10位: {zhipuai_key[:10]}...")