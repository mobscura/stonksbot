from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# Inline Keyboards
def start_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="👛 Открыть Кошелёк", callback_data="open")
    ).adjust(1)
    return builder.as_markup()

def price_keyboard(symbol):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Chart", url=f'https://www.bybit.com/trade/usdt/{symbol}'),
        InlineKeyboardButton(text="News", 
        url='https://coinmarketcap.com/currencies/bitcoin/news/?utm_source=telegram&utm_medium=telegram&utm_campaign=cmcpricebot_2_cmc&utm_content=urlbutton#news')
    ).adjust(2)
    return builder.as_markup()

def config_keyboard(pnl, positions, orders):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text=f'PnL({pnl}$)', callback_data="market"),
        InlineKeyboardButton(text=f'Позиции({positions})', callback_data="positions"),
        InlineKeyboardButton(text=f'Открытые ордера({orders})', callback_data="orders")
    ).adjust(1, 1, 1)
    
    return builder.as_markup()
    
def market_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="< Назад", callback_data="config")
    ).adjust(1)
    return builder.as_markup()

def positions_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Лонг", callback_data="long"),
        InlineKeyboardButton(text="Шорт", callback_data="short"),
        InlineKeyboardButton(text="Все", callback_data="position_all"),
        InlineKeyboardButton(text="< Назад", callback_data="config"),
    ).adjust(2, 1, 1)
    return builder

def long_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Лонг", callback_data="long"),
        InlineKeyboardButton(text="Шорт", callback_data="short"),
        InlineKeyboardButton(text="Все", callback_data="position_all"),
        InlineKeyboardButton(text="< Назад", callback_data="config"),
    ).adjust(2, 1, 1)
    return builder.as_markup()

def short_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Лонг", callback_data="long"),
        InlineKeyboardButton(text="Шорт", callback_data="short"),
        InlineKeyboardButton(text="Все", callback_data="position_all"),
        InlineKeyboardButton(text="< Назад", callback_data="config"),
    ).adjust(2, 1, 1)
    return builder.as_markup()

def position_all_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Лонг", callback_data="long"),
        InlineKeyboardButton(text="Шорт", callback_data="short"),
        InlineKeyboardButton(text="Все", callback_data="position_all"),
        InlineKeyboardButton(text="< Назад", callback_data="config"),
    ).adjust(2, 1, 1)
    return builder.as_markup()

def orders_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Все ордера', callback_data='order_all'),
        InlineKeyboardButton(text='Не используемые', callback_data='now'),
        InlineKeyboardButton(text='< Назад', callback_data='config')
    ).adjust(2, 1)
    return builder.as_markup()

def order_all_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Все ордера', callback_data='order_all'),
        InlineKeyboardButton(text='Не используемые', callback_data='now'),
        InlineKeyboardButton(text='< Назад', callback_data='config')
    ).adjust(2, 1)
    return builder.as_markup()

def now_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text='Все ордера', callback_data='order_all'),
        InlineKeyboardButton(text='Не используемые', callback_data='now'),
        InlineKeyboardButton(text='< Назад', callback_data='config')
    ).adjust(2, 1)
    return builder.as_markup()

def trade_keyboard(symbol):
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Chart", url=f'https://www.bybit.com/trade/usdt/{symbol}')
    ).adjust(1)
    return builder.as_markup()

def positions_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Лонг", callback_data="long"),
        InlineKeyboardButton(text="Шорт", callback_data="short"),
        InlineKeyboardButton(text="Все", callback_data="position_all"),
        InlineKeyboardButton(text="< Назад", callback_data="config")
    ).adjust(2, 1, 1)
    return builder.as_markup()

def orders_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Все ордера", callback_data="order_all"),
        InlineKeyboardButton(text="Не используемые", callback_data="now"),
        InlineKeyboardButton(text="< Назад", callback_data="config")
    ).adjust(2, 1)
    return builder.as_markup()

def now_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Все ордера", callback_data="order_all"),
        InlineKeyboardButton(text="Не используемые", callback_data="now"),
        InlineKeyboardButton(text="< Назад", callback_data="config")
    ).adjust(2, 1)
    return builder.as_markup()
    
    
def long_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Лонг", callback_data="long"),
        InlineKeyboardButton(text="Шорт", callback_data="short"),
        InlineKeyboardButton(text="Все", callback_data="position_all"),
        InlineKeyboardButton(text="< Назад", callback_data="config")
    ).adjust(2, 1, 1)
    return builder.as_markup()

def short_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Лонг", callback_data="long"),
        InlineKeyboardButton(text="Шорт", callback_data="short"),
        InlineKeyboardButton(text="Все", callback_data="position_all"),
        InlineKeyboardButton(text="< Назад", callback_data="config")
    ).adjust(2, 1, 1)
    return builder.as_markup()

def position_all_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Лонг", callback_data="long"),
        InlineKeyboardButton(text="Шорт", callback_data="short"),
        InlineKeyboardButton(text="Все", callback_data="position_all"),
        InlineKeyboardButton(text="< Назад", callback_data="config")
    ).adjust(2, 1, 1)
    return builder.as_markup()

def order_all_keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(text="Все ордера", callback_data="order_all"),
        InlineKeyboardButton(text="Не используемые", callback_data="now"),
        InlineKeyboardButton(text="< Назад", callback_data="config")
    ).adjust(2, 1)
    return builder.as_markup()

# Reply Keyboards
def start_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="конфиг")],
            [KeyboardButton(text="пауза"),     KeyboardButton(text="стоп")],
            [KeyboardButton(text="тп"),       KeyboardButton(text="риск")],
            [KeyboardButton(text="режим")],
            [KeyboardButton(text="плечо"),       KeyboardButton(text="позиция")],
            [KeyboardButton(text="ордера"),       KeyboardButton(text="цена")],
        ],
        resize_keyboard=True
    )
    return keyboard