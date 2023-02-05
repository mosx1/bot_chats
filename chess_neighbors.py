# формат хранения: дом-секция-этаж-квартира-имя-id-авто
from connect import bot, logging, censure_filter
from telebot import types
import time, re


class Chess_neighbots:

    def addUser_in_chess(self, message):

        try:
            mes = message.text.split(" ")
            self.home = int(mes[1])
            self.section = int(mes[2])
            self.floor = int(mes[3])
            self.flat = int(mes[4])
        except Exception as e:
            bot.send_message(message.chat.id, "Неверный формат данных.")
            logging.error(e)
            return

        if len(mes) != 5:
            bot.send_message(message.chat.id, "Неверный формат данных.")
            logging.error("2")
            return

        num_str = 0
        self.coincidences = []

        with open("chess_neighbors.txt", "r+") as file:
            self.lines = file.readlines()
            lines_split = [i.split("-") for i in self.lines]
            
            key = types.InlineKeyboardMarkup()
            no_botton = types.InlineKeyboardButton(text="Нет", callback_data='{"key": "no_edit_chess"}')
            yes_botton = types.InlineKeyboardButton(text="Добавить", callback_data='{"key": "add_chess"}')
            edit_botton = types.InlineKeyboardButton(text="Перезаписать", callback_data='{"key": "edit_chess"}')
            for user in lines_split:
                if int(user[0]) == self.home and int(user[1]) == self.section and int(user[2]) == self.floor and int(user[3]) == self.flat:
                    self.coincidences.append([user, num_str])
                num_str += 1
            
            if len(self.coincidences) != 0:
                name_user = ""
                for user in self.coincidences:
                    name_user += " [" + user[0][4] + "](tg://user?id\=" + user[0][5] + ") ,"
                key.add(yes_botton, edit_botton, no_botton)
                bot.send_message(chat_id = message.chat.id, reply_to_message_id=message.reply_to_message.id, text="В "+ str(self.home) + " домe " + str(self.section) + " секци на " + str(self.floor) + " этажe в " + str(self.flat) + " квартирe уже отмечены:\n" + name_user[:-1] + "\nХотите добавить [" + censure_filter.formating_text_markdownv2(str(message.reply_to_message.from_user.first_name) + " " + str(message.reply_to_message.from_user.last_name or "")) + "](tg://user?id\=" + str(message.reply_to_message.from_user.id) + ") или перезаписать данные?", reply_markup=key, parse_mode="MarkdownV2")
            else:
                key.add(yes_botton, no_botton)
                bot.send_message(chat_id = message.chat.id, reply_to_message_id=message.reply_to_message.id, text="Добавить [" + censure_filter.formating_text_markdownv2(str(message.reply_to_message.from_user.first_name) + " " + (message.reply_to_message.from_user.last_name or "")) + "](tg://user?id\=" + str(message.reply_to_message.from_user.id) + ") как жителя " + str(self.home) + " дома " + str(self.section) + " секции " + str(self.floor) + " этажа " + str(self.flat) + " квартиры?", reply_markup=key, parse_mode="MarkdownV2")
            bot.delete_message(message.chat.id, message.id)
    

    def add_user(self, call):
        user_name = call.message.reply_to_message.from_user.username or (str(call.message.reply_to_message.from_user.first_name) + " " + (call.message.reply_to_message.from_user.last_name or ""))
        user_id = call.message.reply_to_message.from_user.id
        text_str = str(self.home) + "-" + str(self.section) +"-"+ str(self.floor) +"-"+ str(self.flat) + "-" + censure_filter.formating_text_markdownv2(user_name) + "-" + str(user_id) + "\n"
        with open("chess_neighbors.txt", "a") as file:
            file.write(text_str)
        text = "Пользователь " + user_name + " добавлен в шахматку."
        bot.answer_callback_query(callback_query_id=call.id, text=text, show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.id)
        logging.info(text)


    def edit_user(self, call):
        for i in self.coincidences:
            self.lines.pop(i[1])
        with open("chess_neighbors.txt", "w") as file:
            for text_str in self.lines:
                file.write(text_str)
        self.add_user(call)
    

    def add_Avto(self, message):
        try:
            bot.delete_message(message.chat.id, message.id)
            old_message = bot.send_message(chat_id = message.chat.id, reply_to_message_id=message.reply_to_message.id, text ="Загрузка...")
        except Exception:
            old_message = bot.send_message(message.chat.id, "Для добавления номера авто в шахматку необходимо ответить на сообщение хозяина авто")
            time.sleep(5)
            bot.delete_message(old_message.chat.id, old_message.id)
            return
        self.text = message.text.split(" ")
        if len(self.text) != 2 or re.fullmatch(r"^[а-яА-ЯёЁ][0-9]{3}[а-яА-ЯёЁ]{2}[0-9]+$", self.text[1]) == None:
             bot.edit_message_text(chat_id=old_message.chat.id, message_id=old_message.id, text="Неверный формат\. Используйте команду в формате \"/авто м000мм000\"", parse_mode="MarkdownV2")
        key = types.InlineKeyboardMarkup()
        add_botton = types.InlineKeyboardButton(text="Добавить", callback_data='{"key": "add_avto"}')
        edit_botton = types.InlineKeyboardButton(text="Обновить", callback_data='{"key": "edit_avto"}')
        no_botton = types.InlineKeyboardButton(text="Нет", callback_data='{"key": "no_edit_chess"}')
        if len(self.text) == 2 and re.search("^[а-яА-ЯёЁ][0-9]{3}[а-яА-ЯёЁ]{2}[0-9]+$", self.text[1]) != None:
            with open("chess_neighbors.txt", "r") as file:
                self.lines = file.readlines()
                self.lines_split = [i.split("-") for i in self.lines]
                a = 0
                for i in self.lines_split:
                    if int(i[5]) == int(message.reply_to_message.from_user.id):
                        a += 1
                if a == 0:
                    bot.edit_message_text(chat_id=old_message.chat.id, message_id=old_message.id, text="Пользователя нет в шахматке\. Добавьте пользователя в шахматку прежде чем отметить авто\.", parse_mode="MarkdownV2")
                    return
                i = 0
                self.users = []
                for user in self.lines_split:
                    if len(user) == 7 and user[6].lower() == self.text[1].lower():
                        self.users.append([user, i])
                    i += 1
                user_add = "[" + str(message.reply_to_message.from_user.first_name) + " " + (message.reply_to_message.from_user.last_name or "") + "](tg://user?id\=" + str(message.reply_to_message.from_user.id) + ")"
                if len(self.users) == 0:
                    key.add(add_botton, no_botton)
                    text_mes = "Добавить номер " + self.text[1] + " пользователю " + user_add + "?"
                else:
                    list_user = "\nНомер авто уже закреплен за:"
                    for i in self.users:
                        list_user += "\n[" + i[0][4] + "](tg://user?id\=" + str(i[0][5]) + ")"
                    text_mes = "Добавить номер " + self.text[1] + " еще одному пользователю " + user_add + " или обновить данные о номере в шахматке?" + list_user
                    key.add(add_botton, edit_botton, no_botton)
                bot.edit_message_text(chat_id=old_message.chat.id, message_id=old_message.id, text=text_mes, reply_markup=key, parse_mode="MarkdownV2")                 
    

    def add_num_avto(self, call):
        num_line = 0
        num_lines = []
        text = []
        for i in self.lines_split:
            try:
                data_line = int(i[5])
            except Exception:
                data_line = int(i[5][:-1])
            if data_line == int(call.message.reply_to_message.from_user.id):
                num_lines.append(num_line)
            num_line += 1
        with open("chess_neighbors.txt", "r") as file:
            lines = file.readlines()
            a = 0
            for num_line in num_lines:
                lines_split = lines[num_line].split("-")
                text.append("-".join(lines_split[:6]))
                self.lines.pop(num_line - a)
                a += 1
        with open("chess_neighbors.txt", "w") as file:
            print("self ", self.lines)
            for text_str in self.lines:
                file.write(text_str)
                print(text_str)
            text_res = [str(text_user)[:-1] + "-" + str(self.text[1]) + "\n" for text_user in text]
            for text_str in text_res:
                file.write(text_str)
        bot.answer_callback_query(callback_query_id=call.id, text="Номер авто " + str(self.text[1]) + " закреплен за пользователем " + str(call.message.reply_to_message.from_user.first_name) + " " + str(call.message.reply_to_message.from_user.last_name), show_alert=True)
        bot.delete_message(call.message.chat.id, call.message.id)
        logging.info("добавлен номер авто для пользователя " + str(call.message.reply_to_message.from_user.first_name) + " " + (call.message.reply_to_message.from_user.last_name or ""))

    def edit_num_avto(self, call):
        new_user_lines = []
        b = 0
        lines = self.lines
        for i in self.users:
            new_user_lines.append(str(i[0][0]) + "-" + str(i[0][1]) + "-" + str(i[0][2]) + "-" + str(i[0][3]) + "-" + str(i[0][4]) + "-" + str(i[0][5]) + "\n")
            lines.pop(int(i[1]) - b)
            b += 1
        with open("chess_neighbors.txt", "w") as file:
            for text_str in lines:
                file.write(text_str)
            for text_str in new_user_lines:
                file.write(text_str)
        with open("chess_neighbors.txt", "r") as file:
            self.lines = file.readlines()
        self.add_num_avto(call)


    def searchUsers(self, message):
        old_message = bot.send_message(message.chat.id, "Загрузка...")
        text_split = message.text.split(" ")
        text = ""
        file = open("chess_neighbors.txt", "r")
        self.lines = file.readlines()
        lines_split = [i.split("-") for i in self.lines]
        if len(text_split) == 5:
            users = [i for i in lines_split if i[0] == text_split[1] and i[1] == text_split[2] and i[2] == text_split[3] and i[3] == text_split[4]]
            logging.info("Чат: " + message.chat.title + " ; Пользователь: " + message.from_user.first_name + message.from_user.last_name + "; Действите: поиск по квартире.")
        elif len(text_split) == 4:
            users = [i for i in lines_split if i[0] == text_split[1] and i[1] == text_split[2] and i[2] == text_split[3]]
            logging.info("Чат: " + message.chat.title + " ; Пользователь: " + message.from_user.first_name + message.from_user.last_name + "; Действите: поиск по этажу.")
        elif len(text_split) == 3:
            users = [i for i in lines_split if i[0] == text_split[1] and i[1] == text_split[2]]
            logging.info("Чат: " + message.chat.title + " ; Пользователь: " + message.from_user.first_name + message.from_user.last_name + "; Действите: поиск по секции.")
        elif len(text_split) == 2 and len(text_split[1]) <= 2:
            users = [i for i in lines_split if i[0] == text_split[1]]
            logging.info("Чат: " + message.chat.title + " ; Пользователь: " + message.from_user.first_name + message.from_user.last_name + "; Действите: поиск по дому.")
        elif len(text_split) == 2 and re.fullmatch(r"^[а-яА-ЯёЁ][0-9]{3}[а-яА-ЯёЁ]{2}[0-9]+$", text_split[1]) != None:
            users = [i for i in lines_split if len(i) == 7 and i[6][:-1].lower() == text_split[1].lower()]
            logging.info("Чат: " + message.chat.title + " ; Пользователь: " + message.from_user.first_name + message.from_user.last_name + "; Действите: поиск по авто.")
        else:
            logging.error("Чат: " + message.chat.title + " ; Пользователь: " + message.from_user.first_name + message.from_user.last_name + "; Действите: неверный формат поиска: " + message.text)
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            bot.edit_message_text(chat_id=old_message.chat.id, message_id=old_message.id, text="Неверный формат.")
            time.sleep(5)
            bot.delete_message(chat_id=old_message.chat.id, message_id=old_message.id)
            return
        if len(users) == 0:
            bot.edit_message_text(chat_id=old_message.chat.id, message_id=old_message.id, text="Ничего не найдено\.", parse_mode="MarkdownV2")
            logging.info("Чат: " + message.chat.title + " ; Пользователь: " + message.from_user.first_name + message.from_user.last_name + "; Действите: поиск без результата")
        else:
            for i in users:
                text += "Дом: " + str(i[0]) + " секция: " + str(i[1]) + " этаж: " + str(i[2]) + " квартира: " + str(i[3]) + "\nконтакт: [" +str(i[4]) + "](tg://user?id\=" + str(i[5]) + ")\n"
            bot.edit_message_text(chat_id=old_message.chat.id, message_id=old_message.id, text=text, parse_mode="MarkdownV2")