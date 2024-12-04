# Donchian策略
# 入场：突破20日极值 出场：反向突破10日极值 参数entry、exit
# 做多只在50日线大于300日线，做空只在50日线小于300日线 参数short_avg、long_avg

from market_data import get_candlesticks
from utils import convert_date_string_to_milliseconds

def donchian(start_ts, end_ts, bar="1D", trade_pair="BTC-USDT", entry=20, exit=10, short_avg=50, long_avg=300):
    if not ((long_avg > short_avg > 0) and (entry > 0 and exit > 0)):
        return None
    candles = get_candlesticks(start_ts, end_ts, bar, trade_pair)
    close_prices = [float(candle['close']) for candle in candles]
    high_prices = [float(candle['high']) for candle in candles]
    low_prices = [float(candle['low']) for candle in candles]
    holding = False  # 是否持仓
    orig_money = 10000
    entry_price = 0
    # 计算5日均线和30日均线
    for i in range(len(candles)):
        if i < long_avg+1:
            continue
        short_ma = sum(close_prices[i-short_avg-1:i]) / short_avg
        long_ma = sum(close_prices[i-long_avg-1:i]) / long_avg
        if short_ma > long_ma:
            # 做多
            if not holding:
                entry_highest = max(high_prices[i-entry-1:i])
                if candles[i]['high'] > entry_highest:
                    entry_price = entry_highest
                    print(f"{candles[i]['time']} {entry_highest} 做多")
                    holding = True
            else:
                exit_lowest = min(low_prices[i-exit-1:i])
                if candles[i]['low'] < exit_lowest:
                    orig_money = exit_lowest / entry_price * orig_money
                    print(f"{candles[i]['time']} {exit_lowest} 平多 {orig_money}")
                    holding = False
        elif short_ma < long_ma:
            # 做空
            if not holding:
                entry_lowest = min(low_prices[i-entry-1:i])
                if candles[i]['low'] < entry_lowest:
                    entry_price = entry_lowest
                    print(f"{candles[i]['time']} {entry_lowest} 做空")
                    holding = True
            else:
                exit_highest = max(high_prices[i-exit-1:i])
                if candles[i]['high'] > exit_highest:
                    orig_money = (1+(entry_price-exit_highest) / entry_price) * orig_money
                    print(f"{candles[i]['time']} {exit_highest} 平空 {orig_money}")
                    holding = False

if __name__ == '__main__':
    start_ts = convert_date_string_to_milliseconds("2021-09-12 21:29:00")
    end_ts = convert_date_string_to_milliseconds("2022-05-12 21:31:00")
    donchian(start_ts, end_ts,"1H","BTC-USDT",20,10,50,300)
