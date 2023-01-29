# формат хранения: дом-секция-этаж-квартира-имя-id-авто
from connect import bot, logging, censure_filter
from telebot import types


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
    

    def searchUsers(self, message):
        text_split = message.text.split(" ")
        if len(text_split) < 5:
            if len(text_split) == 5:
                pass
        else:
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            bot.send_message(message.chat.id, "Неверый формат.")