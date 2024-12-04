import csv
import datetime
import mplfinance as mpf
import pandas as pd

from candle import candle, get_data, reformatted_data


def plot_candles(start_i, end_i):
    cut_reformatted_data = {}
    for key in reformatted_data.keys():
        cut_reformatted_data[key] = reformatted_data[key][start_i:end_i+1]
    candles_data = pd.DataFrame.from_dict(cut_reformatted_data)
    candles_data.set_index('Date', inplace=True)
    mpf.plot(candles_data, type="candle")


if __name__ == '__main__':
    all_candles = get_data("./COINBASE_BTCUSD_20220101_20241011.csv")
    index_list = []
    for i in range(len(all_candles)-10):
        a = all_candles[i]
        b = all_candles[i + 1]
        c = all_candles[i + 2]
        if not b.is_hammer() or not(a.open >= b.open and a.open >= b.close and c.close >= b.open and c.close >= b.close):
            continue
        index_list.append(b.index)


    reward_ratio = 1
    for reward_ratio in [1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,2.9,3]:
        win_count = 0
        lose_count = 0
        money = 10000
        for index in index_list:
            # if index + 30 > len(all_candles):
            #     continue
            # plot_candles(index-1, index + 20)
            # plotted += 1
            # if plotted == 20:
            #     break
            a = all_candles[index - 1]
            b = all_candles[index]
            c = all_candles[index + 1]
            buy_price = c.close
            stop_loss = b.low
            stop_reward = buy_price + reward_ratio*(buy_price - stop_loss)
            for i in range(index+2, len(all_candles)):
                current_candle = all_candles[i]
                if current_candle.low < stop_loss:
                    money = stop_loss / buy_price * money
                    lose_count += 1
                    break
                elif current_candle.high > stop_reward:
                    money = stop_reward/buy_price * money
                    win_count += 1
                    break
        print(f"reward ratio:{reward_ratio}")
        print(f"win:{win_count}, lose:{lose_count}")
        print(f"money:{money}")






