import os
from openai import OpenAI
import pandas as pd
import json

def generate_user_prompt(question, answer1, answer2):
    return f"""
Question: {question}

Answer 1: {answer1}

Answer 2: {answer2}

Your evaluation result for each criterion (Comprehensiveness, Diversity, Empowerment, Directness) is:
"""

def evaluate_prompt(user_prompt):
    client = OpenAI(
        api_key="sk-9aa672112cb04d078ae92d1f0d720821",
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    message = [{
        'role': 'system', 
        'content':"""
You are a professional text evaluator. Please evaluate the following two answers to the given question based on the following criteria and determine which one is better. If there is no significant difference, declare it as a tie.

Evaluation Criteria:
1. Comprehensiveness: Does the answer provide enough detail to cover all aspects and details of the question?
2. Logical Coherence: Information is well-organized, and arguments are clearly and logically connected. The response should flow smoothly from one point to another, maintaining consistency and coherence.
3. Timeliness: Information, especially on current events or rapidly changing fields like technology trends, should be up-to-date.
4. Directness: Does the answer address the question directly and clearly?

Please provide your response without using any asterisks (**).
"""
        },
        {'role': 'user', 'content': user_prompt},
    ]
    completion = client.chat.completions.create(
        model="qwen-plus",  # qwen-turbo-latest
        messages=message,
    )
    response_dict = json.loads(completion.model_dump_json())
    answer_content = response_dict['choices'][0]['message']['content']

    # print(completion.model_dump_json())
    return answer_content

def main():
    questions = []
    current_question = []
    with open('questions.txt', 'r', encoding='utf-8') as file:
        for line in file:
            stripped_line = line.strip()
            if stripped_line == '':
                if current_question:
                    questions.append('\n'.join(current_question))
                    current_question = []
            else:
                current_question.append(stripped_line)
        if current_question:
            questions.append('\n'.join(current_question))

    
    with open('graphrag_answers.txt', 'r', encoding='utf-8') as file:
        rag_answers = []  # 存储所有问题的答案
        current_answer = []  # 当前正在构建的答案

        for line in file:
            stripped_line = line.strip()
            
            if stripped_line.startswith("Question:"):
                # 如果遇到了新的问题开头，则结束当前答案的收集，并重置current_answer列表
                if current_answer:  # 只有当current_answer不为空时才添加到rag_answers
                    rag_answers.append("\n".join(current_answer))
                    current_answer = []  # 重置当前答案列表
                # 将新问题的第一行也加入到current_answer中
                current_answer.append(stripped_line)
            else:
                # 继续为当前问题积累答案内容
                current_answer.append(stripped_line)
        # 处理最后一个答案（如果存在的话）
        if current_answer:
            rag_answers.append("\n".join(current_answer))
    
    with open('ollama_answers.txt', 'r', encoding='utf-8') as file:
        ollama_answers = []
        current_answer = []
        for line in file:
            stripped_line = line.strip()
            
            if stripped_line.startswith("Question:"):
                if current_answer:
                    ollama_answers.append("\n".join(current_answer))
                    current_answer = []
                current_answer.append(stripped_line)
            else:
                current_answer.append(stripped_line)
        if current_answer:
            ollama_answers.append("\n".join(current_answer))

    with open('evaluations.txt', 'a') as file:
        for i, question in enumerate(questions):
            try:
                user_prompt = generate_user_prompt(question, rag_answers[i], ollama_answers[i])
                print(f"Processing question {i+1}: {question}")
                print("User prompt:", user_prompt)
                
                evaluation = evaluate_prompt(user_prompt)
                print("Evaluation:", evaluation)

                # 将当前评估结果转换为字符串并写入文件
                file.write('Evaluation: of question ' + str(i+1) + ': ' + str(evaluation) + '\n')
                file.flush()
            except Exception as e:
                print(f"An error occurred while processing question {i+1}: {e}")

if __name__ == "__main__":
    main()