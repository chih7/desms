from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

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


class SMSForm(FlaskForm):
    SMSRN = StringField('SMSRN', validators=[InputRequired()])
    SMSRF = StringField('SMSRF', validators=[InputRequired()])
    SMSRB = StringField('SMSRB', validators=[InputRequired()])
    SMSRD = StringField('SMSRD', validators=[InputRequired()])
    SMSRT = StringField('SMSRT', validators=[InputRequired()])
