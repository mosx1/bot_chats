from decimal import ExtendedContext
from shutil import ExecError
from subprocess import call
from requests.models import Response
import telebot
import json
import requests
import sys
import re
import time
import threading, time
from telebot import types
import string
from datetime import datetime
import pytz
import calendar
import asyncio


#'1727195415:AAHuFPGxae30xXpGe8feL6sdsy5pb0m5rAU'
token = '5039865293:AAHUtyFYxOYrkFppyKJGQhAGXaatPjCh4-8'
#
bot = telebot.TeleBot(token)


def updateConnect():
    while True:
        api = requests.post(f"https://api.telegram.org/bot/{token}/getUpdates".format(token))
        time.sleep(10)


class Censure:


    def __init__(self):
        self.chat_filter_mat = []
        self.mat_list = ["хуй", "пизд", "залупа", "ебать", " бля ", "ебать", "ебать", "ебут", "ебал", "еблан", "шлюха", "гандон"]
        self.taxi_button_list = {} #для обьектов такси

    def filter_mat(self, message):
        for mat in self.mat_list:
            message_text = str(message.text).lower()
            if mat in message_text:
                #if message.chat.id in self.chat_filter_mat:
                message_text = message_text.replace(mat, "***")
                bot.delete_message(chat_id = message.chat.id, message_id= message.id)
                bot.send_message(message.chat.id, "Пользователь " + str(message.from_user.first_name) + " " + str(message.from_user.last_name) + " писал: \n " + message_text)


class Bus:


    def __init__(self):
        self.list_chats_bus = []
        self.only_time = []
        self.chat_id = 0
        self.user_id = 0
        self.list_message_bus = {}
        self.old_message_time_bus_id = 0
        self.schedule = "https://t.me/c/1665635878/7253" #ссылка на сообщение с расписанием

    def real_time(self):
        moscow_time_full = datetime.now(pytz.timezone('Europe/Moscow'))
        moscow_time = str(moscow_time_full).split(' ')
        m_time = moscow_time[1][:5]
        only_time = m_time.split(':')
        only_time.append(moscow_time_full.weekday())
        return only_time


    def run_time_bus(self, message, correct=None, ls_time=None):
        i = 0
        while i==0:
            moment_time = self.real_time()
            if int(moment_time[0]) >= 6 and int(moment_time[0]) <= 23:
                if int(moment_time[2]) <=4:
                    short_pause = 840
                    long_pause = 1140
                    one = 6
                else:
                    short_pause = 1140
                    long_pause = 1740
                    one = 7
                for chat_id in self.list_chats_bus:
                    pass
                    #self.bus_time(message,chat_id, short_pause, long_pause, one)
            time.sleep(20)

    def bus_time(self, message, chat_id, short_pause, long_pause, one):
        keybord = types.InlineKeyboardMarkup()
        submit = types.InlineKeyboardButton(text = "Смотреть расписание", url = self.schedule)
        botton_yandex = types.InlineKeyboardButton(text = "Найти на ЯКартах", url="""https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjUhLLXrpn4AhVjmIsKHVF4CcYQFnoECB4QAQ&url=https%3A%2F%2Fyandex.ru%2Fmaps%2F1%2Fmoscow-and-moscow-oblast%2Froutes%2Fminibus_1141%2F796d617073626d313a2f2f7472616e7369742f6c696e653f69643d32303336393235303130266c6c3d33372e35393339343225324335352e353730313937266e616d653d3131343126723d3237303726747970653d6d696e69627573%2F&usg=AOvVaw3uIrCOOfpFrKaj0eqrmGh7""")
        keybord.add(submit, botton_yandex)
        self.only_time = self.real_time()
        while int(self.only_time[0]) >= one and int(self.only_time[0]) < 12:
            if int(self.only_time[0]) == 11 and int(self.only_time[1]) == 30:
                print("last bus in metro")
                old_message2 = bot.send_message(chat_id, str("Маршрутка отправляется от метро. ПЕРЕРЫВ. Сделующая 13:00"), reply_markup=keybord)
                break
            print("6-12")
            short_pause_text = str((short_pause + 60) / 60)
            old_message = bot.send_message(chat_id, str("Маршрутка отправляется от ЖК. Следующая через " + short_pause_text[:2] + " минут."), reply_markup=keybord)
            time.sleep(short_pause)
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)
            self.only_time = self.real_time()
        
        if int(self.only_time[0]) == 12 and int(self.only_time[1]) == 0:
            old_message = bot.send_message(chat_id, str("Маршрутка отправляется от ЖК. ПЕРЕРЫВ. Следующая в ~13:10."), reply_markup=keybord)
            time.sleep(3610)
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)


        
        while int(self.only_time[0]) >= 13 and int(self.only_time[0]) < 15:
            print("13-15")
            long_pause_text = str((long_pause + 60) / 60)
            old_message = bot.send_message(chat_id, str("Маршрутка отправляется от Метро. Следующая через " + long_pause_text[:2] + " минут."), reply_markup=keybord)
            time.sleep(long_pause)
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)
            self.only_time = self.real_time()
        
        while int(self.only_time[0]) >= 15 and int(self.only_time[0]) < 22:
            if int(self.only_time[0]) == 21 and int(self.only_time[1]) >= 40:
                print("21:40")
                old_message = bot.send_message(chat_id, "Последняя маршрутка отправляется от ЖК. ", reply_markup=keybord)
                pause = 60 - int(self.only_time[1]) + 1
                time.sleep(pause)
                break
            print("15-22")
            short_pause_text = str((short_pause + 60) / 60)
            old_message = bot.send_message(chat_id, str("Маршрутка отправляется от Метро. Следующая через " + short_pause_text[:2] + " минут"), reply_markup=keybord)
            time.sleep(short_pause)
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)
            self.only_time = self.real_time()
        
        if int(self.only_time[0]) == 22:
            print("22:00")
            botton_taxi = types.InlineKeyboardButton(text="Заказать такси", url="https://taxi.yandex.ru/")
            keybord.add(botton_taxi)
            old_message = bot.send_message(chat_id, "Последняя маршрутка отправляется от Метро.", reply_markup=keybord)
            time.sleep(6600)
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)


    def option(self, message, callback=None):
        if callback == None:
            keyb = types.InlineKeyboardMarkup(resize_keyboard=True)
            but5 = types.InlineKeyboardButton(text = "Будни", callback_data='{"key": "option_bus", "res": "but5"}')
            but2 = types.InlineKeyboardButton(text = "Выходные", callback_data='{"key": "option_bus", "res": "but2"}')
            keyb.add(but5, but2)
            mes = bot.send_message(message.chat.id, "Вы запустили настройку временных интервалов для автобусов. Пожалуйста выберите какое расписание будем настраивать?", reply_markup=keyb)
            self.chat_id = mes.chat.id
            self.user_id = mes.from_user.id
        elif callback == "but5":
            option_file = open("option_bus5.txt", "w+")
            bot.send_message(self.chat_id, "Введите две цифры. Первая означает окончание окончание временного отрезка, вторая - переодичность приезда:")


    def bus_time_botton(self, message):
        try:
            bot.delete_message(chat_id = message.chat.id, message_id = self.old_message_time_bus_id.id)
        except Exception:
            pass
        nik = str(message.from_user.username)
        if nik == "None":
            nik = ""
        else:
            nik = "\n@" + nik
        moment_time = self.real_time()
        if message.text == "От метро":
            one = 5
            two = 0
        elif message.text == "От ЖК":
            one = 0
            two = 5
        vector = message.text
        if int(moment_time[0]) == 12:
            key = types.InlineKeyboardMarkup()
            botton_timetable = types.InlineKeyboardButton(text = "Смотреть расписание", url = self.schedule)
            botton_taxi = types.InlineKeyboardButton(text="Заказать такси", url="https://taxi.yandex.ru/")
            key.add(botton_timetable, botton_taxi)
            bot.delete_message(chat_id = message.chat.id, message_id=message.id)
            self.old_message_time_bus_id = bot.send_message(message.chat.id, str(message.from_user.first_name) + ", перерыв до 13:00"+ nik, reply_markup=key)
            return
        elif int(moment_time[2]) <=4:
            if int(moment_time[0]) <= 6 and int(moment_time[0]) >= 23:
                key = types.InlineKeyboardMarkup()
                botton_timetable = types.InlineKeyboardButton(text = "Смотреть расписание", url = self.schedule)
                botton_taxi = types.InlineKeyboardButton(text="Заказать такси", url="https://taxi.yandex.ru/")
                key.add(botton_timetable, botton_taxi)
                bot.delete_message(chat_id = message.chat.id, message_id=message.id)
                self.old_message_time_bus_id= bot.send_message(message.chat.id, str(message.from_user.first_name) + ", в это время машрутка не ходит." + nik, reply_markup=key)
                return
            elif int(moment_time[0]) >= 6 and int(moment_time[0]) < 12:
                left_min = 15 - ((int(moment_time[1]) + one) % 15)
            elif int(moment_time[0]) >= 13 and int(moment_time[0]) < 15:
                left_min = 20 - ((int(moment_time[1]) + two) % 20)
            elif int(moment_time[0]) >= 15 and int(moment_time[0]) < 23:
                left_min = 15 - ((int(moment_time[1]) + two) % 15)
                if int(moment_time[0]) == 22 and int(moment_time[1]) >= 40 and message.text == "От ЖК":
                    bot.delete_message(chat_id = message.chat.id, message_id=message.id)
                    self.old_message_time_bus_id = bot.send_message(message.chat.id, str(message.from_user.first_name) +", в это время машрутка не ходит." + nik, reply_markup=key)
                    return
        else:
            if int(moment_time[0]) < 7 and int(moment_time[0]) >= 23:
                key = types.InlineKeyboardMarkup()
                botton_timetable = types.InlineKeyboardButton(text = "Смотреть расписание", url = self.schedule)
                botton_taxi = types.InlineKeyboardButton(text="Заказать такси", url="https://taxi.yandex.ru/")
                key.add(botton_timetable, botton_taxi)
                bot.delete_message(chat_id = message.chat.id, message_id=message.id)
                self.old_message_time_bus_id = bot.send_message(message.chat.id, str(message.from_user.first_name) + ", в это время машрутка не ходит." +  nik, reply_markup=key)
                return
            elif int(moment_time[0]) >= 7 and int(moment_time[0]) < 23: #тут 15 было в место 7
                left_min = 20 - ((int(moment_time[1]) + two) % 20)
                if int(moment_time[0]) == 22 and int(moment_time[1]) >= 40 and message.text == "От ЖК":
                    key = types.InlineKeyboardMarkup()
                    botton_timetable = types.InlineKeyboardButton(text = "Смотреть расписание", url = self.schedule)
                    botton_taxi = types.InlineKeyboardButton(text="Заказать такси", url="https://taxi.yandex.ru/")
                    key.add(botton_timetable, botton_taxi)
                    bot.delete_message(chat_id = message.chat.id, message_id=message.id)
                    self.old_message_time_bus_id = bot.send_message(message.chat.id, str(message.from_user.first_name) + ", в это время машрутка не ходит." +  nik, reply_markup=key)
                    return
        keybord = types.InlineKeyboardMarkup()
        submit = types.InlineKeyboardButton(text = "Смотреть расписание", url = self.schedule)
        botton_yandex = types.InlineKeyboardButton(text = "Найти на ЯКартах", url="""https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjUhLLXrpn4AhVjmIsKHVF4CcYQFnoECB4QAQ&url=https%3A%2F%2Fyandex.ru%2Fmaps%2F1%2Fmoscow-and-moscow-oblast%2Froutes%2Fminibus_1141%2F796d617073626d313a2f2f7472616e7369742f6c696e653f69643d32303336393235303130266c6c3d33372e35393339343225324335352e353730313937266e616d653d3131343126723d3237303726747970653d6d696e69627573%2F&usg=AOvVaw3uIrCOOfpFrKaj0eqrmGh7""")
        keybord.add(submit, botton_yandex)
        bot.delete_message(chat_id = message.chat.id, message_id=message.id)
        self.old_message_time_bus_id = bot.send_message(message.chat.id, str(message.from_user.first_name) + ", мaршруткa " + vector + " будет через " + str(left_min) + " мин." +  nik, reply_markup=keybord)
        return


    
                  

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


    def start_kik(self, message, userid=None):
        self.chat = message.chat.id
        bot.delete_message(chat_id=self.chat, message_id=message.id)
        try:
            self.userid = message.reply_to_message.from_user.id
            self.list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
            if self.userid in self.list_admin:
                bot.send_message(self.chat, "Невозможно кикнуть администратора группы.")
        except Exception:
            bot.send_message(self.chat, "Для того чтоб забанить пользователя нужно ответить на его сообщение")
            return
        else:
            try:
                bot.delete_message(chat_id=self.chat, message_id=self.message)
            except Exception:
                pass
            if message.reply_to_message.from_user.last_name == None:
                self.username = str(message.reply_to_message.from_user.first_name)
            self.username = str(message.reply_to_message.from_user.first_name) + " " + str(message.reply_to_message.from_user.last_name)
            self.useridgolos = 0
            self.qty_yes = 0
            self.qty_no = 0
            self.list_user = []
            self.list_admin = []
            self.initiator = message.from_user.id
            self.del_message_id = str(message.reply_to_message.id)
            #self.survey()

    def survey(self):
        if self.useridgolos in self.list_user:
            pass
        else:
            if self.qty_yes >= 10:
                bot.kick_chat_member(self.chat, self.userid)
                bot.delete_message(chat_id=self.chat, message_id=self.message.message_id)
                bot.send_message(self.chat, "По решению соседей кикнут пользователь " + self.username)
                bot.delete_message(chat_id=self.chat, message_id=self.del_message_id)
                self.qty_yes = 0
                self.qty_no = 0
                return
            elif self.qty_no >= 10:
                bot.delete_message(chat_id=self.chat, message_id=self.message.message_id)
                bot.send_message(self.chat, "По решению соседей " + self.username + " остается в чате.")
                return
            survey_keyvboard = types.InlineKeyboardMarkup()
            Botton_yes = types.InlineKeyboardButton(text = f"Да ({self.qty_yes})", callback_data='{"key": "kik_yes"}')
            Botton_no = types.InlineKeyboardButton(text = f"Нет ({self.qty_no})", callback_data='{"key": "kik_no"}')
            survey_keyvboard.add(Botton_yes, Botton_no)
            kik_text = "Кикнуть " + str(self.username) + " ?"
            if self.qty_yes == 0 and self.qty_no == 0:
                self.message = bot.send_message(self.chat, kik_text, reply_markup=survey_keyvboard)
            else:
                bot.edit_message_text(chat_id=self.chat, message_id=self.message.message_id, text=kik_text, reply_markup=survey_keyvboard)


    def armagedon(self):
        keyword_ban = types.InlineKeyboardMarkup()
        Botton_all_chats = types.InlineKeyboardButton(text = "Удалить из всех чатов", callback_data='{"key": "ban_all", "chat": "all"}')
        keyword_ban.add(Botton_all_chats)
        for id in self.list_chats.keys():
            try:
                status_chat_user = bot.get_chat_member(id, self.userid)
                if status_chat_user.status == "left":
                    continue
                title = self.list_chats[id]["title"]
                Botton = types.InlineKeyboardButton(text = title, callback_data='{"key": "ban_all", "chat":' + str(id) + '}')
                keyword_ban.add(Botton)
            except Exception:
                pass
        bot.send_message(self.chat, f"Выберите в каком чате вы хотите заблокировать пользователя {self.username}:", reply_markup=keyword_ban)
    
    
    def ban_user(self, chat_id):
        if chat_id == "all":
            for chat in self.list_chats.keys():
                try:
                    bot.ban_chat_member(chat, self.userid)
                except Exception:
                    pass
            bot.send_message(self.chat, f"Пользователь {self.username} забанен из всех чатов")
        else:
            bot.ban_chat_member(chat_id, self.userid)
            bot.send_message(self.chat, f"Пользователь {self.username} забанен из чата {self.list_chats[chat_id]['title']}")

    def filter_message(self, message):
        qty_chat = 0
        list_chats = []
        for id in self.list_chats.keys():
            status_chat_user = bot.get_chat_member(id, message.from_user.id)
            if status_chat_user.status != "left" and status_chat_user.status != "kicked":
                list_chats.append(self.list_chats[id]["title"])
                qty_chat += 1              
        if qty_chat == 1:
            print("Удалено сообщение пользователя ", str(message.from_user.first_name) + " " + str(message.from_user.last_name))
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
        else:
            print("Пользователь ", message.from_user.first_name, " есть в следующих чатах: ", list_chats)


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
                self.join_users_id.append("[" + str(str(message.from_user.first_name) + " " + str(message.from_user.last_name)) + "](tg://user?id\=" + str(message.from_user.id) + ")")
            else:
                old_message_1 = bot.send_message(self.init_chat, "[" + str(str(message.from_user.first_name) + " " + str(message.from_user.last_name)) + "](tg://user?id\=" + str(self.init_user_id) + "), мест в этой поездке больше нет\.", reply_to_message_id=self.message_id_g, parse_mode='MarkdownV2')
                time.sleep(5)
                bot.delete_message(chat_id=old_message_1.chat.id, message_id=old_message_1.id)
                return
        elif tap == "taxi-":
            try:
                self.join_users_id.remove("[" + str(str(message.from_user.first_name) + " " + str(message.from_user.last_name)) + "](tg://user?id\=" + str(message.from_user.id) + ")")
            except Exception:
                old_message_2 = bot.send_message(self.init_chat, "[" + str(str(message.from_user.first_name) + " " + str(message.from_user.last_name)) + "](tg://user?id\=" + str(self.init_user_id) + "), вы не учавствовали в этой поездке\.", reply_to_message_id=self.message_id_g, parse_mode='MarkdownV2')
                time.sleep(5)
                bot.delete_message(chat_id=old_message_2.chat.id, message_id=old_message_2.id)
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
        key = types.InlineKeyboardMarkup()
        bot_add = types.InlineKeyboardButton(text="Присоединиться", callback_data='{"key": "taxi+", "id": "' + str(self.init_user_id) + '"}')
        bot_del = types.InlineKeyboardButton(text="Отказаться", callback_data='{"key": "taxi-", "id": "' + str(self.init_user_id) + '"}')
        bot_del_mes = types.InlineKeyboardButton(text="Отменить эту поездку", callback_data='{"key": "mes_tax_del", "id": "' + str(self.init_user_id) + '"}')
        key.add(bot_del_mes)
        key.add(bot_add, bot_del)
        ya_text = self.taxi_yandex()
        print(ya_text)
        text_message_edit = "Пользователь [" + str(self.init_user_name) + "](tg://user?id\=" + str(self.init_user_id) + ") хочет поехать на такси, есть " + str((int(self.init_qty) - len(self.join_users_id))) + " места\.\nКомментарий: __" + str(self.init_text) + "__\n" + str(ya_text) + "К поездке уже присоединились:\n" + str(",\n".join(self.join_users_id))
        try:
            bot.edit_message_text(chat_id = self.init_chat, message_id=self.message_id_g.id, text=text_message_edit, parse_mode='MarkdownV2', reply_markup=key)
        except Exception as e:
            print(e)
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            self.message_id_g = bot.send_message(self.init_chat, text_message_edit, parse_mode='MarkdownV2', reply_markup=key)


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

user_chat_kik = Kik_user()
censure_filter = Censure()
run_bus = Bus()
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



@bot.message_handler(commands=['kik'])
def test(message):

    user_chat_kik.start_kik(message)
    user_chat_kik.survey()

        


@bot.message_handler(commands=['ban_all'])
def choice_method(message):
    message_text = message.text
    arr_message_text = message_text.split(' ')
    if len(arr_message_text) == 1:
        ban_all_chats(message)
    else:
        bot.send_message(message.chat.id, "Неверный формат данных.")
    


def ban_all_chats(message):
    user_chat_kik.start_kik(message)
    list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
    if user_chat_kik.userid in list_admin:
        bot.send_message(message.chat.id, f"Невозможно забанить администратора группы")
    elif message.from_user.id in list_admin:
        user_chat_kik.armagedon()
    else:
        bot.send_message(message.chat.id, f"{message.from_user.username} Вы не администратор группы")


@bot.message_handler(commands=['start_bus'])
def trigger_bus(message):
    run_bus.__init__()
    #thread_bus = threading.Thread(target = run_bus.run_time_bus, args=(message,))
    #thread_bus.start()
    bot.delete_message(chat_id = message.chat.id, message_id= message.id)
    control_list_bus(message)
    print("Уведомления об автобусах запущены")


@bot.message_handler(commands=['bus'])
def control_list_bus(message):
    if message.chat.id in run_bus.list_chats_bus:
        run_bus.list_chats_bus.remove(message.chat.id)
        bot.delete_message(chat_id = message.chat.id, message_id= message.id)
        mes = bot.send_message(message.chat.id, "Уведомления о маршрутке отключены в этом чате.")
        time.sleep(5)
        bot.delete_message(chat_id = message.chat.id, message_id= mes.id)
    else:
        run_bus.list_chats_bus.append(message.chat.id)
        try:
            bot.delete_message(chat_id = message.chat.id, message_id= message.id)
        except Exception:
            pass
        keybord = types.InlineKeyboardMarkup()
        submit = types.InlineKeyboardButton(text = "Смотреть расписание", url = "https://t.me/c/1665635878/5344")
        bus_keybord = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bus_metro_botton = types.KeyboardButton(text = "От метро")
        bus_jk_botton = types.KeyboardButton(text = "От ЖК")
        keybord.add(submit)
        bus_keybord.add(bus_jk_botton, bus_metro_botton)
        bot.send_message(message.chat.id, "Добавлены кнопки", reply_markup=bus_keybord)
        bot.send_message(message.chat.id, "Уведомления о маршрутке включены в этом чате.", reply_markup=keybord)


#включаем проверку остальных чатов для выявления машенников в барахолке
@bot.message_handler(commands=['no_to_swindlers'])
def no_to_swindlers(message):
    list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
    if message.from_user.id in list_admin:
        message_chat_id = message.chat.id
        bot.delete_message(chat_id = message.chat.id, message_id= message.id)
        if message.chat.id in user_chat_kik.check_chats:
            user_chat_kik.check_chats.remove(message.chat.id)
            old_message = bot.send_message(message_chat_id, "Выключен фильтр спам сообщений")
            time.sleep(5)
            bot.delete_message(chat_id = old_message.chat.id, message_id= old_message.id)
        else:
            user_chat_kik.check_chats.append(message.chat.id)
            old_message = bot.send_message(message_chat_id, "Включен фильтр спам сообщений")
            time.sleep(5)
            bot.delete_message(chat_id = old_message.chat.id, message_id= old_message.id)
    else:
        bot.send_message(message.chat.id, f"{message.from_user.username}, вы не администратор группы")
    

@bot.message_handler(commands=["all"])
def print_all_chats(message):
    text = "Бот работает в следующих чатах:\n"
    for i in user_chat_kik.list_chats:
        text += str(user_chat_kik.list_chats[i]['id']) + " - " + user_chat_kik.list_chats[i]['title'] + "\n"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["up"])
def reply_to_publication(message):
    try:
        reply_ro_message_id = message.reply_to_message.id
    except Exception:
        return bot.send_message(message.chat.id, "Для продвижения публикации ответьте на публикацию и укажите соответствующую команду")
    if message.reply_to_message.caption != None:
        reply_to_message_text = message.reply_to_message.caption
    else:
        reply_to_message_text = message.reply_to_message.text
    try:
        reply_to_message_photo_id = message.reply_to_message.photo
    except Exception:
        pass
    bot.delete_message(chat_id=message.chat.id, message_id=message.id)
    try:
        bot.send_photo(chat_id=message.chat.id, photo=message.reply_to_message.photo[0].file_id, caption=reply_to_message_text + "\n---\nНаписать автору объявления: @" + message.reply_to_message.from_user.username)
    except Exception:
        bot.send_message(message.chat.id, reply_to_message_text + "\n---\nНаписать автору объявления: @" + message.reply_to_message.from_user.username)


@bot.message_handler(content_types=['text'])
def collection_data(message):
    flud_list = ["маршрутк"]
    if message.text == "Ищу_попутчиков_в_такси":
        taxi_list[message.from_user.id] = Travel()
        taxi_list[message.from_user.id].taxi(message)
    if message.chat.id in user_chat_kik.list_chats:
        pass
    else:
        user_chat_kik.list_chats[message.chat.id] = {
            "id": message.chat.id, 
            "title" : message.chat.title
        }
    if message.chat.id in run_bus.list_chats_bus:
        if "От ЖК" == message.text or "От метро" == message.text:
            run_bus.bus_time_botton(message)
    if len(user_chat_kik.check_chats) != 0:
        if message.chat.id in user_chat_kik.check_chats:
            user_chat_kik.filter_message(message)
    censure_filter.filter_mat(message)
    

@bot.message_handler(content_types=['photo'])
def coll_data(message):
    if len(user_chat_kik.check_chats) != 0:
        if message.chat.id in user_chat_kik.check_chats:
            user_chat_kik.filter_message(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_woker(call):
    print(call.from_user.id, "callback_woker")

    call_data_json = call.data
    call_data = json.loads(call_data_json)

    if call_data['key'] == "kik_yes":
        user_chat_kik.qty_yes += 1
        user_chat_kik.useridgolos = call.from_user.id
        user_chat_kik.survey()
        user_chat_kik.list_user.append(call.from_user.id)
    elif call_data['key'] == "kik_no":
        user_chat_kik.qty_no += 1
        user_chat_kik.useridgolos = call.from_user.id
        user_chat_kik.survey()
        user_chat_kik.list_user.append(call.from_user.id)
    elif call_data['key'] == "ban_all":
        if user_chat_kik.initiator == call.from_user.id:
            user_chat_kik.ban_user(call_data['chat'])
    elif call_data['key'] == "ctb":
        run_bus.run_time_bus(message = call, correct = 5, ls_time = call_data['ls_time'])
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
    else:
        bot.send_message(call.from_user.id,
                            text='Эта кнопка еще не настроена')



bot.infinity_polling()