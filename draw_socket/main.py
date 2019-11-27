from flask import Flask, render_template, request, send_file, jsonify
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

clients = []

@app.route("/")
@app.route('/index')
def getIndex():
    return render_template("index.html")

@socketio.on('connect', namespace='/draw')
def drawConnect():
    clients.append(request.sid)
    print("New Connection: ", request.sid)

@socketio.on('disconnect', namespace='/draw')
def drawDisconnect():
    clients.remove(request.sid)
    print("User Disconnected: ", request.sid)
    emit('debug', {'data': 'smb left'}, room=clients[0])

@socketio.on('drawTrigger', namespace='/draw')
def draw(coords):
    emit('drawAction', coords, broadcast=True)

@socketio.on('saveImage', namespace='/draw')
def getImg(img):
    print(img);


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')