import pytz
from datetime import datetime

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