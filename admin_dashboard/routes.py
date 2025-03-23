from flask import render_template, jsonify
from flask_login import login_required, current_user
from . import admin_bp  # Імпорт Blueprint
from binance.client import Client
from datetime import datetime
import os

client = Client(os.getenv("API_KEY"), os.getenv("SECRET_KEY"))


# маршрут для admin_dashboard
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_dashboard.html', username=current_user.username)


@admin_bp.route("/get-orders")
@login_required
def get_orders():
    symbol = "XRPUSDT"
    all_orders = client.get_all_orders(symbol=symbol)
    open_orders = client.get_open_orders(symbol=symbol)

    completed_orders = [
        {
            "time": datetime.fromtimestamp(order["time"] / 1000).strftime("%d.%m, %H:%M:%S"),
            "price": float(order["price"]),
            "quantity": float(order["origQty"]),
            "side": order["side"]
        }
        for order in all_orders if order['status'] in ['FILLED', 'PARTIALLY_FILLED']
    ]

    open_orders_list = [
        {
            "time": datetime.fromtimestamp(order["time"] / 1000).strftime("%d.%m, %H:%M:%S"),
            "price": float(order["price"]),
            "quantity": float(order["origQty"]),
            "side": order["side"]
        }
        for order in open_orders
    ]

    return jsonify({"completed_orders": completed_orders[-20:], "open_orders": open_orders_list})
