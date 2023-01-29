import json
import requests
import time
import time
from telebot import types
import logging
from connect import bot, logging, censure_filter, stat, user_chat_kik
from chess_neighbors import Chess_neighbots
from Kik_user import Kik_user

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
            bot.pin_chat_message(chat_id=self.message_id_g.chat.id, message_id=self.message_id_g.id)
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


chess = {}
taxi_list = {}


@bot.message_handler(commands=['шахматка'])
def add_chess(message):
    chess[message.from_user.id] = Chess_neighbots()
    chess[message.from_user.id].addUser_in_chess(message)



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
    try:
        user = str(message.reply_to_message.from_user.first_name) + " " + (str(message.reply_to_message.from_user.last_name) or "")
        kik_text = "Кикнуть " + censure_filter.formating_text_markdownv2(user) + " ?"
        survey_message = bot.send_poll(chat_id=message.reply_to_message.chat.id, question=kik_text, options=['Да', 'Нет', 'Просто удалить сообщение, без кика'], reply_to_message_id=message.reply_to_message.id)
        user_chat_kik[survey_message.poll.id] = Kik_user()
        user_chat_kik[survey_message.poll.id].id = survey_message.id
        user_chat_kik[survey_message.poll.id].reply_to_message_id = message.reply_to_message.id
        user_chat_kik[survey_message.poll.id].start_kik(message)
    except Exception:
        bot.send_message(message.chat_id, "Для того чтоб забанить нужно ответить на сообщение пользователя\." + censure_filter.all_message, parse_mode="MarkdownV2")



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
    user_chat_kik[0].spam_message(message)


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
        b = types.InlineKeyboardButton("Перейти", web_app=types.WebAppInfo('https://google.ru'))
        a = types.InlineKeyboardMarkup()
        a.add(b)
        bot.send_message(message.chat.id, "test", reply_markup=a)
        bot.send_message(message.from_user.id, "Присылайте мне новости. Админ проверит и опубликует их.")
        return


@bot.message_handler(commands=["admin_config"])
def admin_panel(message):
    config_chats = ConfigPanel() #возможно лучше сделать через



@bot.message_handler(content_types=['text'])
def collection_data(message):
    #test
    

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
    logging.info("chat: " + str(call.message.chat.title) + ", user:" + str(call.from_user.first_name) + " " + str((call.from_user.last_name or "")) + " нажата кнопка с ключем " + call_data['key'])
    
    if call_data['key'] == "ban_all":
        if call.from_user.id in [i.user.id for i in bot.get_chat_administrators(call.message.chat.id)]:
            user_chat_kik[0].ban_user(call_data['chat'])
            bot.delete_message(message_id=call.message.id, chat_id=call.message.chat.id)
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
    elif call_data['key'] == "add_chess":
        if call.from_user.id in chess:
            chess[call.from_user.id].add_user(call)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Нет доступа')
    elif call_data['key'] == "no_edit_chess":
        if call.from_user.id in chess:
            bot.delete_message(call.message.chat.id, call.message.id)
            del chess[call.from_user.id]
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Нет доступа')
    elif call_data['key'] == "edit_chess":
        list_admin = [i.user.id for i in bot.get_chat_administrators(call.message.chat.id)]
        if call.from_user.id in list_admin or call.from_user.id == 474425142:
            chess[call.from_user.id].edit_user(call)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Обратитесь к администатору для изменения')
    elif call_data['key'] == "admin_config":
        pass
    else:
        bot.answer_callback_query(callback_query_id=call.id, text='Кнопка еще не настроена.')



@bot.poll_handler(lambda p: True)
def handle_poll(PollOption):
    status_chat_user = bot.get_chat_member(user_chat_kik[PollOption.id].chat_id, user_chat_kik[PollOption.id].userid)
    if status_chat_user.status == "left" or status_chat_user.status == "kicked":
        text = "Пользователь [" + censure_filter.formating_text_markdownv2(user_chat_kik[PollOption.id].username) + "](tg://user?id\=" + str(user_chat_kik[PollOption.id].userid) + ") покинул чат, либо его кикнул администратор\. Голосование окончено\."
        bot.send_message(user_chat_kik[PollOption.id].chat_id, text, parse_mode="MarkdownV2")
        bot.delete_message(chat_id=user_chat_kik[PollOption.id].chat_id,message_id=user_chat_kik[PollOption.id].id)
        return
    if int(PollOption.options[0].voter_count) == int(user_chat_kik[PollOption.id].chat_member_count_golos):
        user_chat_kik[PollOption.id].kik_yes()
    elif int(PollOption.options[1].voter_count) == int(user_chat_kik[PollOption.id].chat_member_count_golos):
        user_chat_kik[PollOption.id].kik_no()
    elif int(PollOption.options[2].voter_count) == int(user_chat_kik[PollOption.id].chat_member_count_golos):
        user_chat_kik[PollOption.id].kik_del_mes()



bot.infinity_polling()