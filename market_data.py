from utils import convert_milliseconds_to_date_string, convert_date_string_to_milliseconds
import okx.MarketData as MarketData
import time

flag = "0"  # 实盘:0 , 模拟盘：1
marketDataAPI = MarketData.MarketAPI(flag=flag)
marketDataAPI.debug = False
import okx.PublicData as PublicData

publicDataAPI = PublicData.PublicAPI(flag=flag)

def get_candlesticks(start_ts, end_ts, bar="1D", trade_pair="BTC-USDT"):
    # 获取指数K线数据
    finished = False
    candlesticks = []  # 日期、收盘价
    while not finished:
        result = marketDataAPI.get_candlesticks(
            instId=trade_pair,
            bar=bar,
            after=end_ts,
            before=start_ts
        )
        for candle in result.get("data"):
            candlesticks.append({
                "time": convert_milliseconds_to_date_string(candle[0]),
                "open": float(candle[1]),
                "high": float(candle[2]),
                "low": float(candle[3]),
                "close": float(candle[4])
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

spots = ["BTC-USDT",
"ETH-USDT",
"SOL-USDT",
"BCH-USDT",
"PEPE-USDT",
"BETH-USDT",
"YFI-USDT",
"MKR-USDT",
"STETH-USDT",
"LTC-USDT",
"WBTC-USDT",
"ORDI-USDT",
"AAVE-USDT",
"AVAX-USDT",
"XRP-USDT",
"ETC-USDT",
"LINK-USDT",
"OKB-USDT",
"BSV-USDT",
"FIL-USDT",
"ENS-USDT",
"UNI-USDT",
"DOT-USDT",
"TRB-USDT",
"APT-USDT",
"SUI-USDT",
"NEO-USDT",
"AR-USDT",
"XAUT-USDT",
"TON-USDT",
"SSV-USDT",
"COMP-USDT",
"KSM-USDT",
"ICP-USDT",
"XCH-USDT",
"METIS-USDT",
"DOGE-USDT",
"TIA-USDT",
"NEAR-USDT",
"WLD-USDT",
"ATOM-USDT",
"INJ-USDT",
"EGLD-USDT",
"ADA-USDT",
"EOS-USDT",
"ONDO-USDT",
"WIF-USDT",
"RENDER-USDT",
"TRX-USDT",
"ZRO-USDT",
"LPT-USDT",
"OM-USDT",
"USDC-USDT",
"PNUT-USDT",
"OP-USDT",
"BANANA-USDT",
"AUCTION-USDT",
"QTUM-USDT",
"AXS-USDT",
"CRV-USDT",
"ILV-USDT",
"STX-USDT",
"CORE-USDT",
"GMX-USDT",
"MOVR-USDT",
"SAND-USDT",
"CTC-USDT",
"ARB-USDT",
"ALGO-USDT",
"LDO-USDT",
"EIGEN-USDT",
"MOODENG-USDT",
"APE-USDT",
"MORPHO-USDT",
"XLM-USDT",
"MASK-USDT",
"ETHFI-USDT",
"PENDLE-USDT",
"IOTA-USDT",
"ETHW-USDT",
"FET-USDT",
"FTM-USDT",
"KP3R-USDT",
"CVX-USDT",
"HBAR-USDT",
"GAS-USDT",
"DYDX-USDT",
"POL-USDT",
"JUP-USDT",
"OKT-USDT",
"OL-USDT",
"JTO-USDT",
"NMR-USDT",
"RAY-USDT",
"XTZ-USDT",
"THETA-USDT",
"ARKM-USDT",
"ZETA-USDT",
"MAJOR-USDT",
"ACT-USDT",
"PYTH-USDT",
"STRK-USDT",
"SUSHI-USDT",
"YGG-USDT",
"MANA-USDT",
"LUNA-USDT",
"KDA-USDT",
"BIGTIME-USDT",
"SNX-USDT",
"CELO-USDT",
"UMA-USDT",
"IMX-USDT",
"FLOW-USDT",
"ACE-USDT",
"CFX-USDT",
"BADGER-USDT"]

if __name__ == '__main__':
    # 获取
    res = {}
    a = marketDataAPI.get_tickers(instType="SPOT")
    for item in a["data"]:
        if '-USDT' in item['instId']:
            volumeUSDT = float(item["volCcy24h"]) * float(item["last"])
            if volumeUSDT < 10000000:
                continue
            instId = item["instId"]
            res[instId] = volumeUSDT
    res = sorted(res.items(), key=lambda x: x[1], reverse=True)
    for i in range(len(res)):
        print(f'\"{res[i][0]}\",')

