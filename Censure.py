import time, threading
from connect import bot, logging, stat
from telebot import types
from pymystem3 import Mystem



class Censure:


    def __init__(self):
        self.chat_filter_mat = []
        self.mat_list = ["хуй", "пизд", "залупа", "ебаный", "ебать", "ебал", " бля ", "ебать", "ебать", "ебут", "еблан", "ебнул", "шлюха", "гандон", "чурка", "хуесос", "уебище", "блядст", "пидр", "пидор", "шлюх", "пиздос", "https://t.me/yubitca"]
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
            text = "Пользователь [" + self.formating_text_markdownv2(str(message.from_user.first_name)) + self.formating_text_markdownv2(str((message.from_user.last_name or ""))) + "](tg://user?id\=" + str(message.from_user.id) + ") писал: \n " + self.formating_text_markdownv2(message_text) + self.all_message
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
            test_commercia = self.test_commercia(self.message_text)
            if self.message_text == None:
                self.message_text_user_info = user_info
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил пост")
            elif test_commercia[0] == True:
                self.message_text_user_info = self.message_text + user_info + "\n\n\#реклама"
                bot.send_message(message.from_user.id, test_commercia[1], parse_mode="MarkdownV2")
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил рекламный пост")
            else:
                self.message_text_user_info = self.message_text + user_info
                bot.send_message(message.from_user.id, test_commercia[1], parse_mode="MarkdownV2")
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил пост")
        else:
            self.message_caption = self.formating_text_markdownv2(message.caption)
            test_commercia = self.test_commercia(self.message_caption)
            if self.message_caption == None:
                self.message_caption_user_info = user_info
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил пост")
            elif test_commercia[0] == True:
                self.message_caption_user_info = self.message_caption + user_info + "\n\n\#реклама"
                bot.send_message(message.from_user.id, test_commercia[1], parse_mode="MarkdownV2")
                logging.info(str(message.from_user.first_name) + " " + str((message.from_user.last_name or "")) + " предложил рекламный пост")
            else:
                self.message_caption_user_info = self.message_caption + user_info
                bot.send_message(message.from_user.id, test_commercia[1], parse_mode="MarkdownV2")
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
    
    

    def test_commercia(self, message):
        m = Mystem()
        message_text = m.lemmatize(message)
        list_commercia = ["услуга", "подключение", "производство", "продажа", "установка", "дешево", "цена", "приглашать", "предлогать"]
        for text_commercia in list_commercia:
            if text_commercia in message_text:
                return True, "Внимание\, в вашем сообщении найдены признаки коммерческой рекламы\. Для размещения рекламы в нашем канале обратитесь к [Максиму](tg://user?id\=474425142)"
        return False, "Ваша публикация отправлена админам\. Вероятно скоро они её опубликуют\."
