import time
import concurrent
from market_data import get_candlesticks
from concurrent.futures import ThreadPoolExecutor
import tkinter as tk
from tkinter import ttk
import threading

watch_list = [
"BTC-USDT","ETH-USDT","SOL-USDT","BCH-USDT","PEPE-USDT","YFI-USDT",
"MKR-USDT","LTC-USDT","ORDI-USDT","AAVE-USDT","AVAX-USDT","XRP-USDT",
"ETC-USDT","LINK-USDT","BSV-USDT","FIL-USDT","ENS-USDT","UNI-USDT",
"DOT-USDT","TRB-USDT","APT-USDT","SUI-USDT","NEO-USDT","AR-USDT",
"TON-USDT","SSV-USDT","COMP-USDT","KSM-USDT","ICP-USDT","XCH-USDT",
"METIS-USDT","DOGE-USDT","TIA-USDT","NEAR-USDT","WLD-USDT","ATOM-USDT",
"INJ-USDT","EGLD-USDT","ADA-USDT","EOS-USDT","ONDO-USDT","WIF-USDT",
"RENDER-USDT","TRX-USDT","ZRO-USDT","LPT-USDT","OM-USDT","USDC-USDT",
"PNUT-USDT","OP-USDT","AUCTION-USDT","QTUM-USDT","AXS-USDT","CRV-USDT",
"STX-USDT","CORE-USDT","GMX-USDT","MOVR-USDT","SAND-USDT","CTC-USDT",
"ARB-USDT","ALGO-USDT","LDO-USDT","EIGEN-USDT","MOODENG-USDT","APE-USDT",
"MORPHO-USDT","XLM-USDT","MASK-USDT","ETHFI-USDT","IOTA-USDT","ETHW-USDT",
"FTM-USDT","CVX-USDT","HBAR-USDT","GAS-USDT","DYDX-USDT","POL-USDT",
"JUP-USDT","OL-USDT","JTO-USDT","NMR-USDT","RAY-USDT","XTZ-USDT","THETA-USDT",
"ARKM-USDT","ZETA-USDT","MAJOR-USDT","ACT-USDT","PYTH-USDT","STRK-USDT",
"SUSHI-USDT","YGG-USDT","MANA-USDT","LUNA-USDT","BIGTIME-USDT","SNX-USDT",
"CELO-USDT","UMA-USDT","IMX-USDT","FLOW-USDT","ACE-USDT","CFX-USDT","BADGER-USDT",
]


period_list = ["1H"]

# 创建一个嵌套字典来存储 candles 数据
candles_map = {}
final_res_1 = []
final_res_2 = []

def fetch_candles(instId, period, max_retries=5):
    start_ts = int((time.time() - 60 * 60 * 12) * 1000)  # 12小时前的时间戳（毫秒）
    end_ts = int(time.time() * 1000)  # 当前时间的时间戳（毫秒）

    attempt = 0
    while attempt < max_retries:
        try:
            candles = get_candlesticks(start_ts, end_ts, period, instId)
            if len(candles) > 0:
                return candles
            else:
                raise ValueError("No candles found.")
        except Exception as e:
            attempt += 1
            time.sleep(0.1)  # 等待0.1秒再重试，以避免过于频繁的请求
    raise TimeoutError("Failed to retrieve candles after multiple attempts.")



def is_candlestick_body_in_third(open_price, close_price, high_price, low_price):
    """
    判断K线实体是否在上下38.2%范围内

    Args:
        open_price (float): 开盘价
        close_price (float): 收盘价
        high_price (float): 最高价
        low_price (float): 最低价

    Returns:
        bool: 如果K线实体在K线整体范围的上38.2%或下38.2%内，则返回True；否则返回False。

    此函数首先计算K线的整体范围（最高价与最低价之差），然后确定上38.2%和下38.2%的界限。
    接着，判断开盘价和收盘价是否都位于上38.2%或下38.2%范围内。如果满足任一条件，则返回True，
    否则返回False。
    """
    # 计算K线的整体范围
    total_range = high_price - low_price

    # 计算上38.2%和下38.2%的界限
    upper_third_start = high_price - (total_range * 0.382)
    lower_third_end = low_price + (total_range * 0.382)

    # 判断实体是否在上38.2%范围内
    in_upper_third = open_price >= upper_third_start and close_price >= upper_third_start
    # 判断实体是否在下38.2%范围内
    in_lower_third = open_price <= lower_third_end and close_price <= lower_third_end

    # 返回结果
    return in_upper_third or in_lower_third


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Pinbar Monitor")

        # 创建列标题
        self.tree = ttk.Treeview(root, columns=("Crypto Pair", "Single Pinbar", "Double Pinbar"), show='headings')
        self.tree.heading("Crypto Pair", text="Crypto Pair")
        self.tree.heading("Single Pinbar", text="Single Pinbar")
        self.tree.heading("Double Pinbar", text="Double Pinbar")
        self.tree.pack(expand=True, fill=tk.BOTH)
        self.tree.tag_configure('green', background='lime green')
        self.tree.tag_configure('yellow', background='yellow')

        # 初始化数据
        self.update_data()

        # 定时更新数据
        self.update_interval = 5  # 更新间隔，单位：秒
        self.root.after(self.update_interval * 1000, self.periodic_update)

    def update_data(self):
        # 清空树视图
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 填充树视图
        for item in watch_list:
            tags = []
            in_final_res_1 = item.split("-")[0] in [x.split()[0] for x in final_res_1]
            in_final_res_2 = item.split("-")[0] in [x.split()[0] for x in final_res_2]
            if in_final_res_1:
                tags.append('green')
            elif in_final_res_2:
                tags.append('yellow')
            self.tree.insert("", tk.END, values=(item, in_final_res_1, in_final_res_2), tags=tags)

    def periodic_update(self):
        self.update_data()
        # 再次设置定时器
        self.root.after(self.update_interval * 1000, self.periodic_update)


def get_data():
    global candles_map
    global final_res_1
    global final_res_2
    while True:
        start_time = time.time()
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_instId_period = {executor.submit(fetch_candles, instId, period): (instId, period) for instId in
                                       watch_list for period in period_list}
            for future in concurrent.futures.as_completed(future_to_instId_period):
                instId, period = future_to_instId_period[future]
                try:
                    candles = future.result()
                    if instId not in candles_map:
                        candles_map[instId] = {}
                    candles_map[instId][period] = candles
                except Exception as exc:
                    print(f"{instId} with period {period} generated an exception: {exc}")
        end_time = time.time()
        final_res_1 = []
        final_res_2 = []
        print(f"Total time taken: {end_time - start_time} seconds")
        for instId, periods in candles_map.items():
            for period, candles in periods.items():

                # single candle pinbar
                if is_candlestick_body_in_third(candles[-1].get('open'), candles[-1].get('close'),
                                                candles[-1].get('high'), candles[-1].get('low')):
                    is_up_tail = True
                    close = candles[-1].get('close')
                    high = candles[-1].get('high')
                    low = candles[-1].get('low')
                    if abs(close - low) > abs(close - high):
                        is_up_tail = False
                    if is_up_tail:
                        if not high > max(candles[-2].get('high'), candles[-3].get('high'), candles[-4].get('high')):
                            continue
                    else:
                        if not low < min(candles[-2].get('low'), candles[-3].get('low'), candles[-4].get('low')):
                            continue
                    final_res_1.append(f'{instId.split("-")[0]} {period}')

                # double candle pinbar
                elif is_candlestick_body_in_third(candles[-2].get('open'), candles[-1].get('close'),
                                                  max(candles[-2].get('high'), candles[-1].get('high')),
                                                  min(candles[-2].get('low'), candles[-1].get('low'))):
                    is_up_tail = True
                    close = candles[-1].get('close')
                    high = max(candles[-2].get('high'), candles[-1].get('high'))
                    low = min(candles[-2].get('low'), candles[-1].get('low'))
                    if abs(close - low) > abs(close - high):
                        is_up_tail = False
                    if is_up_tail:
                        if not high > max(candles[-3].get('high'), candles[-4].get('high'), candles[-5].get('high')):
                            continue
                    else:
                        if not low < min(candles[-3].get('low'), candles[-4].get('low'), candles[-5].get('low')):
                            continue
                    final_res_2.append(f'{instId.split("-")[0]} {period}')

        if len(final_res_1) == 0 and len(final_res_2) == 0:
            print("nothing found")
        else:
            print("=============================")
            if len(final_res_1) != 0:
                print("1-candle pinbar:")
                print('\n'.join(final_res_1))
            if len(final_res_2) != 0:
                print("\n2-candle pinbar:")
                print('\n'.join(final_res_2))
            print("=============================")


if __name__ == '__main__':
    threading.Thread(target=get_data).start()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
