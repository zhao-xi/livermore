import datetime

def convert_milliseconds_to_date_string(milliseconds):
    # 将毫秒时间戳转换为秒（Python的datetime模块使用的是秒级时间戳）
    if isinstance(milliseconds, str):
        milliseconds = float(milliseconds)
    seconds = milliseconds / 1000.0
    # 使用datetime.datetime.fromtimestamp()将秒级时间戳转换为datetime对象
    dt = datetime.datetime.fromtimestamp(seconds)
    # 使用datetime对象的strftime()方法将日期转换为字符串
    date_string = dt.strftime('%Y-%m-%d %H:%M')
    return date_string

def convert_date_string_to_milliseconds(date_string, format='%Y-%m-%d %H:%M:%S'):
    # 使用datetime.datetime.strptime()将日期字符串解析为datetime对象
    dt = datetime.datetime.strptime(date_string, format)
    # 使用datetime对象的timestamp()方法将日期转换为Unix时间戳（秒）
    timestamp = dt.timestamp()
    # 将秒级时间戳转换为毫秒时间戳
    milliseconds = int(timestamp * 1000)
    return milliseconds