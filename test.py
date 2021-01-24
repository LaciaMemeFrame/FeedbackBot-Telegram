# -*- coding: utf-8 -*- 
import telebot
from telebot import TeleBot
import logging
import requests
import nekos
from time import sleep
from PIL import Image 

TOKEN = 'токен'

chat_ids_file = 'chat_ids.txt'

ADMIN_CHAT_ID = [id]
ADMINS = id
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
		response = requests.post(f'http://laciamemeframe.space:49999/bot{TOKEN}/sendMessage', data=data)

	with open(chat_ids_file, "r") as ids_file:
		ids_list = [line.split('\n')[0] for line in ids_file]

	[send_message(chat_id) for chat_id in ids_list]
	bot.send_message(ADMINS, f"<b>сообщение успешно отправлено всем ({users_amount[0]}) пользователям бота!</b>", parse_mode='HTML', disable_notification=True)

@bot.message_handler(commands=['start'])
def handle_grammar2(m):
    bot.send_message(m.from_user.id, f"<b>Добро пожаловать, {m.from_user.first_name}</b>", parse_mode='HTML', disable_notification=True)
    save_chat_id(m.chat.id)

@bot.message_handler(commands=['kitty'])
def kitty(message):
    url = 'https://api.thecatapi.com/v1/images/search'
    r = requests.get(url, allow_redirects=True)
    r.headers['x-api-key'] = 'токен'
    json = r.json()
    for j in json:
      kittyurl = j['url']
      rs = requests.get(kittyurl, allow_redirects=True)
      open('kotik.jpg', 'wb').write(rs.content)
      print("Фото отправленно!")
      bot.send_photo(message. chat.id, open("kotik.jpg","rb"), disable_notification=True)

@bot.message_handler(commands=['dogs'])
def dogs(message):
    url = 'https://api.thedogapi.com/v1/images/search'
    r = requests.get(url, allow_redirects=True)
    r.headers['x-api-key'] = 'токен'
    json = r.json()
    for j in json:
      dogsurl = j['url']
      rs = requests.get(dogsurl, allow_redirects=True)
      open('dogs.jpg', 'wb').write(rs.content)
      print("Фото отправленно!")
      bot.send_photo(message. chat.id, open("dogs.jpg","rb"), disable_notification=True)

@bot.message_handler(commands=['help'])
def commands(message):
    print("Команды бота!")
    bot.send_message(message.chat.id, f"<b>Все команды бота!\n/help - Все команды бота\n/dogs - Собачки с thedogapi.com\n/kitty - Котики с thecatapi.com\n/wallpaper - Аниме обои с nekos.life</b>", parse_mode='HTML', disable_notification=True)

@bot.message_handler(commands=['wallpaper'])
def wallpaper(message):
      url = 'https://nekos.life/api/v2/img/wallpaper'
      r = requests.get(url, allow_redirects=True)
      r.headers
      json = r.json()
      pussyurl = json['url']
      rs = requests.get(pussyurl, allow_redirects=True)
      open('wallpaper.png', 'wb').write(rs.content)
      print("Обои отправленны!")
      bot.send_photo(message.chat.id, open("wallpaper.png", "rb"), disable_notification=True)
      bot.send_document(message.chat.id, open("wallpaper.png","rb"), disable_notification=True)

@bot.message_handler(commands=['ads'])
def ads(message):
    chat_id = int(message.chat.id)
    text = message.text
    if message.chat.id in ADMIN_CHAT_ID: 
        msg = text.replace("/ads ", "")
        send_message_users(msg) 

@bot.message_handler(commands=['stat'])
def stat(message):
    chat_id = int(message.chat.id)
    text = message.text
    if message.chat.id in ADMIN_CHAT_ID:
        bot.send_message(chat_id, f"<b>Статистика пользователей!\nПользователей: {users_amount[0]}</b>", parse_mode='HTML', disable_notification=True)  

@bot.inline_handler(lambda query: query.query == u'kitty')
def query_photo(inline_query):
    try:
        r = types.InlineQueryResultPhoto('1',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline.jpg')      
        r2 = types.InlineQueryResultPhoto('2',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline1.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline1.jpg')     
        r3 = types.InlineQueryResultPhoto('3',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline2.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline2.jpg')     
        r4 = types.InlineQueryResultPhoto('4',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline3.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline3.jpg')    
        r5 = types.InlineQueryResultPhoto('5',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline4.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline4.jpg')
        r6 = types.InlineQueryResultPhoto('6',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline5.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline5.jpg')
        r7 = types.InlineQueryResultPhoto('7',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline6.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline6.jpg') 
        r8 = types.InlineQueryResultPhoto('8',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline7.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline7.jpg')                                   

        bot.answer_inline_query(inline_query.id, [r, r2, r3, r4, r5, r6, r7, r8], cache_time=1)
    except Exception as e:
        print(e)     

@bot.inline_handler(lambda query: query.query == u'dogs')
def query_photo(inline_query):
    try:
        r = types.InlineQueryResultPhoto('1',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inline.jpg')      
        r2 = types.InlineQueryResultPhoto('2',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs1.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs1.jpg')     
        r3 = types.InlineQueryResultPhoto('3',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs2.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs2.jpg')     
        r4 = types.InlineQueryResultPhoto('4',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs3.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs3.jpg')    
        r5 = types.InlineQueryResultPhoto('5',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs4.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs4.jpg')
        r6 = types.InlineQueryResultPhoto('6',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs5.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs5.jpg')
        r7 = types.InlineQueryResultPhoto('7',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs6.jpg',
                                          'https://raw.githubusercontent.com/LaciaMemeFrame/ChatBot-Telegram/master/picture/inlinedogs6.jpg')                                   
                                          
        bot.answer_inline_query(inline_query.id, [r, r2, r3, r4, r5, r6, r7], cache_time=1)
    except Exception as e:
        print(e)     

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
 text = message.text
 url = f'https://duckduckgo.com/?q={text}&kp=-1&kl=ru-ru'
 try:
        response = requests.get(
            f'{url}',
            params={
                'format': 'json'
            }).json()
        text = response.get('AbstractText')
        related_topics_text = response.get('RelatedTopics')[0]['Text']
        related_topics_full_link = response.get('RelatedTopics')[0]['FirstURL']
 except:
        bot.send_message(message.from_user.id, "<b>Результатов не найдено :(</b>", parse_mode='HTML')
        return
 if not text:
            bot.send_message(message.from_user.id, f'<b>{related_topics_text}</b>\n\n{related_topics_full_link}', parse_mode='HTML')
            bot.send_message(ADMINS, f"<b>Тут кто-то что-то искал:</b> {related_topics_full_link}\n\n<b>Исходная ссылка:</b> {url}", parse_mode='HTML', disable_notification=True)

bot.polling(none_stop=True, interval=0)
