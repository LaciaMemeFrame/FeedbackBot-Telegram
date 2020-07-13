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
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline.jpg')      
        r2 = types.InlineQueryResultPhoto('2',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline1.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline1.jpg')     
        r3 = types.InlineQueryResultPhoto('3',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline2.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline2.jpg')     
        r4 = types.InlineQueryResultPhoto('4',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline3.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline3.jpg')    
        r5 = types.InlineQueryResultPhoto('5',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline4.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline4.jpg')
        r6 = types.InlineQueryResultPhoto('6',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline5.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline5.jpg')
        r7 = types.InlineQueryResultPhoto('7',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline6.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline6.jpg') 
        r8 = types.InlineQueryResultPhoto('8',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline7.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline7.jpg')                                   

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
