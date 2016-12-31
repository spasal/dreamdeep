from app.common import mail_handler
from app import create_app

app = create_app('DEVELOPMENT')
app, mail = mail_handler.init_mail_handler(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
