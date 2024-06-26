import tkinter as tk
from tkinter import filedialog
import shutil
import os
import configparser

# 定义一些初始值
astitle = ""
imgpath = ""
exepath = ""

# 创建 as_data 文件夹
if not os.path.exists('as_data'):
    os.makedirs('as_data')

def save_config():
    config = configparser.ConfigParser()
    config['settings'] = {
        'astitle': astitle,
        'imgpath': imgpath,
        'exepath': exepath
    }
    with open('as_data/config.ini', 'w') as configfile:
        config.write(configfile)
    print("Configuration saved!")

def select_image():
    global imgpath
    file_path = filedialog.askopenfilename(title="选择图片", filetypes=[("Image files", "*.jpg *.png *.gif")])
    if file_path:
        new_path = os.path.join('as_data', os.path.basename(file_path))
        shutil.copy(file_path, new_path)
        imgpath = new_path
        print(f"Image selected: {imgpath}")

def select_executable():
    global exepath
    file_path = filedialog.askopenfilename(title="选择可执行程序", filetypes=[("Executable files", "*.exe" if os.name == 'nt' else "*")])
    if file_path:
        exepath = os.path.relpath(file_path, start='as_data')
        print(f"Executable selected: {exepath}")

def set_astitle():
    global astitle
    astitle = title_entry.get()
    print(f"Title set: {astitle}")

# 创建主窗口
root = tk.Tk()
root.title("Configuration Tool")

# 输入栏
title_label = tk.Label(root, text="请输入标题:")
title_label.pack()

title_entry = tk.Entry(root)
title_entry.pack()

# 按钮: 选择图片
img_button = tk.Button(root, text="选择图片", command=select_image)
img_button.pack()

# 按钮: 选择可执行程序
exe_button = tk.Button(root, text="选择可执行程序", command=select_executable)
exe_button.pack()

# 按钮: 保存配置
save_button = tk.Button(root, text="保存配置", command=lambda: [set_astitle(), save_config()])
save_button.pack()

# 运行主循环
root.mainloop()