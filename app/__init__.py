# -*- coding:utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir,ADMINS,MAIL_SERVER,MAIL_PORT 
from config import MAIL_USER_NAME,MAIL_PASSWORD
import os


app=Flask(__name__)
app.config.from_object('config')
db=SQLAlchemy(app)
lm=LoginManager()
lm.init_app(app)
#指明允许登录的页面
lm.login_view='login'

oid=OpenID(app,os.path.join(basedir,'tmp'))


from app import views,models

if not app.debug:
    import logging
    from logging.handlers import SMTPHandler
    from logging.handlers import RotatingFileHandler
    credentials=None
    if MAIL_USER_NAME or MAIL_PASSWORD:
        credentials=(MAIL_USER_NAME,MAIL_PASSWORD)
    mail_handler=SMTPHandler(
        (MAIL_SERVER,MAIL_PORT)
            , 'no-reply@'+MAIL_SERVER,ADMINS,'micro blog failuer'
            ,credentials)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

    file_handler = RotatingFileHandler('tmp/microblog.log', 'a', 1 * 1024 * 1024, 10)

    formatter=logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(formatter)

    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('microblog start up')
