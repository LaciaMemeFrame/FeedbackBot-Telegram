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
    users = types.KeyboardButton(u'Статистика 1 пользователи')
    commands = types.KeyboardButton(u'Статистика 1 команды')
    pussy = types.KeyboardButton(u'🐈pussy')
    pidor = types.KeyboardButton(u'🏳️‍🌈pidor_stat')
    help = types.KeyboardButton(u'🆘Помощь')
    allstatistics = types.KeyboardButton(u'Статистика 1 пользователи команды')
    keyboard.row(pussy, pidor, help)
    keyboard.add(users, commands, allstatistics)
    tg_analytic.statistics (m.chat.id, m.text)
    bot.send_message(m.from_user.id, u'Добро пожаловать', reply_markup=keyboard)

@bot.inline_handler(lambda query: query.query == u'pussy')
def query_photo(inline_query):
    try:
        r = types.InlineQueryResultPhoto('1',
                                          'https://sun9-26.userapi.com/c855328/v855328338/241690/QVaGg9fPkuk.jpg',
                                          'https://sun9-26.userapi.com/c855328/v855328338/241690/QVaGg9fPkuk.jpg')
        bot.answer_inline_query(inline_query.id, [r], cache_time=1)
    except Exception as e:
        print(e)     

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
 #if message.text[:10] == '/помощь' or message.text[:20] == '/help@pixelsetup_bot' or message.text[:30] == '/help':
   #tg_analytic.statistics (message.chat.id, message.text)
   #bot.send_message(message.chat.id, u"Доступные команды: /новости /информация /помощь")
 if message.text == u'/помощь' or message.text == u'/help@pixelsetup_bot' or message.text == u'/help' or message.text == u'🆘Помощь':
   tg_analytic.statistics (message.chat.id, message.text)
   bot.send_message(message.chat.id, u"Доступные команды: /киски /помощь")  
 #if message.text[:40] == u'/новости' or message.text[:50] == u'/news@pixelsetup_bot' or message.text[:60] == u'/news':
   #tg_analytic.statistics (message.chat.id, message.text)
   #bot.send_message(message.chat.id, u"IP SAMP RP сервера сменился 34.91.233.9:7777!")  
 #if message.text[:70] == u'/информация' or message.text[:80] == u'/info@pixelsetup_bot' or message.text[:90] == u'/info':
   #tg_analytic.statistics (message.chat.id, message.text)
   #bot.send_message(message.chat.id, u"Открыт SAMP RP Сервер! IP: 34.91.233.9:7777 Полезные ссылки: Наш сайт - laciamemeframe.space (Сайт создателя проекта, так как сайт самого сервера находится в разработке). Форум - В разработке, Группа Вконтакте - https://vk.com/pixsetup, Свободная группа Вконтакте - В разработке. IP: 34.91.233.9:7777")
 if message.text == u'/pidor_stat' or message.text == u'/pidor_stat@pixelsetup_bot' or message.text == u'🏳️‍🌈pidor_stat':
    tg_analytic.statistics (message.chat.id, message.text)
    bot.send_message(message.chat.id, u"привет пидор")
 if message.text == u'/киски' or message.text == u'/pussy' or message.text == u'/pussy@pixelsetup_bot' or message.text == u'🐈pussy' or message.text == u'киски':  
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
 #elif message.text =="/help":
   #bot.send_message(message.from_user.id, "Доступные команды  /news и /info")
 #else:
    #bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)
