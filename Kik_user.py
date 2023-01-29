from connect import bot, logging, stat, censure_filter
from telebot import types


class Kik_user:

    def __init__(self):
        self.reply_to_message_id = 0
        self.list_chats = {}
        self.list_user = []
        self.initiator = ""
        self.username = ""
        self.check_chats = []
        self.id = 0
        


    def start_kik(self, message):
        self.chat_id = message.chat.id
        self.chat_title = message.chat.title
        self.chat_member_count_golos = bot.get_chat_member_count(chat_id=message.chat.id) // 101 #вычисляем % пользователей
        bot.delete_message(chat_id=self.chat_id, message_id=message.id)
        try:
            self.userid = message.reply_to_message.from_user.id
            self.list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
            if self.userid in self.list_admin:
                stat.add_qty_message()
                bot.send_message(self.chat_id, "Невозможно кикнуть администратора группы" + censure_filter.all_message, parse_mode="MarkdownV2")
                bot.delete_message(chat_id=self.chat_id, message_id=self.id)
                logging.info(self.initiator + " пытался кикнуть администратора")
                return False
        except Exception as e:
            logging.error(self.initiator + " вызвал команду кик не ответив на сообщение, error: " + e)
            return False
        else:
            self.username = censure_filter.formating_text_markdownv2(str(message.reply_to_message.from_user.first_name) + " " + str((message.reply_to_message.from_user.last_name or "")))
            self.list_yes = []
            self.list_no = []
            self.list_admin = []
            self.initiator = message.from_user.id
            self.del_message_id = str(message.reply_to_message.id)
    
    
    def kik_yes(self):
        bot.kick_chat_member(self.chat_id, self.userid)
        stat.add_qty_message()
        bot.send_message(chat_id=self.chat_id, text="По решению соседей из " + censure_filter.formating_text_markdownv2(self.chat_title) +  " кикнут [" + censure_filter.formating_text_markdownv2(self.username) + "](tg://user?id\=" + str(self.userid) + ")" + censure_filter.all_message, parse_mode="MarkdownV2")
        bot.delete_message(chat_id=self.chat_id, message_id=self.id)
        logging.info("Пользователя " + self.username + " кикнули из чата " + self.chat_title + " голосованием.")


    def kik_no(self):
        stat.add_qty_message()
        bot.send_message(chat_id=self.chat_id, text="По решению соседей [" + censure_filter.formating_text_markdownv2(self.username) + "](tg://user?id\=" + str(self.userid) + ") остается в чате\." + censure_filter.all_message, parse_mode="MarkdownV2")
        bot.delete_message(chat_id=self.chat_id, message_id=self.id)
        logging.info("Пользователя " + self.username + " не кикнули из чата " + self.chat_title + " голосованием.")

    def kik_del_mes(self):
        bot.delete_message(chat_id=self.chat_id, message_id=self.reply_to_message_id) #удаляем сообщение пользователя
        bot.delete_message(chat_id=self.chat_id, message_id=self.id) #удаляем голосование
        logging.info("Сообщение пользователя " + self.username + " удалили из чата " + self.chat_title + " голосованием.")

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


    def spam_work(self):
        for i in self.list_chats.keys():
            bot.send_message(i, self.spam_text + self.all_message)