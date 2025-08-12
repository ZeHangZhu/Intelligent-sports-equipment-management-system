# MDViewer.py操作文档
## 一、文件概述
MDViewer.py 是一个用于预览 Markdown 文件的 Python 脚本。它使用 `tkinter `库创建图形用户界面（GUI），并借助`markdown2` 库将 Markdown 文件转换为 HTML 格式，最后使用 `tkhtmlview `库在 GUI 中显示 HTML 内容。

## 二、环境准备
在运行本系统之前，需要确保你的Python环境中安装了以下库：

- tkinter：Python的标准GUI库，通常Python安装时已自带。
- Markdown2：用于处理图像
- tkhtmlview：用于在tkinter中显示HTML内容  
使用`pip install -r requirements.txt`安装所需的第三方库

## 三、函数解释
请参考代码中的注释部分，了解每个函数的功能、参数、返回值等信息。

### 把md转为html
```python
def MD2HTML(filename):
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
```
- 功能：把md转为html
- 参数：filename 文件名
- 返回值：包含html内容的字符串

### 显示html
```python
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

    window.mainloop()
```

### 以html形式显示md文件
```python
def MDViewer(mdfile):
    HtmlShow(MD2HTML(mdfile))
```
- 功能：以html形式显示md文件
- 参数：mdfile md文件名
- 返回值：无

## 注意事项
- 请确保你的 Markdown 文件与脚本在同一目录下，或者提供正确的文件路径。
- 脚本使用了临时文件来缓存转换后的 HTML 内容，在脚本运行结束后，临时文件不会被自动删除。
- 请确保你的 Markdown 文件中的图像路径正确，否则可能无法正确显示图像。
- 代码中注释掉的部分是一些未使用的功能，可以根据需要进行修改和启用。