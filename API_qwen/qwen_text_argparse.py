import os
import argparse
from openai import OpenAI

# 设置命令行参数解析
parser = argparse.ArgumentParser(description="Qwen Chat Completion Example")
parser.add_argument("question", help="The question you want to ask Qwen.")
args = parser.parse_args()

client = OpenAI(
    api_key="sk-9aa672112cb04d078ae92d1f0d720821",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# 使用命令行参数中的问题
messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'user', 'content': args.question},
]

completion = client.chat.completions.create(
    model="qwen-plus", 
    messages=messages,
)

print(completion.model_dump_json())