from wtforms import StringField, Form, validators

from desms import db


class SMS(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    SMSRN = db.Column(db.String(64))  # 发件人姓名
    SMSRF = db.Column(db.String(64))  # 发件人号码
    SMSRB = db.Column(db.String(512))  # 短信内容
    SMSRD = db.Column(db.String(64))  # 发件日期
    SMSRT = db.Column(db.String(64))  # 发件时间

    def __init__(self, SMSRN, SMSRF, SMSRB, SMSRD, SMSRT):
        self.SMSRN = SMSRN
        self.SMSRF = SMSRF
        self.SMSRB = SMSRB
        self.SMSRD = SMSRD
        self.SMSRT = SMSRT


class SMSForm(Form):
    TOKEN = StringField('TOKEN', [validators.DataRequired()])
    SMSRN = StringField('SMSRN', [validators.DataRequired()])
    SMSRF = StringField('SMSRF', [validators.DataRequired()])
    SMSRB = StringField('SMSRB', [validators.DataRequired()])
    SMSRD = StringField('SMSRD', [validators.DataRequired()])
    SMSRT = StringField('SMSRT', [validators.DataRequired()])


class BlockPhoneNumber(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    PhoneNumber = db.Column(db.String(64))

    def __init__(self, PhoneNumber):
        self.PhoneNumber = PhoneNumber
