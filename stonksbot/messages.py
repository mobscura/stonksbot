# from utils import abbre_numbers, format_decimal
from stonksbot.utils import abbre_numbers, format_decimal

def start_text():
    text = "<b>Приступим!</b>\n\nДля открытия кошелька нажмите кнопку ниже."
    return text

def processing_text():
    text = "⏳ Обработка вашего запроса..."
    return text

def config_text(store, balance):
    if store.system:
        system = "Система запущена"
    else:
        system = "Система остановлена"
    if store.mode:
        stop = 'стоп'
    else:
        stop = 'трейлинг'
    text = f'баланс:<b>{balance}$</b>\nриск на сделку <b>{store.risk}</b> от баланса <b>({round(balance * store.risk, 2)}$)</b>\nтп на сделку <b>{store.tp}</b>\n{stop} на сделку <b>{store.stop}%</b>\nплечо на сделку {store.leverage}\n<b>{system}</b>'
    return text

def market_text(pnl, roe):
    text = f'<b>💸 PnL</b>\n\n<b><i>Данные о прибылях и убытках на фьючерсном счете в данный момент</i></b>\n\n<i>PnL: {pnl} USDT ({roe}%)</i>'
    return text

def positions_text(a=[]):
    if a:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>{''.join(a)}</i></b>\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    else:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>🌚 У вас нет открытых позиций.</i></b>\n\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    return text

def long_text(a=[]):
    if a:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>{''.join(a)}</i></b>\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    else:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>🌚 У вас нет открытых позиций.</i></b>\n\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    return text

def short_text(a=[]):
    if a:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>{''.join(a)}</i></b>\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    else:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>🌚 У вас нет открытых позиций.</i></b>\n\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    return text

def position_all_text():
    text = f"<b>Список открытых позиций</b>\n\n<b><i>🌚 У вас нет открытых позиций.</i></b>\n\n<i>Вы можете закрыть " \
           f"позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    return text

def orders_text(a=0, b=0):
    if (a + b) > 0:
        text = f'<b>Количество открытых ордеров</b>\n\nВсе: <b>{a + b}</b>\nТекущие: <b>{a}</b>\n\n<i>Вы можете закрыть ордера, нажав на кнопку <code>/orders btcusdt</code></i>'
    else:
        text = f'<b>Количество открытых ордеров</b>\n\n<b><i>🌚 У вас нет открытых ордеров.</i></b>\n\n<i>Вы можете закрыть ордера, ' \
               f'нажав на кнопку <code>/orders btcusdt</code></i>'
    return text

def order_all_text():
    text = f'<b>Количество открытых ордеров</b>\n\n<b><i>🌚 У вас нет открытых ордеров.</i></b>\n\n<i>Вы можете закрыть ордера, ' \
           f'нажав на кнопку <code>/orders btcusdt</code></i>'
    return text

def now_text(a=0):
    if a > 0:
        text = f'<b>Количество открытых ордеров</b>\n\nВсе: <b>{a}</b>\nТекущие: <b>{a}</b>\n\n<i>Вы можете закрыть ордера, нажав на кнопку <code>/orders btcusdt</code></i>'
    else:
        text = f'<b>Количество открытых ордеров</b>\n\n<b><i>🌚 У вас нет открытых ордеров.</i></b>\n\n<i>Вы можете закрыть ордера, ' \
               f'нажав на кнопку <code>/orders btcusdt</code></i>'
    return text

def selected_tp_text(store):
    text = f"Ок, <b>{store.tp}</b> тп приняты"
    return text


def error_tp_text():
    text = "Укажите действительный тейк-профит, например. <code>/t 1-2-3-4</code>."
    return text

def choose_tp_text():
    text = f"<b>Локальный тейк-профит</b>\n\n<i>Отправьте в сообщении уровени, которые хотите поставить <code>/tp 1-2-3-4</code></i>"
    return text

def pause_text(store):
    if store.system:
        text = f'<b>Система запущена</b>'
    else:
        text = f'<b>Система остановлена</b>'
    return text

def mode_text(store):
    if store.mode:
        text = f'Активирован режим <b>стоп-лосс</b>'
    else: 
        text = f'Активирован режим <b>трейлинг-стоп</b>'
    return text

def selected_stop_text(store):
    if store.mode:
        text = f"Стоп на сделку <b>{store.stop}%</b>"
    else:
        text = f"Трейлинг на сделку <b>{store.stop}%</b>"
    return text

def choose_stop_text():
    text = "<b>Локальный уровень</b>\n\n<i>Отправьте в сообщении уровень, который хотите поставить <code>/stop 2.25</code></i>"
    return text

def error_stop_text():
    text = "Укажите действительный стопа, например. <code>/s 1.25</code>."
    return text

def choose_risk_text():
    text = f"<b>Локальный риск</b>\n\n<i>Отправьте в сообщении уровень, который хотите поставить <code>/risk 0.25</code></i>"
    return text

def selected_risk_text(store, balance):
    text = f"риск на сделку изменен на <b>{store.risk}</b> от баланса <b>({round(balance * store.risk, 2)}$)</b>"
    return text

def error_risk_text():
    text = "Укажите действительный риск, например. <code>/r 1.25</code>."
    return text

def error_rate_text():
    text = "Укажите действительную торговую пару, например. <code>/price btcusdt</code>."
    return text

def rate_text(symbol, price_change, price_change_percent, weighted_avg_price, last_price, open_price, high_price, low_price, quote_volume, volume):
    text = f"<b>{symbol.upper()}</b>\n" \
        f"<b>Price:</b> ${format_decimal(last_price)} USD\n" \
        f"<b>1hr Change:</b> ${format_decimal(price_change)} USD\n" \
        f"<b>1hr Change:</b> {format_decimal(price_change_percent)}%\n" \
        f"<b>openPrice:</b> ${format_decimal(open_price)} USD\n" \
        f"<b>highPrice:</b> ${format_decimal(high_price)} USD\n" \
        f"<b>lowPrice:</b> ${format_decimal(low_price)} USD\n" \
        f"<b>Volume:</b> ${abbre_numbers(volume)} USD\n" \
        f"<b>Total Supply:</b> {abbre_numbers(quote_volume)}\n" \
        f"\n<a href='https://coinmarketcap.com/'>🚀 View on CoinMarketCap</a>"
    return text

def selected_leverage_text(store):
    text = f"Плечо на сделку <b>{store.leverage}</b>"
    return text

def choose_leverage_text():
    text = "<b>Локальные плечо</b>\n\n<i>Отправьте в сообщении плечо, которое хотите поставить на все монеты <code>/leverage 10</code></i>"
    return text

def error_leverage_text():
    text = "Укажите действительное плечо, например. <code>/leverage 10</code>."
    return text

def positions_text(a_list):
    if a_list:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>{''.join(a_list)}</i></b>\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    else:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>🌚 У вас нет открытых позиций.</i></b>\n\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>" 
    return text

def orders_text(a_list, b_list):
    if (a_list + b_list) > 0:
        text = f'<b>Количество открытых ордеров</b>\n\nВсе: <b>{a_list + b_list}</b>\nТекущие: <b>{a_list}</b>\n\n<i>Вы можете закрыть ордера, нажав на кнопку <code>/orders btcusdt</code></i>'
    else:
        text = f'<b>Количество открытых ордеров</b>\n\n<b><i>🌚 У вас нет открытых ордеров.</i></b>\n\n<i>Вы можете закрыть ордера, ' \
               f'нажав на кнопку <code>/orders btcusdt</code></i>'
    return text

def now_text(a_list):
    if a_list > 0:
        text = (
            f"<b>Количество открытых ордеров</b>\n\n"
            f"Все: <b>{a_list}</b>\nТекущие: <b>{a_list}</b>\n\n"
            "<i>Вы можете закрыть ордера, нажав на кнопку <code>/orders btcusdt</code></i>"
        )
    else:
        text = (
            "<b>Количество открытых ордеров</b>\n\n"
            "<b><i>🌚 У вас нет открытых ордеров.</i></b>\n\n"
            "<i>Вы можете закрыть ордера, нажав на кнопку <code>/orders btcusdt</code></i>"
        )
    return text

def long_text(a_list):
    if a_list:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>{''.join(a_list)}</i></b>\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    else:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>🌚 У вас нет открытых позиций.</i></b>\n\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    return text

def short_text(a_list):
    if a_list:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>{''.join(a_list)}</i></b>\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    else:
        text = f"<b>Список открытых позиций</b>\n\n<b><i>🌚 У вас нет открытых позиций.</i></b>\n\n<i>Вы можете закрыть позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    return

def get_position_all():
    text = f"<b>Список открытых позиций</b>\n\n<b><i>🌚 У вас нет открытых позиций.</i></b>\n\n<i>Вы можете закрыть " \
           f"позицию, нажав на кнопку <code>/position btcusdt</code></i>"
    return text

def get_order_all():
    text = f'<b>Количество открытых ордеров</b>\n\n<b><i>🌚 У вас нет открытых ордеров.</i></b>\n\n<i>Вы можете закрыть ордера, ' \
           f'нажав на кнопку <code>/orders btcusdt</code></i>'
    return text

def order_text(msg):
    symbol = msg.split(' ')[1]
    text = f'<i>Отлично, все ордера по торговой паре <b>{symbol.upper()}</b> закрыты!</i>'
    return text

def position_text(msg):
    symbol = msg.split(' ')[1]
    text = f'<i>Отлично, позиция по торговой паре <b>{symbol.upper()}</b> закрыта!</i>'
    return