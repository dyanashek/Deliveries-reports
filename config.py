import telebot
import os
from dotenv import load_dotenv


load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telebot.TeleBot(TELEGRAM_TOKEN)

SQLALCHEMY_DATABASE_URL = "sqlite:///./db.db"

MANAGER_ID = os.getenv('MANAGER_ID')

SPREAD_NAME = 'Flowers-delivery'
ADMINS_LIST_NAME = 'admins'
EMPLOYEES_LIST_NAME = 'employees'
SHOPS_LIST_NAME = 'shops'
DELIVERIES_LIST_NAME = 'deliveries'
AGROCITIES_LIST_NAME = 'agrocities'

DATE_PATTERN = "%d.%m.%y"

MAX_LEN = 4096

TIME_SLEEP = 3600

KEYWORDS = ['готово', 'готов', 'готоа', 'готова']