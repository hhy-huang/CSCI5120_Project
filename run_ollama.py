import requests

# 设置Ollama Mistral API地址
api_url = "http://localhost:11434/api/generate"

def ask_question(question):
    """向Ollama Mistral API发送一个问题并返回响应"""
    payload = {
        "model": "mistral",
        "prompt": question,
        "stream": False  # 禁用流式响应，一次性获取完整响应
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(api_url, json=payload, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            return data.get("response", "没有收到有效答案")
        except ValueError:
            print(f"解析响应出错：{response.text}")
            return
    else:
        return f"请求失败：{response.status_code}"

def main():
    with open('questions.txt', 'r', encoding='utf-8') as file:
        questions = [line.strip() for line in file if line.strip()]
    i = 1
    for q in questions:
        answer = ask_question(q)
        if answer is not None:
            print("answer:")
            print(answer)
            with open('ollama_answers.txt', 'a', encoding='utf-8') as file:
                file.write('Question:' + str(i) + ' ' + q + '\n')
            i += 1
            filtered_content = '\n'.join([line for line in answer.strip().splitlines() if line.strip()])
            with open('ollama_answers.txt', 'a', encoding='utf-8') as file:
                file.write(filtered_content + '\n\n')
    print(f"All answers have been saved to ollama_answers.txt")

if __name__ == "__main__":
    main()