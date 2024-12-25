import subprocess
import os
import sys
import chardet


try:
    os.remove('answer.txt')
except OSError:
    pass  # 如果文件不存在，忽略错误

def read_questions(file_path):
    """ 从指定路径读取问题列表。假设每行一个问题，跳过空行。"""
    with open(file_path, 'r', encoding='utf-8') as file:
        questions = [line.strip() for line in file if line.strip()]
    return questions

def execute_query(question, conda_env):
    """ 在指定的conda环境中执行查询命令，并返回结果。"""

    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建绝对路径
    root_dir = os.path.join(script_dir, 'ragtest')

    # 由于在vscode中配置了虚拟环境，不用在下面这句代码中手动设置conda环境变量
    command = f'python -m graphrag.query --root "{root_dir}" --method global "{question}"'

    print(f"Executing command:\n  {command}")
    
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='gb2312')

    # 原来是用gb2312编码的
    # encoding = chardet.detect(result.stdout)['encoding']
    # print("encoding:" + encoding)

    # 检查是否有错误发生
    if result.returncode != 0:
        print(f"Error occurred: {result.stderr}")
        return None
    
    return result.stdout


def save_answer(answer, output_file):
    """ 将单个答案追加保存到文件中。"""
    # 找到'SUCCESS: Global Search Response:'的位置
    start_index = answer.find('SUCCESS: Global Search Response:')
    # 从该位置开始切片，跳过前面的格式信息
    content = answer[start_index + len('SUCCESS: Global Search Response:'):].strip()
    # 分割字符串为单独的行，并过滤掉空行
    filtered_content = '\n'.join([line for line in content.splitlines() if line.strip()])
    with open(output_file, 'a', encoding='utf-8') as file:
        file.write(filtered_content + '\n\n')

def main():
    # 获取当前脚本所在目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 输入的问题文件和输出的答案文件路径
    input_file = os.path.join(script_dir, 'questions.txt')
    output_file = os.path.join(script_dir, 'answers.txt')
    
    # 读取问题
    questions = read_questions(input_file)

    print("questions:")
    i = 0
    for question in questions:
        print(i, question)
        i += 1

    # 存储答案
    answer = []
    
    # 遍历每个问题，获取答案
    conda_env = 'graphrag-ollama-local'
    i = 1
    for q in questions:
        answer = execute_query(q, conda_env)
        if answer is not None:
            print("answer:")
            print(answer)
            with open(output_file, 'a', encoding='utf-8') as file:
                file.write('Question:' + str(i) + ' ' + q + '\n')
            i += 1
            save_answer(answer, output_file)
            print(f"Processed question: {q[:50]}... Answer saved.")
            sys.stdout.flush()
        else:
            print(f"Error: No answer for question {q[:50]}... Skipping.")
            sys.stdout.flush()
    
    print(f"All answers have been saved to {output_file}")

if __name__ == "__main__":
    main()