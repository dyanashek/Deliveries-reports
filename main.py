import telebot
import threading
import datetime as dt

import config
import utils
import db_functions
import functions
import text
from config import bot


threading.Thread(daemon=True, target=functions.update_deliveries).start()


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = str(message.from_user.id)
    if  user_id == config.MANAGER_ID or db_functions.get_admin(user_id):
        try:
            bot.send_message(chat_id=user_id,
                                text=text.START_MESSAGE,
                                parse_mode='Markdown',
                                )
        except:
            pass


@bot.message_handler(commands=['update'])
def update(message):
    user_id = str(message.from_user.id)
    if  user_id == config.MANAGER_ID or db_functions.get_admin(user_id):
        try:
            bot.send_message(chat_id=user_id,
                                text=text.STARTED_UPDATE,
                                parse_mode='Markdown',
                                )
        except:
            pass

        threading.Thread(daemon=True, target=functions.handle_update, args=(user_id,)).start()

    else:
        try:
            bot.send_message(chat_id=user_id,
                                text=text.NOT_ALLOWED,
                                parse_mode='Markdown',
                                )
        except:
            pass


@bot.message_handler(commands=['id'])
def update(message):
    user_id = str(message.from_user.id)
    if  user_id == config.MANAGER_ID or db_functions.get_admin(user_id):
        try:
            bot.send_message(chat_id=user_id,
                                    text=str(message.chat.id),
                                    parse_mode='Markdown',
                                    )
        except:
            pass

    else:
        try:
            bot.send_message(chat_id=user_id,
                                text=text.NOT_ALLOWED,
                                parse_mode='Markdown',
                                )
        except:
            pass


@bot.message_handler(commands=['cancel'])
def update(message):
    user_id = str(message.from_user.id)
    if  user_id == config.MANAGER_ID or db_functions.get_admin(user_id):
        if delivery_id := utils.extract_id(message.text):
            if db_functions.delete_delivery(delivery_id):
                try:
                    bot.send_message(chat_id=user_id,
                                    text=text.DELIVERY_DELETED,
                                    parse_mode='Markdown',
                                    )
                except:
                    pass
            else:
                try:
                    bot.send_message(chat_id=user_id,
                                    text=text.ID_NOT_FOUND,
                                    parse_mode='Markdown',
                                    )
                except:
                    pass

        else:
            try:
                bot.send_message(chat_id=user_id,
                                 text=text.WRONG_ID,
                                 parse_mode='Markdown',
                                 )
            except:
                pass

    else:
        try:
            bot.send_message(chat_id=user_id,
                                text=text.NOT_ALLOWED,
                                parse_mode='Markdown',
                                )
        except:
            pass


@bot.message_handler(commands=['done'])
def update(message):
    user_id = str(message.from_user.id)
    chat_id = str(message.chat.id)

    employee = db_functions.get_employee(user_id)
    shop = db_functions.get_shop(chat_id)

    if employee and shop:
        address = utils.extract_address(message.text)
        curr_time = dt.datetime.utcnow() + dt.timedelta(hours=3)

        db_functions.add_delivery(employee=employee,
                                  shop=shop,
                                  employee_price = employee.employee_price,
                                  shop_price = shop.shop_price,
                                  address=address,
                                  curr_time=curr_time,
                                  )


@bot.message_handler(commands=['employee'])
def employee_handler(message):
    user_id = str(message.from_user.id)
    if  user_id == config.MANAGER_ID or db_functions.get_admin(user_id):
        data = utils.extract_employee_request(message.text)
        employee_name, start_date, end_date = utils.validate_data_request(data)

        if employee_name and start_date and end_date:
            employee = db_functions.get_employee_by_name(employee_name)
            if employee:
                deliveries = db_functions.get_delivery_by_employee(employee, start_date, end_date)
                threading.Thread(daemon=True, target=functions.construct_employee_reply, args=(user_id, deliveries,)).start()
            else:
                try:
                    bot.send_message(chat_id=user_id,
                                        text=text.NO_EMPLOYEE,
                                        parse_mode='Markdown',
                                        )
                except:
                    pass

        else:
            try:
                bot.send_message(chat_id=user_id,
                                    text=text.ERROR_REQUEST,
                                    parse_mode='Markdown',
                                    )
            except:
                pass

    else:
        try:
            bot.send_message(chat_id=user_id,
                                text=text.NOT_ALLOWED,
                                parse_mode='Markdown',
                                )
        except:
            pass


@bot.message_handler(commands=['shop'])
def update(message):
    user_id = str(message.from_user.id)
    if  user_id == config.MANAGER_ID or db_functions.get_admin(user_id):
        data = utils.extract_shop_request(message.text)
        shop_name, start_date, end_date = utils.validate_data_request(data)

        if shop_name and start_date and end_date:
            shop = db_functions.get_shop_by_name(shop_name)
            if shop:
                deliveries = db_functions.get_delivery_by_shop(shop, start_date, end_date)
                threading.Thread(daemon=True, target=functions.construct_shop_reply, args=(user_id, deliveries,)).start()
            else:
                try:
                    bot.send_message(chat_id=user_id,
                                        text=text.NO_SHOP,
                                        parse_mode='Markdown',
                                        )
                except:
                    pass

        else:
            try:
                bot.send_message(chat_id=user_id,
                                    text=text.ERROR_REQUEST,
                                    parse_mode='Markdown',
                                    )
            except:
                pass

    else:
        try:
            bot.send_message(chat_id=user_id,
                                text=text.NOT_ALLOWED,
                                parse_mode='Markdown',
                                )
        except:
            pass


@bot.message_handler(content_types=['text'])
def handle_text(message):
    handle = False

    for keyword in config.KEYWORDS:
        if keyword in message.text.lower():
            handle = True
    
    if handle:
        user_id = str(message.from_user.id)
        chat_id = str(message.chat.id)

        employee = db_functions.get_employee(user_id)
        shop = db_functions.get_shop(chat_id)

        if employee and shop:
            address = utils.extract_address_from_text(message.text)
            curr_time = dt.datetime.utcnow() + dt.timedelta(hours=3)

            db_functions.add_delivery(employee=employee,
                                    shop=shop,
                                    employee_price = employee.employee_price,
                                    shop_price = shop.shop_price,
                                    address=address,
                                    curr_time=curr_time,
                                    )
    

if __name__ == '__main__':
    # bot.polling(timeout=80)
    while True:
        try:
            bot.polling()
        except:
            pass