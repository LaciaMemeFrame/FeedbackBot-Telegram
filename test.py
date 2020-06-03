# -*- coding: utf-8 -*- 
import telebot;
import logging;
import requests;

bot = telebot.TeleBot('токен');

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
 if message.text ==u"/помощь":
   bot.send_message(message.chat.id, u"Доступные команды: /новости /информация /помощь")
 if message.text ==u"/help@pixelsetup_bot":
   bot.send_message(message.chat.id, u"Доступные команды: /новости /информация /помощь") 
 if message.text ==u"/help":
   bot.send_message(message.chat.id, u"Доступные команды: /новости /информация /помощь")   
 if message.text ==u"/новости":
   bot.send_message(message.chat.id, u"IP SAMP RP сервера сменился 34.91.233.9:7777!")
 if message.text ==u"/news@pixelsetup_bot":
   bot.send_message(message.chat.id, u"IP SAMP RP сервера сменился 34.91.233.9:7777!")
 if message.text ==u"/news":
   bot.send_message(message.chat.id, u"IP SAMP RP сервера сменился 34.91.233.9:7777!")   
 if message.text ==u"/информация":
    bot.send_message(message.chat.id, u"Открыт SAMP RP Сервер! IP: 34.91.233.9:7777 Полезные ссылки: Наш сайт - laciamemeframe.space (Сайт создателя проекта, так как сайт самого сервера находится в разработке). Форум - В разработке, Группа Вконтакте - https://vk.com/pixsetup, Свободная группа Вконтакте - В разработке. IP: 34.91.233.9:7777")
 if message.text ==u"/info@pixelsetup_bot":
    bot.send_message(message.chat.id, u"Открыт SAMP RP Сервер! IP: 34.91.233.9:7777 Полезные ссылки: Наш сайт - laciamemeframe.space (Сайт создателя проекта, так как сайт самого сервера находится в разработке). Форум - В разработке, Группа Вконтакте - https://vk.com/pixsetup, Свободная группа Вконтакте - В разработке. IP: 34.91.233.9:7777")
 if message.text ==u"/info":
    bot.send_message(message.chat.id, u"Открыт SAMP RP Сервер! IP: 34.91.233.9:7777 Полезные ссылки: Наш сайт - laciamemeframe.space (Сайт создателя проекта, так как сайт самого сервера находится в разработке). Форум - В разработке, Группа Вконтакте - https://vk.com/pixsetup, Свободная группа Вконтакте - В разработке. IP: 34.91.233.9:7777")       
 if message.text ==u"/pidor_stat@pixelsetup_bot": 
    bot.send_message(message.chat.id, u"привет пидор")
 if message.text ==u"/pidor_stat": 
    bot.send_message(message.chat.id, u"привет пидор")
 if message.text ==u"/киски":  
    url = 'https://api.thecatapi.com/v1/images/search'
    r = requests.get(url, allow_redirects=True)
    r.headers['x-api-key'] = 'токен'
    json = r.json()
    for j in json:
      kittyurl = j['url']
      rs = requests.get(kittyurl, allow_redirects=True)
      open('kotik.jpg', 'wb').write(rs.content)
      bot.send_photo(message. chat.id, open("kotik.jpg","rb"))
 if message.text ==u"/pussy":  
    url = 'https://api.thecatapi.com/v1/images/search'
    r = requests.get(url, allow_redirects=True)
    r.headers['x-api-key'] = 'токен'
    json = r.json()
    for j in json:
      kittyurl = j['url']
      rs = requests.get(kittyurl, allow_redirects=True)
      open('kotik.jpg', 'wb').write(rs.content)
      bot.send_photo(message. chat.id, open("kotik.jpg","rb"))
 if message.text ==u"/pussy@pixelsetup_bot":  
    url = 'https://api.thecatapi.com/v1/images/search'
    r = requests.get(url, allow_redirects=True)
    r.headers['x-api-key'] = 'токен'
    json = r.json()
    for j in json:
      kittyurl = j['url']
      rs = requests.get(kittyurl, allow_redirects=True)
      open('kotik.jpg', 'wb').write(rs.content)
      bot.send_photo(message. chat.id, open("kotik.jpg","rb"))        
 #elif message.text =="/help":
   #bot.send_message(message.from_user.id, "Доступные команды  /news и /info")
 #else:
    #bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
bot.polling(none_stop=True, interval=0)
