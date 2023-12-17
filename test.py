
import telebot
#import pb
import datetime
import pytz
import json
import traceback
import main
from reverso_context_api import Client
import random
import time
import datetime
from multiprocessing import *
import schedule
import requests
import test
import re
import env
from random import sample
from time import sleep, time
from functools import wraps
from itertools import groupby
from aiogram import Bot, Dispatcher, executor, types

from aiogram import Bot, Dispatcher, types, executor

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from multiprocessing import *
import schedule
from functools import wraps

bot = Bot(token=env.TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=['new_chat_members'])
async def new_chat_members(message):
  await message.answer(f"Hello. Choose your quiz: /eng (quiz with russian answers), /rus (quiz with english answers), /ran (random quiz all dictonary), /ran10 (quiz with 10 random words), /last20 (quiz with 20 last words) , /last50 (quiz with 50 last words) /cr_ran10 (list of 10 random words), /cr_dict (create all dictonary), /cr_last20 (list of 20 last words), /cr_last50 (list of 50 last words)")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
   kb = [
       [
           types.KeyboardButton(text="/ran"),
           types.KeyboardButton(text="/ran10"),
           types.KeyboardButton(text="/last20"),
           types.KeyboardButton(text="/last50")

       ],
   ]
   keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
 
   await message.reply("Hello. Choose your quiz: /eng (quiz with russian answers), /rus (quiz with english answers), /ran (random quiz all dictonary), /ran10 (quiz with 10 random words), /last20 (quiz with 20 last words) , /last50 (quiz with 50 last words) /cr_ran10 (list of 10 random words), /cr_dict (create all dictonary), /cr_last20 (list of 20 last words), /cr_last50 (list of 50 last words)", reply_markup=keyboard)


def reverso():
    client = Client("en", "ru", credentials=(env.USER, env.PASSWORD))
    result = list(client.get_favorites())
    #jsonStr = json.dumps(result)
    #json_obj = json.loads(jsonStr)
    #with open('data.json', 'w') as f:
    #    json.dump(json_obj, f)
    return result

def dictonary_read():
    with open('dictonary.json') as f:
        templates = json.load(f)
    return templates

@dp.message_handler(commands=['cr_dict'])
async def start(message: types.Message):
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
    #for x in dict_sum: 
    #    if dict_sum.count(x) > 1: 
    #        dict_sum.remove(x)
    with open("dictonary.json", "w", encoding="utf-8") as file:
        json.dump(dict_sum, file)
    len_dict = str(len(dict_sum))
    await bot.send_message(message.chat.id, "Dictonary is created! Amout of words: " + len_dict)


def defin(x):
    try:
        response = requests.get('https://api.dictionaryapi.dev/api/v2/entries/en/'+ x)
        json_res = response.json()
        definition = json_res[0]['meanings'][0]['definitions'][0]['definition']
        pronounce = json_res[0]['phonetic']
    except TypeError:
        print('Ошибка TypeError')
        definition = '#'
        pronounce = '#'
    except SystemError:
        print('Ошибка SystemError')
        definition = '#'
        pronounce = '#'
    except ValueError:
        print('Ошибка ValueError')
        definition = '#'
        pronounce = '#'
    except SyntaxError:
        print('Ошибка SyntaxError')
        definition = '#'
        pronounce = '#'
    except KeyError:
        print('Ошибка KeyError')
        definition = '#'
        pronounce = '#'
    except UnboundLocalError:
        print('Ошибка UnboundLocalError')
        definition = '#'
        pronounce = '#'
    return [definition,pronounce]


@dp.message_handler(commands=['eng'])
async def start(message: types.Message):
    result = dictonary_read()
    ran = random.choice(result)
    source_text = str(ran['source_text'])
    remove_soorce_text = re.sub('[-,.\-/=!&?-]', '', source_text)
    len_text = len(remove_soorce_text)
    target_text = str(ran['target_text'])
    remove_targ_text = re.sub('[-,.\-/=!&?-]', '', target_text)
    target_context = str(ran['target_context'])
    remove_target = target_context[:75]
    source_context = str(ran['source_context'])
    clean_context = re.sub('[-,.\-/=!&?-]', '', source_context)
    remove_context = re.sub(source_text, len_text * '_ ', source_context)
    random_extra = random.choice(result)
    extra_word = str(random_extra['source_text'])
    transl_extra_word = str(random_extra['target_text'])
    random_extra1 = random.choice(result)
    extra_word1 = str(random_extra1['source_text'])
    transl_extra_word1 = str(random_extra1['target_text'])
    n = '\n'
    total_list = []
    while source_text == extra_word or extra_word1 == extra_word or extra_word1 == source_text:
        random_extra = random.choice(result)
        extra_word = str(random_extra['source_text'])
        transl_extra_word = str(random_extra['target_text'])
        random_extra1 = random.choice(result)
        extra_word1 = str(random_extra1['source_text'])
        transl_extra_word1 = str(random_extra1['target_text'])
    total_list.append(source_text)
    total_list.append(extra_word)
    total_list.append(extra_word1)
    random.shuffle(total_list)
    dp = defin(source_text)
    defenition = str(dp[0])
    pronounce = str(dp[1])
    #a, b, c = total_list[:3]
    options = total_list[:3]
    correct = total_list.index(source_text)
    first_text = 'D: ' + defenition + n + 'E: ' + remove_context
    tips = 'T: ' + remove_target + n + 'CA: ' + source_text.upper() + ' ' + '[' + pronounce + ']' + ' - ' + target_text + n + extra_word + ' - ' + transl_extra_word + ' ; ' + extra_word1 + ' - ' + transl_extra_word1
    dict_eng = {'total_issue':first_text,'total_options':options,'total_tips':tips,'total_answer':correct}
    await bot.send_poll(message.chat.id, first_text,
        options,
        type='quiz', correct_option_id=correct ,explanation=tips, is_anonymous=False)


@dp.message_handler(commands=['cr_ran10'])
async def start(message: types.Message):
    list_ten_ = dictonary_read()
    ran = sample(list_ten_,10)
    with open("ran.json", "w", encoding="utf-8") as file:
        json.dump(ran, file)
    string_words = ''
    for i in ran:
        string_words += f"{i['source_text']} - {i['target_text']}" + '\n'
    await bot.send_message(message.chat.id, string_words)

def write_list():
    with open('ran.json') as f:
        templates = json.load(f)
    return templates




@dp.message_handler(commands=['cr_last20'])
async def start(message: types.Message):
    list_ten_ = dictonary_read()
    ran = list_ten_[0:19]
    with open("last20.json", "w", encoding="utf-8") as file:
        json.dump(ran, file)
    #source_text = ran['source_text']
    #target_text = ran['target_text']
    string_words = ''
    for i in ran:
        string_words += f"{i['source_text']} - {i['target_text']}" + '\n'
    await bot.send_message(message.chat.id, string_words)

def write_last10():
    with open('last20.json') as f:
        templates = json.load(f)
    return templates


@dp.message_handler(commands=['cr_last50'])
async def start(message: types.Message):
    list_ten_ = dictonary_read()
    ran = list_ten_[0:49]
    with open("last50.json", "w", encoding="utf-8") as file:
        json.dump(ran, file)
    await bot.send_message(message.chat.id, "Last50 is created")

def write_last50():
    with open('last50.json') as f:
        templates = json.load(f)
    return templates


@dp.message_handler(commands=['last50'])
async def start(message: types.Message):
    result = write_last50()
    ran = random.choice(result)
    source_text = str(ran['source_text'])
    remove_soorce_text = re.sub('[-,.\-/=!&?-]', '', source_text)
    len_text = len(remove_soorce_text)
    target_text = str(ran['target_text'])
    remove_targ_text = re.sub('[-,.\-/=!&?-]', '', target_text)
    target_context = str(ran['target_context'])
    remove_target = target_context[:75]
    source_context = str(ran['source_context'])
    clean_context = re.sub('[-,.\-/=!&?-]', '', source_context)
    remove_context = re.sub(source_text, len_text * '_ ', source_context)
    random_extra = random.choice(result)
    extra_word = str(random_extra['source_text'])
    transl_extra_word = str(random_extra['target_text'])
    random_extra1 = random.choice(result)
    extra_word1 = str(random_extra1['source_text'])
    transl_extra_word1 = str(random_extra1['target_text'])
    n = '\n'
    total_list = []
    while source_text == extra_word or extra_word1 == extra_word or extra_word1 == source_text:
        random_extra = random.choice(result)
        extra_word = str(random_extra['source_text'])
        transl_extra_word = str(random_extra['target_text'])
        random_extra1 = random.choice(result)
        extra_word1 = str(random_extra1['source_text'])
        transl_extra_word1 = str(random_extra1['target_text'])
    total_list.append(source_text)
    total_list.append(extra_word)
    total_list.append(extra_word1)
    random.shuffle(total_list)
    dp = defin(source_text)
    defenition = str(dp[0])
    pronounce = str(dp[1])
    #a, b, c = total_list[:3]
    options = total_list[:3]
    correct = total_list.index(source_text)
    first_text = 'D: ' + defenition + n + 'E: ' + remove_context
    tips = 'T: ' + remove_target + n + 'CA: ' + source_text.upper() + ' ' + '[' + pronounce + ']' + ' - ' + target_text + n + extra_word + ' - ' + transl_extra_word + ' ; ' + extra_word1 + ' - ' + transl_extra_word1
    dict_eng = {'total_issue':first_text,'total_options':options,'total_tips':tips,'total_answer':correct}
    #####rus
    result_rus = write_last50()
    ran_rus = random.choice(result_rus)
    source_text_rus = str(ran_rus['source_text'])
    remove_soorce_text_rus = re.sub('[-,.\-/=!&?-]', '', source_text_rus)
    len_text_rus = len(remove_soorce_text_rus)
    target_text_rus = str(ran_rus['target_text'])
    remove_targ_text_rus = re.sub('[-,.\-/=!&?-]', '', target_text_rus)
    target_context_rus = str(ran_rus['target_context'])
    remove_target_rus = target_context_rus[:75]
    source_context_rus = str(ran_rus['source_context'])
    clean_context_rus = re.sub('[-,.\-/=!&?-]', '', source_context_rus)
    remove_context_rus = re.sub(source_text_rus, source_text_rus.upper(), source_context_rus)
    random_extra_rus = random.choice(result_rus)
    extra_word_rus = str(random_extra_rus['target_text'])
    transl_extra_word_rus = str(random_extra_rus['source_text'])
    random_extra1_rus = random.choice(result_rus)
    extra_word1_rus = str(random_extra1_rus['target_text'])
    transl_extra_word1_rus = str(random_extra1_rus['source_text'])
    n = '\n'
    total_list_rus = []
    while target_text_rus == extra_word_rus or extra_word1_rus == extra_word_rus or extra_word1_rus == target_text_rus:
        random_extra_rus = random.choice(result_rus)
        extra_word_rus = str(random_extra_rus['target_text'])
        transl_extra_word_rus = str(random_extra_rus['source_text'])
        random_extra1_rus = random.choice(result_rus)
        extra_word1_rus = str(random_extra1_rus['target_text'])
        transl_extra_word1_rus = str(random_extra1_rus['source_text'])
    total_list_rus.append(target_text_rus)
    total_list_rus.append(extra_word_rus)
    total_list_rus.append(extra_word1_rus)
    random.shuffle(total_list_rus)
    dp_rus = defin(source_text_rus)
    defenition_rus = str(dp_rus[0])
    pronounce_rus = str(dp_rus[1])
    #a, b, c = total_list[:3]
    first_text_rus = 'D: ' + defenition_rus + n + 'E: ' + remove_context_rus
    options_rus = total_list_rus[:3]
    tips_rus = 'T: ' + remove_target_rus + n + 'CA: ' + source_text_rus.upper() + ' ' + '[' + pronounce_rus + ']' + ' - ' + target_text_rus + n + transl_extra_word_rus + ' - ' + extra_word_rus + ' ; ' + transl_extra_word1_rus + ' - ' + extra_word1_rus
    correct_rus = total_list_rus.index(target_text_rus)
    dict_rus = {'total_issue':first_text_rus,'total_options':options_rus,'total_tips':tips_rus,'total_answer':correct_rus}
    together_list = []
    together_list.append(dict_eng)
    together_list.append(dict_rus)
    random_dict = random.choices(together_list)
    total_issue = random_dict[0]['total_issue']
    total_options = random_dict[0]['total_options']
    total_tips = random_dict[0]['total_tips']
    total_answer = random_dict[0]['total_answer']
    await bot.send_poll(message.chat.id, total_issue,
        total_options,
        type='quiz', correct_option_id=total_answer ,explanation=total_tips, is_anonymous=False)


@dp.message_handler(commands=['last20'])
async def start(message: types.Message):
    result = write_last10()
    ran = random.choice(result)
    source_text = str(ran['source_text'])
    remove_soorce_text = re.sub('[-,.\-/=!&?-]', '', source_text)
    len_text = len(remove_soorce_text)
    target_text = str(ran['target_text'])
    remove_targ_text = re.sub('[-,.\-/=!&?-]', '', target_text)
    target_context = str(ran['target_context'])
    remove_target = target_context[:75]
    source_context = str(ran['source_context'])
    clean_context = re.sub('[-,.\-/=!&?-]', '', source_context)
    remove_context = re.sub(source_text, len_text * '_ ', source_context)
    random_extra = random.choice(result)
    extra_word = str(random_extra['source_text'])
    transl_extra_word = str(random_extra['target_text'])
    random_extra1 = random.choice(result)
    extra_word1 = str(random_extra1['source_text'])
    transl_extra_word1 = str(random_extra1['target_text'])
    n = '\n'
    total_list = []
    while source_text == extra_word or extra_word1 == extra_word or extra_word1 == source_text:
        random_extra = random.choice(result)
        extra_word = str(random_extra['source_text'])
        transl_extra_word = str(random_extra['target_text'])
        random_extra1 = random.choice(result)
        extra_word1 = str(random_extra1['source_text'])
        transl_extra_word1 = str(random_extra1['target_text'])
    total_list.append(source_text)
    total_list.append(extra_word)
    total_list.append(extra_word1)
    random.shuffle(total_list)
    dp = defin(source_text)
    defenition = str(dp[0])
    pronounce = str(dp[1])
    #a, b, c = total_list[:3]
    options = total_list[:3]
    correct = total_list.index(source_text)
    first_text = 'D: ' + defenition + n + 'E: ' + remove_context
    tips = 'T: ' + remove_target + n + 'CA: ' + source_text.upper() + ' ' + '[' + pronounce + ']' + ' - ' + target_text + n + extra_word + ' - ' + transl_extra_word + ' ; ' + extra_word1 + ' - ' + transl_extra_word1
    dict_eng = {'total_issue':first_text,'total_options':options,'total_tips':tips,'total_answer':correct}
    #####rus
    result_rus = write_last10()
    ran_rus = random.choice(result_rus)
    source_text_rus = str(ran_rus['source_text'])
    remove_soorce_text_rus = re.sub('[-,.\-/=!&?-]', '', source_text_rus)
    len_text_rus = len(remove_soorce_text_rus)
    target_text_rus = str(ran_rus['target_text'])
    remove_targ_text_rus = re.sub('[-,.\-/=!&?-]', '', target_text_rus)
    target_context_rus = str(ran_rus['target_context'])
    remove_target_rus = target_context_rus[:75]
    source_context_rus = str(ran_rus['source_context'])
    clean_context_rus = re.sub('[-,.\-/=!&?-]', '', source_context_rus)
    remove_context_rus = re.sub(source_text_rus, source_text_rus.upper(), source_context_rus)
    random_extra_rus = random.choice(result_rus)
    extra_word_rus = str(random_extra_rus['target_text'])
    transl_extra_word_rus = str(random_extra_rus['source_text'])
    random_extra1_rus = random.choice(result_rus)
    extra_word1_rus = str(random_extra1_rus['target_text'])
    transl_extra_word1_rus = str(random_extra1_rus['source_text'])
    n = '\n'
    total_list_rus = []
    while target_text_rus == extra_word_rus or extra_word1_rus == extra_word_rus or extra_word1_rus == target_text_rus:
        random_extra_rus = random.choice(result_rus)
        extra_word_rus = str(random_extra_rus['target_text'])
        transl_extra_word_rus = str(random_extra_rus['source_text'])
        random_extra1_rus = random.choice(result_rus)
        extra_word1_rus = str(random_extra1_rus['target_text'])
        transl_extra_word1_rus = str(random_extra1_rus['source_text'])
    total_list_rus.append(target_text_rus)
    total_list_rus.append(extra_word_rus)
    total_list_rus.append(extra_word1_rus)
    random.shuffle(total_list_rus)
    dp_rus = defin(source_text_rus)
    defenition_rus = str(dp_rus[0])
    pronounce_rus = str(dp_rus[1])
    #a, b, c = total_list[:3]
    first_text_rus = 'D: ' + defenition_rus + n + 'E: ' + remove_context_rus
    options_rus = total_list_rus[:3]
    tips_rus = 'T: ' + remove_target_rus + n + 'CA: ' + source_text_rus.upper() + ' ' + '[' + pronounce_rus + ']' + ' - ' + target_text_rus + n + transl_extra_word_rus + ' - ' + extra_word_rus + ' ; ' + transl_extra_word1_rus + ' - ' + extra_word1_rus
    correct_rus = total_list_rus.index(target_text_rus)
    dict_rus = {'total_issue':first_text_rus,'total_options':options_rus,'total_tips':tips_rus,'total_answer':correct_rus}
    together_list = []
    together_list.append(dict_eng)
    together_list.append(dict_rus)
    random_dict = random.choices(together_list)
    total_issue = random_dict[0]['total_issue']
    total_options = random_dict[0]['total_options']
    total_tips = random_dict[0]['total_tips']
    total_answer = random_dict[0]['total_answer']
    await bot.send_poll(message.chat.id, total_issue,
        total_options,
        type='quiz', correct_option_id=total_answer ,explanation=total_tips, is_anonymous=False)

@dp.message_handler(commands=['ran10'])
async def start(message: types.Message):
    result = write_list()
    ran = random.choice(result)
    source_text = str(ran['source_text'])
    remove_soorce_text = re.sub('[-,.\-/=!&?-]', '', source_text)
    len_text = len(remove_soorce_text)
    target_text = str(ran['target_text'])
    remove_targ_text = re.sub('[-,.\-/=!&?-]', '', target_text)
    target_context = str(ran['target_context'])
    remove_target = target_context[:75]
    source_context = str(ran['source_context'])
    clean_context = re.sub('[-,.\-/=!&?-]', '', source_context)
    remove_context = re.sub(source_text, len_text * '_ ', source_context)
    random_extra = random.choice(result)
    extra_word = str(random_extra['source_text'])
    transl_extra_word = str(random_extra['target_text'])
    random_extra1 = random.choice(result)
    extra_word1 = str(random_extra1['source_text'])
    transl_extra_word1 = str(random_extra1['target_text'])
    n = '\n'
    total_list = []
    while source_text == extra_word or extra_word1 == extra_word or extra_word1 == source_text:
        random_extra = random.choice(result)
        extra_word = str(random_extra['source_text'])
        transl_extra_word = str(random_extra['target_text'])
        random_extra1 = random.choice(result)
        extra_word1 = str(random_extra1['source_text'])
        transl_extra_word1 = str(random_extra1['target_text'])
    total_list.append(source_text)
    total_list.append(extra_word)
    total_list.append(extra_word1)
    random.shuffle(total_list)
    dp = defin(source_text)
    defenition = str(dp[0])
    pronounce = str(dp[1])
    #a, b, c = total_list[:3]
    options = total_list[:3]
    correct = total_list.index(source_text)
    first_text = 'D: ' + defenition + n + 'E: ' + remove_context
    tips = 'T: ' + remove_target + n + 'CA: ' + source_text.upper() + ' ' + '[' + pronounce + ']' + ' - ' + target_text + n + extra_word + ' - ' + transl_extra_word + ' ; ' + extra_word1 + ' - ' + transl_extra_word1
    dict_eng = {'total_issue':first_text,'total_options':options,'total_tips':tips,'total_answer':correct}
    #####rus
    result_rus = write_list()
    ran_rus = random.choice(result_rus)
    source_text_rus = str(ran_rus['source_text'])
    remove_soorce_text_rus = re.sub('[-,.\-/=!&?-]', '', source_text_rus)
    len_text_rus = len(remove_soorce_text_rus)
    target_text_rus = str(ran_rus['target_text'])
    remove_targ_text_rus = re.sub('[-,.\-/=!&?-]', '', target_text_rus)
    target_context_rus = str(ran_rus['target_context'])
    remove_target_rus = target_context_rus[:75]
    source_context_rus = str(ran_rus['source_context'])
    clean_context_rus = re.sub('[-,.\-/=!&?-]', '', source_context_rus)
    remove_context_rus = re.sub(source_text_rus, source_text_rus.upper(), source_context_rus)
    random_extra_rus = random.choice(result_rus)
    extra_word_rus = str(random_extra_rus['target_text'])
    transl_extra_word_rus = str(random_extra_rus['source_text'])
    random_extra1_rus = random.choice(result_rus)
    extra_word1_rus = str(random_extra1_rus['target_text'])
    transl_extra_word1_rus = str(random_extra1_rus['source_text'])
    n = '\n'
    total_list_rus = []
    while target_text_rus == extra_word_rus or extra_word1_rus == extra_word_rus or extra_word1_rus == target_text_rus:
        random_extra_rus = random.choice(result_rus)
        extra_word_rus = str(random_extra_rus['target_text'])
        transl_extra_word_rus = str(random_extra_rus['source_text'])
        random_extra1_rus = random.choice(result_rus)
        extra_word1_rus = str(random_extra1_rus['target_text'])
        transl_extra_word1_rus = str(random_extra1_rus['source_text'])
    total_list_rus.append(target_text_rus)
    total_list_rus.append(extra_word_rus)
    total_list_rus.append(extra_word1_rus)
    random.shuffle(total_list_rus)
    dp_rus = defin(source_text_rus)
    defenition_rus = str(dp_rus[0])
    pronounce_rus = str(dp_rus[1])
    #a, b, c = total_list[:3]
    first_text_rus = 'D: ' + defenition_rus + n + 'E: ' + remove_context_rus
    options_rus = total_list_rus[:3]
    tips_rus = 'T: ' + remove_target_rus + n + 'CA: ' + source_text_rus.upper() + ' ' + '[' + pronounce_rus + ']' + ' - ' + target_text_rus + n + transl_extra_word_rus + ' - ' + extra_word_rus + ' ; ' + transl_extra_word1_rus + ' - ' + extra_word1_rus
    correct_rus = total_list_rus.index(target_text_rus)
    dict_rus = {'total_issue':first_text_rus,'total_options':options_rus,'total_tips':tips_rus,'total_answer':correct_rus}
    together_list = []
    together_list.append(dict_eng)
    together_list.append(dict_rus)
    random_dict = random.choices(together_list)
    total_issue = random_dict[0]['total_issue']
    total_options = random_dict[0]['total_options']
    total_tips = random_dict[0]['total_tips']
    total_answer = random_dict[0]['total_answer']
    await bot.send_poll(message.chat.id, total_issue,
        total_options,
        type='quiz', correct_option_id=total_answer ,explanation=total_tips, is_anonymous=False)


@dp.message_handler(commands=['rus'])
async def start(message: types.Message):
    result = dictonary_read()
    ran = random.choice(result)
    source_text = str(ran['source_text'])
    remove_soorce_text = re.sub('[-,.\-/=!&?-]', '', source_text)
    len_text = len(remove_soorce_text)
    target_text_rus = str(ran['target_text'])
    remove_targ_text = re.sub('[-,.\-/=!&?-]', '', target_text_rus)
    target_context = str(ran['target_context'])
    remove_target = target_context[:75]
    source_context = str(ran['source_context'])
    clean_context = re.sub('[-,.\-/=!&?-]', '', source_context)
    remove_context_rus = re.sub(source_text, source_text.upper(), source_context)
    random_extra_rus = random.choice(result)
    extra_word_rus = str(random_extra_rus['target_text'])
    transl_extra_word_rus = str(random_extra_rus['source_text'])
    random_extra1_rus = random.choice(result)
    extra_word1_rus = str(random_extra1_rus['target_text'])
    transl_extra_word1_rus = str(random_extra1_rus['source_text'])
    n = '\n'
    total_list_rus = []
    while target_text_rus == extra_word_rus or extra_word1_rus == extra_word_rus or extra_word1_rus == target_text_rus:
        random_extra_rus = random.choice(result)
        extra_word_rus = str(random_extra_rus['target_text'])
        transl_extra_word_rus = str(random_extra_rus['source_text'])
        random_extra1_rus = random.choice(result)
        extra_word1_rus = str(random_extra1_rus['target_text'])
        transl_extra_word1_rus = str(random_extra1_rus['source_text'])
    total_list_rus.append(target_text_rus)
    total_list_rus.append(extra_word_rus)
    total_list_rus.append(extra_word1_rus)
    random.shuffle(total_list_rus)
    dp_rus = defin(source_text)
    defenition_rus = str(dp_rus[0])
    pronounce_rus = str(dp_rus[1])
    #a, b, c = total_list[:3]
    first_text_rus = 'D: ' + defenition_rus + n + 'E: ' + remove_context_rus
    options_rus = total_list_rus[:3]
    tips_rus = 'T: ' + remove_target + n + 'CA: ' + source_text.upper() + ' ' + '[' + pronounce_rus + ']' + ' - ' + target_text_rus + n + transl_extra_word_rus + ' - ' + extra_word_rus + ' ; ' + transl_extra_word1_rus + ' - ' + extra_word1_rus
    correct_rus = total_list_rus.index(target_text_rus)
    dict_rus = {'total_issue':first_text_rus,'total_options':options_rus,'total_tips':tips_rus,'total_answer':correct_rus}
    await bot.send_poll(message.chat.id, first_text_rus,
        options_rus,
        type='quiz', correct_option_id=correct_rus ,explanation=tips_rus, is_anonymous=False)



@dp.message_handler(commands=['ran'])
async def start(message: types.Message):      
    result = dictonary_read()
    ran = random.choice(result)
    source_text = str(ran['source_text'])
    remove_soorce_text = re.sub('[-,.\-/=!&?-]', '', source_text)
    len_text = len(remove_soorce_text)
    target_text = str(ran['target_text'])
    remove_targ_text = re.sub('[-,.\-/=!&?-]', '', target_text)
    target_context = str(ran['target_context'])
    remove_target = target_context[:75]
    source_context = str(ran['source_context'])
    clean_context = re.sub('[-,.\-/=!&?-]', '', source_context)
    remove_context = re.sub(source_text, len_text * '_ ', source_context)
    random_extra = random.choice(result)
    extra_word = str(random_extra['source_text'])
    transl_extra_word = str(random_extra['target_text'])
    random_extra1 = random.choice(result)
    extra_word1 = str(random_extra1['source_text'])
    transl_extra_word1 = str(random_extra1['target_text'])
    n = '\n'
    total_list = []
    while source_text == extra_word or extra_word1 == extra_word or extra_word1 == source_text:
        random_extra = random.choice(result)
        extra_word = str(random_extra['source_text'])
        transl_extra_word = str(random_extra['target_text'])
        random_extra1 = random.choice(result)
        extra_word1 = str(random_extra1['source_text'])
        transl_extra_word1 = str(random_extra1['target_text'])
    total_list.append(source_text)
    total_list.append(extra_word)
    total_list.append(extra_word1)
    random.shuffle(total_list)
    dp = defin(source_text)
    defenition = str(dp[0])
    pronounce = str(dp[1])
    #a, b, c = total_list[:3]
    options = total_list[:3]
    correct = total_list.index(source_text)
    first_text = 'D: ' + defenition + n + 'E: ' + remove_context
    tips = 'T: ' + remove_target + n + 'CA: ' + source_text.upper() + ' ' + '[' + pronounce + ']' + ' - ' + target_text + n + extra_word + ' - ' + transl_extra_word + ' ; ' + extra_word1 + ' - ' + transl_extra_word1
    dict_eng = {'total_issue':first_text,'total_options':options,'total_tips':tips,'total_answer':correct}
    #####rus
    result_rus = dictonary_read()
    ran_rus = random.choice(result_rus)
    source_text_rus = str(ran_rus['source_text'])
    remove_soorce_text_rus = re.sub('[-,.\-/=!&?-]', '', source_text_rus)
    len_text_rus = len(remove_soorce_text_rus)
    target_text_rus = str(ran_rus['target_text'])
    remove_targ_text_rus = re.sub('[-,.\-/=!&?-]', '', target_text_rus)
    target_context_rus = str(ran_rus['target_context'])
    remove_target_rus = target_context_rus[:75]
    source_context_rus = str(ran_rus['source_context'])
    clean_context_rus = re.sub('[-,.\-/=!&?-]', '', source_context_rus)
    remove_context_rus = re.sub(source_text_rus, source_text_rus.upper(), source_context_rus)
    random_extra_rus = random.choice(result_rus)
    extra_word_rus = str(random_extra_rus['target_text'])
    transl_extra_word_rus = str(random_extra_rus['source_text'])
    random_extra1_rus = random.choice(result_rus)
    extra_word1_rus = str(random_extra1_rus['target_text'])
    transl_extra_word1_rus = str(random_extra1_rus['source_text'])
    n = '\n'
    total_list_rus = []
    while target_text_rus == extra_word_rus or extra_word1_rus == extra_word_rus or extra_word1_rus == target_text_rus:
        random_extra_rus = random.choice(result_rus)
        extra_word_rus = str(random_extra_rus['target_text'])
        transl_extra_word_rus = str(random_extra_rus['source_text'])
        random_extra1_rus = random.choice(result_rus)
        extra_word1_rus = str(random_extra1_rus['target_text'])
        transl_extra_word1_rus = str(random_extra1_rus['source_text'])
    total_list_rus.append(target_text_rus)
    total_list_rus.append(extra_word_rus)
    total_list_rus.append(extra_word1_rus)
    random.shuffle(total_list_rus)
    dp_rus = defin(source_text_rus)
    defenition_rus = str(dp_rus[0])
    pronounce_rus = str(dp_rus[1])
    #a, b, c = total_list[:3]
    first_text_rus = 'D: ' + defenition_rus + n + 'E: ' + remove_context_rus
    options_rus = total_list_rus[:3]
    tips_rus = 'T: ' + remove_target_rus + n + 'CA: ' + source_text_rus.upper() + ' ' + '[' + pronounce_rus + ']' + ' - ' + target_text_rus + n + transl_extra_word_rus + ' - ' + extra_word_rus + ' ; ' + transl_extra_word1_rus + ' - ' + extra_word1_rus
    correct_rus = total_list_rus.index(target_text_rus)
    dict_rus = {'total_issue':first_text_rus,'total_options':options_rus,'total_tips':tips_rus,'total_answer':correct_rus}
    together_list = []
    together_list.append(dict_eng)
    together_list.append(dict_rus)
    random_dict = random.choices(together_list)
    total_issue = random_dict[0]['total_issue']
    total_options = random_dict[0]['total_options']
    total_tips = random_dict[0]['total_tips']
    total_answer = random_dict[0]['total_answer']
    await bot.send_poll(message.chat.id, total_issue,
        total_options,
        type='quiz', correct_option_id=total_answer ,explanation=total_tips, is_anonymous=False)




@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("Hello. Choose your quiz: /eng (quiz with russian answers), /rus (quiz with english answers), /ran (random quiz all dictonary), /ran10 (quiz with 10 random words), /last20 (quiz with 20 last words) , /last50 (quiz with 50 last words) /cr_ran10 (list of 10 random words), /cr_dict (create all dictonary), /cr_last20 (list of 20 last words), /cr_last50 (list of 50 last words)")

executor.start_polling(dp, skip_updates=True)


#@dp.callback_query_handler(state=Questions.q1)
#async def q1(c: types.CallbackQuery, state: FSMContext):
#    # Получаем ответ от первого вопроса и отправляем второй вопрос
#
#    # Вы можете сохранить ответ пользователя так (если надо):
#    #await state.set_data(q1=c.data)
#
#    # переходим в следущий state и задаем вопрос
#    await Questions.next()
#    await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
#                                text='Вы любите новый год?', reply_markup=christmas_keyboard)
#
#    # if c.data == 'нет':
#    #     await bot.answer_callback_query(c.id, text='')
#    # elif c.data == 'да':
#    #     await bot.answer_callback_query(c.id, text='')
#
#
#@dp.callback_query_handler(state=Questions.q2)
#async def q2(c: types.CallbackQuery, state: FSMContext):
#    #await state.set_data(q2=c.data)
#    await Questions.next()
#    await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
#                                text='Викторина закончена, спасибо за участие!', reply_markup=end_vic_keyboard)
#
#    # if c.data == 'нет':
#    #     await bot.answer_callback_query(c.id, text='')
#    # elif c.data == 'да':
#    #     await bot.answer_callback_query(c.id, text='')
#
#
#@dp.callback_query_handler(state='*')
#async def inlines(c: types.CallbackQuery, state: FSMContext):
#    # передаём ответы пользователя в переменную перед тем как завершить fsm
#    answers = await state.get_data()
#
#    # завершаем fsm
#    await state.finish()
#
#    if c.data == 'replaytest':
#        # заново начинаем вопрос
#        await Questions.next()
#
#        # в конце ты мошежь показать ответы пользователя так
#        await c.message.answer('1-вопрос: ' + answers['q1'] + \
#                               '2-вопрос: ' + answers['q2'])
#
#        await bot.answer_callback_query(c.id, text='')
#        await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
#                                    text='У вас появилось новогоднее настроение?😀', reply_markup=christmas_keyboard)
#
#        await c.message.answer('викторина началась!')
#        await c.message.answer('Вы дарите подарки?', reply_markup=christmas_keyboard)
#
#    elif c.data == 'exit':
#        await bot.answer_callback_query(c.id, text='')
#        await bot.edit_message_text(chat_id=c.message.chat.id, message_id=c.message.message_id,
#                                    text='Спасибо за участие, викторина закончена!', reply_markup=end_vic_keyboard)
