import os
from openai import OpenAI


# 初始化OpenAI客户端（请确保你已安装openai库并正确设置API密钥）
def init_client():
    # api_key = os.getenv("OPENAI_API_KEY")  # 从环境变量中读取API密钥
    # if not api_key:
    #     raise ValueError("Please set the OPENAI_API_KEY environment variable.")
    client = OpenAI(
        api_key = "sk-9aa672112cb04d078ae92d1f0d720821",
        base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    return client

def get_response(client, messages):
    try:
        completion = client.chat.completions.create(model="qwen-max", messages=messages)    # "qwen-plus"
        return completion
    except Exception as e:
        return f"发生错误：{e}"

def main():
    client = init_client()
    messages = [{"role": "system", "content": "你是一个帮助助手，可以回答各种问题并进行多轮对话。"}]
    
    print("欢迎使用多轮对话系统，请输入您的问题或信息（输入'q'结束对话）：")
    while True:
        user_input = input("> ")
        # user_input = input()
        if user_input.lower() == "q":
            break
        
        # 添加用户的输入到消息列表
        messages.append({"role": "user", "content": user_input})
        
        # 获取并打印模型的响应
        assistant_output = get_response(client, messages)
        print(f"助手：{assistant_output}")
        
        # 将助手的回复也加入到消息列表，以便维持对话的连贯性
        messages.append({"role": "assistant", "content": assistant_output})

if __name__ == "__main__":
    main()