import okx.MarketData as MarketData
import pandas
import prettytable as pt
from utils import convert_milliseconds_to_date_string, convert_date_string_to_milliseconds
from market_data import get_candlesticks

def get_livermore_chart(start_ts, end_ts, params=[0.06, 0.03], bar="1D", trade_pair="BTC-USTD"):
    """
    获取利弗莫尔表格，默认第一个点记录于“上升趋势”
    :param start_ts: 起始毫秒时间戳
    :param end_ts: 终止毫秒时间戳
    :param params: 转向参数和突破参数，默认为6%和3%
    :param bar: 时间粒度，默认为天级k线
    :return: 利弗莫尔表格，长度为6的二维数组，分别为次级回升、自然回升、上升趋势、下降趋势、自然回撤、次级回撤
    """
    # 获取指数K线数据，整理为日期、收盘价格式
    datetime_and_close_price = get_candlesticks(start_ts, end_ts, bar, trade_pair)

    # livermore_chart，利弗莫尔表格为六列二维数组
    # 每个元素为[日期，次级回升栏，自然回升栏，上升趋势栏，下降趋势栏，自然回撤栏，次级回撤栏]的数组
    # 原文中画红线的数字使用-o后缀，黑线使用-x后缀
    livermore_chart = []
    current_recording_column = 3  # 当前正在记录列的下标，默认在上升趋势
    uptrend = True  # 当前是否在上升趋势中，默认为True
    last_value = [0, 0, 0, 0, 0, 0, 0]  # 每列的上一个值，第一个元素不用
    last_index = [0, 0, 0, 0, 0, 0, 0]  # 每列上一个有记录的index，第一个元素不用
    cur_trend_key_values = [0, 0]  # 当前趋势的关键点
    for item in datetime_and_close_price:
        cur_line = [item[0], "", "", "", "", "", ""]
        price = float(item[1])
        match current_recording_column:
            case 1:
                # 当前次级回升栏记录
                if price > last_value[1]:
                    if uptrend and price > cur_trend_key_values[0]:
                        # 上升趋势恢复
                        current_recording_column = 3
                        cur_line[3] = price
                        last_value[3] = price
                        cur_trend_key_values = [0, 0]
                    elif not uptrend and price > cur_trend_key_values[0] * (1+params[1]) > 0:
                        # 下降趋势中，向上3点突破
                        current_recording_column = 3
                        cur_line[3] = price
                        last_value[3] = price
                        uptrend = True
                        cur_trend_key_values = [0, 0]
                    elif price > last_value[2]:
                        current_recording_column = 2
                        cur_line[2] = price
                        last_value[2] = price
                    else:
                        cur_line[1] = price
                        last_value[1] = price
                elif price < last_value[1] * (1 - params[0]):
                    # 6点转向
                    if not uptrend and price < last_value[4]:
                        # 当前为下降趋势，转向后价格小于下降趋势栏最后数字，转为在下降趋势栏中记录
                        current_recording_column = 4
                        cur_line[4] = price
                        last_value[4] = price
                        cur_trend_key_values = [0, 0]
                    elif uptrend and price < cur_trend_key_values[1] * (1-params[1]):
                        # 上升趋势中，3点突破向下，转为下降趋势
                        current_recording_column = 4
                        cur_line[4] = price
                        last_value[4] = price
                        uptrend = False
                        cur_trend_key_values = [0, 0]
                    else:
                        if uptrend and price > last_value[5]:
                            # 上升趋势中，自然回升6点转向，未跌破自然回撤底点，为次级回撤
                            current_recording_column = 6
                            cur_line[6] = price
                            last_value[6] = price
                        else:
                            # 在自然回撤栏中记录
                            current_recording_column = 5
                            cur_line[5] = price
                            last_value[5] = price
            case 2:
                # 当前在自然回升栏记录
                if price > last_value[2]:
                    if uptrend and price > cur_trend_key_values[0]:
                        # 上升趋势恢复
                        current_recording_column = 3
                        cur_line[3] = price
                        last_value[3] = price
                        cur_trend_key_values = [0, 0]
                    elif not uptrend and price > cur_trend_key_values[0] * (1+params[1]) > 0:
                        # 下降趋势中，向上3点突破
                        current_recording_column = 3
                        cur_line[3] = price
                        last_value[3] = price
                        uptrend = True
                        cur_trend_key_values = [0, 0]
                    else:
                        # 持续上升，在自然回升栏记录
                        cur_line[2] = price
                        last_value[2] = price
                elif price < last_value[2] * (1-params[0]):
                    # 6点转向
                    if not uptrend and price < last_value[4]:
                        # 当前为下降趋势，转向后价格小于下降趋势栏最后数字，转为在下降趋势栏中记录
                        current_recording_column = 4
                        cur_line[4] = price
                        last_value[4] = price
                        cur_trend_key_values = [0, 0]
                    elif uptrend and price < cur_trend_key_values[1] * (1-params[1]):
                        # 上升趋势中，3点突破向下，转为下降趋势
                        current_recording_column = 4
                        cur_line[4] = price
                        last_value[4] = price
                        uptrend = False
                        cur_trend_key_values = [0, 0]
                    else:
                        if uptrend and price > last_value[5]:
                            # 上升趋势中，自然回升6点转向，未跌破自然回撤底点，为次级回撤
                            current_recording_column = 6
                            cur_line[6] = price
                            last_value[6] = price
                        else:
                            # 在自然回撤栏中记录
                            current_recording_column = 5
                            cur_line[5] = price
                            last_value[5] = price
                        if cur_trend_key_values[0] == 0:
                            if uptrend:
                                cur_trend_key_values[0] = last_value[2]
                                livermore_chart[last_index[2]][2] = str(livermore_chart[last_index[2]][2]) + "-o"
                            else:
                                cur_trend_key_values[0] = last_value[2]
                                livermore_chart[last_index[2]][2] = str(livermore_chart[last_index[2]][2]) + "-x"
            case 3:
                # 当前在上升趋势栏记录
                if price > last_value[3]:
                    # 如果当前价格持续上升，继续在上升趋势栏记录
                    last_value[3] = price
                    cur_line[3] = price
                elif price < last_value[3] * (1-params[0]):
                    # 6点转向：价格回撤超过6点转至自然回撤栏记录，上升趋势栏最后一个数加红线
                    current_recording_column = 5
                    cur_line[5] = price
                    last_value[5] = price
                    livermore_chart[last_index[3]][3] = str(livermore_chart[last_index[3]][3]) + "-o"
                    if cur_trend_key_values[0] == 0:
                        cur_trend_key_values[0] = last_value[3]
            case 4:
                # 当前在下降趋势栏记录
                if price < last_value[4]:
                    # 如果当前价格持续下降，继续在下降趋势栏记录
                    last_value[4] = price
                    cur_line[4] = price
                elif price > last_value[4] * (1+params[0]):
                    # 6点转向，价格回升超过6点转至自然回升栏记录，下降趋势栏最后一个数加黑线
                    current_recording_column = 2
                    cur_line[2] = price
                    last_value[2] = price
                    livermore_chart[last_index[4]][4] = str(livermore_chart[last_index[4]][4]) + "-x"
                    if cur_trend_key_values[1] == 0:
                        cur_trend_key_values[1] = last_value[4]
            case 5:
                # 当前在自然回撤栏记录
                if price < last_value[5]:
                    if not uptrend and price < cur_trend_key_values[1]:
                        # 下降趋势恢复
                        current_recording_column = 4
                        cur_line[4] = price
                        last_value[4] = price
                        cur_trend_key_values = [0, 0]
                    elif uptrend and price < cur_trend_key_values[1] * (1 - params[1]):
                        # 上升趋势中，向下3点突破
                        current_recording_column = 4
                        cur_line[4] = price
                        last_value[4] = price
                        uptrend = False
                        cur_trend_key_values = [0, 0]
                    else:
                        # 如果价格持续下降，继续在自然回撤栏记录
                        last_value[5] = price
                        cur_line[5] = price
                elif price > last_value[5] * (1+params[0]):
                    # 6点转向
                    if uptrend and price > last_value[3]:
                        # 当前在上升趋势，如果价格超过上升趋势栏最后一个数字，则在上升趋势栏记录
                        current_recording_column = 3
                        cur_line[3] = price
                        last_value[3] = price
                        cur_trend_key_values = [0, 0]
                    elif not uptrend and price > cur_trend_key_values[0] * (1+params[1]):
                        # 3点突破，当前在下降趋势，如果价格超过上个关键点高点，转为上升趋势
                        current_recording_column = 3
                        cur_line[3] = price
                        last_value[3] = price
                        uptrend = True
                        cur_trend_key_values = [0, 0]
                    else:
                        if not uptrend and price < last_value[2]:
                            # 下降趋势中，如果未超过上个自然回升顶点，则记录于次级回升
                            current_recording_column = 1
                            cur_line[1] = price
                            last_value[1] = price
                        else:
                            # 在自然回升栏记录
                            current_recording_column = 2
                            cur_line[2] = price
                            last_value[2] = price
                        if cur_trend_key_values[1] == 0:
                            if uptrend:
                                cur_trend_key_values[1] = last_value[5]
                                livermore_chart[last_index[5]][5] = str(livermore_chart[last_index[5]][5]) + "-o"
                            else:
                                cur_trend_key_values[1] = last_value[5]
                                livermore_chart[last_index[5]][5] = str(livermore_chart[last_index[5]][5]) + "-x"
            case 6:
                # 当前在次级回撤栏记录
                if price < last_value[5]:
                    if not uptrend and price < cur_trend_key_values[1]:
                        # 下降趋势恢复
                        current_recording_column = 4
                        cur_line[4] = price
                        last_value[4] = price
                        cur_trend_key_values = [0, 0]
                    elif uptrend and price < cur_trend_key_values[1] * (1 - params[1]):
                        # 上升趋势中，向下3点突破
                        current_recording_column = 4
                        cur_line[4] = price
                        last_value[4] = price
                        uptrend = False
                        cur_trend_key_values = [0, 0]
                    elif price < last_value[5]:
                        # 小于自然回撤低点，转至自然回撤栏记录
                        current_recording_column = 5
                        cur_line[5] = price
                        last_value[5] = price
                    else:
                        # 如果价格持续下降，继续在自然回撤栏记录
                        last_value[6] = price
                        cur_line[6] = price
                elif price > last_value[5] * (1 + params[0]):
                    # 6点转向
                    if uptrend and price > last_value[3]:
                        # 当前在上升趋势，如果价格超过上升趋势栏最后一个数字，则在上升趋势栏记录
                        current_recording_column = 3
                        cur_line[3] = price
                        last_value[3] = price
                        cur_trend_key_values = [0, 0]
                    elif not uptrend and price > cur_trend_key_values[0] * (1 + params[1]):
                        # 3点突破，当前在下降趋势，如果价格超过上个关键点高点，转为上升趋势
                        current_recording_column = 3
                        cur_line[3] = price
                        last_value[3] = price
                        uptrend = True
                        cur_trend_key_values = [0, 0]
                    else:
                        if not uptrend and price < last_value[2]:
                            # 下降趋势中，如果未超过上个自然回升顶点，则记录于次级回升
                            current_recording_column = 1
                            cur_line[1] = price
                            last_value[1] = price
                        else:
                            # 在自然回升栏记录
                            current_recording_column = 2
                            cur_line[2] = price
                            last_value[2] = price
        if cur_line[current_recording_column] != "":
            last_index[current_recording_column] = len(livermore_chart)
        livermore_chart.append(cur_line)

    return livermore_chart

if __name__ == '__main__':
    start_ts = convert_date_string_to_milliseconds("2024-05-12 21:29:00")
    end_ts = convert_date_string_to_milliseconds("2023-05-12 21:31:00")

    result = marketDataAPI.get_history_candlesticks(
        instId="BTC-USDT",
        bar="1s",
        after=end_ts,
        before=start_ts
    )
    for candle in result.get("data")[::-1]:
        print([convert_milliseconds_to_date_string(candle[0]), "开盘价", candle[1]])
        print([convert_milliseconds_to_date_string(candle[0]), "收盘价", candle[4]])


    #chart = get_livermore_chart(start_ts, end_ts, params=[0.02, 0.01], bar="1m")

    # tb = pt.PrettyTable()
    # tb.field_names = ["日期","次级回升","自然回升","上升趋势","下降趋势","自然回撤","次级回撤"]
    # for line in chart:
    #     tb.add_row(line)
    # print(tb)

    # df = pandas.DataFrame(chart, columns=["日期","次级回升","自然回升","上升趋势","下降趋势","自然回撤","次级回撤"])
    # df.style.map(lambda x: "background-color: red" if isinstance(x, str) and x.endswith("-o") else "background-color: white")
    # df.style.map(lambda x: "background-color: green" if isinstance(x, str) and x.endswith("-x") else "background-color: white")
    # df.to_excel('output.xlsx', index=False)


