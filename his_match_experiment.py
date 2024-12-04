import csv
import datetime
import mplfinance as mpf
import pandas as pd
from candle import candle, get_data, reformatted_data

all_candles = []

def diff_ratio(candles_1, candles_2):
    if len(candles_1) != len(candles_2):
        raise Exception("length not equal")
    # # cosine similarity
    # vector_1 = [candle.get_rate() for candle in candles_1]
    # vector_2 = [candle.get_rate() for candle in candles_2]
    # dot_product = sum([a * b for a, b in zip(vector_1, vector_2)])
    # magnitude_a = sum([a ** 2 for a in vector_1]) ** 0.5
    # magnitude_b = sum([b ** 2 for b in vector_2]) ** 0.5
    # cosine_similarity = dot_product / (magnitude_a * magnitude_b)
    # return cosine_similarity

    sum_diff = 0
    for i in range(len(candles_1)):
        rate1 = candles_1[i].get_rate()
        rate2 = candles_2[i].get_rate()
        sum_diff += abs((rate1 - rate2) / rate1)
        if rate1 * rate2 < 0:
            sum_diff *= 3
    return -sum_diff

def plot_candles(start_i, end_i):
    cut_reformatted_data = {}
    for key in reformatted_data.keys():
        cut_reformatted_data[key] = reformatted_data[key][start_i:end_i]
    candles_data = pd.DataFrame.from_dict(cut_reformatted_data)
    candles_data.set_index('Date', inplace=True)
    mpf.plot(candles_data, type="candle")

def get_similar_candles(cur_index, duration, top_n=10):
    candles = get_data('./COINBASE_BTCUSD_20220101_20241011.csv')
    all_candles.extend(candles)

    cur_candles = candles[cur_index - duration:cur_index]
    similar_ranges = []

    print("cur time: {}, start time: {}".format(candles[cur_index].time, candles[cur_index - 60].time))
    print("select duration: {}".format(duration))
    storage = []
    for i in range(cur_index - 2 * duration):
        comp_candles = candles[i:i + duration]
        sim = diff_ratio(cur_candles, comp_candles)
        tmp = {"candle": candles[i], "diff_ratio": sim}
        storage.append(tmp)
    sorted_storage = sorted(storage, key=lambda x: -x['diff_ratio'])
    final_result_candles_list = []
    for item in sorted_storage:
        add = True
        for res in final_result_candles_list:
            if abs(res["candle"].get_time_stamp() - item["candle"].get_time_stamp()) < duration * 3600:
                add = False
                break
        if not add:
            continue
        final_result_candles_list.append(item)
        if len(final_result_candles_list) == top_n:
            break
    for item in final_result_candles_list:
        print("index: [{},{}], time: {}, diff_ratio: {:.5f}".format(item["candle"].index, item["candle"].index + duration, item["candle"].time, item["diff_ratio"]))
        similar_ranges.append([item["candle"].index, item["candle"].index + duration])
    return similar_ranges

if __name__ == '__main__':
    cur_index = 20000
    duration = 10
    similar_ranges = get_similar_candles(cur_index, duration, 6)
    cur_candles = all_candles[cur_index - duration:cur_index]
    for r in similar_ranges:
        comp_candles = all_candles[r[0]:r[1]]
        print("similarity: ", diff_ratio(cur_candles, comp_candles))

    # 已获取了相似k线，画图
    # 画当前图
    plot_candles(cur_index - duration, cur_index)

    # 画每个对照图
    for r in similar_ranges:
        plot_candles(r[0], r[1])





