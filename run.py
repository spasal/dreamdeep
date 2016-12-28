# from gevent.wsgi import WSGIServer
from app import create_app

# http://stackoverflow.com/questions/30901998/threading-true-with-flask-socketio

app = create_app('PRODUCTION')

if __name__ == '__main__':
    # app.debug = True
    # http_server = WSGIServer(('127.0.0.1', 8000), app)
    # http_server.serve_forever()
    app.run(host='0.0.0.0', port=8080, threaded=True)
