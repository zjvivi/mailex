from flask import Flask, render_template, redirect, url_for, session, copy_current_request_context
import os
from flask_mail import Mail
from flask_mail import Message
from threading import Thread
import forms


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mail ex'

app.config['MAIL_SERVER'] = 'smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True  # 启用安全套接层协议
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')



mail = Mail(app)

# 同步发送
# def send_email(to, subject, template, **kwargs):
#     msg = Message(subject,
#                   sender=app.config['MAIL_USERNAME'], recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     mail.send(msg)



# 异步发送
def send_email(to, subject, template, **kwargs):
    msg = Message(subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr=Thread(target=send_async_email,args=[app,msg])
    thr.start()
    return thr


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


@app.route('/', methods=['GET', 'POST'])
def index():
#     # testing mail
#     msg = Message('Hello', sender='zjvivi@126.com', recipients=['2570201@qq.com'])
#     msg.body = "This is the email body"
#     mail.send(msg)
#     return 'success!'
    form = forms.NameForm()
    if form.validate_on_submit():
        user = {'username': form.name.data}
        if app.config['MAIL_USERNAME']:
            send_email(user['username'], '新用户', 'mail/new_user', user=user)
            session['is_send'] = True
            form.name.data = ''
            return render_template('result.html',is_send=session.get('is_send'))
    return render_template('index.html', form=form, is_send=session.get('is_send', False))



if __name__ == '__main__':
    app.run()
