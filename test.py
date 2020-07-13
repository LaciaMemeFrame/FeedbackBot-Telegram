# -*- coding: utf-8 -*- 
import telebot
from telebot import types
import logging
import requests
import tg_analytic

bot = telebot.TeleBot('токен');

@bot.message_handler(commands=['start'])
def handle_grammar2(m):
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    pussy = types.KeyboardButton(u'🐈pussy')
    keyboard.row(pussy)
    tg_analytic.statistics (m.chat.id, m.text)
    bot.send_message(m.from_user.id, u'Добро пожаловать', reply_markup=keyboard)

@bot.inline_handler(lambda query: query.query == u'pussy')
def query_photo(inline_query):
    try:
        r = types.InlineQueryResultPhoto('1',
                                          'https://sun9-46.userapi.com/c206716/v206716770/166429/UyOS_SNoRDM.jpg',
                                          'https://sun9-46.userapi.com/c206716/v206716770/166429/UyOS_SNoRDM.jpg')      
        r2 = types.InlineQueryResultPhoto('2',
                                          'https://sun9-53.userapi.com/c206720/v206720770/163a59/Y8bseTZwT5A.jpg',
                                          'https://sun9-53.userapi.com/c206720/v206720770/163a59/Y8bseTZwT5A.jpg')     
        r3 = types.InlineQueryResultPhoto('3',
                                          'https://sun9-13.userapi.com/c206720/v206720770/163a7e/LzBLvtcIrf4.jpg',
                                          'https://sun9-13.userapi.com/c206720/v206720770/163a7e/LzBLvtcIrf4.jpg')     
        r4 = types.InlineQueryResultPhoto('4',
                                          'https://sun9-35.userapi.com/c206720/v206720770/163a92/m2t8oBngAHs.jpg',
                                          'https://sun9-35.userapi.com/c206720/v206720770/163a92/m2t8oBngAHs.jpg')    
        r5 = types.InlineQueryResultPhoto('5',
                                          'https://sun9-71.userapi.com/c206720/v206720770/163a99/vh64Re-hvtU.jpg',
                                          'https://sun9-71.userapi.com/c206720/v206720770/163a99/vh64Re-hvtU.jpg')
        r6 = types.InlineQueryResultPhoto('6',
                                          'https://sun9-71.userapi.com/c206720/v206720770/163aa0/Dx7GUv0hy84.jpg',
                                          'https://sun9-71.userapi.com/c206720/v206720770/163aa0/Dx7GUv0hy84.jpg')
        r7 = types.InlineQueryResultPhoto('7',
                                          'https://sun9-72.userapi.com/c206720/v206720770/163aa7/0IsuVtROia4.jpg',
                                          'https://sun9-72.userapi.com/c206720/v206720770/163aa7/0IsuVtROia4.jpg') 
        r8 = types.InlineQueryResultPhoto('8',
                                          'https://sun9-71.userapi.com/c206720/v206720770/163ab0/4YXzj0vXVWU.jpg',
                                          'https://sun9-71.userapi.com/c206720/v206720770/163ab0/4YXzj0vXVWU.jpg')                                   

        bot.answer_inline_query(inline_query.id, [r, r2, r3, r4, r5, r6, r7, r8], cache_time=1)
    except Exception as e:
        print(e)     

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
 if message.text == u'/pussy' or message.text == u'/pussy@pixelsetup_bot' or message.text == u'🐈pussy':  
    url = 'https://api.thecatapi.com/v1/images/search'
    r = requests.get(url, allow_redirects=True)
    r.headers['x-api-key'] = 'токен'
    json = r.json()
    for j in json:
      kittyurl = j['url']
      rs = requests.get(kittyurl, allow_redirects=True)
      open('kotik.jpg', 'wb').write(rs.content)
      tg_analytic.statistics (message.chat.id, message.text)
      bot.send_photo(message. chat.id, open("kotik.jpg","rb"))
 if message.text[:10] == u'статистика' or message.text[:10] == u'Статистика':
        st = message.text.split(' ')
        if 'txt' in st or 'тхт' in st:
            tg_analytic.analysis(st,message.chat.id)
            with open('%s.txt' %message.chat.id ,'r',encoding='UTF-8') as file:
                tg_analytic.statistics (message.chat.id, message.text)
                bot.send_document(message.chat.id,file)
                tg_analytic.remove(message.chat.id)
        else:
            messages = tg_analytic.analysis(st,message.chat.id)
            tg_analytic.statistics (message.chat.id, message.text)
            bot.send_message(message.chat.id, messages)         

bot.polling(none_stop=True, interval=0)
