from db_models import SessionLocal, DBAdmins, DBDeliveries, DBEmployees, DBShops


from sqlalchemy import asc


def get_admin(user_id: str):  
    with SessionLocal() as db:
        admin = db.query(DBAdmins).filter(DBAdmins.admin_id == user_id).first()
    return admin


def add_admin(user_id: str):
    db_admin = DBAdmins(admin_id = user_id)

    with SessionLocal() as db:
        db.add(db_admin)
        try:
            db.commit()
        except:
            pass


def delete_admins():
    with SessionLocal() as db:
        db.query(DBAdmins).delete()
        db.commit()


def get_employee(user_id: str):  
    with SessionLocal() as db:
        employee = db.query(DBEmployees).filter(DBEmployees.employee_id == user_id).first()
    return employee


def get_employee_by_name(user_name: str):  
    with SessionLocal() as db:
        employee = db.query(DBEmployees).filter(DBEmployees.employee_name == user_name).first()
    return employee


def add_employee(user_name: str, user_id: str):
    db_employee = DBEmployees(employee_name = user_name, employee_id = user_id)

    with SessionLocal() as db:
        db.add(db_employee)
        db.commit()



def get_shop(shop_id: str):  
    with SessionLocal() as db:
        shop = db.query(DBShops).filter(DBShops.shop_id == shop_id).first()
    return shop


def get_shop_by_name(shop_name: str):  
    with SessionLocal() as db:
        shop = db.query(DBShops).filter(DBShops.shop_name == shop_name).first()
    return shop


def add_shop(shop_name: str, shop_id: str, shop_price: float):
    db_shop = DBShops(shop_name = shop_name, shop_id = shop_id, shop_price = shop_price)

    with SessionLocal() as db:
        db.add(db_shop)
        db.commit()


def add_delivery(user_name: str, user_id: str, shop_name: str, shop_id: str, shop_price: float, address, curr_time):
    db_delivery = DBDeliveries(employee_name = user_name, employee_id = user_id, 
                               shop_name = shop_name, shop_id = shop_id, shop_price = shop_price,
                               address = address, delivery_time = curr_time)

    with SessionLocal() as db:
        db.add(db_delivery)
        db.commit()


def get_delivery_by_employee(user_name, start_date, end_date):
    with SessionLocal() as db:
        deliveries = db.query(DBDeliveries).filter(DBDeliveries.employee_name == user_name, 
                                             DBDeliveries.delivery_time >= start_date, 
                                             DBDeliveries.delivery_time <= end_date,
                                             ).order_by(asc(DBDeliveries.shop_name),
                                                        asc(DBDeliveries.delivery_time),
                                                        ).all()
    return deliveries


def get_delivery_by_shop(shop_name, start_date, end_date):
    with SessionLocal() as db:
        deliveries = db.query(DBDeliveries).filter(DBDeliveries.shop_name == shop_name, 
                                             DBDeliveries.delivery_time >= start_date, 
                                             DBDeliveries.delivery_time <= end_date,
                                             ).order_by(asc(DBDeliveries.employee_name),
                                                        asc(DBDeliveries.delivery_time),
                                                        ).all()
    return deliveries


def get_all_deliveries():
    with SessionLocal() as db:
        deliveries = db.query(DBDeliveries).order_by(asc(DBDeliveries.delivery_time)).all()

    return deliveries