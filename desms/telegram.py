import telegram
from functools import wraps
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackQueryHandler, Dispatcher

from desms import logger
from desms.config import TOKEN, ADMINS_ID, HOST, PORT
from desms.sms_code import parse_sms_code_if_exists, is_code_sms
from desms.utils import Utils

# Initial bot by Telegram access token
bot = telegram.Bot(token=TOKEN)


def send_action(action):
    """Sends `action` while processing func command."""

    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.effective_message.chat_id, action=action)
            return func(bot, update, **kwargs)

        return command_func

    return decorator


def start(bot, update):
    update.message.reply_text('welcome!')


def send_to_telegram(sms_rb, sms):
    """send sms to telegram"""

    button_list = [
        InlineKeyboardButton("add to block contacts", callback_data='add_block'),
        InlineKeyboardButton("mark as spam", callback_data='is_spam')
    ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=2))

    bot.send_message(chat_id=ADMINS_ID, text=sms, reply_markup=reply_markup)

    if is_code_sms(sms_rb):
        sms_code = parse_sms_code_if_exists(sms_rb)
        bot.send_message(chat_id=ADMINS_ID, text=sms_code)


def build_menu(buttons,
               n_cols,
               header_buttons=None,
               footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu


def button(bot, update):
    query = update.callback_query

    bot.edit_message_text(text="Selected option: {}".format(query.data),
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


class BotDispatcher:
    def __init__(self):
        self.dispatcher = Dispatcher(bot, None, workers=0)
        self.dispatcher.add_handler(CommandHandler('start', start))
        self.dispatcher.add_handler(CommandHandler('help', help))
        self.dispatcher.add_handler(CallbackQueryHandler(button))
        self.dispatcher.add_error_handler(error)

    def process_update(self, update):
        self.dispatcher.process_update(update)


bot_dispatcher = BotDispatcher()
utils = Utils(bot)


def _hook(request):
    update = telegram.update.Update.de_json(request.get_json(force=True), bot)
    logger.debug("webhook update: {}".format(update))

    utils.set_update(update)
    bot_dispatcher.process_update(update)


def set_webhook():
    response = bot.set_webhook(url='https://%s:%s/hook/%s' % (HOST, PORT, TOKEN), timeout=20)
    logger.info("set_webhook response: {}".format(response))
