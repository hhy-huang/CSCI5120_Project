import os
from openai import OpenAI
import json

client = OpenAI(
    api_key="sk-9aa672112cb04d078ae92d1f0d720821",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def clean_text_batch(text_batch):
    messages = [
        {'role': 'system', 'content':
        """
        你是一个专业的文本编辑助手，专门负责清洗和优化文章内容。请你清洗文本，去除资料来源，并保持内容的连贯性和可读性。其他要求如下：

        1.对于形如**[ARTICLE X: yyy - ChainCatcher]**的内容，去除其中的**- ChainCatcher**，保留文章编号及标题。

        例如：
        [ARTICLE X: yyy - ChainCatcher]将被清洗为：[ARTICLE X: yyy]

        2.请关注正文开头部分，对于形如**_原标题：_  _来源：Cointelegraph，Fortune_  _编译：Felix, PANews_  **的内容，将其去除。

        3.请关注正文结尾部分，对于形如**  _Story co-authored by Danny B and Nermin Haj_  _and  Images via xxx_  **的内容，将其去除。
        
        4.在两个段落之间不能使用额外的换行符，对于形如**\n\n\n**的内容，将其去除。

        5.去除形如**===============**, **------** 或**___**的内容。

        6.不能输出形如**清洗后的文本**的内容，请直接输出清洗后的文本。

        7.去除形如**图源：xxx**或**图片来源：xxx**的内容。
        
        以下是需要清洗的文本：
        """
        },
        {'role': 'user', 'content': text_batch},
    ]
    completion = client.chat.completions.create(
        model="qwen-turbo-latest",  # qwen-plus
        messages=messages,
    )
    response_dict = json.loads(completion.model_dump_json())
    answer_content = response_dict['choices'][0]['message']['content']

    # print(completion.model_dump_json())
    return answer_content

def process_text_file(input_file_path, output_file_path, batch_size=5000):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    print("length of text:", len(text))

    # 分批处理文本
    batches = [text[i:i+batch_size] for i in range(0, len(text), batch_size)]
    cleaned_text = ""

    for batch in batches:
        # 调用大模型清洗文本
        cleaned_batch = clean_text_batch(batch)
        print("--------")
        cleaned_text += cleaned_batch

    # 将清洗后的文本保存到输出文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

def read_file_and_remove_blank_lines(remove_enter_input_filename):
    # 使用with语句打开文件，这样可以确保文件最终会被正确关闭
    with open(remove_enter_input_filename, 'r', encoding='utf-8') as file:
        # 读取所有行，并使用strip()去除每行首尾的空白字符（包括空格、制表符和换行符）
        # 然后通过列表推导式过滤掉只包含空白或完全为空的行
        lines = [line.strip() for line in file if line.strip()]
    return lines

# 设置输入和输出文件路径
input_file_path = 'input.txt'
output_file_path = 'output.txt'

# 处理文本文件
process_text_file(input_file_path, output_file_path)

remove_enter_input_filename = 'output.txt'  # 这里替换为你的文件名
cleaned_lines = read_file_and_remove_blank_lines(remove_enter_input_filename)

remove_enter_output_filename = 'cleaned-output.txt'

with open(remove_enter_output_filename, 'w', encoding='utf-8') as file:
    for item in cleaned_lines:
        file.write(item + '\n')  # 每个元素后添加换行符