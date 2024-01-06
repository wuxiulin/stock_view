import tkinter as tk
from tkinter import filedialog
import subprocess

def execute_python_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
    
    if file_path:
        try:
            # 执行本地Python文件
            result = subprocess.run(["python", file_path], capture_output=True, text=True)
            
            # 获取执行结果并显示在界面上
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, result.stdout)
            result_text.insert(tk.END, result.stderr)
            result_text.config(state=tk.DISABLED)
        except Exception as e:
            result_text.config(state=tk.NORMAL)
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, f"Error: {str(e)}")
            result_text.config(state=tk.DISABLED)

# 创建主窗口
root = tk.Tk()
root.title("Python文件执行器")

# 创建按钮
execute_button = tk.Button(root, text="执行Python文件", command=execute_python_file)
execute_button.pack(pady=10)

# 创建文本框用于显示执行结果
result_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)
result_text.pack(padx=10, pady=10)

# 运行主循环
root.mainloop()
