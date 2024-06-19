from utils import convert_milliseconds_to_date_string, convert_date_string_to_milliseconds
import okx.MarketData as MarketData

flag = "0"  # 实盘:0 , 模拟盘：1
marketDataAPI = MarketData.MarketAPI(flag=flag)

def get_candlesticks(start_ts, end_ts, bar="1D", trade_pair="BTC-USDT"):
    # 获取指数K线数据，整理为日期、收盘价格式
    finished = False
    candlesticks = []  # 日期、收盘价
    while not finished:
        result = marketDataAPI.get_history_candlesticks(
            instId=trade_pair,
            bar=bar,
            after=end_ts,
            before=start_ts
        )
        for candle in result.get("data"):
            candlesticks.append({
                "time": convert_milliseconds_to_date_string(candle[0]),
                "open": candle[1],
                "high": candle[2],
                "low": candle[3],
                "close": candle[4]
            })
        if len(result.get("data")) > 0 and float(result.get("data")[-1][0]) > start_ts:
            end_ts = int(result.get("data")[-1][0])
        else:
            finished = True
    candlesticks = candlesticks[::-1]
    return candlesticks


def cal_max(candlesticks, period):
    max_prices = []
    for candle in candlesticks:
        max_prices.append(candle.get("high"))
    # 计算period期间最高价格
    max_prices_in_period = [-1] * len(candlesticks)
    # 每个元素是过去period天的最高价
    for i in range(len(candlesticks)):
        if i < period - 1:
            max_prices_in_period[i] = -1
        else:
            max_prices_in_period[i] = max(max_prices[i - period + 1: i + 1])
    return max_prices_in_period


def cal_min(candlesticks, period):
    # 计算period期间最低价格
    min_prices = []
    for candle in candlesticks:
        min_prices.append(candle.get("low"))
    # 计算period期间最高价格
    min_prices_in_period = [-1] * len(candlesticks)
    # 每个元素是过去period天的最高价
    for i in range(len(candlesticks)):
        if i < period - 1:
            min_prices_in_period[i] = -1
        else:
            min_prices_in_period[i] = min(min_prices[i - period + 1: i + 1])
    return min_prices_in_period


def cal_avg(candlesticks, period):
    # 计算period期间MA均线
    pass


def cal_avg_exp(candlesticks, period):
    # 计算period期间EMA均线
    pass


if __name__ == '__main__':
    start_ts = convert_date_string_to_milliseconds("2023-05-12 21:29:00")
    end_ts = convert_date_string_to_milliseconds("2024-05-12 21:31:00")
    get_candlesticks(start_ts, end_ts)
    # test cal_max
    candlesticks = [{"high":5}, {"high":2}, {"high":3}, {"high":6}, {"high":2}, {"high":1}, {"high":0}, {"high":9}]
    maxes = cal_max(candlesticks, 3)
    print(maxes)

    # test cal_min
    candlesticks = [{"low":5}, {"low":2}, {"low":3}, {"low":6}, {"low":5}, {"low":1}, {"low":0}, {"low":9}]
    mins = cal_min(candlesticks, 3)
    print(mins)