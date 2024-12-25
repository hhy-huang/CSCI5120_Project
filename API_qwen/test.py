def read_file_and_remove_blank_lines(filename):
    # 使用with语句打开文件，这样可以确保文件最终会被正确关闭
    with open(filename, 'r', encoding='utf-8') as file:
        # 读取所有行，并使用strip()去除每行首尾的空白字符（包括空格、制表符和换行符）
        # 然后通过列表推导式过滤掉只包含空白或完全为空的行
        lines = [line.strip() for line in file if line.strip()]
    return lines

# 使用函数
filename = 'output.txt'  # 这里替换为你的文件名
cleaned_lines = read_file_and_remove_blank_lines(filename)

output_file_path = 'output.txt'

with open(output_file_path, 'w', encoding='utf-8') as file:
    for item in cleaned_lines:
        file.write(item + '\n')  # 每个元素后添加换行符