from decimal import ExtendedContext
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



token = ''
bot = telebot.TeleBot(token)


def updateConnect():
    while True:
        api = requests.post(f"https://api.telegram.org/bot/{token}/getUpdates".format(token))
        time.sleep(10)


class Censure:


    def __init__(self):
        self.chat_filter_mat = []
        self.mat_list = ["хуй", "пизд", "залупа", "ебать", " бля ", "ебать", "ебать", "ебут", "ебала", "еблан"]

    def filter_mat(self, message):
        for mat in self.mat_list:
            message_text = str(message.text).lower()
            if mat in message_text:
                if message.chat.id in self.chat_filter_mat:
                    message_text = message_text.replace(mat, "***")
                    bot.delete_message(chat_id = message.chat.id, message_id= message.id)
                    bot.send_message(message.chat.id, "Пользователь " + str(message.from_user.first_name) + " " + str(message.from_user.last_name) + " писал: \n " + message_text)


class Bus:


    def __init__(self):
        self.list_chats_bus = []
        self.only_time = []
        self.chat_id = 0
        self.user_id = 0

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
                if correct != None:
                        rest_time = (int(moment_time[1]) - int(self.only_time[1])) * 60
                        ls_time = int(ls_time) - int(rest_time) - int(correct)
                        time.sleep(ls_time)
                        for chat_id in self.list_chats_bus:
                            self.bus_time(message,chat_id, short_pause, long_pause, one)
                elif int(moment_time[1]) == 0:
                    for chat_id in self.list_chats_bus:
                        self.bus_time(message,chat_id, short_pause, long_pause, one)
            time.sleep(20)

    def bus_time(self, message, chat_id, short_pause, long_pause, one):
        ls_time = ""
        keybord = types.InlineKeyboardMarkup()
        keybord_correct = types.InlineKeyboardMarkup()
        submit = types.InlineKeyboardButton(text = "Смотреть расписание", url = "https://t.me/c/1665635878/6335")
        botton_yandex = types.InlineKeyboardButton(text = "Найти на ЯКартах", url="""https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjUhLLXrpn4AhVjmIsKHVF4CcYQFnoECB4QAQ&url=https%3A%2F%2Fyandex.ru%2Fmaps%2F1%2Fmoscow-and-moscow-oblast%2Froutes%2Fminibus_1141%2F796d617073626d313a2f2f7472616e7369742f6c696e653f69643d32303336393235303130266c6c3d33372e35393339343225324335352e353730313937266e616d653d3131343126723d3237303726747970653d6d696e69627573%2F&usg=AOvVaw3uIrCOOfpFrKaj0eqrmGh7""")
        keybord.add(submit, botton_yandex)
        self.only_time = self.real_time()
        while int(self.only_time[0]) >= one and int(self.only_time[0]) < 12:
            ls_time = short_pause
            botton_correct = types.InlineKeyboardButton(text = "Выехала 5 минут назад", callback_data='{"key": "ctb", "ls_time": "' + ls_time + '"}')
            keybord.add(botton_correct)
            if int(self.only_time[0]) == 11 and int(self.only_time[1]) == 30:
                print("last bus in metro")
                old_message2 = bot.send_message(chat_id, str("Маршрутка отправляется от метро. ПЕРЕРЫВ. Сделующая 13:00"), reply_markup=keybord)
                break
            print("6-12")
            short_pause_text = str((short_pause + 60) / 60)
            old_message = bot.send_message(chat_id, str("Маршрутка отправляется от ЖК. Следующая через " + short_pause_text[:2] + " минут."), reply_markup=keybord)
            time.sleep(60)
            bot.edit_message_text(chat_id=chat_id, message_id=old_message.id, text=old_message.text, reply_markup=keybord)
            time.sleep(short_pause)
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)
            self.only_time = self.real_time()
        
        if int(self.only_time[0]) == 12 and int(self.only_time[1]) == 0:
            old_message = bot.send_message(chat_id, str("Маршрутка отправляется от ЖК. ПЕРЕРЫВ. Следующая в ~13:10."), reply_markup=keybord)
            time.sleep(3610)
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)


        
        while int(self.only_time[0]) >= 13 and int(self.only_time[0]) < 15:
            print("13-15")
            ls_time = long_pause
            botton_correct = types.InlineKeyboardButton(text = "Выехала 5 минут назад", callback_data='{"key": "ctb", "ls_time": "' + ls_time + '"}')
            keybord.add(botton_correct)
            bot.delete_message(chat_id = chat_id, message_id= old_message2.id)
            long_pause_text = str((long_pause + 60) / 60)
            old_message = bot.send_message(chat_id, str("Маршрутка отправляется от Метро. Следующая через " + long_pause_text[:2] + " минут."), reply_markup=keybord)
            time.sleep(60)
            bot.edit_message_text(chat_id=chat_id, message_id=old_message.id, text=old_message.text, reply_markup=keybord)
            time.sleep(long_pause)
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)
            self.only_time = self.real_time()
        
        while int(self.only_time[0]) >= 15 and int(self.only_time[0]) < 22:
            ls_time = short_pause
            botton_correct = types.InlineKeyboardButton(text = "Выехала 5 минут назад", callback_data='{"key": "ctb", "ls_time": "' + ls_time + '"}')
            keybord.add(botton_correct)
            if int(self.only_time[0]) == 21 and int(self.only_time[1]) >= 40:
                print("21:40")
                old_message = bot.send_message(chat_id, "Последняя маршрутка отправляется от ЖК. ", reply_markup=keybord)
                pause = 60 - int(self.only_time[1]) + 1
                time.sleep(pause)
                break
            print("15-22")
            short_pause_text = str((short_pause + 60) / 60)
            old_message = bot.send_message(chat_id, str("Маршрутка отправляется от Метро. Следующая через " + short_pause_text[:2] + " минут"), reply_markup=keybord)
            time.sleep(60)
            bot.edit_message_text(chat_id=chat_id, message_id=old_message.id, text=old_message.text, reply_markup=keybord)
            time.sleep(short_pause)
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)
            self.only_time = self.real_time()
        
        if int(self.only_time[0]) == 22:
            print("22:00")
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)
            botton_taxi = types.InlineKeyboardButton(text="Заказать такси", url="https://taxi.yandex.ru/")
            keybord.add(botton_taxi)
            old_message = bot.send_message(chat_id, "Последняя маршрутка отправляется от Метро.", reply_markup=keybord)
            time.sleep(6600)
            bot.delete_message(chat_id = chat_id, message_id= old_message.id)


    def option(self, message, callback=None):
        if callback == None:
            keyb = types.InlineKeyboardMarkup()
            but5 = types.InlineKeyboardButton(text = "Будни", callback_data='{"key": "option_bus", "res": "but5"}')
            but2 = types.InlineKeyboardButton(text = "Выходные", callback_data='{"key": "option_bus", "res": "but2"}')
            keyb.add(but5, but2)
            mes = bot.send_message(message.chat.id, "Вы запустили настройку временных интервалов для автобусов. Пожалуйста выберите какое расписание будем настраивать?", reply_markup=keyb)
            self.chat_id = mes.chat.id
            self.user_id = mes.from_user.id
        elif callback == "but5":
            option_file = open("option_bus5.txt", "w+")
            bot.send_message(self.chat_id, "Введите две цифры. Первая означает окончание окончание временного отрезка, вторая - переодичность приезда:")
            
        


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
            self.username = str(message.reply_to_message.from_user.first_name) + " " + str(message.reply_to_message.from_user.last_name)
            self.useridgolos = 0
            self.qty_yes = 0
            self.qty_no = 0
            self.list_user = []
            self.list_admin = []
            self.initiator = message.from_user.id
            #self.survey()

    def survey(self):
        if self.useridgolos in self.list_user:
            pass
        else:
            if self.qty_yes >= 10:
                bot.kick_chat_member(self.chat, self.userid)
                bot.delete_message(chat_id=self.chat, message_id=self.message)
                bot.send_message(self.chat, "По решению соседей кикнут пользователь " + self.username)
                self.qty_yes = 0
                self.qty_no = 0
                return
            elif self.qty_no >= 10:
                bot.delete_message(chat_id=self.chat, message_id=self.message)
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
                print(status_chat_user.status)
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



user_chat_kik = Kik_user()
censure_filter = Censure()
run_bus = Bus()

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


@bot.message_handler(commands=['spam'])
def spam(message):
    list_admin = [i.user.id for i in bot.get_chat_administrators(message.chat.id)]
    if message.from_user.id in list_admin:
        message_text = str(message.text).split(" ", 1)
        bot.delete_message(chat_id = message.chat.id, message_id= message.id)
        for chat_id in user_chat_kik.list_chats:
            bot.send_message(chat_id, message_text[1])
            print("отправляю спам в чат ", chat_id['name'])
            time.sleep(5)
    else:
        bot.delete_message(chat_id = message.chat.id, message_id= message.id)
        bot_message = bot.send_message(message.chat.id, "Функция доступна только администраторам.")
        time.sleep(5)
        bot.delete_message(chat_id = message.chat.id, message_id= bot_message.id)

@bot.message_handler(commands=['kik'])
def test(message):
    user_chat_kik.start_kik(message)
    user_chat_kik.survey()

        


@bot.message_handler(commands=['ban_all'])
def choice_method(message):
    message_text = message.text
    bot.delete_message(chat_id = message.chat.id, message_id= message.id)
    arr_message_text = message_text.split(' ')
    if len(arr_message_text) == 1:
        ban_all_chats(message)
    else:
        bot.send_message(message.chat.id, "Неверный формат данных.")
    bot.delete_message(chat_id = message.chat.id, message_id= message.id)
    


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
    thread_bus = threading.Thread(target = run_bus.run_time_bus, args=(message,))
    thread_bus.start()
    bot.delete_message(chat_id = message.chat.id, message_id= message.id)
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
        bot.delete_message(chat_id = message.chat.id, message_id= message.id)
        mes = bot.send_message(message.chat.id, "Уведомления о маршрутке включены в этом чате.")
        time.sleep(5)
        bot.delete_message(chat_id = message.chat.id, message_id= mes.id)


@bot.message_handler(content_types=['text'])
def collection_data(message):
    flud_list = ["маршрутк"]
    if message.chat.id in user_chat_kik.list_chats:
        pass
    else:
        user_chat_kik.list_chats[message.chat.id] = {
            "id": message.chat.id, 
            "title" : message.chat.title
        }
    if message.chat.id in run_bus.list_chats_bus:
        pass
    else:
        for flud in flud_list:
            if flud in message.text.lower():
                key = types.InlineKeyboardMarkup()
                sub = types.InlineKeyboardButton(text = "Войти в чат Попутчики", url="https://t.me/+Ml7N5lMqc9JmNDli")
                key.add(sub)
                bot.send_message(message.chat.id, "Информацию о маршрутке можно найти в чате ЮБ Попутчики.", reply_to_message_id = message.id, reply_markup=key)
    censure_filter.filter_mat(message)



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
    else:
        bot.send_message(call.from_user.id,
                            text='Эта кнопка еще не настроена')



bot.infinity_polling()
