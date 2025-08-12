# !usr/bin/python3
# @writer ZhuZehang
# @Last:2025年1月25日

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import MDViewer
from Web.db import *
import ollama
import json
###############################################################
'''设置主要窗口基本信息'''
window = tk.Tk()
window.title("体育器材管理")
window.iconbitmap("./ICONs/Windows.ico")
window.geometry("470x300")
style = ttk.Style()
style.theme_use('clam')
###############################################################
# 基础初始化设置
base_url = "http://localhost:11434/api"

headers = {
    "Content-Type": "application/json"
}

'''用户名和密码'''
users = {
    "admin": "123456",
}

model_name = "qwen2.5:7b"

settings = {"base_url": base_url, "headers": headers, "model_name": model_name, "users": users}

def write_config_to_file():

    try:
        with open('config.json', 'w') as file:
            json.dump(settings, file)
        return True
    except Exception as e:
        print(f"Fail to write {e}")
    file.close()

def set_config_from_file():
    global base_url
    global users
    global model_name
    try:
        with open('config.json', 'r') as file:
            config = json.load(file)
        base_url = config['base_url']
        users = config['users']
        model_name = config['model_name']
        file.close()
        return True
    except Exception as e:
        print(f"Error reading config file: {e}")
        file.close()
        return False
###############################################################
ChildWindowGeometry = "200x150"
'''定义菜单命令函数'''
# 借器材
def action_borrow():
    # 创建主窗口
    root = tk.Tk()
    root.title("借出")
    root.attributes('-topmost', True)
    # 设置窗口大小为400x300像素
    root.attributes('-topmost', True)
    root.geometry(ChildWindowGeometry)
    
    # 创建并放置姓名标签和输入框
    label_name = tk.Label(root, text="姓名:")
    label_name.grid(row=0, column=0)
    entry_name = tk.Entry(root)
    entry_name.grid(row=0, column=1)

    # 创建并放置班级标签和输入框
    label_class = tk.Label(root, text="班级:")
    label_class.grid(row=1, column=0)
    entry_class = tk.Entry(root)
    entry_class.grid(row=1, column=1)

    # 创建并放置器材编号标签和输入框
    label_num = tk.Label(root, text="器材编号:")
    label_num.grid(row=2, column=0)
    # label_num.config(state='readonly')
    entry_num = tk.Entry(root)
    entry_num.grid(row=2, column=1)

    # 定义提交按钮的回调函数，用于获取输入框内容并打印
    def submit():
        global name, class_name, num
        name = entry_name.get()
        class_name = entry_class.get()
        num = entry_num.get()
        # print(f"Name: {name}, Class: {class_name}, Number: {num}")
        
        # 如果器材存在且未被借出
        if(check_code_exists(num) and (get_equipment_state(num) != -1)):
            try:
                addLog(name,class_name,num)
                update_equipment_state(num,-1)
                messagebox.showinfo("信息", "登记成功!")
            
            except Exception as E:
                messagebox.showerror("错误",E)
        else:
            messagebox.showinfo("信息",f"器材:{num}不存在或被借出!")

        root.destroy()


    # 创建并放置确定按钮，点击时调用submit函数
    submit_button = tk.Button(root, text="登记", command=lambda:submit())
    submit_button.grid(row=3, columnspan=2) 

    # 启动主事件循环
    root.mainloop()

# 还器材
def action_return():
    # 定义一个内部函数，用于获取输入框中的器材编码并打印
    def get_equipment_code():
        global num  # 声明num为全局变量，以便在函数外部也能访问
        num = entry.get()  # 从输入框中获取文本内容

        if(get_log_state(num) == -25565):
            messagebox.showinfo("提示",f"编号为{num}的器材没有借出记录")
        else:
            try:
                update_equipment_state(num,0)
                update_log_state(num)
                return_value :int = add_return_time(num)
                if(return_value == 0):
                    messagebox.showinfo("信息", f"编号为{num}的器材没有借出记录")
                if(return_value == -1):
                    messagebox.showerror("错误", f"数据库操作失败!")
                    exit(-1)
                else:
                    messagebox.showinfo("信息", "归还成功")
            except Exception as E:
                messagebox.showerror("错误",E)
                exit(-1)
        root.destroy()


    # 创建主窗口
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.geometry(ChildWindowGeometry)  # 设置窗口大小为400x300像素
    root.title("归还")  # 设置窗口标题为“归还”

    # 创建并放置标签，提示用户输入器材编号
    label = tk.Label(root, text="器材编号:")
    label.pack()  # 使用pack布局管理器自动调整位置

    # 创建输入框，供用户输入器材编号
    entry = tk.Entry(root)
    entry.pack()  # 使用pack布局管理器自动调整位置

    # 创建提交按钮，点击时调用get_equipment_code函数
    submit_button = tk.Button(root, text="Submit", command=lambda:get_equipment_code())
    submit_button.pack()  # 使用pack布局管理器自动调整位置

    # 启动主事件循环，等待用户操作
    root.mainloop()

# 新增器材
def action_addEquipment():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.geometry(ChildWindowGeometry)  # 设置窗口大小为400x300像素
    root.title("增加器材")  # 设置窗口标题为“增加器材”
        
    # 创建标签和输入框
    label_kind = tk.Label(root, text="种类:")
    label_kind.pack()
    entry_kind = tk.Entry(root)
    entry_kind.pack()

    # 处理输入
    def get_input():
        kind = entry_kind.get()

        try:
            code = generate_next_code()
            addEquipment(f'{kind}',f'{code}')
        except Exception as E:
            messagebox.showerror("错误",f"错误:{E}")
            exit()
        messagebox.showinfo("信息",f"物品{kind}添加成功,编号:{code}")
        root.destroy()
    
    # 创建确定按钮
    button_confirm = tk.Button(root, text="确定", command=lambda:get_input())
    button_confirm.pack()

    # 运行主循环
    root.mainloop()
def action_log():
    def fetch_data():

        comEquipment.execute("SELECT * FROM LOG ORDER BY ID DESC")  # 按ID倒序排列
        rows = comEquipment.fetchall()
        return rows

    class App:
        def __init__(self, root):
            self.root = root
            root.attributes('-topmost', True)
            self.root.title("登记记录浏览")
            root.geometry("800x400")
            # 创建Listbox控件
            self.listbox = tk.Listbox(root, width=80, height=20)
            self.listbox.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
            # # 添加滑动条
            # self.scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.listbox.yview)
            # self.listbox.configure(yscrollcommand=self.scrollbar.set)
            # self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            # 加载数据到Listbox
            self.load_data()
        def load_data(self):
            data = fetch_data()
            for row in data:
                state_text = "已归还" if row[5] == 1 else "未归还"
                # 假设 TIME2 是 row[6]，根据实际情况调整索引
                self.listbox.insert(tk.END, f"ID: {row[0]}, 姓名: {row[1]}, 班级: {row[2]}, CODE: {row[3]}, 借出时间: {row[4]}, 状态: {state_text}, 归还时间: {row[6]}")
    root = tk.Tk()
    app = App(root)
    root.mainloop()
def action_AI():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.title('AI建议')
    root.geometry('400x300')

    # 创建一个文本框来显示聊天内容
    text_box = tk.Text(root, height=15, width=50)
    text_box.pack()
    comEquipment.execute("SELECT NAME, CLASS, CODE,TIME,STATE FROM LOG")
    logs = comEquipment.fetchall()

    temp = ""
    for log in logs:
        temp += f"在{log[3]}借出{get_equipment_type_by_code(log[2])}器材,"

    completion = f"你是一个数据分析员,下面是一个学校的器材借出记录,已知{temp}猜测一\
                                     下今后一周内借用的趋势和提出详细的器材增加的建议"
    stream = ollama.chat(
        model='qwen2.5:7b',
        messages=[{'role': 'user', 'content': completion}],
        stream=True,
    )

    for chunk in stream:
        # print(chunk)
        # 将聊天内容插入到文本框中
        text_box.insert(tk.END, chunk['message']['content'])
        # 滚动到文本框的底部，以便始终显示最新的消息
        text_box.see(tk.END)
        # 更新窗口，以便立即显示新的聊天内容
        root.update()

    root.mainloop()

def action_delEquipment():
    # 创建主窗口
    root = tk.Tk()
    root.geometry(ChildWindowGeometry)  # 设置窗口大小为400x300像素
    root.title("删除器材")

    # 创建一个标签并添加到主窗口中
    label = tk.Label(root, text="请输入编号:")
    label.pack()

    # 创建一个输入框并添加到主窗口中
    entry = tk.Entry(root)
    entry.pack()

    # 定义按钮点击事件的处理函数
    def on_button_click():
        # 获取输入框中的文本内容
        code = entry.get()
        # 弹出一个提问框，返回值是 'yes' 或 'no'
        response = messagebox.askquestion("提问", "你确定要继续删除吗?(此操作不可逆!)")
        
        if response == 'yes':
            delete_equipment_by_code(code)
            # 在这里添加用户选择“是”时的操作
        root.destroy()
    # 创建一个按钮并设置点击事件处理函数
    button = tk.Button(root, text="提交", command=on_button_click)
    button.pack()

    # 进入主循环，显示窗口
    root.mainloop()
def action_settings():
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.geometry("490x250")  # 适当增加窗口宽度以适应布局变化
    root.title("系统配置")

    # 创建标签和输入框，使用 grid 布局
    # Base URL 部分
    label_base_url = tk.Label(root, text="AI服务器地址:")
    label_base_url.grid(row=0, column=0, padx=10, pady=5)
    entry_base_url = tk.Entry(root, width=50)  # 增加输入框长度
    entry_base_url.insert(0, base_url)  # 设置默认值
    entry_base_url.grid(row=0, column=1, padx=10, pady=5)

    # Model Name 部分
    label_model_name = tk.Label(root, text="模型名称:")
    label_model_name.grid(row=1, column=0, padx=10, pady=5)
    entry_model_name = tk.Entry(root, width=50)  # 增加输入框长度
    entry_model_name.insert(0, model_name)  # 设置默认值
    entry_model_name.grid(row=1, column=1, padx=10, pady=5)

    # Headers 部分
    label_headers = tk.Label(root, text="Headers:")
    label_headers.grid(row=2, column=0, padx=10, pady=5)
    entry_headers = tk.Entry(root, width=50)  # 增加输入框长度
    entry_headers.insert(0, str(headers))  # 设置默认值
    entry_headers.grid(row=2, column=1, padx=10, pady=5)

    # 处理确定按钮点击事件
    def confirm_settings():
        global base_url, model_name, headers
        try:
            base_url = entry_base_url.get()
            model_name = entry_model_name.get()
            headers = eval(entry_headers.get())  # 将输入的字符串转换为字典
            settings = {"base_url": base_url, "headers": headers, "model_name": model_name, "users": users}
            if write_config_to_file():
                messagebox.showinfo("信息", "配置保存成功！")
                root.destroy()
            else:
                messagebox.showerror("错误", "配置保存失败！")
        except Exception as e:
            messagebox.showerror("错误", f"配置保存失败：{e}")
    # 处理取消按钮点击事件
    def cancel_settings():
        root.destroy()
    # 处理配置用户按钮点击事件
    def configure_users():
        """
        配置用户信息的窗口
        """
        # 创建新窗口
        user_window = tk.Tk()
        user_window.attributes('-topmost', True)
        user_window.title("配置用户")
        user_window.geometry("300x250")

        # 新用户名输入框
        label_new_username = tk.Label(user_window, text="新用户名:")
        label_new_username.grid(row=0, column=0, padx=10, pady=5)
        entry_new_username = tk.Entry(user_window)
        entry_new_username.grid(row=0, column=1, padx=10, pady=5)

        # 原先密码输入框
        label_old_password = tk.Label(user_window, text="原先密码:")
        label_old_password.grid(row=1, column=0, padx=10, pady=5)
        entry_old_password = tk.Entry(user_window, show="*")
        entry_old_password.grid(row=1, column=1, padx=10, pady=5)

        # 新密码输入框
        label_new_password = tk.Label(user_window, text="新密码:")
        label_new_password.grid(row=2, column=0, padx=10, pady=5)
        entry_new_password = tk.Entry(user_window, show="*")
        entry_new_password.grid(row=2, column=1, padx=10, pady=5)

        # 确认新密码输入框
        label_confirm_password = tk.Label(user_window, text="确认新密码:")
        label_confirm_password.grid(row=3, column=0, padx=10, pady=5)
        entry_confirm_password = tk.Entry(user_window, show="*")
        entry_confirm_password.grid(row=3, column=1, padx=10, pady=5)

        def update_user_info():
            """
            更新用户信息的函数
            """
            new_username = entry_new_username.get()
            old_password = entry_old_password.get()
            new_password = entry_new_password.get()
            confirm_password = entry_confirm_password.get()

            # 检查新密码和确认新密码是否一致
            if new_password != confirm_password:
                messagebox.showerror("错误", "新密码和确认新密码不一致，请重新输入！")
                return

            # 检查原先密码是否正确（这里假设只有一个用户 "admin"）
            if "admin" in users and users["admin"] == old_password:
                # 更新用户信息
                users[new_username] = new_password
                # 更新 settings 字典
                settings["users"] = users
                # 保存配置到文件
                if write_config_to_file():
                    messagebox.showinfo("信息", "用户信息更新成功！")
                    user_window.destroy()
                else:
                    messagebox.showerror("错误", "用户信息更新失败，请稍后重试！")
            else:
                messagebox.showerror("错误", "原先密码错误，请重新输入！")

        # 修改按钮
        button_update = tk.Button(user_window, text="修改", command=update_user_info)
        button_update.grid(row=4, column=0, columnspan=2, pady=20)

        # 运行主循环
        user_window.mainloop()

    # 创建按钮，使用 grid 布局让按钮横向分布
    button_configure_users = tk.Button(root, text="配置用户", command=configure_users)
    button_configure_users.place(x=50,y=150)
    button_cancel = tk.Button(root, text="取消", command=cancel_settings)
    button_cancel.place(x=250,y=150)
    button_confirm = tk.Button(root, text="确定", command=confirm_settings)
    button_confirm.place(x=300,y=150)

    # 运行主循环
    root.mainloop()

def exit_app():
    window.quit()

def about():
    messagebox.showinfo("关于", "体育器材管理器by@朱泽杭")

def action_help():
    MDViewer.MDViewer("./help/sec.help.md")

def action_excel():
    # 弹出文件保存对话框，让用户选择保存位置和文件名
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            # 调用导出函数，将文件路径作为参数传入
            export_log_table_to_excel(file_path)
            messagebox.showinfo("信息", "记录导出为 Excel 文件成功！")
        except Exception as e:
            messagebox.showerror("错误", f"导出失败：{e}")
    else:
        messagebox.showinfo("提示", "未选择文件，导出取消。")

###############################################################
'''主函数'''
def main():
    '''创建菜单栏'''
    menubar = tk.Menu(window)

    # 创建“文件”菜单
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="配置", command=action_settings)  # 添加“新建”子菜单项
    file_menu.add_separator()  # 添加分隔线
    file_menu.add_command(label="退出", command=exit_app)  # 添加“退出”子菜单项
    menubar.add_cascade(label="软件", menu=file_menu)  # 将“文件”菜单添加到菜单栏

    # 创建“体育器材”菜单
    equipment_menu = tk.Menu(menubar, tearoff=0)
    equipment_menu.add_command(label="增加器材", command=lambda:action_addEquipment())  # 添加子菜单项
    equipment_menu.add_command(label="删除器材", command=lambda:action_delEquipment())  # 添加子菜单项
    equipment_menu.add_separator()  # 添加分隔线
    equipment_menu.add_command(label="记录导出为Excel", command=lambda:action_excel())  # 添加子菜单项
    menubar.add_cascade(label="体育器材", menu=equipment_menu)  # 将"体育器材"菜单添加到菜单栏

    # 创建“帮助”菜单
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="使用帮助", command=lambda:action_help())  # 添加子菜单项
    help_menu.add_command(label="关于", command=about)  # 添加子菜单项
    menubar.add_cascade(label="帮助", menu=help_menu)  # 将“帮助”菜单添加到菜单栏

    # 配置窗口使用菜单栏
    window.config(menu=menubar)

    '''创建快捷按钮'''
    bBorrow = tk.Button(window,text="借器材",height=3,width=10,command=lambda:action_borrow())
    bBorrow.grid(row=1,column=1)

    bReturn = tk.Button(window,text="还器材",height=3,width=10,command=lambda:action_return())
    bReturn.grid(row=2,column=1)

    bLog = tk.Button(window,text="登记记录",height=3,width=10,command=lambda:action_log())
    bLog.grid(row=3,column=1)

    bAnalysis = tk.Button(window,text="器材使用\n情况AI分析",height=3,width=10,command=lambda:action_AI())
    bAnalysis.grid(row=4,column=1)
    '''绘制背景'''
    # 加载图片
    image = Image.open("./data/bg.png")
    photo = ImageTk.PhotoImage(image)

    # 创建一个Label，用于显示图片
    label = tk.Label(window, image=photo)
    label.image = photo  # keep a reference!
    label.place(x=79,y=0)
    # 窗口主循环
    window.mainloop()

###############################################################
if __name__ == "__main__":
    set_config_from_file()
    main()
