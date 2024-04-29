from db_models import SessionLocal, DBAdmins, DBDeliveries, DBEmployees, DBShops, DBAgrocities


from sqlalchemy import asc
from sqlalchemy.orm import joinedload


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


def add_employee(user_name: str, user_id: str, employee_price: float):
    db_employee = DBEmployees(employee_name = user_name, employee_id = user_id, employee_price = employee_price)

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


def add_delivery(employee, shop, employee_price: float, shop_price: float, address, curr_time):
    db_delivery = DBDeliveries(employee = employee, shop = shop, shop_price = shop_price,
                               employee_price = employee_price, address = address, 
                               delivery_time = curr_time)

    with SessionLocal() as db:
        db.add(db_delivery)
        db.commit()


def get_delivery_by_employee(employee, start_date, end_date):
    with SessionLocal() as db:
        deliveries = db.query(DBDeliveries).join(
                                             DBEmployees, 
                                             DBDeliveries.employee_id == DBEmployees.employee_id
                                             ).options(joinedload(DBDeliveries.employee)).join(
                                             DBShops, 
                                             DBDeliveries.shop_id == DBShops.shop_id
                                             ).options(joinedload(DBDeliveries.shop)).filter(
                                                DBDeliveries.employee == employee, 
                                                DBDeliveries.delivery_time >= start_date, 
                                                DBDeliveries.delivery_time <= end_date,
                                                ).order_by(asc(DBShops.shop_name),
                                                        asc(DBDeliveries.delivery_time),
                                                        ).all()
    return deliveries


def get_delivery_by_shop(shop, start_date, end_date):
    with SessionLocal() as db:
        deliveries = db.query(DBDeliveries).join(
                                             DBEmployees, 
                                             DBDeliveries.employee_id == DBEmployees.employee_id
                                             ).options(joinedload(DBDeliveries.employee)).join(
                                             DBShops, 
                                             DBDeliveries.shop_id == DBShops.shop_id
                                             ).options(joinedload(DBDeliveries.shop)).filter(
                                                DBDeliveries.shop == shop, 
                                                DBDeliveries.delivery_time >= start_date, 
                                                DBDeliveries.delivery_time <= end_date,
                                                ).order_by(asc(DBEmployees.employee_name),
                                                        asc(DBDeliveries.delivery_time),
                                                        ).all()
    return deliveries


def get_all_deliveries():
    with SessionLocal() as db:
        deliveries = db.query(DBDeliveries).join(
                                             DBEmployees, 
                                             DBDeliveries.employee_id == DBEmployees.employee_id
                                             ).options(joinedload(DBDeliveries.employee)).join(
                                             DBShops, 
                                             DBDeliveries.shop_id == DBShops.shop_id
                                             ).options(joinedload(DBDeliveries.shop)).order_by(asc(DBDeliveries.delivery_time)).all()

    return deliveries


def delete_delivery(delivery_id):
    with SessionLocal() as db:
        delivery = db.query(DBDeliveries).filter(DBDeliveries.id == delivery_id).first()
        if delivery:
            try:
                db.delete(delivery)
                db.commit()

                return True
            except:
                return False
        else:
            return False

def update_shop_info(shop_id, shop_name, price):
    with SessionLocal() as db:
        shop = db.query(DBShops).filter(DBShops.shop_id == shop_id).first()
        shop.shop_price = price
        shop.shop_name = shop_name
        db.commit()


def update_employee_name(employee_id, employee_name, employee_price):
    with SessionLocal() as db:
        employee = db.query(DBEmployees).filter(DBEmployees.employee_id == employee_id).first()
        employee.employee_name = employee_name
        employee.employee_price = employee_price
        db.commit()


def get_agrocity(city: str):  
    with SessionLocal() as db:
        admin = db.query(DBAgrocities).filter(DBAgrocities.city == city).first()
    return admin


def add_agrocity(city: str):
    db_city = DBAgrocities(city = city)

    with SessionLocal() as db:
        db.add(db_city)
        try:
            db.commit()
        except:
            pass


def delete_agrocities():
    with SessionLocal() as db:
        db.query(DBAgrocities).delete()
        db.commit()