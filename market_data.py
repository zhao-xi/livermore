from utils import convert_milliseconds_to_date_string, convert_date_string_to_milliseconds
import okx.MarketData as MarketData

flag = "0"  # 实盘:0 , 模拟盘：1
marketDataAPI = MarketData.MarketAPI(flag=flag)

def get_date_and_close_price(start_ts, end_ts, bar="1D"):
    # 获取指数K线数据，整理为日期、收盘价格式
    finished = False
    datetime_and_close_price = []  # 日期、收盘价
    while not finished:
        result = marketDataAPI.get_history_candlesticks(
            instId="BTC-USDT",
            bar=bar,
            after=end_ts,
            before=start_ts
        )
        for candle in result.get("data"):
            datetime_and_close_price.append([convert_milliseconds_to_date_string(candle[0]), candle[4]])
            day_highest[convert_milliseconds_to_date_string(candle[0])] = float(candle[2])
            day_lowest[convert_milliseconds_to_date_string(candle[0])] = float(candle[3])
        if len(result.get("data")) > 0 and float(result.get("data")[-1][0]) > start_ts:
            end_ts = int(result.get("data")[-1][0])
        else:
            finished = True
    datetime_and_close_price = datetime_and_close_price[::-1]