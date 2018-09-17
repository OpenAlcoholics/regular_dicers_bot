import json
import re
import threading
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove

from .calendar import Calendar


class Bot:
    custom_keyboard_attend = [["Dabei"], ["Nicht dabei"]]
    offset = 0

    def __init__(self, updater):
        self.updater = updater
        self.user_ids = set()
        self.attend_markup = ReplyKeyboardMarkup(self.custom_keyboard_attend, one_time_keyboard=True)
        self.calendar = Calendar()

    def register(self, update):
        try:
            user = update.message.chat_id
            original_length = len(self.user_ids)
            self.user_ids.add(user)

            with open("users.json", "w+") as f:
                json.dump(list(self.user_ids), f)

            if len(self.user_ids) == original_length:
                self.updater.bot.send_message(chat_id=user, text="Why would you register twice, dumbass!")
            else:
                self.updater.bot.send_message(chat_id=user, text="You have been registered.")
        except Exception as e:
            print(e)

    def remind_users(self, update):
        # Check for admin user
        if update.message.chat_id != "139656428":
            self.updater.bot.send_message(chat_id=update.message.chat_id, text="Fuck you")
        else:
            for user in self.user_ids:
                self.updater.bot.send_message(chat_id=user, text="Wer ist dabei?", reply_markup=self.attend_markup)

    def check_participation_message(self, update):
        positive_messages = ["^dabei$", "👍", "ja", "👌", "yes", "\+1?"]
        negative_messages = ["^nicht dabei$", "👎", "nein", "-1?", "nope"]
        for positive_message in positive_messages:
            if re.match(positive_message, update.message.text.lower()):
                self.calendar.create()
                update.message.reply_text("🍹❤️", quote=True, reply_markup=ReplyKeyboardRemove(True))
        for negative_message in negative_messages:
            if re.match(negative_message, update.message.text.lower()):
                update.message.reply_text("Shame on you", quote=True, reply_markup=ReplyKeyboardRemove(True))

    def remind_user(self, update):
        self.updater.bot.send_message(chat_id=update.message.chat_id, text="Wer ist dabei?", reply_markup=self.attend_markup)
