from aiogram import types
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from conf.config import TOKEN, receiver_id, robot_id
from stonksbot.store import Store
from stonksbot.utils import get_signal, get_parameter
from stonksbot.keyboards import start_keyboard, config_keyboard, price_keyboard, trade_keyboard, positions_keyboard, orders_keyboard, now_keyboard, long_keyboard, short_keyboard, position_all_keyboard, order_all_keyboard
from stonksbot.messages import processing_text, config_text, selected_tp_text, choose_tp_text, pause_text, selected_stop_text, choose_stop_text, mode_text, selected_risk_text, choose_risk_text, error_rate_text, rate_text, market_text, selected_leverage_text, choose_leverage_text, position_text, order_text, now_text, long_text, short_text, position_all_text, order_all_text, orders_text, positions_text
from stonksbot.client import get_config, get_balance, get_prices, get_market, trade, get_stats, get_positions, get_orders, get_now, get_long, get_short, get_position_all, get_order_all, close_orders, close_position

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command(commands=["start", "config", "pause", "mode", "stop", "tp", "risk", "leverage", "position", "orders", "price"]))
async def command_start(message: Message) -> None:
    store = Store()
    chat_id = message.chat.id
    message_id = message.message_id
    msg = message.text
    if chat_id in robot_id:
        if msg == "/start":
            await bot.send_message(chat_id=chat_id, text=f"<b>Приступим!</b>\n\nКоманды:\n/config - Получить конфиг\n/pause - остановить/запустить\n/mode - стоп-лосс/трейлинг-стоп\n/stop - установить процент стопа\n/tp - установить тейк-профиты\n/risk - установить процент риска\n/leverage - установить плечо для монеты\n/position - закрыть позицию у монеты\n/orders - закрыть ордера у монеты\n/price - получить курс монеты\n\nДля открытия терминала нажмите кнопку ниже.", reply_markup=start_keyboard(), parse_mode="HTML")
        elif msg == "/config":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            balance = get_config(store)
            pnl, positions, orders = get_stats(store)
            await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=config_text(store, balance), reply_markup=config_keyboard(pnl, positions, orders), parse_mode='HTML')
        elif msg == "/pause":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            Store.system = not store.system
            await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=pause_text(store), parse_mode="HTML")
        elif msg == "/mode":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            Store.mode = not store.mode
            await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=mode_text(store), parse_mode="HTML")
        elif msg.split(' ')[0] == "/stop":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(' ')) == 2:
                try:
                    count = float(msg.split(' ')[1])
                    if count == int(count):
                        count = int(count)
                    item = count
                    Store.stop = item
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=selected_stop_text(store),
                                                parse_mode='html')
                except:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_stop_text(),
                                                parse_mode='html')
            else:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_stop_text(),
                                            parse_mode='html')
        elif msg.split(' ')[0] == "/tp":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(" ")) == 2:
                try:
                    item = msg.split(" ")[1]
                    Store.tp = item
                    await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=selected_tp_text(), parse_mode="HTML")
                except:
                    await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=choose_tp_text(), parse_mode="HTML")
            else:
                await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=choose_tp_text(), parse_mode="HTML")
        elif msg.split(' ')[0] == "/risk":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(' ')) == 2:
                try:
                    count = float(msg.split(' ')[1])
                    if count == int(count):
                        count = int(count)
                    item = count
                    Store.risk = item
                    balance = get_balance(store)
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=selected_risk_text(store, balance),
                                                parse_mode='html')
                except:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_risk_text(),
                                                parse_mode='html')
            else:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_risk_text(),
                                            parse_mode='html')
        elif msg.split(' ')[0] == "/leverage":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(' ')) == 2:
                try:
                    count = float(msg.split(' ')[1])
                    if count == int(count):
                        count = int(count)
                    item = count
                    Store.leverage = item
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=selected_leverage_text(store),
                                                parse_mode='html')
                except:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_leverage_text(),
                                                parse_mode='html')
            else:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_leverage_text(),
                                            parse_mode='html')
        elif msg.split(' ')[0] == "/position":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(' ')) == 2:
                try:
                    close_position(msg)
                    await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=position_text(msg), parse_mode="HTML")
                except:
                    a_list = get_positions(store)
                    await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=positions_text(a_list), reply_markup=positions_keyboard(), parse_mode="HTML")
            else:
                a_list = get_positions(store)
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=positions_text(a_list), reply_markup=positions_keyboard(), parse_mode="HTML")
        elif msg.split(' ')[0] == "/orders":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(' ')) == 2:
                try:
                    close_orders(msg)
                    await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=order_text(msg), parse_mode="HTML")
                except:
                    a_list, b_list = get_orders()
                    await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=orders_text(a_list, b_list), reply_markup=orders_keyboard(), parse_mode="HTML")
            else:
                a_list, b_list = get_orders()
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=orders_text(a_list, b_list), reply_markup=orders_keyboard(), parse_mode="HTML")
        elif msg.split(' ')[0] == "/price":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(' ')) == 2:
                try:
                    price_change, price_change_percent, weighted_avg_price, last_price, open_price, high_price, low_price, volume, quote_volume = get_prices(msg)
                    await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=rate_text(msg.split(' ')[1], price_change, price_change_percent, weighted_avg_price, last_price, open_price, high_price, low_price, volume, quote_volume),
                                                reply_markup=price_keyboard(msg.split(' ')[1]), parse_mode='html', disable_web_page_preview=True)
                except:
                    await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=error_rate_text(),
                                                parse_mode='html')
            else:
                await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=error_rate_text(),
                                            parse_mode='html')
    else:
        await bot.send_message(
            chat_id, f"Hello world, {message.from_user.first_name}! My name is decrypt, im your best AI helper.", parse_mode="HTML"
        )
    
@dp.message()
async def text_receiver(message: types.Message):
    store = Store()
    msg = message.text
    chat_id = message.chat.id
    if chat_id in robot_id:
        if msg == "конфиг":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            balance = get_config(store)
            pnl, positions, orders = get_stats(store)
            await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=config_text(store, balance), reply_markup=config_keyboard(pnl, positions, orders), parse_mode='HTML')
        elif msg == "пауза":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            Store.system = not store.system
            await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=pause_text(store), parse_mode="HTML")
        elif msg == "стоп":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(' ')) == 2:
                try:
                    count = float(msg.split(' ')[1])
                    if count == int(count):
                        count = int(count)
                    item = count
                    Store.stop = item
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=selected_stop_text(store),
                                                parse_mode='html')
                except:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_stop_text(),
                                                parse_mode='html')
            else:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_stop_text(),
                                            parse_mode='html')
        elif msg == "риск":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(' ')) == 2:
                try:
                    count = float(msg.split(' ')[1])
                    if count == int(count):
                        count = int(count)
                    item = count
                    Store.risk = item
                    balance = get_balance(store)
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=selected_risk_text(store, balance),
                                                parse_mode='html')
                except:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_risk_text(),
                                                parse_mode='html')
            else:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_risk_text(),
                                            parse_mode='html')
        elif msg == "тп":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(" ")) == 2:
                try:
                    item = msg.split(" ")[1]
                    Store.tp = item
                    await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=selected_tp_text(store), parse_mode="HTML")
                except:
                    await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=choose_tp_text(), parse_mode="HTML")
            else:
                await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=choose_tp_text(), parse_mode="HTML")
        elif msg == "режим":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            Store.mode = not store.mode
            await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=mode_text(store), parse_mode="HTML")
        elif msg == "плечо":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(' ')) == 2:
                try:
                    count = float(msg.split(' ')[1])
                    if count == int(count):
                        count = int(count)
                    item = count
                    Store.leverage = item
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=selected_leverage_text(store),
                                                parse_mode='html')
                except:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_leverage_text(),
                                                parse_mode='html')
            else:
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id + 1, text=choose_leverage_text(),
                                            parse_mode='html')
        elif msg == "цена":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            if len(msg.split(' ')) == 2:
                try:
                    price_change, price_change_percent, weighted_avg_price, last_price, open_price, high_price, low_price, volume, quote_volume = get_prices(msg)
                    await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=rate_text(msg.split(' ')[1], price_change, price_change_percent, weighted_avg_price, last_price, open_price, high_price, low_price, volume, quote_volume),
                                                reply_markup=price_keyboard(msg.split(' ')[1]), parse_mode='html', disable_web_page_preview=True)
                except:
                    await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=error_rate_text(),
                                                parse_mode='html')
            else:
                await bot.edit_message_text(chat_id=chat_id, message_id=message.message_id + 1, text=error_rate_text(),
                                            parse_mode='html')
            
    elif chat_id in receiver_id:
        if get_signal(message) and store.system:
            coin_name, coin_flag, symbol = get_parameter(message)
            text = trade(store, coin_name, coin_flag, symbol)
            markup = trade_keyboard(symbol)
            try:
                for i in range(len(receiver_id)):
                    new_chat_id = receiver_id[i]
                    await bot.send_message(new_chat_id, text, reply_markup=markup, parse_mode='html')
            except:
                pass
           
@dp.callback_query()
async def inlines(c: types.CallbackQuery):
    store = Store()
    data = c.data or ""
    chat_id = c.message.chat.id
    message_id = c.message.message_id
    parts = data.split()       
    cmd = parts[0]             
    args = parts[1:]           

    if cmd in {"config", "stop", "market", "positions",
               "long", "short", "position_all", "orders", "order_all",
               "now", "open"}:
        if cmd == "config":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            balance = get_config(store)
            pnl, positions, orders = get_stats(store)
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=config_text(store, balance), reply_markup=config_keyboard(pnl, positions, orders), parse_mode='HTML')
        elif cmd == "stop":
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=choose_stop_text(),
                                            parse_mode='html')
        elif cmd == "market":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            pnl, roe = get_market(store)
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=market_text(pnl, roe), parse_mode="HTML")
        elif cmd == "positions":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            a_list = get_positions(store)
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=positions_text(a_list), reply_markup=positions_keyboard(), parse_mode="HTML")
        elif cmd == "long":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            a_list = get_long(store)
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=long_text(a_list), reply_markup=long_keyboard(), parse_mode="HTML")
        elif cmd == "short":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            a_list = get_short(store)
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=short_text(a_list), reply_markup=short_keyboard(), parse_mode="HTML")
        elif cmd == "position_all":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            get_position_all()
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=position_all_text(), reply_markup=position_all_keyboard(), parse_mode="HTML")
        elif cmd == "orders":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            a_list, b_list = get_orders()
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=orders_text(a_list, b_list), reply_markup=orders_keyboard(), parse_mode="HTML")
        elif cmd == "order_all":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            get_order_all()
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=order_all_text(), reply_markup=order_all_keyboard(), parse_mode="HTML")
        elif cmd == "now":
            await bot.send_message(chat_id=chat_id, text=processing_text(), parse_mode="HTML")
            a_list = get_now()
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id + 1, text=now_text(a_list), reply_markup=now_keyboard(), parse_mode="HTML")

    else:
        await c.answer("Unknown team", show_alert=True)
        
        

async def trader() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    