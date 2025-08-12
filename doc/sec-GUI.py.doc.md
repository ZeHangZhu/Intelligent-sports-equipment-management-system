# 体育器材管理系统操作文档
## 一、系统概述
本系统是一个基于Python的体育器材管理系统，使用 tkinter 库构建图形用户界面（GUI），实现了体育器材的借用、归还、新增、删除等功能。

## 二、环境准备
在运行本系统之前，需要确保你的Python环境中安装了以下库：

- tkinter：Python的标准GUI库，通常Python安装时已自带。
- Pillow：用于处理图像  
使用`pip install -r requirements.txt`安装所需的第三方库

## 三、函数解释
请参考代码中的注释部分，了解每个函数的功能、参数、返回值等信息。

### 设置全局变量
```python
'''设置主要窗口基本信息'''
window = tk.Tk()
window.title("体育器材管理")
window.iconbitmap("./ICONs/Windows.ico")
window.geometry("470x300")
style = ttk.Style()
style.theme_use('clam')
```
- 功能：设置主要窗口基本信息
- 参数：无
- 返回值：无

### 处理借用器材命令
```python
def mBorrow():
    # 创建主窗口
    root = tk.Tk()
    root.title("借出")
    # 设置窗口大小为400x300像素
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
```
- 功能：处理借用器材命令
- 参数：无
- 返回值：无

### 处理归还器材命令
```python
def mReturn():
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
                messagebox.showinfo("信息", "归还成功")
            except Exception as E:
                messagebox.showerror("错误",E)
                exit(-1)
        root.destroy()


    # 创建主窗口
    root = tk.Tk()
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
```
- 功能：处理归还器材命令
- 参数：无
- 返回值：无

### 处理新增器材命令
```python
def mAddEquipment():
    root = tk.Tk()
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
```
- 功能：处理新增器材命令
- 参数：无
- 返回值：无

### 处理删除器材命令
```python
def mDelEquipment():
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
```
- 功能：处理删除器材命令
- 参数：无
- 返回值：无

### 查看记录
```python
def mLog():
    def fetch_data():

        comEquipment.execute("SELECT * FROM LOG ORDER BY ID DESC")  # 按ID倒序排列
        rows = comEquipment.fetchall()
        return rows

    class App:
        def __init__(self, root):
            self.root = root
            self.root.title("Log Data Viewer")
            root.geometry("666x400")

            
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
                self.listbox.insert(tk.END, f"ID: {row[0]}, NAME: {row[1]},\
                                    CLASS: {row[2]}, CODE: {row[3]}, TIME: {row[4]}, STATE: {row[5]}")
    root = tk.Tk()
    app = App(root)
    root.mainloop()
```
- 功能：查看记录
- 参数：无
- 返回值：无

### AI分析
```python
def mAI():
    root = tk.Tk()
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
```
- 功能：AI分析
- 参数：无
- 返回值：无

### 处理菜单命令
```python
def exit_app():
    window.quit()

def about():
    messagebox.showinfo("关于", "体育器材管理器by@朱泽杭")

def mHelp():
    MDViewer.MDViewer("./help/sec.help.md")

```
- 功能：处理菜单命令
- 参数：无
- 返回值：无

### 主函数
```python
def main():
    '''创建菜单栏'''
    menubar = tk.Menu(window)

    # 创建“文件”菜单
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="配置", command=mSettings)  # 添加“新建”子菜单项
    file_menu.add_separator()  # 添加分隔线
    file_menu.add_command(label="退出", command=exit_app)  # 添加“退出”子菜单项
    menubar.add_cascade(label="软件", menu=file_menu)  # 将“文件”菜单添加到菜单栏

    # 创建“体育器材”菜单
    equipment_menu = tk.Menu(menubar, tearoff=0)
    equipment_menu.add_command(label="增加器材", command=lambda:mAddEquipment())  # 添加子菜单项
    equipment_menu.add_command(label="删除器材", command=lambda:mDelEquipment())  # 添加子菜单项
    menubar.add_cascade(label="体育器材", menu=equipment_menu)  # 将"体育器材"菜单添加到菜单栏

    # 创建“帮助”菜单
    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="使用帮助", command=lambda:mHelp())  # 添加子菜单项
    help_menu.add_command(label="关于", command=about)  # 添加子菜单项
    menubar.add_cascade(label="帮助", menu=help_menu)  # 将“帮助”菜单添加到菜单栏

    # 配置窗口使用菜单栏
    window.config(menu=menubar)

    '''创建快捷按钮'''
    bBorrow = tk.Button(window,text="借器材",height=3,width=10,command=lambda:mBorrow())
    bBorrow.grid(row=1,column=1)

    bReturn = tk.Button(window,text="还器材",height=3,width=10,command=lambda:mReturn())
    bReturn.grid(row=2,column=1)

    bLog = tk.Button(window,text="登记记录",height=3,width=10,command=mLog)
    bLog.grid(row=3,column=1)

    bAnalysis = tk.Button(window,text="器材使用\n情况AI分析",height=3,width=10,command=mAI)
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
if __name__ == "__main__":
    main()
```
- 功能：主函数
- 参数：无
- 返回值：无

## 五、注意事项
- 在使用借器材功能时，请确保输入的器材编号准确无误，否则可能会导致登记失败。

