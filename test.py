# -*- coding: utf-8 -*- 
import telebot
from telebot import TeleBot
import logging
import requests
import tg_analytic
import nekos
from time import sleep
from PIL import Image 

TOKEN = 'токен'

chat_ids_file = 'chat_ids.txt'

ADMIN_CHAT_ID = 503174223
users_amount = [0]
types = telebot.types
bot = TeleBot(TOKEN)

def save_chat_id(chat_id):
	chat_id = str(chat_id)
	with open(chat_ids_file,"a+") as ids_file:
		ids_file.seek(0)

		ids_list = [line.split('\n')[0] for line in ids_file]

		if chat_id not in ids_list:
			ids_file.write(f'{chat_id}\n')
			ids_list.append(chat_id)
			print(f'New chat_id saved: {chat_id}')
		else:
			print(f'chat_id {chat_id} is already saved')
		users_amount[0] = len(ids_list)
	return


def send_message_users(message):

	def send_message(chat_id):
		data = {
			'chat_id': chat_id,
			'text': message
		}
		response = requests.post(f'https://api.telegram.org/bot{TOKEN}/sendMessage', data=data)

	with open(chat_ids_file, "r") as ids_file:
		ids_list = [line.split('\n')[0] for line in ids_file]

	[send_message(chat_id) for chat_id in ids_list]
	bot.send_message(ADMIN_CHAT_ID, f"сообщение успешно отправлено всем ({users_amount[0]}) пользователям бота!")

@bot.message_handler(commands=['start'])
def handle_grammar2(m):
    tg_analytic.statistics (m.chat.id, m.text)
    bot.send_message(m.from_user.id, f"<b>Добро пожаловать, {m.from_user.first_name}</b>", parse_mode='HTML', disable_notification=True)
    save_chat_id(m.chat.id)
    sleep(0.01)

@bot.inline_handler(lambda query: query.query == u'kitty')
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

@bot.inline_handler(lambda query: query.query == u'dogs')
def query_photo(inline_query):
    try:
        r = types.InlineQueryResultPhoto('1',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inline.jpg')      
        r2 = types.InlineQueryResultPhoto('2',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs1.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs1.jpg')     
        r3 = types.InlineQueryResultPhoto('3',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs2.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs2.jpg')     
        r4 = types.InlineQueryResultPhoto('4',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs3.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs3.jpg')    
        r5 = types.InlineQueryResultPhoto('5',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs4.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs4.jpg')
        r6 = types.InlineQueryResultPhoto('6',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs5.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs5.jpg')
        r7 = types.InlineQueryResultPhoto('7',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs6.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/inlinedogs6.jpg')                                   
                                          
        bot.answer_inline_query(inline_query.id, [r, r2, r3, r4, r5, r6, r7], cache_time=1)
    except Exception as e:
        print(e)     

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
 chat_id = int(message.chat.id)
 text = message.text
 if message.text == u'/dogs' or message.text == u'/dogs@pixelsetup_bot':  
    url = 'https://api.thedogapi.com/v1/images/search'
    r = requests.get(url, allow_redirects=True)
    r.headers['x-api-key'] = 'токен'
    json = r.json()
    for j in json:
      dogsurl = j['url']
      rs = requests.get(dogsurl, allow_redirects=True)
      open('dogs.jpg', 'wb').write(rs.content)
      print("Фото отправленно!")
      tg_analytic.statistics (message.chat.id, message.text)
      bot.send_photo(message. chat.id, open("dogs.jpg","rb"), disable_notification=True)
      sleep(5)

 if message.text == u'/kitty' or message.text == u'/kitty@pixelsetup_bot':  
    url = 'https://api.thecatapi.com/v1/images/search'
    r = requests.get(url, allow_redirects=True)
    r.headers['x-api-key'] = 'токен'
    json = r.json()
    for j in json:
      kittyurl = j['url']
      rs = requests.get(kittyurl, allow_redirects=True)
      open('kotik.jpg', 'wb').write(rs.content)
      print("Фото отправленно!")
      tg_analytic.statistics (message.chat.id, message.text)
      bot.send_photo(message. chat.id, open("kotik.jpg","rb"), disable_notification=True)
      sleep(5)

 if message.text == u'/help' or message.text == u'/help@pixelsetup_bot':
      print("Команды бота!")
      tg_analytic.statistics (message.chat.id, message.text)
      bot.send_message(message.chat.id, f"<b>Все команды бота!\n/help - Все команды бота\n/dogs - Собачки с thedogapi.com\n/kitty - Котики с thecatapi.com\n/wallpaper - Аниме обои с nekos.life</b>", parse_mode='HTML', disable_notification=True)
      sleep(5)

 if message.text == u'/wallpaper' or message.text == u'/wallpaper@pixelsetup_bot':
      url = 'https://nekos.life/api/v2/img/wallpaper'
      r = requests.get(url, allow_redirects=True)
      r.headers
      json = r.json()
      pussyurl = json['url']
      rs = requests.get(pussyurl, allow_redirects=True)
      open('wallpaper.png', 'wb').write(rs.content)
      print("Обои отправленны!")
      tg_analytic.statistics (message.chat.id, message.text)
      bot.send_photo(message.chat.id, open("wallpaper.png", "rb"), disable_notification=True)
      sleep(3)
      bot.send_document(message.chat.id, open("wallpaper.png","rb"), disable_notification=True)
      sleep(3)
      bot.send_message(message.chat.id, f"<b>Обои можно запрашивать раз в 10 секунд!</b>", parse_mode='HTML', disable_notification=True)
      sleep(10)
          
 elif 'Lacia' in text and chat_id == ADMIN_CHAT_ID:
        st = message.text.split(' ')
        if 'txt' in st or 'тхт' in st:
            tg_analytic.analysis(st,message.chat.id)
            with open('%s.txt' %message.chat.id ,'r',encoding='UTF-8') as file:
                print("Показ статистики!")
                tg_analytic.statistics (message.chat.id, message.text)
                bot.send_document(message.chat.id,file, disable_notification=True)
                tg_analytic.remove(message.chat.id)
        else:
            messages = tg_analytic.analysis(st,message.chat.id)
            print("Показ статистики!")
            tg_analytic.statistics (message.chat.id, message.text)
            bot.send_message(message.chat.id, messages, disable_notification=True)

 elif 'Статистика'in text and chat_id == ADMIN_CHAT_ID:
		bot.send_message(chat_id, f"<b>Статистика пользователей!\nПользователей: {users_amount[0]}</b>", parse_mode='HTML', disable_notification=True)              
  
 elif 'РАЗОСЛАТЬ: ' in text and chat_id == ADMIN_CHAT_ID:
    msg = text.replace("РАЗОСЛАТЬ: ", "")
    send_message_users(msg)            

bot.polling(none_stop=True, interval=0)
