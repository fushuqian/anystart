import configparser
import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

from PIL import Image, ImageTk

# Initialize configuration parser
config = configparser.ConfigParser()
config_folder = 'as_data'
config_file = os.path.join(config_folder, 'config.ini')
os.makedirs(config_folder, exist_ok=True)

if os.path.exists(config_file):
    config.read(config_file)
else:
    config['settings'] = {'imgpath': '', 'exepath': '', 'astitle': 'Main Window'}
    with open(config_file, 'w') as cf:
        config.write(cf)

img_path = config.get('settings', 'imgpath', fallback='default.png')
exe_path = config.get('settings', 'exepath', fallback='default.exe')
as_title = config.get('settings', 'astitle', fallback='Main Window')

if not os.path.exists(img_path):
    img_path = 'default.png'


root = tk.Tk()
root.title(as_title)
root.resizable(False, False)

def center_window(window, width, height):
    # 获取屏幕尺寸
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # 计算中心位置
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    # 设置窗口位置
    window.geometry(f'{width}x{height}+{x}+{y}')

# 设置窗口大小和居中显示
center_window(root, 400, 600)



def load_image(path):
    try:
        image = Image.open(path)
    except FileNotFoundError:
        image = Image.new('RGB', (400, 300), color='gray')
    image = image.resize((400, int(400 * image.height / image.width)), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(image)

photo = load_image(img_path)
image_label = tk.Label(root, image=photo)
image_label.pack(side='top', fill='x')

def start_program():
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    try:
        subprocess.Popen(f'"{exe_path}"', startupinfo=startupinfo)
    except Exception as e:
        messagebox.showerror("错误", f"无法启动程序: {e}")

def open_settings_window():
    settings_window = tk.Toplevel(root)
    settings_window.title("设置")
    settings_window.geometry("310x220")
    settings_window.grab_set()
    settings_window.resizable(False, False)
    center_window(settings_window , 310, 260)

    frame = tk.Frame(settings_window, padx=10, pady=10)
    frame.pack(expand=True, fill='both')

    tk.Label(frame, text="设置窗口标题").grid(row=0, column=0, padx=10, pady=10, sticky='e')

    title_entry = tk.Entry(frame)
    title_entry.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
    title_entry.insert(0, config.get('settings', 'astitle', fallback='AnyStart'))
    button_width = 40  # 可以调整这个值来改变所有按钮的宽度

    def sel_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            file_name = os.path.basename(file_path)
            target_path = os.path.join(config_folder, file_name)
            shutil.copy(file_path, target_path)
            config.set('settings', 'imgpath', target_path)
            with open(config_file, 'w') as configfile:
                config.write(configfile)
            messagebox.showinfo("成功", "图片已更新")
            global photo
            photo = load_image(target_path)
            image_label.config(image=photo)

    img_button = tk.Button(frame, text="更换封面", command=sel_image, width=button_width)
    img_button.grid(row=1, column=0, columnspan=2, pady=20, sticky='ew')

    exe_entry = tk.Entry(frame)  # 添加定义
    exe_entry.grid(row=2, column=1, padx=10, pady=10, sticky='ew')
    exe_entry.insert(0, exe_path)

    def browse_exe():
        filename = filedialog.askopenfilename(filetypes=[("应用程序", "*.exe")])
        if filename:
            exe_entry.delete(0, tk.END)
            exe_entry.insert(0, filename)

    browse_button = tk.Button(frame, text="选择程序", command=browse_exe, width=button_width)
    browse_button.grid(row=2, column=0, columnspan=2, pady=5, sticky='ew')

    def save_settings():
        new_title = title_entry.get()
        selected_exe = exe_entry.get()
        selected_img_path = config.get('settings', 'imgpath', fallback='default.png')
        config.set('settings', 'astitle', new_title)
        config.set('settings', 'exepath', selected_exe)
        config.set('settings', 'imgpath', selected_img_path)
        with open(config_file, 'w') as configfile:
            config.write(configfile)
        messagebox.showinfo("Info", "设置已保存")
        settings_window.destroy()
        root.title(new_title)
        global photo
        photo = load_image(selected_img_path)
        image_label.config(image=photo)

    save_button = tk.Button(frame, text="保存", command=save_settings, width=button_width)
    save_button.grid(row=3, column=0, columnspan=2, pady=20)

start_button = tk.Button(root, text="开始", command=start_program)
settings_button = tk.Button(root, text="设置", command=open_settings_window)
exit_button = tk.Button(root, text="退出", command=root.quit)

button_width = 80
button_height = 30
button_spacing = (400 - 3 * button_width) // 4
button_y = photo.height() + 10

start_button.place(x=button_spacing, y=button_y, width=button_width, height=button_height)
settings_button.place(x=2 * button_spacing + button_width, y=button_y, width=button_width, height=button_height)
exit_button.place(x=3 * button_spacing + 2 * button_width, y=button_y, width=button_width, height=button_height)

root.geometry(f"400x{button_y + button_height + 10}")
root.mainloop()