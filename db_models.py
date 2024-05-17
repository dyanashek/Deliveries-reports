from config import SQLALCHEMY_DATABASE_URL


from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DBEmployees(Base):
    __tablename__ = "employees"

    employee_id = Column(String, primary_key = True, unique=True, nullable=False)
    employee_name = Column(String, unique=True, nullable=False)
    employee_price = Column(Float, nullable=False)

    deliveries = relationship('DBDeliveries', back_populates='employee')


class DBAdmins(Base):
    __tablename__ = "admins"

    admin_id = Column(String, primary_key = True, unique=True, nullable=False)


class DBShops(Base):
    __tablename__ = "shops"

    shop_id = Column(String, primary_key = True, unique=True, nullable=False)
    shop_name = Column(String, unique=True, nullable=False)
    shop_price = Column(Float, nullable=False)

    deliveries = relationship('DBDeliveries', back_populates='shop')


class DBDeliveries(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String, ForeignKey('employees.employee_id'))
    shop_id = Column(String, ForeignKey('shops.shop_id'))
    shop_price = Column(Float, nullable=False)
    employee_price = Column(Float, nullable=False)
    address = Column(String, nullable=False)
    delivery_time = Column(DateTime, nullable=False)

    #relations
    employee = relationship('DBEmployees', back_populates='deliveries')
    shop = relationship('DBShops', back_populates='deliveries')


class DBAgrocities(Base):
    __tablename__ = "agrocities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=False)


Base.metadata.create_all(bind=engine)