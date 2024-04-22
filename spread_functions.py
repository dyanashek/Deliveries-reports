import gspread


import config

service_acc = gspread.service_account(filename='service_account.json')
sheet = service_acc.open(config.SPREAD_NAME)


def get_employees():
    work_sheet = sheet.worksheet(config.EMPLOYEES_LIST_NAME)
    employees = work_sheet.get_all_values()[1::]
    
    return employees


def get_shops():
    work_sheet = sheet.worksheet(config.SHOPS_LIST_NAME)
    shops = work_sheet.get_all_values()[1::]
    
    return shops


def get_admins():
    work_sheet = sheet.worksheet(config.ADMINS_LIST_NAME)
    admins = work_sheet.get_all_values()[1::]
    
    return admins


def update_deliveries(deliveries):
    work_sheet = sheet.worksheet(config.DELIVERIES_LIST_NAME)
    work_sheet.update(f'A2:DJ{len(deliveries) + 1}', deliveries)