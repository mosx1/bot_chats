import telebot, time, requests, threading, logging
from Statistik import Statistik

token = '' #test
#token = ''
bot = telebot.TeleBot(token)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
stat = Statistik

from Censure import Censure
censure_filter = Censure()

from Kik_user import Kik_user
user_chat_kik = {}
user_chat_kik[0] = Kik_user()



def updateConnect():
    while True:
        requests.post(f"https://api.telegram.org/bot/{token}/getUpdates".format(token))
        time.sleep(10)


thread = threading.Thread(target = updateConnect)
thread.start()