import threading

import telegram
from  telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters

from mongodb_manager import MondoClientManager


class Telegram_API:
    def __init__(self):
        self.__token = 'Token'

        self.__updater = Updater(token=self.__token, use_context=True)

        self.check_bot_credentials()
        self.register_handlers()

        threading.Thread(target=self.start_polling, args=()).start()

        self.__mongoClient = MondoClientManager()
        self.__mongoClient.initialize_connection()

    def check_bot_credentials(self):
        bot = telegram.Bot(token=self.__token)
        print(bot.getMe())

    def register_handlers(self):
        dispatcher = self.__updater.dispatcher

        start_handler = CommandHandler('start', self.__on_start_callback)
        dispatcher.add_handler(start_handler)

        random_handler = CommandHandler('random', self.__on_random_callback)
        dispatcher.add_handler(random_handler)

        select_handler = CommandHandler('select', self.__on_select_callback)
        dispatcher.add_handler(select_handler)

        dispatcher.add_handler(CallbackQueryHandler(self.__on_button_callback))

        echo_handler = MessageHandler(Filters.text & (~Filters.command), self.__echo_callback)
        dispatcher.add_handler(echo_handler)

    def start_polling(self):
        self.__updater.start_polling()

    def __on_start_callback(self, update, context):
        main_options = [[telegram.KeyboardButton('/random')],
                        [telegram.KeyboardButton('/select')]]

        reply_markup = telegram.ReplyKeyboardMarkup(main_options,
                                                    resize_keyboard=True,
                                                    one_time_keyboard=True)

        msg = 'Please, select the option:'
        context.bot.send_message(chat_id=update.effective_chat.id, text=msg,
                                 reply_markup=reply_markup)

    def __on_random_callback(self, update, context):
        quote = self.__mongoClient.get_random_quote()
        context.bot.send_message(chat_id=update.effective_chat.id, text=quote)

    def __on_select_callback(self, update, context):
        philosophers = self.__mongoClient.get_philosophers_collection()
        keyboards = []

        for item in philosophers:
            button = [telegram.InlineKeyboardButton(item, callback_data=item)]
            keyboards.append(button)

        reply_markup = telegram.InlineKeyboardMarkup(keyboards)

        context.bot.send_message(chat_id=update.effective_chat.id, text="Select Philosof!",
                                 reply_markup=reply_markup)

    def __on_button_callback(self, update, context):
        query = update.callback_query
        response_quote = self.__mongoClient.get_quote(query.data)

        query.edit_message_text(text=response_quote)

    def __echo_callback(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)
