#!/usr/bin/python3
from flask import Flask, Response, session
from flask import render_template, send_file
from flask import Flask, request, jsonify
from flask import redirect
from flask import request
from db import *
import chart
import requests
import json

# 基础初始化设置
base_url = "http://localhost:11434/api"

headers = {
    "Content-Type": "application/json"
}

'''用户名和密码'''
users = {
    "admin": "123456",
    "test": "123456"
}

model_name = "qwen2.5:7b"

settings = {"base_url": base_url, "headers": headers, "model_name": model_name, "users": users}

is_login :bool = False

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

app = Flask(__name__, static_folder="./Web")  # 创建Flask对象，把当前模块的名称作为参数传递进去
app.secret_key = 'your_secret_key'  # 设置会话的密钥

# 定义主页路由
@app.route('/')
def PageMain():
    if(is_login == False):
        return render_template("login.html")
    else:
        # 查询Log表中的所有数据
        comEquipment.execute("SELECT NAME, CLASS, CODE,TIME,STATE,TIME2 FROM Log")
        logs = comEquipment.fetchall()
        
        
        # 返回值可以包含HTML标签
        return render_template("index.html", logs=logs)

# 登录处理路由
@app.route('/login', methods=['POST'])
def login():
    # 刷新设置
    set_config_from_file()

    global is_login  # 使用 global 关键字声明使用全局变量
    account = request.form.get('account')
    password = request.form.get('password')

    # 检查用户名和密码是否匹配
    print(f"[*] {account} {password}")
    if account in users and users[account] == password:
        is_login = True  # 修改全局变量
        return redirect('/index')
    else:
        return render_template("login_wron.html")

# 登出处理路由
@app.route('/logout')
def logout():
    is_login = False
    return render_template("login.html")

# 定义需要登录才能访问的路由
@app.route('/index', methods=['GET'])
def PageIndex():
    if(is_login == False):
        return render_template("login.html")
    # 查询Log表中的所有数据
    comEquipment.execute("SELECT NAME, CLASS, CODE,TIME,STATE,TIME2 FROM Log")
    logs = comEquipment.fetchall()
    
    # 返回值可以包含HTML标签
    return render_template("index.html", logs=logs)

# 其他路由也需要添加登录检查
@app.route('/borrow', methods=['GET', 'POST'])
def PageBorrow():
    if(is_login == False):
        return render_template("login.html")
    # 返回值可以包含HTML标签
    if request.method == 'POST':
        ClassName = request.form['class']
        Name = request.form['name']
        code = request.form['code']

        print(f"[POST] {ClassName},{Name},{code}")
        if not check_code_exists(code):
            # 器材不存在
            return render_template("error.html")
        else:
            # 器材存在
            if get_equipment_state(code) == 0:
                # 器材可用
                addLog(Name, ClassName, code)
                return render_template("borrow_success.html")
            else:
                return render_template("borrowed.html")

    if request.method == 'GET':
        return render_template("borrow.html")

@app.route('/return',methods=['GET', 'POST'])
def PageReturn():
    if(is_login == False):
        return render_template("login.html")
    if(request.method == 'POST'):
        num = request.form['code']
        print(f"[*]CODE:{num}")

        if(get_log_state(num) == -25565 or get_log_state(num) == 1):
           print("未找到该器材")

           return render_template("nolog.html")

        else:
            try:
                update_equipment_state(num,0)
                update_log_state(num)
                print("归还成功")
                return render_template("return_success.html")
            except Exception as E:
                print(f'[!]{E}')
                exit(-1)
                return E
    if(request.method == 'GET'):
        return render_template("return.html")


@app.route('/analysis')
def PageAnalysis():
    # 创建图表
    chart.create_charts()
    # 将数据传递给模板
    return render_template("analysis.html")

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

@app.route('/help')
def PageHelp():
    # 返回值可以包含HTML标签
    return render_template("help.html") 

@app.route('/wbg.png')
def ImgWBG():
    # 返回值可以包含HTML标签
    return send_file(".\\img\\wbg.png")

@app.route('/beijing.jpg')
def ImgBeijing():
    # 返回值可以包含HTML标签
    return send_file(".\\img\\beijing.jpg")
@app.route('/logo.png')
def ImgLogo():
    return send_file(".\\img\\logo.png")
@app.route('/PageAI')
def PageAI():
    return render_template("AI.html")

@app.route('/stream_response', methods=['POST'])
def stream_response():
    comEquipment.execute("SELECT NAME, CLASS, CODE,TIME,STATE FROM LOG")
    logs = comEquipment.fetchall()

    temp = ""
    for log in logs:
        temp += f"在{log[3]}借出{get_equipment_type_by_code(log[2])}器材,"

    completion = f"你是一个数据分析员,下面是一个学校的器材借出记录,已知{temp}猜测一\
                                     下今后一周内借用的趋势和提出详细的器材增加的建议"
    def generate(prompt, model=model_name):
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
                try:
                    yield json.loads(line.decode('utf-8'))["response"]
                except Exception as e:
                    print(e)
    return Response(generate(completion), content_type='text/plain')
from datetime import datetime


def convert_date_format(date_str):
    """
    将 'YYYY-MM-DD' 格式的日期字符串转换为 'YYYY年M月D日' 格式。

    :param date_str: 输入的日期字符串，格式为 'YYYY-MM-DD'
    :return: 转换后的日期字符串，格式为 'YYYY年M月D日'
    """
    try:
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return f"{dt.year}年{str(dt.month).lstrip('0')}月{str(dt.day).lstrip('0')}日"
    except ValueError:
        print(f"输入的日期格式不正确，应为 'YYYY-MM-DD'，输入的是 {date_str}")
        return None


@app.route('/filter', methods=['GET', 'POST'])
def PageFilter():
    if is_login == False:
        return render_template("login.html")
    
    elif request.method == 'POST':
        # 获取用户输入的查询条件
        name = request.form.get('name')
        class_ = request.form.get('class')
        code = request.form.get('code')
        date = request.form.get('date')

        # 转换用户输入的日期格式
        if date:
            formatted_date = convert_date_format(date)

        # 构建 SQL 查询语句
        query = "SELECT * FROM LOG WHERE 1=1"
        params = []
        if name:
            query += " AND NAME LIKE ?"
            params.append(f"%{name}%")
        if class_:
            query += " AND CLASS LIKE ?"
            params.append(f"%{class_}%")
        if code:
            query += " AND CODE = ?"
            params.append(int(code))
        if date:
            query += " AND TIME LIKE ?"
            params.append(f"{formatted_date}%")

        # 执行查询
        comEquipment.execute(query, params)
        results = comEquipment.fetchall()
    else:
        results = []


    return render_template('filter.html', results=results)

@app.route('/excel')
def download_excel():
    export_log_table_to_excel("./web/excel.xlsx")
    return send_file("excel.xlsx", as_attachment=True)

if __name__ == '__main__':
    # 刷新设置
    set_config_from_file()
    # 启动Flask程序
    app.run(host='0.0.0.0', port=80) 