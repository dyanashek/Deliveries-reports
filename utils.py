import datetime as dt


import config


def extract_address(text: str):
    text = text.replace('/done', '').lstrip(' ')

    return text


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