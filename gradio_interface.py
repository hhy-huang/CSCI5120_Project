import gradio as gr
import subprocess
import webbrowser

def query_graphrag(question):
    """调用graphrag.query命令并返回结果"""
    # 构建命令
    command = [
        "python", "-m", "graphrag.query",
        "--root", "./ragtest",
        "--method", "global",
        question
    ]
    
    # 执行命令并捕获输出
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        output = result.stdout
        
        # 查找 "SUCCESS: Global Search Response:" 标记的位置
        success_index = output.find("SUCCESS: Global Search Response:")
        
        # 如果找到了标记，从标记之后开始截取字符串；否则返回原始输出
        if success_index != -1:
            output = output[success_index + 32:]
        
        return output
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

# 创建Gradio界面
iface = gr.Interface(
    fn=query_graphrag,
    inputs=gr.Textbox(lines=2, placeholder="在这里输入您的问题..."),
    outputs=gr.Textbox(),
    title="Ollama GraphRAG 聊天机器人",
    description="欢迎！请输入您的问题开始对话。"
)

# 启动服务并获取本地URL
app, local_url, public_url = iface.launch(share=False)  # 设置share=True在公共URL上共享

# 自动打开浏览器并导航到本地URL,但是没用
webbrowser.open(local_url)