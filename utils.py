import datetime as dt


import config


def extract_address(text: str):
    text = text.replace('/done', '').lstrip(' ')

    return text


def extract_address_from_text(text: str):
    text = text.lower()
    for keyword in config.KEYWORDS:
        text = text.replace(keyword, '')

    text = text.strip(' ').capitalize()

    return text


def extract_id(text: str):
    delivery_id = text.replace('/cancel', '').strip(' ')
    try:
        delivery_id = int(delivery_id)
    except:
        delivery_id = False
    
    return delivery_id


def extract_employee_request(text: str):
    text = text.replace('/employee', '').lstrip(' ')
    data = text.split(' ')

    return data


def extract_shop_request(text: str):
    text = text.replace('/shop', '').lstrip(' ')
    data = text.split(' ')

    return data


def validate_date(date):
    try:
        date = dt.datetime.strptime(date, config.DATE_PATTERN)
    except:
        return False

    return date


def validate_data_request(data):
    if len(data) >= 3:
        start_date = validate_date(data[-2])
        end_date = transform_end_date(validate_date(data[-1]))
        param = ' '.join(data[:-2])

        if start_date and end_date and param:
            return param, start_date, end_date

    return False, False, False
        

def transform_end_date(end_date):
    try:
        year = end_date.year
        month = end_date.month
        day = end_date.day
    except:
        return False

    return dt.datetime(year, month, day, 23, 59, 59)


def escape_markdown(text):
    characters_to_escape = ['_', '*', '[', ']', '`']
    for char in characters_to_escape:
        text = text.replace(char, '\\' + char)

    return text


def numbers_format(value):
    """Makes a good looking numbers format."""

    return '{:,}'.format(value).replace(',', ' ')


def validate_add_data(data):
    if len(data) == 4:
        if command_date := validate_date(data[-1]):
            data[-1] = command_date
            return data

    return False


def parse_add_command(text: str):
    text = text.replace('/add', '').strip(' ')
    data = text.split(';')
    return validate_add_data(data)


def parse_shop_price_command(text: str):
    text = text.replace('/shop_price', '').strip(' ')
    data = text.split(' ')
    if len(data) == 2:
        try:
            delivery_id = int(data[0])
        except:
            delivery_id = False
        
        try:
            price = float(data[1].replace(',', '.'))
        except:
            price = False

        return delivery_id, price

    return False, False


def parse_employee_price_command(text: str):
    text = text.replace('/employee_price', '').strip(' ')
    data = text.split(' ')
    if len(data) == 2:
        try:
            delivery_id = int(data[0])
        except:
            delivery_id = False
        
        try:
            price = float(data[1].replace(',', '.'))
        except:
            price = False

        return delivery_id, price

    return False, False