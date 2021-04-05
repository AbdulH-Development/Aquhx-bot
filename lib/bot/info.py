"""Just a way to clean up __init__.py"""
from dotenv import load_dotenv
import os

load_dotenv()
IP = os.getenv("IP")
load_dotenv()
PASSWD = os.getenv("PASSWD")
load_dotenv()
DB = os.getenv("DB")
load_dotenv()
USER = os.getenv("USER")

dbinfo = {
    'user': USER,
    'host': IP,
    'password': PASSWD,
    'database': DB
}
