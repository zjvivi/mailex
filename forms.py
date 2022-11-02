from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import data_required

class NameForm(FlaskForm):
    name=StringField("请输入注册邮箱：",validators=[data_required()])
    submit=SubmitField('发送邮件')
