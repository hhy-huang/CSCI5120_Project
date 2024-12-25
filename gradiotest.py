import gradio as gr
import subprocess
import webbrowser
import os
import csv

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

# 自定义JavaScript代码来修改Flag按钮的文字和行为
js_code = """
<script>
document.addEventListener('DOMContentLoaded', function() {
    // 修改Flag按钮的文字
    var flagButtons = document.querySelectorAll('.gr-button.flag');
    for (var i = 0; i < flagButtons.length; i++) {
        flagButtons[i].innerText = 'Save';
    }

    // 添加点击事件
    var flagButton = document.querySelector('.gr-button.flag');
    if (flagButton) {
        flagButton.addEventListener('click', function() {
            alert('保存成功！');
        });
    }
});
</script>
"""

# 创建Gradio界面
with gr.Blocks() as iface:
    # 设置标题和描述
    gr.Markdown("# Ollama GraphRAG 聊天机器人")
    gr.Markdown("欢迎！请输入您的问题开始对话。")
    
    # 输入组件
    input_text = gr.Textbox(lines=2, placeholder="在这里输入您的问题...")
    
    # 输出组件
    output_text = gr.Textbox()
    
    # 添加自定义的HTML组件
    gr.HTML(js_code)
    
    # 定义接口函数
    def process_question(question):
        return query_graphrag(question)
    
    # 为“清空”按钮添加处理函数
    def clear_inputs():
        return "", ""  # 返回两个空字符串以匹配输入和输出组件
    
    # 为“Save”按钮添加处理函数
    def save_inputs(input_text, output_text):
        # 确保保存目录存在
        save_dir = os.path.join(".gradio", "flagged")
        os.makedirs(save_dir, exist_ok=True)
        
        # 生成文件名
        file_name = f"saved_data_{len(os.listdir(save_dir)) + 1}.csv"
        file_path = os.path.join(save_dir, file_name)
        
        # 保存数据到CSV文件
        with open(file_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["input", input_text])
            writer.writerow(["output", output_text])
        
        return input_text, output_text  # 返回相同的值以保持界面不变

    # 将输入和输出绑定到处理函数
    with gr.Row():
        submit_button = gr.Button("发送")
        clear_button = gr.Button("清空")
        flag_button = gr.Button("Save")
        
    # 绑定按钮事件
    submit_button.click(process_question, inputs=[input_text], outputs=output_text)
    clear_button.click(clear_inputs, inputs=[], outputs=[input_text, output_text])
    flag_button.click(save_inputs, inputs=[input_text, output_text], outputs=[input_text, output_text])

# 启动服务并获取本地URL
app, local_url, public_url = iface.launch(share=False)  # 设置share=True在公共URL上共享

# 自动打开浏览器并导航到本地URL
webbrowser.open(local_url)