# from gevent.wsgi import WSGIServer
from app import create_app


app = create_app('PRODUCTION')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)
