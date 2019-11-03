from telegram.ext import Updater, CommandHandler
from telegram import Bot
import os
import logging
import time
import handlers
import schedule

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=os.environ["TOKEN"], use_context=True)
dispatcher = updater.dispatcher

start_handler = CommandHandler('start', handlers.start)
addgroup_handler = CommandHandler('addgroup', handlers.addgroup)
removegroup_handler = CommandHandler("removegroup", handlers.removegroup)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(removegroup_handler)
dispatcher.add_handler(addgroup_handler)
dispatcher.add_error_handler(handlers.onerror)

updater.start_polling()

schedule.every(60).to(100).seconds.do(handlers.checkupdates, bot=Bot(token=os.environ["TOKEN"]))

while True:
    schedule.run_pending()
    time.sleep(1)