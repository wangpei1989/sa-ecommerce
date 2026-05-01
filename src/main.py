"""
南非跨境电商 Agent - 运行入口
"""
import os
import sys

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.agent import build_agent

def main():
    """启动 Agent 服务"""
    print("=" * 50)
    print("🇿🇦 南非跨境电商 Agent 启动中...")
    print("=" * 50)
    
    try:
        agent = build_agent()
        print("✅ Agent 初始化成功！")
        print(f"📦 加载工具数量: {len(agent.tools)}")
        print("🎯 Agent 已就绪，等待用户输入...")
        
        # 交互式测试
        print("\n💡 输入 'quit' 退出")
        while True:
            user_input = input("\n👤 您: ")
            if user_input.lower() == 'quit':
                print("👋 再见！")
                break
            
            # 调用 Agent
            result = agent.invoke({"messages": [("user", user_input)]})
            print(f"\n🤖 Agent: {result}")
            
    except Exception as e:
        print(f"❌ Agent 启动失败: {e}")
        raise

if __name__ == "__main__":
    main()
