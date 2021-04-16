"""Just a way to clean up __init__.py"""
import time
import sys
import mariadb
from discord.ext.commands import when_mentioned_or
from discord.ext.commands import *
from discord.ext import *
from dotenv import load_dotenv
import os
import praw

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

OWNER_IDS = [541722893747224589]


def print_percent_done(index, total, bar_len=50, title='Starting bot'):
    percent_done = (index+1)/total*100
    percent_done = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '░'*int(togo)

    print(f'⏳{title}: [{done_str}{togo_str}] {percent_done}% done', end='\r')
    if round(percent_done) == 100:
        print('\nCompleted!')


reddit = praw.Reddit(client_id='c_85u5DZ793OFQ',
                     client_secret='iBBJIhWmv6uB3E6R7UNlgC7t8Go',
                     username="Electronbot123",
                     password="Electronbot123",
                     user_agent="Memes",
                     check_for_async=False)


def convertTuple(tup):
    str = ''.join(tup)
    return str


def get_prefix(client, message):
    conn = mariadb.connect(**dbinfo)
    cursor = conn.cursor()
    cursor.execute(
        'SELECT prefix FROM prefixes WHERE guild_id = ?', (message.guild.id, ))
    prefix = cursor.fetchone()
    prefixes = convertTuple(prefix)
    return when_mentioned_or(prefixes[0])(client, message)
