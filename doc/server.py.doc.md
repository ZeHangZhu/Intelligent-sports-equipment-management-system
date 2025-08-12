# 体育器材管理服务端操作文档
## 概述
此部分代码主要进行基础的初始化设置，定义了 API 请求的基础 URL 和请求头，用于后续与特定 API 进行交互。

## 二、环境要求
- Python 3.x
- Flask 框架
- requests 库  
使用`pip install -r requirements.txt`安装所需的第三方库

## 三、文件结构
文件包含以下几个主要部分：
1. **初始化设置**：定义了基础的 URL 和请求头。
2. **API 请求函数**：涵盖了获取器材列表、获取器材详情、添加器材、删除器材、更新器材、获取日志列表、获取日志详情、添加日志、删除日志、更新日志等功能。

## 四、函数详细解释
请参考代码中的注释部分，了解每个函数的功能、参数、返回值等信息。

### （一）全局变量
```python
# 基础初始化设置
base_url = "http://localhost:11434/api"
headers = {
    "Content-Type": "application/json"
}
```
- `base_url`：基础的 URL，用于构建完整的 API 请求 URL。
- `headers`：请求头，用于指定请求的内容类型为 JSON。

### (二)主页
```python
@app.route('/')
def PageMain():
    # 查询Log表中的所有数据
    comEquipment.execute("SELECT NAME, CLASS, CODE,TIME,STATE FROM Log")
    logs = comEquipment.fetchall()
    
    # 返回值可以包含HTML标签
    return render_template("index.html",logs=logs)
```

```python
@app.route('/index')
def PageIndex():
    # 查询Log表中的所有数据
    comEquipment.execute("SELECT NAME, CLASS, CODE,TIME,STATE FROM Log")
    logs = comEquipment.fetchall()
    
    # 返回值可以包含HTML标签
    return render_template("index.html",logs=logs)
```
- 功能：主页
- 参数：无
- 返回值：HTML页面

### (三)借器材页面
```python
@app.route('/borrow',methods=['GET', 'POST'])
def PageBorrow():
    # 返回值可以包含HTML标签
    if(request.method == 'POST'):
        ClassName = request.form['class']
        Name = request.form['name']
        code = request.form['code']

        print(f"[POST] {ClassName},{Name},{code}")
        if(not check_code_exists(code)):
            # 器材不存在
            return '''<!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>弹出错误提示框</title>
    </head>
    <body>
        <script>
            alert("体育器材不存在，请重新输入");
        </script>
        <a href="/borrow">
    </body>
    </html>'''
        else:
            # 器材存在
            if(get_equipment_state(code)==0):
                # 器材可用
                addLog(Name, ClassName, code)
                return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>成功</title>
    </head>
    <body>
        <p>体育器材借用成功！</p>
        <a href="/borrow">点此返回</a>
    </body>
    </html>
                        '''
            else:
                return '''<!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>提示</title>
    </head>
    <body>
        <script>
            alert("体育器材已被借用，请重新选择");
        </script>
        <a href="/borrow">
    </body>
    </html>'''

    if(request.method == 'GET'):
        return render_template("borrow.html") 
```
- 功能：借器材页面
- 参数：无
- 返回值：HTML页面

### (四)归还器材页面
```python
@app.route('/return',methods=['GET', 'POST'])
def PageReturn():
    if(request.method == 'POST'):
        num = request.form['code']
        print(f"[*]CODE:{num}")

        if(get_log_state(num) == -25565):
           print("未找到该器材")

           return '''<!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>错误</title>
    </head>
    <body>
        <script>
            alert("体育器材不存在或没有借出记录，请重新输入");
        </script>
        <a href="/return">
    </body>
    </html>'''

        else:
            try:
                update_equipment_state(num,0)
                update_log_state(num)
                print("归还成功")
                return '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>成功</title>
    </head>
    <body>
        <p>体育器材归还成功！</p>
        <a href="/return">点此返回</a>
    </body>
    </html>
                        '''
            except Exception as E:
                print(f'[!]{E}')
                exit(-1)
                return E
    if(request.method == 'GET'):
        return render_template("return.html")

```
- 功能：归还器材页面
- 参数：无
- 返回值：HTML页面

### (五)器材使用分析页面
```python
@app.route('/analysis')
def PageAnalysis():
    # 创建图表
    chart.create_charts()
    # 将数据传递给模板
    return render_template("analysis.html")
```
- 功能：器材使用分析页面
- 参数：无
- 返回值：HTML页面

### (六)器材分析图表生成
```python
@app.route('/all_usage_bar.html')
def PageAnalysisBar():

    # 将数据传递给模板
    return render_template("all_usage_bar.html")

@app.route('/all_usage_line.html')
def PageAnalysisLine():

    # 将数据传递给模板
    return render_template("all_usage_line.html")

@app.route('/all_usage_pie.html')
def PageAnalysisPie():

    # 将数据传递给模板
    return render_template("all_usage_pie.html")
```
- 功能：器材分析图表生成
- 参数：无
- 返回值：HTML页面

### 帮助页面
```python
@app.route('/help')
def PageHelp():
    # 返回值可以包含HTML标签
    return render_template("help.html") 
```
- 功能：帮助页面
- 参数：无
- 返回值：HTML页面

### AI分析页面
```python
@app.route('/PageAI')
def PageAI():
    return render_template("AI.html")
```
- 功能：AI分析页面
- 参数：无
- 返回值：HTML页面

### AI分析API接口
```python
@app.route('/stream_response', methods=['POST'])
def stream_response():
    comEquipment.execute("SELECT NAME, CLASS, CODE,TIME,STATE FROM LOG")
    logs = comEquipment.fetchall()

    temp = ""
    for log in logs:
        temp += f"在{log[3]}借出{get_equipment_type_by_code(log[2])}器材,"

    completion = f"你是一个数据分析员,下面是一个学校的器材借出记录,已知{temp}猜测一\
                                     下今后一周内借用的趋势和提出详细的器材增加的建议"
    def generate(prompt, model="qwen2.5:7b"):
        url = f"{base_url}/generate"
        data = {
            "model": model,
            "prompt": prompt,
            "stream": True
        }
        response = requests.post(url, headers=headers, json=data, stream=True)
        result = ""
        for line in response.iter_lines():
            if line:
                result += line.decode('utf-8')
                yield json.loads(line.decode('utf-8'))["response"]
    return Response(generate(completion), content_type='text/plain')
```
- 功能：AI分析API接口
- 参数：无
- 返回值：JSON数据