from gevent import monkey
monkey.patch_all() 

from flask import Flask, Response, render_template, request, make_response, url_for, redirect, abort, send_file
from flask_socketio import SocketIO, disconnect, emit
from service import Yt, Clean, Auth
import time
import os
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__, static_url_path='',  static_folder='web/static', template_folder='web/')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
socketio = SocketIO(app, async_mode="gevent")

clean = Clean()
authorization = Auth()
load_dotenv()

def check(sessionId, yt):
    last_status = None
    while True:
        current_status = yt.checkDownload(sessionId)

        if not current_status == 'error':

            if current_status != last_status:
                socketio.emit('check', current_status)
                last_status = current_status

            if 'file' in current_status and current_status['file']:
                return
            time.sleep(0.2) 

        else:
            socketio.emit('error')
            return
        
@app.route('/', methods=['GET'])
def home():
    cookieToken = request.cookies.get('token')
    if cookieToken:

        data = authorization.decodeToken(cookieToken, app)

        if data.get('session'):
            clean.remove(data.get('session'))
            year = datetime.now().year
            return render_template('index.html', year=year)

    return redirect(url_for('auth'))
        
@socketio.on('connect')
def handle_connect():
    cookieToken = request.cookies.get('token')
    authorizated = authorization.decodeToken(cookieToken, app)
    if not authorizated:
        disconnect()
    else:
        pass

@socketio.on('error')
def error():
    pass

@socketio.on('start')
def start(data):
    yt = Yt()
    try:
        cookieToken = request.cookies.get('token')
        token = authorization.decodeToken(cookieToken, app)
        session = token.get('session')

        socketio.start_background_task(check, session, yt)
        downloadTheVideo = yt.download(data['playlist'], data['type'], data['url'], session)
        if not downloadTheVideo:
            yt.setErrorToTrue()
            socketio.emit('error')
            disconnect()
    except:
        yt.setErrorToTrue()
        socketio.emit('error')
        disconnect()


@socketio.on('disconnect')
def handle_disconnect():
    disconnect()

@app.route('/file/<string:name>')
def getFile(name):

    cookieToken = request.cookies.get('token')

    if cookieToken:
        data = authorization.decodeToken(cookieToken, app)
        if data.get('session'):
            session = data.get('session')
            directory = os.path.join('files', session)
            filepath = os.path.join(directory, name)

            if not os.path.abspath(filepath).startswith(os.path.abspath(directory)):
                abort(403)

            return send_file(filepath, as_attachment=True)

    return redirect(url_for('auth'))
    
@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'GET':
        return render_template('auth.html')
    else:
        try:
            password = request.get_json()['password']
            if authorization.checkPassword(password):
                res = make_response(Response(status=200))
                res.set_cookie('token', authorization.encodeToken(app), httponly=True) 
                return res
            else:
                return Response(status=401)
        except Exception as e:
            return Response(status=400)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)