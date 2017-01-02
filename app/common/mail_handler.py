''''from flask_mail import Mail, Message
import os, sys


def init_mail_handler(app):
    app.config.update(dict(
        DEBUG = True,
        # mail server
        MAIL_SERVER = 'smtp.googlemail.com',
        MAIL_PORT = 465,
        MAIL_USE_TLS = False,
        MAIL_USE_SSL = True,
        MAIL_USERNAME = os.environ.get('MAIL_USERNAME'),
        MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD'),

        # administrator list
        ADMINS = [os.environ.get('MAIL_USERNAME')]
    ))
    mail = Mail(app)

    return app, mail


from run import mail, app


def send_mail(recipient, file):
    msg = Message("Deep Dreams were made of You",
                sender="alex.spassovsimeonov@gmail.com",
                recipients=[recipient])

    msg.html = "<b>Deep dreams were made of you, click on the link to make them appear</b>"

    download_path = sys.path[0] + "/resources/static/uploads/history/" + file
    with app.open_resource(download_path) as img:
        msg.attach("dream.jpg", "image/jpg", img.read())

    mail.send(msg)
'''
def send_mail(recipient, file):
    print("bluh")
