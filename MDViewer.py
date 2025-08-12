import tkinter as tk
from tkinter import messagebox
from tkhtmlview import HTMLLabel
import markdown2
import sys

def MD2HTML(filename):
    # window.title(f"浏览- {filename}")
    string = ""
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            html_content = markdown2.markdown(content)
            string += html_content
    except Exception as e:
        messagebox.showerror("错误", f"无法打开文件: {e}")
    
    # 保存缓存文件
    # try:
    #     os.remove(f"%temp%/{filename}.tmp.html")
    # except:
    #     pass
    # tempfile = open(f"%temp%/{filename}.tmp.html",'w+')
    # tempfile.write(string)

    return string

def HtmlShow(html_content):
    # 创建主窗口
    window = tk.Tk()
    window.title("MD文件预览器")
    window.iconbitmap("./ICONs/Documentation.ico")
    window.geometry("800x600")
    # 创建框架用于包含 HTMLLabel 和滚动条
    frame = tk.Frame(window)
    frame.pack(fill=tk.BOTH, expand=True)

    # 创建 HTMLLabel 用于显示 HTML 文件内容
    html_label = HTMLLabel(frame, html=html_content, background="white")
    html_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # 创建垂直滚动条
    scrollbar = tk.Scrollbar(frame, command=html_label.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # 配置 HTMLLabel 使用滚动条
    html_label.configure(yscrollcommand=scrollbar.set)

    # # 定义打开文件函数
    # def open_file():
    #     file_path = filedialog.askopenfilename(defaultextension=".html", filetypes=[("HTML files", "*.html"), ("All files", "*.*")])
    #     if file_path:
    #         try:
    #             with open(file_path, 'r', encoding='utf-8') as file:
    #                 content = file.read()
    #                 html_label.set_html(content)
    #         except Exception as e:
    #             messagebox.showerror("错误", f"无法打开文件: {e}")

    # # 创建菜单栏
    # menubar = tk.Menu(window)

    # # 创建“文件”菜单
    # file_menu = tk.Menu(menubar, tearoff=0)
    # file_menu.add_command(label="打开", command=open_file)  # 添加“打开”子菜单项
    # menubar.add_cascade(label="文件", menu=file_menu)  # 将“文件”菜单添加到菜单栏

    # # 配置窗口使用菜单栏
    # window.config(menu=menubar)

    # 运行主循环
    window.mainloop()

def MDViewer(mdfile):
    HtmlShow(MD2HTML(mdfile))

if __name__ == "__main__":
    filename = sys.argv[1]
    MDViewer(filename)