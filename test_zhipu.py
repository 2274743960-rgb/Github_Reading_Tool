# test_zhipu.py - 测试智谱AI API密钥
import os
from dotenv import load_dotenv
from zhipuai import ZhipuAI

load_dotenv()

def test_zhipu_api():
    print("=== 测试智谱AI API ===")
    
    api_key = os.getenv('ZHIPUAI_API_KEY')
    if not api_key:
        print("❌ 未找到ZHIPUAI_API_KEY环境变量")
        return
    
    print(f"✅ API密钥长度: {len(api_key)}")
    print(f"API密钥前10位: {api_key[:10]}...")
    
    try:
        client = ZhipuAI(api_key=api_key)
        print("✅ ZhipuAI客户端创建成功")
        
        # 测试一个简单的请求
        response = client.chat.completions.create(
            model="glm-3-turbo",
            messages=[{"role": "user", "content": "请回复'你好'来测试API连接"}],
            max_tokens=10
        )
        
        print("✅ API请求成功！")
        print(f"响应: {response.choices[0].message.content}")
        
    except Exception as e:
        print(f"❌ API请求失败: {e}")
        
        # 提供具体的错误处理建议
        if "401" in str(e) or "身份验证" in str(e):
            print("\n🔧 解决方案:")
            print("1. 检查API密钥是否正确")
            print("2. 确认账户已完成实名认证")
            print("3. 登录 https://open.bigmodel.cn/ 检查账户状态")
        elif "额度" in str(e) or "余额" in str(e):
            print("\n🔧 解决方案:")
            print("1. 账户可能没有剩余额度")
            print("2. 登录控制台查看余额并充值")
        else:
            print("\n🔧 请检查网络连接和API服务状态")

if __name__ == "__main__":
    test_zhipu_api()