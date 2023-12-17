
import telebot
#import pb
import datetime
import pytz
import json
import traceback
from reverso_context_api import Client
import random
import time
import datetime
from multiprocessing import *
import schedule
import requests
import re
import env
import schedule
import env
import json
import time
from reverso_context_api import Client
from random import sample
import schedule
import env
import json
import time
from reverso_context_api import Client

bot = telebot.TeleBot(env.TOKEN)

def reverso():
    client = Client("en", "ru", credentials=(env.USER, env.PASSWORD))
    result = list(client.get_favorites())
    #jsonStr = json.dumps(result)
    #json_obj = json.loads(jsonStr)
    #with open('data.json', 'w') as f:
    #    json.dump(json_obj, f)
    with open('dictonary.json') as f:
        templates = json.load(f)
    dict_sum = list(result + templates)
    dict_sum[:] = [x for i, x in enumerate(dict_sum) if i == dict_sum.index(x)]
    with open("dictonary.json", "w", encoding="utf-8") as file:
        json.dump(dict_sum, file)
    len_dict = str(len(dict_sum))
    bot.send_message(env.CHAT_ID, text = "Dictonary is created! Amout of words: " + len_dict )

#schedule.every().day.at("00:30").do(reverso)
#schedule.every(0.05).minutes.do(reverso)
schedule.every().day.at("00:31").do(reverso)

while True:
    schedule.run_pending()
    time.sleep(1)