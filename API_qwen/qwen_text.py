import os
from openai import OpenAI

client = OpenAI(
    api_key="sk-9aa672112cb04d078ae92d1f0d720821",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

print("请输入你的问题:")
user_input = input()

messages = [
    {'role': 'system', 'content': '你是一个人工智能翻译助手，现在有一篇论文中的片段需要翻译，请提供中文译文。以下为原文。'},
    {'role': 'user', 'content': user_input},
]

completion = client.chat.completions.create(
    model="qwen-plus",  # qwen-plus
    messages=messages,
)

print(completion.model_dump_json())
