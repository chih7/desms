import telegram
from flask import request
from telegram.ext import Dispatcher, MessageHandler, Filters

from desms import config, db, app
from desms.models import SMSForm, SMS
from desms.sms_code import parse_sms_code_if_exists, contains_keywords

token = config['TELEGRAM']['ACCESS_TOKEN']
admins_id = config['TELEGRAM']['ADMINS_ID']

# Initial bot by Telegram access token
bot = telegram.Bot(token=token)


@app.route('/test')
def test():
    """Set route /test with GET method will trigger this method."""
    if request.method == "GET":
        print("GET /test")
        return 'GET /test'
    """Set route /test with POST method will trigger this method."""
    if request.method == "POST":
        print("POST /test")
        return 'POST /test'
    return 'Not GET or POST'


@app.route('/hook', methods=['POST'])
def hook_handler():
    """Set route /hook with POST method will trigger this method."""
    if request.method == "POST":
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return 'ok'


@app.route('/input', methods=['GET'])
def input_handler():
    """Set route /input with POST method will trigger this method."""

    # return app.config['SQLALCHEMY_DATABASE_URI']

    sms_form = SMSForm()
    if request.method == "GET":  # and sms_form.validate():
        sms_rn = request.args['SMSRN']
        sms_rb = request.args['SMSRB']
        sms_rf = request.args['SMSRF']
        sms_rd = request.args['SMSRD']
        sms_rt = request.args['SMSRT']

        sms = SMS(SMSRN=sms_rn, SMSRB=sms_rb, SMSRF=sms_rf, SMSRD=sms_rd, SMSRT=sms_rt)
        db.session.add(sms)
        db.session.commit()

        sms = 'from: ' + sms_rn + '/' + sms_rf + 'content:' + sms_rb

        # send sms to telegram
        bot.send_message(chat_id=admins_id, text=sms)

        if contains_keywords(sms_rb):
            sms_code = parse_sms_code_if_exists(sms_rb)
            bot.send_message(chat_id=admins_id, text='验证码: ' + sms_code)
        return 'send success'

    return 'ok'


def reply_handler(bot, update):
    """Reply message."""
    text = update.message.text
    update.message.reply_text(text)


# New a dispatcher for bot
dispatcher = Dispatcher(bot, None)

# Add handler for handling message, there are many kinds of message. For this handler, it particular handle text
# message.
dispatcher.add_handler(MessageHandler(Filters.text, reply_handler))

if __name__ == "__main__":
    # Running server
    app.run(debug=True)
