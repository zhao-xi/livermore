from utils import convert_milliseconds_to_date_string, convert_date_string_to_milliseconds
import okx.MarketData as MarketData

flag = "0"  # 实盘:0 , 模拟盘：1
marketDataAPI = MarketData.MarketAPI(flag=flag)

def get_candlesticks(start_ts, end_ts, bar="1D"):
    # 获取指数K线数据，整理为日期、收盘价格式
    finished = False
    candlesticks = []  # 日期、收盘价
    while not finished:
        result = marketDataAPI.get_history_candlesticks(
            instId="BTC-USDT",
            bar=bar,
            after=end_ts,
            before=start_ts
        )
        for candle in result.get("data"):
            candlesticks.append([convert_milliseconds_to_date_string(candle[0]), candle[4]])
            candlesticks.append({
                "time": convert_milliseconds_to_date_string(candle[0]),
                "open": candle[1],
                "highest": candle[2],
                "lowest": candle[3],
                "close": candle[4]
            })
        if len(result.get("data")) > 0 and float(result.get("data")[-1][0]) > start_ts:
            end_ts = int(result.get("data")[-1][0])
        else:
            finished = True
    candlesticks = candlesticks[::-1]
    return candlesticks


def cal_max(candlesticks, period):
    # 计算period期间最高价格
    pass


def cal_min(candlesticks, period):
    # 计算period期间最低价格
    pass


def cal_avg(candlesticks, period):
    # 计算period期间MA均线
    pass


def cal_avg_exp(candlesticks, period):
    # 计算period期间EMA均线
    pass