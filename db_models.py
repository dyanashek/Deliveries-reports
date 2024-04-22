from config import SQLALCHEMY_DATABASE_URL


from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float
from sqlalchemy.orm import sessionmaker, declarative_base


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class DBEmployees(Base):
    __tablename__ = "employees"

    employee_id = Column(String, primary_key = True, unique=True, nullable=False)
    employee_name = Column(String, unique=True, nullable=False)


class DBAdmins(Base):
    __tablename__ = "admins"

    admin_id = Column(String, primary_key = True, unique=True, nullable=False)


class DBShops(Base):
    __tablename__ = "shops"

    shop_id = Column(String, primary_key = True, unique=True, nullable=False)
    shop_name = Column(String, unique=True, nullable=False)
    shop_price = Column(Float, nullable=False)


class DBDeliveries(Base):
    __tablename__ = "deliveries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    employee_id = Column(String, nullable=False)
    employee_name = Column(String, nullable=False)
    shop_id = Column(String, nullable=False)
    shop_name = Column(String, nullable=False)
    shop_price = Column(Float, nullable=False)
    address = Column(String, nullable=False)
    delivery_time = Column(DateTime, nullable=False)


Base.metadata.create_all(bind=engine)