import datetime as dt
import time

import db_functions
import spread_functions
import text
import utils
import config
from config import bot


def handle_update(user_id):
    try:
        admins = spread_functions.get_admins()
        employees = spread_functions.get_employees()
        shops = spread_functions.get_shops()
        cities = spread_functions.get_agrocities()
    except:
        try:
            bot.send_message(chat_id=user_id,
                                text=text.NOT_UPDATED,
                                )
        except:
            pass

        return

    db_functions.delete_admins()
    for admin in admins:
        if admin:
            db_functions.add_admin(admin[0])

    db_functions.delete_agrocities()
    for city in cities:
        if city:
            try:
                city = utils.escape_markdown(city[0].strip(' ').lower())
                db_functions.add_agrocity(city)
            except:
                pass

    for shop in shops:
        shop_obj = db_functions.get_shop(shop[1])
        if not shop_obj:
            try:
                db_functions.add_shop(shop[0], shop[1], float(shop[2].replace(',', '.')))
            except:
                try:
                    bot.send_message(chat_id=user_id,
                                    text=text.shop_exist(shop[0]),
                                    )
                except:
                    pass
        
        else:
            try:
                db_functions.update_shop_info(shop[1], shop[0], float(shop[2].replace(',', '.')))
            except:
                pass


    for employee in employees:
        if not db_functions.get_employee(employee[1]):
            try:
                if employee[2].lower().strip(' ') == 'full':
                    price = 0
                else:
                    price = float(employee[2].replace(',', '.'))

                db_functions.add_employee(employee[0], employee[1], price)
            except:
                try:
                    bot.send_message(chat_id=user_id,
                                    text=text.employee_exist(employee[0]),
                                    )
                except:
                    pass
        else:
            try:
                if employee[2].lower().strip(' ') == 'full':
                    price = 0
                else:
                    price = float(employee[2].replace(',', '.'))

                db_functions.update_employee_name(employee[1], employee[0], price)
            except:
                pass

    try:
        bot.send_message(chat_id=user_id,
                        text=text.UPDATED,
                        )
    except:
        pass


def construct_employee_reply(user_id, deliveries):
    if deliveries:
        reply = ''

        deliveries_count = len(deliveries)

        curr_filter = ''
        numerate = 1
        total_salary = 0
        for num, delivery in enumerate(deliveries):
            shop_name = utils.escape_markdown(delivery.shop.shop_name)
            delivery_time = dt.datetime.strftime(delivery.delivery_time, config.DATE_PATTERN)
            address = utils.escape_markdown(delivery.address)

            total_salary += delivery.employee_price

            if num == 0:
                employee_name = utils.escape_markdown(delivery.employee.employee_name)
                curr_filter = shop_name
                reply += f'*{employee_name}:*\n\n╔*{shop_name}:*\n'

            if shop_name == curr_filter:
                reply += f'╠*{numerate}.* (id: {delivery.id}) {address} - {delivery_time}\n'
                numerate += 1

            else:
                curr_filter = shop_name
                reply += '╚═════════════\n'
                numerate = 1
                reply += f'╔*{shop_name}:*\n'
                reply += f'╠*{numerate}.* (id: {delivery.id}) {address} - {delivery_time}\n'
                numerate += 1
        
        total_salary = utils.numbers_format(total_salary)

        reply += '╚═════════════\n'
        reply += f'*ИТОГО ДОСТАВОК:* {deliveries_count}\n*ЗП:* {total_salary} р.'

        replies = [reply[i:i + config.MAX_LEN] for i in range(0, len(reply), config.MAX_LEN)]
        for reply in replies:
            try:
                bot.send_message(chat_id = user_id,
                                text = reply,
                                parse_mode = 'Markdown',
                                )
            except:
                pass
    
    else:
        try:
            bot.send_message(chat_id = user_id,
                            text = text.NO_DATA,
                            parse_mode = 'Markdown',
                            )
        except:
            pass


def construct_shop_reply(user_id, deliveries):
    if deliveries:
        reply = ''

        deliveries_count = len(deliveries)

        total_payout = 0

        for num, delivery in enumerate(deliveries):
            shop_name = utils.escape_markdown(delivery.shop.shop_name)
            employee_name = utils.escape_markdown(delivery.employee.employee_name)
            delivery_time = dt.datetime.strftime(delivery.delivery_time, config.DATE_PATTERN)
            address = utils.escape_markdown(delivery.address)
            
            total_payout += delivery.shop_price

            symbol = '╠'
            if num == 0:
                reply += f'*{shop_name}:*\n\n'
                symbol = '╔'
            
            reply += f'{symbol}*{num + 1}.* (id: {delivery.id}) {address} - {delivery_time}, {employee_name}'

            if delivery.shop_price == delivery.shop.shop_price:
                reply += '\n'
            else:
                reply += f' - {delivery.shop_price} р.\n'

        total_payout = utils.numbers_format(total_payout)

        reply += '╚═════════════\n'
        reply += f'*ИТОГО ДОСТАВОК:* {deliveries_count}\n*ВЫПЛАТА:* {total_payout} р.'

        replies = [reply[i:i + config.MAX_LEN] for i in range(0, len(reply), config.MAX_LEN)]
        for reply in replies:
            try:
                bot.send_message(chat_id = user_id,
                                text = reply,
                                parse_mode = 'Markdown',
                                )
            except:
                pass
    
    else:
        try:
            bot.send_message(chat_id = user_id,
                            text = text.NO_DATA,
                            parse_mode = 'Markdown',
                            )
        except:
            pass


def update_deliveries():
    while True:
        try:
            db_deliveries = db_functions.get_all_deliveries()

            deliveries = []

            for delivery in db_deliveries:
                delivery_time = dt.datetime.strftime(delivery.delivery_time, config.DATE_PATTERN)
                deliveries.append([delivery.id, 
                                   delivery.employee.employee_name, 
                                   delivery.shop.shop_name,
                                   delivery.address,
                                   delivery_time,
                                   delivery.employee_price,
                                   delivery.shop_price,
                                   ])
            
            spread_functions.update_deliveries(deliveries)

            time.sleep(config.TIME_SLEEP)
        except:
            pass