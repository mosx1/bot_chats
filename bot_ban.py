import telebot
import json
import requests
import time
import threading, time
from telebot import types
from datetime import datetime
import pytz
import logging
from pymystem3 import Mystem

token = '1727195415:AAHuFPGxae30xXpGe8feL6sdsy5pb0m5rAU' #test
#token = '5039865293:AAHUtyFYxOYrkFppyKJGQhAGXaatPjCh4-8'

bot = telebot.TeleBot(token)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def updateConnect():
    while True:
        api = requests.post(f"https://api.telegram.org/bot/{token}/getUpdates".format(token))
        time.sleep(10)


class Censure:


    def __init__(self):
        self.chat_filter_mat = []
        self.mat_list = ["хуй", "пизд", "залупа", "ебаный", "ебать", "ебал", " бля ", "ебать", "ебать", "ебут", "еблан", "ебнул", "шлюха", "гандон", "чурка", "хуесос", "уебище", "блядст", "пидр", "пидор", "шлюх", "пиздос"]
        self.escaped_characters = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
        self.taxi_button_list = {} #для обьектов такси
        self.all_message = "" #реклама
        self.admin_chat = ""
        self.channel_id = "" #-1001158441558 - id новостей ЮБ
        self.public = {}
        self.public_info_user = {}
        self.message_text_user_info = ""
        self.message_caption_user_info = ""
        self.message_text = ""
        self.message_caption = ""

    def filter_mat(self, message):
        i = 0
        message_text = str(message.text).lower()
        for mat in self.mat_list:
            if mat in message_text:
                #if message.chat.id in self.chat_filter_mat:
                message_text = message_text.replace(mat, "*" * len(mat))
                i += 1
        if i > 0 :
            bot.delete_message(chat_id = message.chat.id, message_id= message.id)
            text = "Пользователь [" + self.formating_text_markdownv2(str(message.from_user.first_name)) + self.formating_text_markdownv2(str((message.from_user.last_name or ""))) + "](tg://user?id\=" + str(message.from_user.id) + ") писал: \n " + self.formating_text_markdownv2(message_text) + censure_filter.all_message
            stat.add_qty_message()
            bot.send_message(message.chat.id, text, parse_mode="MarkdownV2")
            logging.info("Сработал фильтр мата на пользователя " + str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")))
    
    
    def formating_text_markdownv2(self, message_text):
        for escaped_characters in self.escaped_characters:
            try:
                if escaped_characters in message_text:
                    message_text = str(message_text).replace(escaped_characters, "\\" + escaped_characters)
            except TypeError:
                logging.error("Переданное сообщение не является текстом")
                break
        return message_text
    

    def offer_news(self, message):
        key = types.InlineKeyboardMarkup()
        botton_yes_not_user = types.InlineKeyboardButton(text="Опубликовать", callback_data='{"key": "botton_yes_not_user", "id":"' + str(message.id) + '"}')
        botton_yes_user = types.InlineKeyboardButton(text="Обупликовать с автором", callback_data='{"key": "botton_yes_user", "id":"' + str(message.id) + '"}')
        botton_no = types.InlineKeyboardButton(text="Удалить", callback_data='{"key": "botton_not_public", "id":"' + str(message.id) + '"}')
        key.add(botton_yes_user)
        key.add(botton_yes_not_user,botton_no)
        self.public[message.id] = message
        user_info = "\n\nАвтор: [" + str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + "](tg://user?id\=" + str(message.from_user.id) + ")"
        if message.text != None:
            self.message_text = self.formating_text_markdownv2(message.text)
            if self.message_text == None:
                self.message_text_user_info = user_info
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил пост")
            elif self.test_commercia(self.message_text) == True:
                self.message_text_user_info = self.message_text + user_info + "\n\n#реклама"
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил рекламный пост")
            else:
                self.message_text_user_info = self.message_text + user_info
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил пост")
        else:
            self.message_caption = self.formating_text_markdownv2(message.caption)
            if self.message_caption == None:
                self.message_caption_user_info = user_info
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил пост")
            elif self.test_commercia(self.message_caption) == True:
                self.message_caption_user_info = self.message_caption + user_info + "\n\n#реклама"
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил рекламный пост")
            else:
                self.message_caption_user_info = self.message_caption + user_info
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил пост")

        try:
            self.public_info_user[message.id] = bot.send_video(self.admin_chat, video=self.public[message.id].video.file_id, caption=self.message_caption_user_info, reply_markup=key, parse_mode="MarkdownV2")
            logging.info("Предложена публикация пользователем: " + str(message.from_user.first_name) + " " + str(message.from_user.last_name))
            return
        except Exception:
            pass
        try:
            self.public_info_user[message.id] = bot.send_photo(self.admin_chat, photo=self.public[message.id].photo[0].file_id, caption=self.message_caption_user_info, reply_markup=key, parse_mode="MarkdownV2")
        except Exception:
            if message.text != "/start":
                self.public_info_user[message.id] = bot.send_message(self.admin_chat, self.message_text_user_info, reply_markup=key, parse_mode="MarkdownV2")
        logging.info("Предложена публикация пользователем: " + str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")))


    def public_news(self, info_user, id):
        if info_user == True:
            caption = self.message_caption_user_info
            text = self.message_text_user_info
        elif info_user == False:
            caption = self.message_caption
            text = self.message_text
        elif info_user == None:
            bot.delete_message(chat_id = str(self.admin_chat), message_id = self.public_info_user[id].id)
            return
        try:
            bot.send_video(self.channel_id, video=self.public_info_user[id].video.file_id, caption=caption, parse_mode="MarkdownV2")
        except Exception:
            pass
        try:
            bot.send_photo(self.channel_id, photo=self.public_info_user[id].photo[0].file_id, caption=caption, parse_mode="MarkdownV2")
        except Exception:
            bot.send_message(self.channel_id, text, parse_mode="MarkdownV2")
        logging.info("Публикация одобрена")
        bot.delete_message(chat_id = str(self.admin_chat), message_id = self.public_info_user[id].id)
        del self.public_info_user[id]
        del self.public[id]

    def spam_message(self, message):
        list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
        if message.from_user.id not in list_admin:
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            old_message = bot.send_message(message.chat.id, "Вы не администратор. Действите запрещено")
            time.sleep(5)
            bot.delete_message(chat_id=message.chat.id, message_id=old_message.id)
            return
        arr_message = message.text.split(" ", 1)
        if len(arr_message) != 2:
            old_message = bot.send_message(message.chat.id, """Напшите сообщение в формате "/spam Тут ваш текст". """)
            time.sleep(5)
            bot.delete_message(chat_id=message.chat.id, message_id=old_message.id)
        else:
            logging.info("Запущена рассылка для чатов пользователем " + str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")))
            self.spam_text = arr_message[1]
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            spam_work_tread = threading.Thread(target = self.spam_work)
            spam_work_tread.start()
    

    def spam_work(self):
        for i in user_chat_kik[0].list_chats.keys():
            bot.send_message(i, self.spam_text + censure_filter.all_message)
    

    def test_commercia(message):
        m = Mystem()
        message_text = m.lemmatize(message.text)
        list_commercia = ["услуга", "подключение", "производство", "продажа"]
        for text_commercia in list_commercia:
            if text_commercia in message_text:
                return "Внимание, в вашем сообщении найдены признаки коммерческой рекламы. Для размещения рекламы в нашем канале обратитесь к [Максиму](tg://user?id\=474425142)"
        return "Ваша публикация отправлена админам. Вероятно скоро они её опубликуют."

                  
thread = threading.Thread(target = updateConnect)
thread.start()


class Kik_user:

    def __init__(self):
        self.qty_yes = 0
        self.qty_no = 0
        self.useridgolos = 0
        self.list_chats = {}
        self.list_user = []
        self.initiator = ""
        self.username = ""
        self.check_chats = []
        self.id = 0


    def start_kik(self, message):
        self.chat_id = message.chat.id
        self.chat_title = message.chat.title
        bot.delete_message(chat_id=self.chat_id, message_id=message.id)
        try:
            self.userid = message.reply_to_message.from_user.id
            self.list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
            if self.userid in self.list_admin:
                stat.add_qty_message()
                bot.send_message(self.chat_id, "Невозможно кикнуть администратора группы" + censure_filter.all_message, parse_mode="MarkdownV2")
                logging.info(self.initiator + " пытался кикнуть администратора")
                return False
        except Exception as e:
            stat.add_qty_message()
            bot.send_message(self.chat_id, "Для того чтоб забанить нужно ответить на сообщение пользователя\." + censure_filter.all_message, parse_mode="MarkdownV2")
            logging.error(self.initiator + " вызвал команду кик не ответив на сообщение, error: " + e)
            return False
        else:
            self.username = censure_filter.formating_text_markdownv2(str(message.reply_to_message.from_user.first_name) + " " + str((message.reply_to_message.from_user.last_name or "")))
            self.list_yes = []
            self.list_no = []
            self.list_admin = []
            self.initiator = message.from_user.id
            self.del_message_id = str(message.reply_to_message.id)
            #self.survey()

    def survey(self, kik_id, call=None, voice=None):
        if (call != None) and (call.from_user.id in self.list_no + self.list_yes):
            bot.answer_callback_query(callback_query_id=call.id, text='Вы уже проголосовали')
        else:
            if voice == False:
                self.list_no.append(int(call.from_user.id))
            elif voice == True:
                self.list_yes.append(int(call.from_user.id))
            status_chat_user = bot.get_chat_member(self.chat_id, self.userid)
            if status_chat_user.status == "left" or status_chat_user.status == "kicked":
                text = "Пользователь [" + censure_filter.formating_text_markdownv2(self.username) + "](tg://user?id\=" + str(self.userid) + ") покинул чат, либо его кикнул администратор\. Голосование окончено\."
                try:
                    bot.edit_message_text(chat_id=self.chat_id, message_id=self.survey_message.id, text=text, parse_mode="MarkdownV2")
                except AttributeError:
                    bot.send_message(self.chat_id, text, parse_mode="MarkdownV2")
                return
            if len(self.list_yes) >= 10:
                bot.kick_chat_member(self.chat_id, self.userid)
                stat.add_qty_message()
                bot.edit_message_text(chat_id=self.chat_id, message_id=self.survey_message.id, text="По решению соседей из " + censure_filter.formating_text_markdownv2(self.chat_title) +  " кикнут [" + censure_filter.formating_text_markdownv2(self.username) + "](tg://user?id\=" + str(self.userid) + ")" + censure_filter.all_message, parse_mode="MarkdownV2")
                logging.info("Пользователя " + self.username + " кикнули из чата " + self.chat_title + " голосованием.")
                return "end_survey"
            elif len(self.list_no) >= 10:
                stat.add_qty_message()
                bot.edit_message_text(chat_id=self.chat_id, message_id=self.survey_message.id, text="По решению соседей [" + censure_filter.formating_text_markdownv2(self.username) + "](tg://user?id\=" + str(self.userid) + ") остается в чате\." + censure_filter.all_message, parse_mode="MarkdownV2")
                logging.info("Пользователя " + self.username + " не кикнули из чата " + self.chat_title + " голосованием.")
                return "end_survey"
            survey_keyvboard = types.InlineKeyboardMarkup()
            Botton_yes = types.InlineKeyboardButton(text = f"Да ({len(self.list_yes)})", callback_data='{"key": "kik_yes", "id": "' + str(kik_id) + '"}')
            Botton_no = types.InlineKeyboardButton(text = f"Нет ({len(self.list_no)})", callback_data='{"key": "kik_no", "id": "' + str(kik_id) + '"}')
            survey_keyvboard.add(Botton_yes, Botton_no)
            kik_text = "Кикнуть [" + censure_filter.formating_text_markdownv2(self.username)+ "](tg://user?id\=" + str(self.userid) + ") \?"
            if len(self.list_yes) == 0 and len(self.list_no) == 0:
                self.survey_message = bot.send_message(self.chat_id, kik_text, reply_markup=survey_keyvboard, parse_mode="MarkdownV2", timeout=2)
            else:
                bot.edit_message_text(chat_id=self.chat_id, message_id=self.survey_message.id, text=kik_text, reply_markup=survey_keyvboard, parse_mode="MarkdownV2")


    def armagedon(self, user=None):
        if user == None:
            user = self.userid
        keyword_ban = types.InlineKeyboardMarkup()
        Botton_all_chats = types.InlineKeyboardButton(text = "Удалить из всех чатов", callback_data='{"key": "ban_all", "chat": "all"}')
        keyword_ban.add(Botton_all_chats)
        for id in self.list_chats.keys():
            try:
                status_chat_user = bot.get_chat_member(id, user)
                if "left, kicked".count(status_chat_user.status) != 0:
                    continue
                title = self.list_chats[id]["title"]
                Botton = types.InlineKeyboardButton(text = title, callback_data='{"key": "ban_all", "chat":' + str(id) + '}')
                keyword_ban.add(Botton)
            except Exception:
                logging.error("Пользователь не смог вызвать команду армагедон.")
        bot.send_message(self.chat_id, "Выберите в каком чате вы хотите заблокировать пользователя [" + str(self.username) + "](tg://user?id\=" + str(self.userid) + "):", reply_markup=keyword_ban, parse_mode="MarkdownV2")
    
    
    def ban_user(self, chat_id, user=None):
        if chat_id == "all":
            for chat in self.list_chats.keys():
                try:
                    bot.ban_chat_member(chat, self.userid)
                except Exception:
                    pass
            stat.add_qty_message()
            bot.send_message(self.chat_id, "[" + str(self.username) + "](tg://user?id\=" + str(self.userid) + ") забанен из всех чатов" + censure_filter.all_message, parse_mode="MarkdownV2")
            logging.info(self.username + " забанен из всех чатов.")
        else:
            bot.ban_chat_member(chat_id, self.userid)
            stat.add_qty_message()
            bot.send_message(self.chat_id, "[" + str(self.username) + "](tg://user?id\=" + str(self.userid) + ") забанен из чата " + self.list_chats[chat_id]['title'] + censure_filter.all_message, parse_mode="MarkdownV2")
            logging.info(self.username + " забанен из чата "+ self.list_chats[chat_id]['title'])

    def filter_message(self, message):
        qty_chat = 0
        list_chats = []
        for id in self.list_chats.keys():
            status_chat_user = bot.get_chat_member(id, message.from_user.id)
            if status_chat_user.status != "left" and status_chat_user.status != "kicked":
                list_chats.append(self.list_chats[id]["title"])
                qty_chat += 1              
        if qty_chat == 1:
            logging.info("Удалено сообщение пользователя " + str(message.from_user.first_name))
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        else:
            text = ""
            for i in list_chats:
                if i == None:
                    continue
                text += " " + str(i)
            logging.info("Пользователь " + str(message.from_user.first_name) + str(message.from_user.last_name) + " есть в следующих чатах: " + text)


class Travel:


    def __init__(self):
        
        self.join_users_id = []
        self.qty_places = 4
        self.init_qty = 0
        self.init_text = ""
        self.clid = "ak220909"
        self.apikey = "DptuFxzhpvQBGEcXDZfGTkvKGXQppJeDXCdql"
        self.UB = "37.597252,55.555616"
        self.An = "37.599157,55.583953"
        self.BDD = "37.577116,55.570182"
        self.class_taxi = "econom"

    def taxi(self, message = None, tap = None):
        if tap == "taxi+":
            if int(self.init_qty) - len(self.join_users_id) > 0:
                self.join_users_id.append("[" + str(str(message.from_user.first_name) + " " + (str(message.from_user.last_name) or "")) + "](tg://user?id\=" + str(message.from_user.id) + ")")
            else:
                bot.answer_callback_query(callback_query_id=message.id, text='Мест нет.')
                return
        elif tap == "taxi-":
            try:
                self.join_users_id.remove("[" + censure_filter.formating_text_markdownv2(str(message.from_user.first_name) + " " + (str(message.from_user.last_name) or "")) + "](tg://user?id\=" + str(message.from_user.id) + ")")
            except Exception:
                bot.answer_callback_query(callback_query_id=message.id, text='Вы не учавствовали в этой поездке.')
                return       
        elif message != None:
            self.init_user_id = message.from_user.id
            self.init_user_name = str(message.from_user.first_name) + " " + str(message.from_user.last_name)
            self.init_chat = message.chat.id
            message_text_arr = str(message.text).split(" ", 2)
            if len(message_text_arr) != 3 or type(int(message_text_arr[1])) != int:
                if len(message_text_arr) == 1:
                    self.taxi_button()
                    return
            elif self.init_text == "":
                self.init_qty = message_text_arr[1]
                self.init_text = message_text_arr[2].replace('.', '\.')
        if len(self.join_users_id) == 0:
            title_user_list = ""
        else:
            title_user_list = "К поездке уже присоединились:\n"
        key = types.InlineKeyboardMarkup()
        bot_add = types.InlineKeyboardButton(text="Присоединиться", callback_data='{"key": "taxi+", "id": "' + str(self.init_user_id) + '"}')
        bot_del = types.InlineKeyboardButton(text="Отказаться", callback_data='{"key": "taxi-", "id": "' + str(self.init_user_id) + '"}')
        bot_del_mes = types.InlineKeyboardButton(text="Отменить эту поездку", callback_data='{"key": "mes_tax_del", "id": "' + str(self.init_user_id) + '"}')
        key.add(bot_del_mes)
        key.add(bot_add, bot_del)
        ya_text = self.taxi_yandex()
        
        text_message_edit = "Пользователь [" + censure_filter.formating_text_markdownv2(self.init_user_name) + "](tg://user?id\=" + str(self.init_user_id) + ") хочет поехать на такси, есть " + str((int(self.init_qty) - len(self.join_users_id))) + " места\.\nКомментарий: __" + str(self.init_text) + "__\n" + str(ya_text) + title_user_list + str(",\n".join(self.join_users_id) + censure_filter.all_message)
        try:
            bot.edit_message_text(chat_id = self.init_chat, message_id=self.message_id_g.id, text=text_message_edit, parse_mode='MarkdownV2', reply_markup=key)
        except Exception as e:
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            stat.add_qty_message()
            self.message_id_g = bot.send_message(self.init_chat, text_message_edit, parse_mode='MarkdownV2', reply_markup=key)
            bot.pin_chat_message(chat_id=self.message_id_g.chat.id, message_id=self.message_id_g.id)
            logging.info(self.init_user_name + " создал поездку")
            

    def taxi_button(self, places=None, frame_res=None, hour=None, minute=None):
        frame = 12
        arr = []
        bot_del_mes = types.InlineKeyboardButton(text="Отменить эту поездку", callback_data='{"key": "mes_tax_del", "id": "' + str(self.init_user_id) + '"}')
        if places == None and self.init_qty == 0:
            censure_filter.taxi_button_list[self.init_user_id] = self.init_chat
            qty_places = 0
            key_places = types.InlineKeyboardMarkup()
            while self.qty_places != qty_places:
                qty_places += 1
                button_places = types.InlineKeyboardButton(text=str(qty_places), callback_data='{"key": "taxi_places", "places":"' + str(qty_places) + '", "id": "' + str(self.init_user_id) + '"}')
                arr.append(button_places)
            key_places.add(*arr)
            key_places.add(bot_del_mes)
            self.message_id_g = bot.send_message(self.init_chat, "[" + str(self.init_user_name) + "](tg://user?id\=" + str(self.init_user_id) + "), выберите колличество свободных мест в машине:", reply_markup=key_places , parse_mode='MarkdownV2')
        elif places != None:
            self.init_qty = places
            key_frame = types.InlineKeyboardMarkup()
            i = 0
            while frame != i:
                i += 1
                button_frame = types.InlineKeyboardButton(text="От " + str(i) + " корпуса", callback_data='{"key": "frame", "frame": "' + str(i) + '", "id": "' + str(self.init_user_id) + '"}')
                arr.append(button_frame)
            key_frame.add(*arr)
            button_metro = types.InlineKeyboardButton(text="От метро Аннино", callback_data='{"key":"frame", "frame":"0" , "id": "' + str(self.init_user_id) + '"}')
            button_metro_bdd = types.InlineKeyboardButton(text="От метро БДД", callback_data='{"key":"frame", "frame":"БДД" , "id": "' + str(self.init_user_id) + '"}')
            key_frame.add(button_metro, button_metro_bdd)
            key_frame.add(bot_del_mes)
            bot.edit_message_text(chat_id = self.init_chat,message_id=self.message_id_g.id, text = "[" + str(self.init_user_name) + "](tg://user?id\=" + str(self.init_user_id) + "), выберите откуда вызываете такси:", reply_markup=key_frame , parse_mode='MarkdownV2')
        elif frame_res != None:
            if frame_res==str(0):
                self.init_text += "От метро Аннино "
                self.start = self.An
                self.stop = self.UB
            elif frame_res == str("БДД"):
                self.init_text += "От метро БДД "
                self.start = self.BDD
                self.stop = self.UB
            else:
                self.init_text += "От " + str(frame_res) + " корпуса "
                self.start = self.UB
                self.stop = self.BDD
            key_hour = types.InlineKeyboardMarkup()
            i = 0
            while i != 24:
                button_hour = types.InlineKeyboardButton(text=str(i), callback_data='{"key": "hour", "hour": "' + str(i) + '", "id": "' + str(self.init_user_id) + '"}')
                i += 1
                arr.append(button_hour)
            key_hour.add(*arr)
            key_hour.add(bot_del_mes)
            bot.edit_message_text(chat_id = self.init_chat, message_id=self.message_id_g.id, text = "[" + str(self.init_user_name) + "](tg://user?id\=" + str(self.init_user_id) + "), выберите в котором часу вы хотите вызвать такси:", reply_markup=key_hour , parse_mode='MarkdownV2')
        elif hour != None:
            self.init_text += "в " + str(hour) + ":"
            key_min = types.InlineKeyboardMarkup()
            i = 0
            while i != 60:
                button_min = types.InlineKeyboardButton(text=str(i), callback_data='{"key": "min", "min":"' + str(i) + '", "id": "' + str(self.init_user_id) + '"}')
                i += 5
                arr.append(button_min)
            key_min.add(*arr)
            key_min.add(bot_del_mes)
            bot.edit_message_text(chat_id = self.init_chat, message_id=self.message_id_g.id, text = "[" + str(self.init_user_name) + "](tg://user?id\=" + str(self.init_user_id) + "), выберите во сколько минут собираемся:", reply_markup=key_min , parse_mode='MarkdownV2')
        elif minute != None:
                if int(minute) <= 9:
                    minute = "0" + str(minute)
                self.init_text += str(minute)
                self.taxi()
    

    def taxi_yandex(self):
        res = requests.get('https://taxi-routeinfo.taxi.yandex.net/taxi_info?clid='+self.clid+'&apikey='+self.apikey+'&rll='+self.start+'~' + self.stop)
        res = json.loads(res.text)
        price_text = res['options'][0]['price_text']
        if res['options'][0]['waiting_time'] <= 60:
            waiting_time = res['options'][0]['waiting_time']
            time_text = " сек"
        else:
            waiting_time = res['options'][0]['waiting_time'] // 60
            time_text = " мин"
        print(res)
        text_yandex_info = "\nПримерная стоимость по данным Яндекс такси: " + str(res['options'][0]['price_text'][1:-1]) + ";\nВремя подачи машины: " + str(round(waiting_time)) + str(time_text) + ";\nВремя поездки: " + str(res['time_text']) + ";\n"
        return text_yandex_info


class Statistik:
    def __init__(self):
        self.qty_message = 0
        self.qty_chats = 0
        self.qty_users = 0
        self.data = {}
        self.day_message = 9
        self.qty_day = 0
        self.all_message = 0
        self.mean_qty_message = 0


    def real_time(self):
        moscow_time_full = datetime.now(pytz.timezone('Europe/Moscow'))
        moscow_time = str(moscow_time_full).split(' ')
        m_time = moscow_time[1][:5]
        only_time = m_time.split(':')
        only_time.append(moscow_time_full.weekday())
        return only_time


    def add_qty_message(self):
        real_time = self.real_time()
        if real_time[2] != self.day_message:
            self.day_message = real_time[2]
            self.qty_day += 1
        self.all_message += 1
        self.mean_qty_message = self.all_message // self.qty_day


    def add_qty_chat(self):
        self.qty_chats += 1

    
class ConfigPanel:
    

    def __init__(self):
        self.user_id = 0
    

    def list_chats(self, message):
        list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
        if message.from_user.id in list_admin or message.from_user.id == 474425142:
            pass
        else:
            bot.send_message(message.chat.id, f"{message.from_user.username}, вы не администратор группы")
            return

        #file_chats_config = open("chats_config.txt", "w+")
        keyboard_admin = types.InlineKeyboardMarkup()

        for id in user_chat_kik[0].list_chats.keys():
                try:
                    status_chat_user = bot.get_chat_member(id, message.from_user.id)
                    if "left, kicked".count(status_chat_user.status) != 0:
                        continue
                    title = user_chat_kik[0].list_chats[id]["title"]
                    Botton = types.InlineKeyboardButton(text = title, callback_data='{"key": "admin_config", "chat":' + str(id) + '}')
                    keyboard_admin.add(Botton)
                except Exception:
                    logging.error(str(message.from_user.first_name) + " не смог вызвать панель администратора.")
        bot.send_message(message.from_user.id, "Вычерите чат для настройки:", reply_markup=keyboard_admin)
        #file_chats_config.close()


        def config_chat(self, chat):
            keyboard_config_chat = types.InlineKeyboardMarkup()
            chat = user_chat_kik[0].list_chats[chat]
            bot.send_message(self.user.id, "Настройка параметров чата " + chat["title"], reply_markup=keyboard_config_chat)


stat = Statistik()
user_chat_kik = {}
user_chat_kik[0] = Kik_user()
censure_filter = Censure()
taxi_list = {}


@bot.message_handler(commands=['tb'])
def tax_b(message):
    key = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b = types.KeyboardButton(text="Ищу_попутчиков_в_такси")
    key.add(b)
    bot.send_message(message.chat.id, "Кнопка добавлена", reply_markup=key)


@bot.message_handler(commands=['taxi'])
def start(message):

    taxi_list[message.from_user.id] = Travel()
    taxi_list[message.from_user.id].taxi(message)

 
@bot.message_handler(commands=['mat'])
def mat_on(message):
    bot.delete_message(chat_id = message.chat.id, message_id= message.id)
    if message.chat.id in censure_filter.chat_filter_mat:
        list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
        if message.from_user.id in list_admin:
            censure_filter.chat_filter_mat.remove(message.chat.id)
            bot_message = bot.send_message(message.chat.id, "Фильтр нецензурных слов выключен для этого чата.")
            time.sleep(5)
            bot.delete_message(chat_id = message.chat.id, message_id= bot_message.id)
        else:
            bot_message = bot.send_message(message.chat.id, "Для отключения фильтра матных слов нужно быть администратором группы.")
            time.sleep(5)
            bot.delete_message(chat_id = message.chat.id, message_id= bot_message.id)
    else:
        censure_filter.chat_filter_mat.append(message.chat.id)
        bot_message = bot.send_message(message.chat.id, "Фильтр нецензурных слов включен для этого чата.")
        time.sleep(5)
        bot.delete_message(chat_id = message.chat.id, message_id= bot_message.id)


@bot.message_handler(commands=['admin_news'])
def admin_news(message):
    censure_filter.admin_chat = message.chat.id
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    bot.send_message(message.chat.id, "Чат зарегистрирован как чат для предложений новостей")


@bot.message_handler(commands=['kik'])
def test(message):
    if (message.reply_to_message.chat.id + message.reply_to_message.from_user.id) not in user_chat_kik.keys():
        user_chat_kik[message.reply_to_message.chat.id + message.reply_to_message.from_user.id] = Kik_user()
        res_start = user_chat_kik[message.reply_to_message.chat.id + message.reply_to_message.from_user.id].start_kik(message)
        if res_start == False:
            return
        else:
            user_chat_kik[message.reply_to_message.chat.id + message.reply_to_message.from_user.id].survey(message.reply_to_message.chat.id + message.reply_to_message.from_user.id)
    else:
        old_message = bot.send_message(message.chat.id, "Голосование уже создано. Найдите его в чате и проголосуйте.")
        time.sleep(5)
        bot.delete_message(chat_id = old_message.chat.id, message_id= old_message.id)


@bot.message_handler(commands=['ban_all'])
def choice_method(message):
    message_text = message.text
    arr_message_text = message_text.split(' ')
    if len(arr_message_text) == 1:
        ban_all_chats(message)
    else:
        old_message = bot.send_message(message.chat.id, "Неверная команда.")
        time.sleep(5)
        bot.delete_message(chat_id = old_message.chat.id, message_id= old_message.id)
    


def ban_all_chats(message):
    user_chat_kik[0].start_kik(message)
    list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
    if user_chat_kik[0].userid in list_admin:
        stat.add_qty_message()
        bot.send_message(message.chat.id, f"Невозможно забанить администратора группы" + censure_filter.all_message, parse_mode="MarkdownV2")
    elif message.from_user.id in list_admin:
        user_chat_kik[0].armagedon()
    else:
        stat.add_qty_message()
        bot.send_message(message.chat.id, f"{message.from_user.username} Вы не администратор группы" + censure_filter.all_message, parse_mode="MarkdownV2")


#включаем проверку остальных чатов для выявления машенников в барахолке
@bot.message_handler(commands=['no_to_swindlers'])
def no_to_swindlers(message):
    list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
    if message.from_user.id in list_admin or message.from_user.id == 474425142:
        message_chat_id = message.chat.id
        bot.delete_message(chat_id = message.chat.id, message_id= message.id)
        if message.chat.id in user_chat_kik[0].check_chats:
            user_chat_kik[0].check_chats.remove(message.chat.id)
            old_message = bot.send_message(message_chat_id, "Выключен фильтр спам сообщений")
            time.sleep(5)
            bot.delete_message(chat_id = old_message.chat.id, message_id= old_message.id)
            logging.info("Выключен фильтр спам сообщений в чате " + message.chat.title)
        else:
            user_chat_kik[0].check_chats.append(message.chat.id)
            old_message = bot.send_message(message_chat_id, "Включен фильтр спам сообщений")
            time.sleep(5)
            bot.delete_message(chat_id = old_message.chat.id, message_id= old_message.id)
            logging.info("Включен фильтр спам сообщений в чате " + message.chat.title)
    else:
        bot.send_message(message.chat.id, f"{message.from_user.username}, вы не администратор группы")
    

@bot.message_handler(commands=["all"])
def print_all_chats(message):
    bot.delete_message(chat_id = message.chat.id, message_id= message.id)
    text = "All chats:\n"
    for i in user_chat_kik[0].list_chats:
        text += "[" + censure_filter.formating_text_markdownv2(user_chat_kik[0].list_chats[i]['title']) + "](tg://chat?id\=" + str(user_chat_kik[0].list_chats[i]['id']) + ")\n"
    bot.send_message(message.chat.id, text, parse_mode="MarkdownV2")


@bot.message_handler(commands=["spam"])
def spam_message(message):
    censure_filter.spam_message(message)


@bot.message_handler(commands=["statistic"])
def statistic(message):
    bot.send_message(message.chat.id, "*Статистика по рекламному сообщению:*\nдней сбора статистики: " + str(stat.qty_day) + "\nвсего сообщений за эти дни: " + str(stat.all_message) + "\nв среднем за день: " + str(stat.mean_qty_message), parse_mode="MarkdownV2")


#@bot.message_handler(content_types=['new_chat_members'])
# любая функция, которая будет исполняться после того, как человек зайдёт в чат


@bot.channel_post_handler(commands=['offer_news'])
def new_post(message):
    bot.delete_message(message.chat.id, message.id)
    censure_filter.channel_id = message.chat.id
    key_offer = types.InlineKeyboardMarkup()
    botton_offer = types.InlineKeyboardButton(text="Прислать новость", url="https://t.me/lol_chat_bitca_bot")
    key_offer.add(botton_offer)
    bot.send_message(censure_filter.channel_id, "Дорогие соседи,\nтеперь можно предложить новость о нашем ЖК. Для этого нажмите кнопку под этим постом или прямо в закрепленных сообщениях, запустите бота и напишите ему то, что вы хотите предложить опубликовать. После проверки администраторами вашей публикации - пост будет размещен. В некоторых случаях аннонимно, в некоторых нет.\nВажно:\nПо техническим причинам, в публикации пока что может быть только одно фото или видео и текст или просто текст.", reply_markup=key_offer)


@bot.message_handler(commands=["добавить"])
def add_chat(message):
    bot.delete_message(message.chat.id, message.id)
    #проверяем является ли бот администратором и вызвал ли команду пользователь, который подтвердил, что будет настраивать чаты.
    bot.send_message(message.from_user.id, "Чат " + censure_filter.formating_text_markdownv2(message.chat.title) + " добавлен", parse_mode="MarkdownV2")


@bot.message_handler(commands=["новость"])
def offer_news_message(message):
    censure_filter.offer_news(message.reply_to_message)
    old_message = bot.send_message(message.chat.id, "Предложена новость")
    time.sleep(5)
    bot.delete_message(chat_id=old_message.chat.id, message_id=old_message.id)


@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type == "private":
        bot.send_message(message.from_user.id, "Присылайте мне новости. Админ проверит и опубликует их.")
        return


@bot.message_handler(commands=["admin_config"])
def admin_panel(message):
    config_chats = ConfigPanel() #возможно лучше сделать через


@bot.message_handler(content_types=['text'])
def collection_data(message):
    if message.chat.type == "private":
        censure_filter.offer_news(message)
        return
    if message.text == "Ищу_попутчиков_в_такси":
        bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        taxi_list[message.from_user.id] = Travel()
        taxi_list[message.from_user.id].taxi(message)
    if message.chat.id in user_chat_kik[0].list_chats:
        pass
    else:
        user_chat_kik[0].list_chats[message.chat.id] = {
            "id": message.chat.id, 
            "title" : message.chat.title
        }
    if len(user_chat_kik[0].check_chats) != 0:
        if message.chat.id in user_chat_kik[0].check_chats:
            user_chat_kik[0].filter_message(message)
    censure_filter.filter_mat(message)
        
    

@bot.message_handler(content_types=['photo'])
def coll_data(message):
    if message.chat.type == "private":
        censure_filter.offer_news(message)
        return
    if len(user_chat_kik[0].check_chats) != 0:
        if message.chat.id in user_chat_kik[0].check_chats:
            user_chat_kik[0].filter_message(message)


@bot.message_handler(content_types=['video'])
def coll_data(message):
    if message.chat.type == "private":
        censure_filter.offer_news(message)
        bot.send_message(message.from_user.id, censure_filter.formating_text_markdownv2("Напоминаем, что проходит конкурс на звание лучшего фильма (не более 3х минут) о нашем ЖК. Выбирать лучший будем голосованием. Победители, вошедшие в тройку лидеров получат материальный приз. Какой? Узнаем по итогам розыгрыша :) ") + censure_filter.all_message, parse_mode="MarkdownV2")
        stat.add_qty_message()
        #if message.video.duration < 181 вероятно так можно проверить длинну видео. надо потестить.
        return


@bot.callback_query_handler(func=lambda call: True)
def callback_woker(call):
    call_data_json = call.data
    call_data = json.loads(call_data_json)
    logging.info("chat: " + str(call.chat.title) + ", user:" + str(call.from_user.first_name) + " " + str((call.from_user.last_name or "")) + " нажата кнопка с ключем " + call_data['key'])
    
    if call_data['key'] == "kik_yes":
        res = user_chat_kik[int(call_data['id'])].survey(call_data['id'], call=call, voice=True)
        if res == "end_survey":
            del user_chat_kik[int(call_data['id'])]
    elif call_data['key'] == "kik_no":
        res = user_chat_kik[int(call_data['id'])].survey(call_data['id'], call=call, voice=False)
        if res == "end_survey":
            del user_chat_kik[int(call_data['id'])]
    elif call_data['key'] == "ban_all":
        if call.from_user.id in [i.user.id for i in bot.get_chat_administrators(call.chat.id)]:
            user_chat_kik[0].ban_user(call_data['chat'])
            bot.answer_callback_query(callback_query_id=call.id, text='Пользователь забанен в выбранном чате.', show_alert=True)
            logging.info(str(call.from_user.first_name) + " " + str((call.from_user.last_name or "")) + " забанил пользователя в чате.")
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Вы не администратор группы.')
            logging.error(str(call.from_user.first_name) + " " + str((call.from_user.last_name or "")) + " не смог забанить пользователя. Недостаточно прав.")
    elif call_data['key'] == "taxi+" or call_data['key'] == "taxi-":
        obj_id = call_data['id']
        taxi_list[int(obj_id)].taxi(message = call, tap = call_data['key'])
    elif call_data['key'] == "mes_tax_del":
        obj_id = call_data['id']
        if obj_id == str(call.from_user.id):
            bot.delete_message(chat_id=taxi_list[int(obj_id)].init_chat, message_id=taxi_list[int(obj_id)].message_id_g.id)
    elif call_data['key'] == "taxi_places":
        obj_id = call_data['id']
        if obj_id == str(call.from_user.id):
            taxi_list[int(obj_id)].taxi_button(places = call_data['places'])
    elif call_data['key'] == "frame":
        obj_id = call_data['id']
        if obj_id == str(call.from_user.id):
            taxi_list[int(obj_id)].taxi_button(frame_res = call_data['frame'])
    elif call_data['key'] == "hour":
        obj_id = call_data['id']
        if obj_id == str(call.from_user.id):
            taxi_list[int(obj_id)].taxi_button(hour = call_data['hour'])
    elif call_data['key'] == "min":
        obj_id = call_data['id']
        if obj_id == str(call.from_user.id):
            taxi_list[int(obj_id)].taxi_button(minute = call_data['min'])
    elif call_data['key'] == "botton_yes_user":
        censure_filter.public_news(True, int(call_data['id']))
    elif call_data['key'] == "botton_yes_not_user":
        censure_filter.public_news(False, int(call_data['id']))
    elif call_data['key'] == "botton_not_public":
        censure_filter.public_news(None, int(call_data['id']))
    elif call_data['key'] == "admin_config":
        pass
    else:
        bot.answer_callback_query(callback_query_id=call.id, text='Кнопка еще не настроена.')



bot.infinity_polling()