import telebot, time, requests, threading, logging


token = '1727195415:AAHuFPGxae30xXpGe8feL6sdsy5pb0m5rAU' #test
#token = '5039865293:AAHUtyFYxOYrkFppyKJGQhAGXaatPjCh4-8'
bot = telebot.TeleBot(token)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

def updateConnect():
    while True:
        api = requests.post(f"https://api.telegram.org/bot/{token}/getUpdates".format(token))
        time.sleep(10)


thread = threading.Thread(target = updateConnect)
thread.start()