from flask import request

from desms import app, db
from desms.config import TOKEN, INPUT_TOKEN
from desms.filter import is_need_filter
from desms.models import SMSForm, SMS
from desms.spam import is_spam
from desms.telegram import send_to_telegram, _hook, set_webhook


# create all db tables
@app.before_first_request
def create_tables():
    db.create_all()


@app.before_first_request
def init():
    set_webhook()


@app.route('/hook/' + TOKEN, methods=['POST'])
def webhook():
    if request.method == "POST":
        _hook(request)
    return "ok"


@app.route('/input', methods=['POST'])
def input_handler():
    """Set route /input with POST method will trigger this method."""

    sms_form = SMSForm(request.form)
    if request.method == "POST" and sms_form.validate():
        token_r = sms_form.TOKEN.data
        sms_rn = sms_form.SMSRN.data
        sms_rb = sms_form.SMSRB.data
        sms_rf = sms_form.SMSRF.data
        sms_rd = sms_form.SMSRD.data
        sms_rt = sms_form.SMSRT.data

        if token_r != INPUT_TOKEN:
            return 'token verification failed'

        sms = SMS(SMSRN=sms_rn, SMSRB=sms_rb, SMSRF=sms_rf, SMSRD=sms_rd, SMSRT=sms_rt)

        # save to database
        db.session.add(sms)
        db.session.commit()

        # is spam?
        if is_spam(sms_rb):
            return 'is spam sms'
        # is need filter?
        if is_need_filter(sms_rf, sms_rb):
            return 'is need filter'

        sms = 'from: ' + sms_rn + ' / ' + sms_rf + '\n' + sms_rb
        send_to_telegram(sms_rb, sms)

        return 'send success'
    return 'failed'


@app.route('/add_block')
def list_all_sms():
    smses = db.session.query(SMS).all()
    return smses


if __name__ == "__main__":
    # Running server
    app.run(debug=True)
