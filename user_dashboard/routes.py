import pandas as pd
from binance.client import Client
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from . import user_bp

client = Client("", "")
LENGTH = 14
TIME_FRAME = Client.KLINE_INTERVAL_1HOUR
TIME_START = f"{LENGTH * 60} minutes ago UTC"


def rma(s: pd.Series, period: int) -> pd.Series:
    return s.ewm(alpha=1 / period).mean()


def atr(df: pd.DataFrame, length: int = 14) -> pd.Series:
    high, low, prev_close = df['high'], df['low'], df['close'].shift()
    tr_all = [high - low, high - prev_close, low - prev_close]
    tr_all = [tr.abs() for tr in tr_all]
    tr = pd.concat(tr_all, axis=1).max(axis=1)
    atr_ = rma(tr, length)
    return atr_


def price_atr_percent(coin: str, only_atr=False):
    coin = coin.upper()
    try:
        klines = client.get_historical_klines(
            f"{coin}USDT",
            TIME_FRAME,
            TIME_START
        )
    except:
        return f"Монети {coin} немає"

    data = pd.DataFrame(klines, columns=["timestamp", "open", "high", "low", "close", "volume",
                                         "close_time", "quote_asset_volume", "number_of_trades",
                                         "taker_buy_base", "taker_buy_quote", "ignore"])
    data = data[["high", "low", "close"]].astype(float)
    if len(data) > 0:
        atr_values = atr(data, length=LENGTH)

        current_price = data["close"].iloc[-1]
        current_atr = atr_values.iloc[-1]

        if only_atr:
            return round(current_atr / current_price * 100, 2)

        return f"{coin} {round(current_atr / current_price * 100, 2)}% ATR"
    elif not only_atr:
        return f"Немає руху ціни {coin} для обрахунку ATR"


def get_top_atr():
    exchange_info = client.get_exchange_info()
    usdt_pairs = [s['baseAsset'] for s in exchange_info['symbols'] if s['quoteAsset'] == 'USDT']

    atr_list = []
    for pair in usdt_pairs[:50]:
        pair_price_atr = price_atr_percent(pair, only_atr=True)
        if pair_price_atr:
            atr_list.append({'coin': pair, 'percent': pair_price_atr})

    return sorted(atr_list, key=lambda x: x["percent"], reverse=True)[:10]


@user_bp.route("/get-top-atr", methods=["GET"])
@login_required
def get_top_atr_api():
    data = get_top_atr()
    return jsonify(data)


@user_bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
    result = ""
    if request.method == 'POST':
        coin = request.form.get('coin', '')
        result = price_atr_percent(coin)
    return render_template('user_dashboard.html', result=result)
