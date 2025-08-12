# chart.py操作文档

## 一、概述
本 Python 文件 用于创建图标并保存图标为html文件至指定目录。

## 二、环境要求
- Python 3.x
- pyecharts  
使用`pip install -r requirements.txt`安装所需的第三方库

## 三、函数解释

### 绘制条形统计图
```python
def create_All_BarChart(logs):
    """
    根据日志数据创建所有体育器材的柱状图

    :param logs: 包含体育器材使用记录的列表
    """
    # 初始化一个字典，用于存储每种器材类型的借用次数
    DICT = {}
    for log in logs:
        # 打印当前日志记录
        # print(log)
        # print(get_equipment_type_by_code(log[2]))
        DICT[get_equipment_type_by_code(log[2])] = DICT.get(get_equipment_type_by_code(log[2]),0) + 1
    # print(DICT)

    temp = DICT.keys()
    # 初始化一个列表，用于存储器材类型
    types = []
    for i in temp:
        # 将器材类型添加到列表中
        types.append(i)
    # 初始化一个列表，用于存储借用次数
    nums = []
    for i in types:
        # 打印当前器材类型
        # print(i)
        # 将对应器材类型的借用次数添加到列表中
        nums.append(DICT[i])
    # 打印器材类型列表
    # print(types)
    # 打印第二个器材类型的借用次数
    # print(nums[1])
    # 创建一个柱状图实例
    bar = Bar()

    # 添加 x 轴数据
    bar.add_xaxis(types)

    # 添加 y 轴数据
    bar.add_yaxis("体育器材",nums)

    # 设置全局配置项
    # bar.set_global_opts(
    #     title_opts=opts.TitleOpts(title="所有"),
    #     xaxis_opts=opts.AxisOpts(name="器材"),
    #     yaxis_opts=opts.AxisOpts(name="借用次数")
    # )

    # 渲染图表到 HTML 文件
    bar.render("./Web/templates/all_usage_bar.html")
    print("成功创建/Web/templates/all_usage_bar.html")

```
- 功能：根据日志数据创建所有体育器材的柱状图
- 参数：logs 包含体育器材使用记录的列表
- 返回值：无

### 绘制折线统计图
```python
def create_All_LineChart_byDay(logs):
    """
    根据日志数据创建所有体育器材的柱状图

    :param logs: 包含体育器材使用记录的列表
    """
    
    DICT = {}
    # 把日期转换为列表
    for log in logs:
        string = log[3]
        temp = ""
        for chr in string:
            temp += chr
            if(chr == '日'):
                break
        DICT[temp] = DICT.get(temp,0) + 1
    
    # print(DICT)

    # 把字典的键值对转换为列表
    types = list(DICT.keys())
    nums = []
    for i in types:
        nums.append(DICT[i])

    result = {}
    for log1 in logs:
        date = log1[3].split()[0]  # 提取日期部分
        code1 = get_equipment_type_by_code(log1[2])  # 提取器材代码
        count = 1  # 假设每次记录为借用一次

        if date not in result:
            result[date] = {}
        result[date][code1] = result[date].get(code1, 0) + count
    
    # print(result)

    dates = list(result.keys())  # 获取所有日期
    codes = set()  # 用于存储所有器材代码
    
    for date_data in result.values():
        codes.update(date_data.keys())

    # 创建折线图
    line = Line()
    
    line.add_xaxis(types)
    line.add_yaxis('每日总借用情况',y_axis=nums,is_smooth = False)

    for code2 in codes:
        counts = [result[date].get(code2, 0) for date in dates]
        line.add_yaxis(code2,y_axis=counts,is_smooth = False)
        # print(counts)

    # line.set_global_opts(xaxis_opts=opts.AxisOpts(splitline_opts = opts.SplitLineOpts(is_show=True)))
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="每日器材借用情况"),
        xaxis_opts=opts.AxisOpts(name="日期"),
        yaxis_opts=opts.AxisOpts(name="借用次数"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
    )

    line.render("./Web/templates/all_usage_line.html")
    print("成功创建./Web/templates/all_usage_line.html")

```
- 功能：根据日志数据创建所有体育器材的柱状图
- 参数：logs 包含体育器材使用记录的列表
- 返回值：无

### 绘制饼图
```python
def create_All_PieChart(logs):
    result = {}
    for log in logs:
        code = get_equipment_type_by_code(log[2])  # 提取器材代码
        count = 1  # 假设每次记录为借用一次

        if code not in result:
            result[code] = 0
        result[code] += count

    pie = Pie()
    codes = list(result.keys())
    counts = list(result.values())

    # 添加数据
    pie.add("", [list(z) for z in zip(codes, counts)])

    # 设置全局配置项
    pie.set_global_opts(
        title_opts=opts.TitleOpts(title="器材借用占比"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="2%")
    )

    # 设置系列配置项
    pie.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))

    # 渲染图表到 HTML 文件
    pie.render("./Web/templates/all_usage_pie.html")
    print("成功创建./Web/templates/equipment_usage_pie.html")

```
- 功能：根据日志数据创建所有体育器材的柱状图
- 参数：logs 包含体育器材使用记录的列表
- 返回值：无

## 注意事项
- 本文件中的函数需要在其他文件中调用才能生效。
- 请确保你的 html 文件中的图像路径正确，否则可能无法正确显示图像。
- 代码中注释掉的部分是一些未使用的功能，可以根据需要进行修改和启用。