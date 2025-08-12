# 体育器材管理数据库操作文档

## 一、概述
本 Python 文件 `p:/体育器材管理/Web/db.py` 主要用于管理体育器材数据库，借助 SQLite 数据库实现器材信息的增删改查操作，同时记录器材使用日志。

## 二、环境要求
- Python 3.x
- 无需额外安装第三方库

## 三、文件结构
文件包含以下几个主要部分：
1. **数据库初始化**：连接到 SQLite 数据库并创建游标。
2. **数据库操作函数**：涵盖增加器材、增加日志、重建数据库、生成代码、检查代码是否存在等功能。

## 四、函数详细说明

### （一）数据库初始化
```python
import sqlite3
from datetime import datetime

'''初始化数据库'''
dbEquipment = sqlite3.connect('./data/Equipment.db', check_same_thread=False)
comEquipment = dbEquipment.cursor()
```

- 功能：连接到 ./data/Equipment.db 数据库，并创建一个游标对象用于执行 SQL 语句。
- 参数：
check_same_thread=False：
    - 允许在不同线程中使用同一个数据库连接。

### （二）增加器材
```python
def addEquipment(type, code):
    # 获取当前最大ID
    comEquipment.execute('SELECT MAX(ID) FROM EQUIPMENT')
    max_id = comEquipment.fetchone()[0]
    if max_id is None:
        max_id = 0
    new_id = max_id + 1
    
    # 插入新记录
    comEquipment.execute(f'''INSERT INTO EQUIPMENT (ID, CODE, TYPE, STATE) 
                         VALUES ({new_id}, {code},"{type}",0);''')
    dbEquipment.commit()
```

- 功能：向 EQUIPMENT 表中添加新的器材记录。
- 参数：
    - type：器材的类型，字符串类型。
    - code：器材的代码，整数类型。
- 注意事项：
    - 函数会自动生成新的 ID，其值为当前最大 ID 加1。
    - 新器材的初始状态 STATE 为 0。

### （三）增加日志
```python
def addLog(name, GradeAndClass, code):
    # 获取当前最大ID
    comEquipment.execute('SELECT MAX(ID) FROM LOG')
    max_id = comEquipment.fetchone()[0]
    if max_id is None:
        max_id = 0
    new_id = max_id + 1

    # 获取当前时间
    now = datetime.now()

    # 提取年、月、日、小时和分钟
    year = now.year
    month = now.month
    day = now.day
    hour = now.hour
    minute = now.minute

    DateAndTime = f"{year}年{month}月{day}日 {hour}点{minute}分"

    # 插入新记录
    comEquipment.execute(f'''INSERT INTO LOG (ID, NAME, CLASS, CODE, TIME, STATE) 
                         VALUES ({new_id}, "{name}","{GradeAndClass}",{code},"{DateAndTime}",0)''')
    dbEquipment.commit()
```
- 功能：向 LOG 表中添加新的日志记录。
- 参数：
    - name：使用器材的人员姓名，字符串类型。
    - GradeAndClass：使用器材的人员班级，字符串类型。
    - code：器材的代码，整数类型。
- 注意事项：
    - 函数会自动生成新的 ID，其值为当前最大 ID 加 1。
    - 日志记录的初始状态 STATE 为 0。
    - 日志记录会包含当前的日期和时间。

### （四）重新建立数据库文件并创建表
```python
def reInstallEquipment():
    # os.remove("./Data/Equipment.db")
    try:
        comEquipment.execute('''CREATE TABLE EQUIPMENT
        (ID INT PRIMARY KEY      NOT NULL,
            CODE           INT     NOT NULL,
            TYPE           TEXT     NOT NULL,
            STATE          INT      NOT NULL);''')
        comEquipment.execute('''CREATE TABLE LOG
        (ID INT PRIMARY KEY      NOT NULL,
            NAME           TEXT     NOT NULL,
            CLASS          TEXT     NOT NULL,
            CODE           INT     NOT NULL,
            TIME           TEXT     NOT NULL,
            STATE          INT      NOT NULL);''')
    except Exception as E:
        print(f"[!]{E}")
```
- 功能：重新建立数据库文件，并创建 EQUIPMENT 和 LOG 两个表。
- 注意事项：
    - 函数会删除原有的数据库文件，然后重新创建两个表。
    - 如果创建表时发生错误，会打印错误信息。

### （五）生成随机的器材代码
```python
def generate_next_code():
    # 获取当前最大CODE
    comEquipment.execute('SELECT MAX(CODE) FROM EQUIPMENT')
    max_code = comEquipment.fetchone()[0]
    if max_code is None:
        max_code = 0
    next_code = max_code + 1
    return next_code
```
- 功能：生成下一个可用的器材代码。
- 返回值：下一个可用的器材代码，整数类型。
- 注意事项：
    - 函数会查询 EQUIPMENT 表中当前最大的 CODE 值，然后返回该值加 1。
    - 如果 EQUIPMENT 表中没有记录，函数会返回 1。

### （六）检查器材代码是否存在
```python
def check_code_exists(code):
    # 查询CODE是否存在
    query = "SELECT COUNT(*) FROM EQUIPMENT WHERE CODE = ?"
    comEquipment.execute(query, (code,))
    
    # 获取查询结果
    result = comEquipment.fetchone()
    count = result[0]
    
    # 返回查询结果
    return count > 0
```
- 功能：检查给定的器材代码是否存在于 EQUIPMENT 表中。
- 参数：
    - code：要检查的器材代码，整数类型。
- 返回值：如果器材代码存在，返回 True；否则返回 False。

### （七）获取器材的类型
```python
def update_equipment_state(code, state):
    """
    更新EQUIPMENT表中指定CODE的STATE字段
    :param code: int, 设备的CODE
    :param state: int, 要更新的STATE值
    """
    try:
        # 更新STATE字段
        comEquipment.execute('''
        UPDATE EQUIPMENT
        SET STATE = ?
        WHERE CODE = ?
        ''', (state, code))
        
        # 提交事务
        dbEquipment.commit()
        print(f"Successfully updated the state for code {code} to {state}")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
```
- 功能：更新 EQUIPMENT 表中指定 CODE 的 STATE 字段。
- 参数：
    - code：要更新的器材代码，整数类型。
    - state：要更新的器材状态，整数类型。
- 注意事项：
    - 如果更新成功，会打印成功信息。
    - 如果更新失败，会打印错误信息。

### （八）获取器材的类型
```python
def get_equipment_state(code):
    """
    获取EQUIPMENT表中指定CODE的STATE字段的值
    :param code: int, 设备的CODE
    :return: int, 对应的STATE值
    """
    try:
        # 查询STATE字段
        comEquipment.execute('''
        SELECT STATE FROM EQUIPMENT
        WHERE CODE = ?
        ''', (code,))
        
        # 获取查询结果
        result = comEquipment.fetchone()
        if result:
            return result[0]
        else:
            print(f"No record found for code {code}")
            return -25565   # 返回错误代码
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
```
- 功能：获取 EQUIPMENT 表中指定 CODE 的 STATE 字段的值。
- 参数：
    - code：要查询的器材代码，整数类型。
- 返回值：对应的器材状态，整数类型。
- 注意事项：
    - 如果查询成功，返回 STATE 值。
    - 如果查询失败，返回 -25565。

### （九）获取日志的状态
```python
def get_log_state(code):
    query = """
    SELECT STATE FROM LOG WHERE CODE = ? ORDER BY ID DESC LIMIT 1
    """
    comEquipment.execute(query, (code,))
    result = comEquipment.fetchone()
    
    if result:
        return result[0]
    else:
        return -25565
```
- 功能：获取 LOG 表中指定 CODE 的最新状态。
- 参数：
    - code：要查询的器材代码，整数类型。
- 返回值：对应的日志状态，整数类型。
- 注意事项：
    - 如果查询成功，返回最新的 STATE 值。
    - 如果查询失败，返回 -25565。

### (十)更新日志的状态
```python
def update_log_state(code):
    # 找到最后一条对应 code 的记录
    query = """
    SELECT ID FROM LOG WHERE CODE = ? ORDER BY ID DESC LIMIT 1
    """
    comEquipment.execute(query, (code,))
    result = comEquipment.fetchone()
    
    if result:
        try:
            last_id = result[0]
            
            # 更新该记录的 STATE 为 1
            update_query = """
            UPDATE LOG SET STATE = 1 WHERE ID = ?
            """
            comEquipment.execute(update_query, (last_id,))
            dbEquipment.commit()
            print(f"Updated the state of record with ID {last_id} to 1.")
        except Exception as e:
            print(f"Error updating state: {e}")

    else:
        print(f"No record found for code {code}.")
```
- 功能：更新 LOG 表中指定 CODE 的最新状态为 1。
- 参数：
    - code：要更新的器材代码，整数类型。
- 注意事项：
    - 如果更新成功，会打印成功信息。
    - 如果更新失败，会打印错误信息。
    - 如果没有找到对应的记录，会打印相应信息。

### (十一)通过编号删除器材
```python
def delete_equipment_by_code(code):
    """
    删除数据库中CODE对应的设备记录

    参数:
    db_path (str): SQLite数据库文件的路径
    code (int): 要删除的设备CODE
    """
    try:
        # 执行删除操作
        sql_delete_query = '''DELETE FROM EQUIPMENT WHERE CODE = ?'''
        comEquipment.execute(sql_delete_query, (code,))
        
        # 提交事务
        dbEquipment.commit()
        print(f"成功删除CODE为{code}的设备记录")
    
    except Exception as E:
        print(f"错误:{E}")
```
- 功能：删除数据库中指定 CODE 的器材记录。
- 参数：
    - code：要删除的器材代码，整数类型。
- 注意事项：
    - 如果删除成功，会打印成功信息。
    - 如果删除失败，会打印错误信息。

### (十二)获取器材的类型
```python
def get_equipment_type_by_code(code):
    """
    根据设备的CODE获取对应的TYPE

    参数:
    code (int): 设备的CODE

    返回:
    str: 设备的TYPE，如果未找到则返回None
    """
    try:
        # 执行查询操作
        sql_select_query = '''SELECT TYPE FROM EQUIPMENT WHERE CODE = ?'''
        comEquipment.execute(sql_select_query, (code,))
        
        # 获取查询结果
        result = comEquipment.fetchone()
        if result:
            return result[0]
        else:
            print(f"未找到CODE为{code}的设备记录")
            return None
    
    except Exception as E:
        print(f"错误:{E}")
```
- 功能：根据设备的 CODE 获取对应的 TYPE。
- 参数：
    - code：要查询的器材代码，整数类型。
- 返回值：对应的器材类型，字符串类型。
- 注意事项：
    - 如果查询成功，返回 TYPE 值。
    - 如果查询失败，返回 None。
    