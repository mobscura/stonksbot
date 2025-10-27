from pybit.unified_trading import HTTP
from conf.config import API_KEY, SECRET_KEY
from typing import Tuple, List
import math 
import logging
import time

client = HTTP(
    testnet=False,
    api_key=API_KEY,
    api_secret=SECRET_KEY,
)

def get_config(store):
    resp = client.get_wallet_balance(accountType="UNIFIED", coin="USDT")
    
    data_list = resp.get("result", {}).get("list", [])
    if not data_list:
        return 0.0

    coin_list = data_list[0].get("coin", [])
    if not coin_list:
        return 0.0

    usdt_info = next((c for c in coin_list if c.get("coin") == "USDT"), None)
    if usdt_info is None:
        return 0.0

    raw_balance = usdt_info.get("walletBalance", 0)
    balance = round(float(raw_balance) * store.multiplier, 2)
    return balance

def get_market(store):
    resp = client.get_positions(
        accountType="UNIFIED",
        category="linear",   
        settleCoin="USDT",
        limit=200     
    )

    positions = resp.get("result", {}).get("list", [])
    total_pnl = 0.0
    total_margin = 0.0

    for pos in positions:
        pnl = float(pos.get("unrealisedPnl", 0))
        margin = float(pos.get("positionMargin", 0))  
        total_pnl += pnl
        total_margin += margin

    total_pnl = total_pnl * store.multiplier
    total_margin = total_margin * store.multiplier

    overall_roe = (total_pnl / total_margin) * 100 if total_margin else 0.0

    total_pnl = round(total_pnl, 4)
    overall_roe = round(overall_roe, 2)

    return total_pnl, overall_roe

def get_stats(store):
    pos_resp = client.get_positions(
        accountType="UNIFIED",
        category="linear",
        settleCoin="USDT",
        limit=200
    )
    positions = pos_resp.get("result", {}).get("list", [])
    
    total_pnl = sum(
        float(pos.get("unrealisedPnl", 0)) * store.multiplier
        for pos in positions
    )
    total_pnl = round(total_pnl, 4)

    total_positions = len(positions)
    
    ord_resp = client.get_open_orders(
        category="linear",
        settleCoin="USDT",
        openOnly=0,
        limit=200  
    )
    orders = ord_resp.get("result", {}).get("list", [])
    
    total_orders = len(orders)
    
    return total_pnl, total_positions, total_orders

def positions(store) -> List[str]:
    """
    Возвращает список строк вида "Лонг BTCUSDT 12.34 USDT" / "Шорт ETHUSDT 5.67 USDT"
    """
    pos_res = client.get_positions(category="linear", limit=200) 
    out = []
    for p in pos_res["result"]["list"]:
        amt = float(p.get("size", 0))
        if amt != 0.0:
            flag = 'Лонг' if amt > 0 else 'Шорт'
            pnl = round(float(p.get("unrealisedPnl", 0)) * store.multiplier, 2)
            out.append(f"{flag} {p['symbol']} {pnl} USDT")
    return out

def long() -> List[str]:
    """
    Закрывает все длинные позиции и возвращает обновлённый список позиций.
    """
    pos_res = client.get_positions(category="linear", limit=200) 
    for p in pos_res["result"]["list"]:
        amt = float(p.get("size", 0))
        if amt > 0:
            client.place_order(
                category="linear", symbol=p["symbol"],
                side="Sell", orderType="Market",
                qty=str(amt), positionIdx=1 
            )
    return positions()

def short() -> List[str]:
    """
    Закрывает все короткие позиции и возвращает обновлённый список позиций.
    """
    pos_res = client.get_positions(category="linear", limit=200)  
    for p in pos_res["result"]["list"]:
        amt = float(p.get("size", 0))
        if amt < 0:
            client.place_order(
                category="linear", symbol=p["symbol"],
                side="Buy", orderType="Market",
                qty=str(abs(amt)), positionIdx=2  
            )
    return positions()

def position_all() -> None:
    """
    Закрывает все позиции (и лонги, и шорты).
    """
    pos_res = client.get_positions(category="linear", limit=200)  
    for p in pos_res["result"]["list"]:
        amt = float(p.get("size", 0))
        if amt != 0.0:
            side = "Sell" if amt > 0 else "Buy"
            idx = 1 if amt > 0 else 2
            client.place_order(
                category="linear", symbol=p["symbol"],
                side=side, orderType="Market",
                qty=str(abs(amt)), positionIdx=idx 
            )

def orders(a: int = 0, b: int = 0) -> Tuple[int, int]:
    """
    Возвращает:
      a: число ордеров для открытых позиций
      b: число ордеров для закрытых позиций
    """
    open_orders = client.get_active_orders(category="linear", limit=200)["result"]["list"]  
    positions = client.get_positions(category="linear", limit=200)["result"]["list"]  
    for o in open_orders:
        pos = next((p for p in positions if p["symbol"] == o["symbol"]), None)
        if pos and float(pos.get("size", 0)) != 0.0:
            a += 1
        else:
            b += 1
    return a, b

def order_all() -> None:
    """
    Отменяет все открытые ордера для каждой позиции.
    """
    open_orders = client.get_active_orders(category="linear", limit=200)["result"]["list"]  
    symbols = {o["symbol"] for o in open_orders}
    for sym in symbols:
        client.cancel_all_active_orders(category="linear", symbol=sym)

def now() -> int:
    """
    Считает текущие открытые ордера по активным позициям, 
    отменяя ордера для закрытых позиций.
    """
    count = 0
    positions = client.get_positions(category="linear", limit=200)["result"]["list"] 
    open_orders = client.get_active_orders(category="linear", limit=200)["result"]["list"] 
    for o in open_orders:
        pos = next((p for p in positions if p["symbol"] == o["symbol"]), None)
        if pos and float(pos.get("size", 0)) != 0.0:
            count += 1
        else:
            client.cancel_all_active_orders(category="linear", symbol=o["symbol"]) 
    return count

def get_prices(msg):
    parts = msg.split()
    if len(parts) < 2:
        raise ValueError("Symbol not provided")
    symbol = parts[1].upper()

    if symbol.endswith("USDT"):
        category = "linear"
    elif symbol.endswith("USD"):
        category = "inverse"
    else:
        category = "linear"

    resp = client.get_tickers(category=category, symbol=symbol)
    ticker_list = resp["result"]["list"]
    if not ticker_list:
        raise ValueError(f"Symbol {symbol} not found on Bybit")

    data = ticker_list[0]
    last_price             = float(data["lastPrice"])
    open_price             = float(data["prevPrice24h"])
    high_price             = float(data["highPrice24h"])
    low_price              = float(data["lowPrice24h"])
    price_change           = last_price - open_price
    price_change_percent   = float(data["price24hPcnt"]) * 100
    volume                 = float(data["volume24h"])
    quote_volume           = float(data["turnover24h"])

    weighted_avg_price     = (quote_volume / volume) if volume else 0.0

    return (
        price_change,
        price_change_percent,
        weighted_avg_price,
        last_price,
        open_price,
        high_price,
        low_price,
        volume,
        quote_volume
    )
    
def get_positions(store):
    a = []
    cursor = ""
    
    # Получаем все позиции с использованием пагинации
    while True:
        params = {
            'category': 'linear', 
            'settleCoin': 'USDT',
            'limit': 200  # Максимальный лимит на страницу
        }
        if cursor:
            params['cursor'] = cursor
            
        response = client.get_positions(**params)
        positions = response['result']['list']
        
        for pos in positions:
            symbol = pos['symbol']
            size = float(pos['size'])

            if size != 0.0:
                flag = 'Лонг' if pos['side'].upper() == 'BUY' else 'Шорт'
                pnl = round(float(pos['unrealisedPnl']) * store.multiplier, 2)
                a.append(f"{flag} {symbol} {pnl} USDT\n")
        
        # Проверяем, есть ли еще страницы
        cursor = response['result'].get('nextPageCursor')
        if not cursor:
            break
    
    return a
    
def get_orders(a=0, b=0):
    open_orders = client.get_open_orders(category='linear', settleCoin='USDT', limit=200)['result']['list']
    positions = client.get_positions(category='linear', settleCoin='USDT', limit=200)['result']['list']

    # Проходим по всем позициям
    for pos in positions:
        symbol = pos['symbol']
        position_amt = float(pos['size'])

        for order in open_orders:
            if order['symbol'] == symbol:
                if position_amt != 0.0:
                    a += 1 
                else:
                    b += 1 
    return a, b
    
def get_now(a=0):
    open_orders = client.get_open_orders(category='linear', settleCoin='USDT', limit=200)['result']['list']
    positions = client.get_positions(category='linear', settleCoin='USDT', limit=200)['result']['list']

    for pos in positions:
        symbol = pos['symbol']
        position_amt = float(pos['size'])

        for order in open_orders:
            if order['symbol'] == symbol:
                if position_amt != 0.0:
                    a += 1 
                else:
                    client.cancel_all_orders(category='linear', symbol=symbol)
    return a
    
def get_long(store):
    # Получаем все позиции по USDT с увеличенным лимитом
    positions_data = client.get_positions(category='linear', settleCoin='USDT', limit=200)['result']['list']

    # Закрываем все ЛОНГ позиции (позиции > 0)
    for pos in positions_data:
        symbol = pos['symbol']
        size = float(pos['size'])
        notional = float(pos['notional'])

        if size > 0 and notional > 0:
            client.place_order(
                category='linear',
                symbol=symbol,
                side='Sell',
                orderType='Market',
                qty=str(size),
                reduceOnly=True
            )

    # Обновляем список позиций после закрытия
    updated_positions = client.get_positions(category='linear', settleCoin='USDT', limit=200)['result']['list']

    a = []
    for pos in updated_positions:
        symbol = pos['symbol']
        size = float(pos['size'])
        unrealized_pnl = round(float(pos['unrealisedPnl']) * store.multiplier, 2)

        if size != 0.0:
            direction = 'Лонг' if size > 0 else 'Шорт'
            a.append(f"{direction} {symbol} {unrealized_pnl} USDT\n")
    return a

def get_short(store):
    # Получаем текущие позиции с увеличенным лимитом
    positions_data = client.get_positions(category='linear', settleCoin='USDT', limit=200)['result']['list']

    # Закрываем все ШОРТ позиции (позиции < 0)
    for pos in positions_data:
        symbol = pos['symbol']
        size = float(pos['size'])
        notional = float(pos['notional'])

        if size < 0 and notional < 0:
            client.place_order(
                category='linear',
                symbol=symbol,
                side='Buy',
                orderType='Market',
                qty=str(abs(size)),
                reduceOnly=True
            )

    # Обновляем список позиций после закрытия
    updated_positions = client.get_positions(category='linear', settleCoin='USDT', limit=200)['result']['list']

    a = []
    for pos in updated_positions:
        symbol = pos['symbol']
        size = float(pos['size'])
        unrealized_pnl = round(float(pos['unrealisedPnl']) * store.multiplier, 2)

        if size != 0.0:
            direction = 'Лонг' if size > 0 else 'Шорт'
            a.append(f"{direction} {symbol} {unrealized_pnl} USDT\n")
    return a

def get_position_all():
    # Получаем все позиции по USDT с увеличенным лимитом
    positions_data = client.get_positions(category='linear', settleCoin='USDT', limit=200)['result']['list']

    # Закрываем каждую позицию (и лонг, и шорт)
    for pos in positions_data:
        symbol = pos['symbol']
        size = float(pos['size'])

        if size > 0:
            # Лонг -> закрываем SELL
            client.place_order(
                category='linear',
                symbol=symbol,
                side='Sell',
                orderType='Market',
                qty=str(size),
                reduceOnly=True
            )
        elif size < 0:
            # Шорт -> закрываем BUY
            client.place_order(
                category='linear',
                symbol=symbol,
                side='Buy',
                orderType='Market',
                qty=str(abs(size)),
                reduceOnly=True
            )
    return

def get_order_all():
    # Получаем открытые ордера на фьючерсах с увеличенным лимитом
    open_orders = client.get_open_orders(category='linear', limit=200)['result']['list']

    # Получаем список уникальных тикеров с ордерами
    symbols_with_orders = {order['symbol'] for order in open_orders}

    # Отменяем ордера по каждому тикеру
    for symbol in symbols_with_orders:
        client.cancel_all_orders(category='linear', symbol=symbol)
    return
   
def close_orders(msg):
    symbol = msg.split(' ')[1].upper()

    # Получение всех открытых ордеров по фьючерсам
    open_orders = client.get_open_orders(category='linear', symbol=symbol)['result']['list']

    # Проверка наличия ордеров и их отмена
    if open_orders:
        client.cancel_all_orders(category='linear', symbol=symbol)
    return
    
def close_position(msg):
    symbol = msg.split(' ')[1].upper()

    # Получаем все позиции
    positions = client.get_positions(category='linear', symbol=symbol)['result']['list']

    for pos in positions:
        pos_symbol = pos['symbol']
        pos_size = float(pos['size'])
        pos_side = pos['side']  # 'Buy' или 'Sell'

        if pos_symbol == symbol and pos_size > 0:
            # Определяем противоположную сторону для закрытия позиции
            side = 'Sell' if pos_side == 'Buy' else 'Buy'

            # Отправляем маркет-ордер на закрытие позиции
            client.place_order(
                category='linear',
                symbol=symbol,
                side=side,
                orderType='Market',
                qty=str(pos_size),
                reduceOnly=True
            )
            break
    return
    
# Trading
MIN_ORDER_VALUE_USDT = 5.0

def get_leverage(symbol: str) -> int:
    resp = client.get_positions(
        accountType="UNIFIED",
        category="linear",
        settleCoin="USDT",
        symbol=symbol.upper(),
        limit=200
    )
    lst = resp.get("result", {}).get("list", [])
    if lst and lst[0].get("leverage") is not None:
        return int(lst[0]["leverage"])
    return 10

def get_min_qty(symbol: str) -> float:
    resp = client.get_instruments_info(category="linear", symbol=symbol.upper())
    lst = resp.get("result", {}).get("list", [])
    # print("resp: ", resp)
    # print("lst: ", lst)
    return float(lst[0]["lotSizeFilter"]["minOrderQty"]) if lst else 0.0

def get_balance(store) -> float:
    resp = client.get_wallet_balance(accountType="UNIFIED", coin="USDT")
    data_list = resp.get("result", {}).get("list", [])
    if not data_list:
        return 0.0

    coin_list = data_list[0].get("coin", [])
    if not coin_list:
        return 0.0

    usdt_info = next((c for c in coin_list if c.get("coin") == "USDT"), None)
    if usdt_info is None:
        return 0.0
    
    raw_balance = float(usdt_info.get("walletBalance", 0)) * store.multiplier
    return round(raw_balance, 2)

def get_default_balance() -> float:
    resp = client.get_wallet_balance(accountType="UNIFIED", coin="USDT")
    data_list = resp.get("result", {}).get("list", [])
    if not data_list:
        return 0.0

    coin_list = data_list[0].get("coin", [])
    if not coin_list:
        return 0.0

    usdt_info = next((c for c in coin_list if c.get("coin") == "USDT"), None)
    if usdt_info is None:
        return 0.0
    
    raw_balance = float(usdt_info.get("walletBalance", 0))
    return round(raw_balance, 2)

def get_price(symbol: str) -> float:
    try:
        resp = client.get_tickers(category="linear", symbol=symbol.upper())
        lst = resp.get("result", {}).get("list", [])
        if not lst:
            return None
        return float(lst[0]["lastPrice"])
    except:
        return None

def get_stop_price(store, entry_price: float, coin_flag: str) -> float:
    pct = store.stop / 100.0
    delta = entry_price * pct
    price = entry_price - delta if coin_flag.lower()=="long" else entry_price + delta
    return round(price, 8)

def get_tp_price(entry_price: float, tp_pct: float, coin_flag: str) -> float:
    delta = entry_price * (tp_pct/100.0)
    price = entry_price + delta if coin_flag.lower()=="long" else entry_price - delta
    return round(price, 8)

def get_side(coin_flag: str):
    return ("Buy","Sell") if coin_flag.lower()=="long" else ("Sell","Buy")

def get_qty(store, balance: float, min_qty: float, price: float) -> float:
    risk_amount = balance * store.risk
    raw_qty = risk_amount / price
    min_by_value = MIN_ORDER_VALUE_USDT / price
    base_qty = max(raw_qty, min_by_value)
    # Используем ceil вместо int для правильного округления вверх
    steps = max(math.ceil(base_qty / min_qty), 1)
    qty = round(steps * min_qty, len(str(min_qty).split('.')[-1]))
    
    # Логирование для отладки
    logging.debug(f"get_qty: balance={balance}, risk={store.risk}, price={price}")
    logging.debug(f"risk_amount={risk_amount}, raw_qty={raw_qty}, min_by_value={min_by_value}")
    logging.debug(f"base_qty={base_qty}, min_qty={min_qty}, steps={steps}, final_qty={qty}")
    
    return qty

def calc_precision(min_qty: float) -> int:
    """Рассчитывает точность для округления количества"""
    if min_qty == 0:
        return 0
    
    # Обработка очень маленьких чисел в научной нотации
    if min_qty < 1e-10:
        return 12
    
    # Преобразуем в строку и обрабатываем
    s = f"{min_qty:.12f}".rstrip('0')
    if '.' in s:
        return len(s.split('.')[-1])
    return 0


def trade(store, coin_name: str, coin_flag: str, symbol: str) -> str:
    """
    Открывает торговую позицию с проверками и валидацией
    """
    # Валидация входных параметров
    if not symbol or not coin_name or not coin_flag:
        return "Ошибка: отсутствуют обязательные параметры"
    
    if coin_flag.lower() not in ['long', 'short']:
        return "Ошибка: coin_flag должен быть 'long' или 'short'"
    
    side, opposite = ("Buy", "Sell") if coin_flag.lower() == 'long' else ("Sell", "Buy")
    symbol = symbol.upper()

    last_price = get_price(symbol)
    if not last_price:
        return f"Торговой пары @{symbol} на рынке не существует"

    desired_lev = store.leverage
    try:
        current_lev = get_leverage(symbol)
        if current_lev != desired_lev:
            client.set_leverage(
                category="linear",
                symbol=symbol,
                buyLeverage=str(desired_lev),
                sellLeverage=str(desired_lev),
                accountType="UNIFIED"
            )
    except:
        pass

    # Проверка существующей позиции
    resp_pos = client.get_positions(accountType="UNIFIED", category="linear", settleCoin="USDT", limit=200)
    existing = next((p for p in resp_pos["result"]["list"] if p.get("symbol") == symbol), None)
    exist_size = abs(float(existing.get("size", 0))) if existing else 0.0
    exist_side = 'long' if existing and existing.get('side') == 'Buy' else 'short'
    
    position_needs_flip = existing and exist_size > 0 and exist_side != coin_flag
    position_same_side = existing and exist_size > 0 and exist_side == coin_flag

    balance = get_default_balance()
    if balance <= 0:
        return "Ошибка: недостаточный баланс для торговли"
    
    min_qty = get_min_qty(symbol)
    if min_qty <= 0:
        return f"Ошибка: не удалось получить минимальное количество для {symbol}"
    
    new_qty = get_qty(store, balance, min_qty, last_price)

    # Проверка минимального значения ордера
    if new_qty * last_price < MIN_ORDER_VALUE_USDT:
        return f"Ошибка: сумма ордера {new_qty * last_price:.2f} USDT меньше минимума {MIN_ORDER_VALUE_USDT}"

    report = [f"@{symbol} {'Лонг' if side == 'Buy' else 'Шорт'} {new_qty} {coin_name} @ {last_price} USDT", f"Плечо: {desired_lev}x"]

    try:
        # Если направление противоположное — закрываем позицию и ордера
        if position_needs_flip:
            client.cancel_all_orders(category="linear", symbol=symbol, accountType="UNIFIED")
            client.place_order(
                category="linear",
                symbol=symbol,
                side=("Sell" if existing.get("side") == "Buy" else "Buy"),
                orderType="Market",
                qty=str(exist_size),
                reduceOnly=True,
                timeInForce="IOC",
                positionIdx=0,
                accountType="UNIFIED"
            )
            time.sleep(1)

        # Если позиция в ту же сторону — добавим к ней
        if position_same_side:
            client.cancel_all_orders(category="linear", symbol=symbol, accountType="UNIFIED")

        total_qty = new_qty + exist_size if position_same_side else new_qty

        # Проверка валидности total_qty
        if total_qty * last_price < MIN_ORDER_VALUE_USDT:
            return f"Ошибка: общая сумма позиции {total_qty * last_price:.2f} USDT меньше минимума {MIN_ORDER_VALUE_USDT}"

    except Exception as e:
        try:
            # Форсируем закрытие позиции
            if existing and exist_size > 0:
                client.cancel_all_orders(category="linear", symbol=symbol, accountType="UNIFIED")
                client.place_order(
                    category="linear",
                    symbol=symbol,
                    side=("Sell" if existing.get("side") == "Buy" else "Buy"),
                    orderType="Market",
                    qty=str(exist_size),
                    reduceOnly=True,
                    timeInForce="IOC",
                    positionIdx=0,
                    accountType="UNIFIED"
                )
        except:
            pass
        return f"Ошибка при обработке позиции: {e}"

    # TP ордера
    if store.tp:
        tp_vals = [float(x) for x in store.tp.split('-') if x]
        n = len(tp_vals)
        precision = calc_precision(min_qty)
        
        # Claculate optimal TP size that meets minimum value requirement
        min_tp_qty = math.ceil(MIN_ORDER_VALUE_USDT / last_price / min_qty) * min_qty
        tp_qty = max(total_qty / n, min_tp_qty)
        tp_qty = round(tp_qty, precision)
        
        remaining_qty = total_qty
        for i, pct in enumerate(tp_vals):
            if remaining_qty < min_tp_qty:
                break
            
            # For last TP order, use all remaining quantity 
            if i == len(tp_vals) - 1:
                tp_qty = remaining_qty
                
            tp_price = get_tp_price(last_price, pct, coin_flag)
            
            
            try:
                client.place_order(
                    category="linear",
                    symbol=symbol,
                    side=opposite,
                    orderType="Market",
                    qty=str(tp_qty),
                    reduceOnly=True,
                    triggerPrice=str(tp_price),
                    triggerBy="LastPrice",
                    triggerDirection=(1 if coin_flag.lower() == "long" else 2),
                    positionIdx=0,
                    accountType="UNIFIED"
                )
                report.append(f"ТП(+{pct}%): {tp_qty}@{tp_price}")
                remaining_qty -= tp_qty
            except Exception as e:
                report.append(f"ТП(+{pct}%): Ошибка ({e})")
                
    # if store.tp:
    #     tp_vals = [float(x) for x in store.tp.split('-') if x]
    #     n = len(tp_vals)
    #     precision = calc_precision(min_qty)
    #     skipped_all = True

    #     for pct in tp_vals:
    #         tp_price = get_tp_price(last_price, pct, coin_flag)
    #         # Используем более точный расчет для TP количества
    #         raw_each = total_qty / n
    #         # Обеспечиваем, что TP не превышает общее количество
    #         steps = max(math.floor(raw_each / min_qty), 1)
    #         tp_qty = round(steps * min_qty, precision)
            
    #         # Дополнительная проверка - TP не должен превышать total_qty
    #         tp_qty = min(tp_qty, total_qty)

    #         if tp_qty < min_qty or tp_qty * tp_price < MIN_ORDER_VALUE_USDT:
    #             report.append(f"ТП(+{pct}%): Скип (qty={tp_qty}, value={tp_qty * tp_price:.2f})")
    #             continue

    #         try:
    #             client.place_order(
    #                 category="linear",
    #                 symbol=symbol,
    #                 side=opposite,
    #                 orderType="Market",
    #                 qty=str(tp_qty),
    #                 reduceOnly=True,
    #                 triggerPrice=str(tp_price),
    #                 triggerBy="LastPrice",
    #                 triggerDirection=(1 if coin_flag.lower() == "long" else 2),
    #                 positionIdx=0,
    #                 accountType="UNIFIED"
    #             )
    #             report.append(f"ТП(+{pct}%): {tp_qty}@{tp_price}")
    #             skipped_all = False
    #         except Exception as e:
    #             report.append(f"ТП(+{pct}%): Ошибка ({e})")

        # if skipped_all:
        #     pct = tp_vals[-1]
        #     tp_price = get_tp_price(last_price, pct, coin_flag)
        #     # Используем более консервативный подход для финального TP
        #     raw_each = total_qty / n
        #     steps = max(math.floor(raw_each / min_qty), 1)
        #     tp_qty = round(steps * min_qty, precision)
        #     tp_qty = min(tp_qty, total_qty)
            
        #     try:
        #         client.place_order(
        #             category="linear",
        #             symbol=symbol,
        #             side=opposite,
        #             orderType="Market",
        #             qty=str(tp_qty),
        #             reduceOnly=True,
        #             triggerPrice=str(tp_price),
        #             triggerBy="LastPrice",
        #             triggerDirection=(1 if coin_flag.lower() == "long" else 2),
        #             positionIdx=0,
        #             accountType="UNIFIED"
        #         )
        #         report.append(f"ТП(+{pct}%): {tp_qty}@{tp_price}")
        #     except Exception as e:
        #         report.append(f"ТП(+{pct}%): Ошибка ({e})")

    # SL
    stop_price = get_stop_price(store, last_price, coin_flag)
    try:
        client.place_order(
            category="linear",
            symbol=symbol,
            side=opposite,
            orderType="Market",
            qty=str(total_qty),
            reduceOnly=True,
            triggerPrice=str(stop_price),
            triggerBy="LastPrice",
            triggerDirection=(2 if coin_flag.lower() == "long" else 1),
            positionIdx=0,
            accountType="UNIFIED"
        )
        report.append(f"СЛ({store.stop}%): {total_qty}@{stop_price}")
    except Exception as e:
        report.append(f"СЛ({store.stop}%): Ошибка ({e})")
        return "\n".join(report)

    # Открыть позицию
    try:
        client.place_order(
            category="linear",
            symbol=symbol,
            side=side,
            orderType="Market",
            qty=str(new_qty),
            timeInForce="FOK",
            reduceOnly=False,
            positionIdx=0,
            accountType="UNIFIED"
        )
        report.append(f"Позиция открыта: {new_qty} {symbol} {side}")
    except Exception as e:
        report.append(f"Открыть позицию: Ошибка ({e})")
        try:
            # Закрываем, если не получилось открыть
            client.place_order(
                category="linear",
                symbol=symbol,
                side=opposite,
                orderType="Market",
                qty=str(total_qty),
                reduceOnly=True,
                timeInForce="IOC",
                positionIdx=0,
                accountType="UNIFIED"
            )
            report.append(f"Аварийное закрытие позиции: {total_qty} {symbol}")
        except Exception as ex:
            report.append(f"Аварийное закрытие: не удалось ({ex})")

    return "\n".join(report)




