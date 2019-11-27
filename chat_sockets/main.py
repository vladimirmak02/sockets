from flask import Flask, render_template, request, send_file, jsonify
from flask_socketio import SocketIO, emit
import datetime, random

app = Flask(__name__)
socketio = SocketIO(app)

colors = ['Navy', 'DarkBlue', 'MediumBlue', 'Blue', 'DarkGreen', 'Green', 'Teal', 'DarkCyan', 'DeepSkyBlue', 'DarkTurquoise', 'MediumSpringGreen', 'Lime', 'SpringGreen', 'Aqua', 'Cyan', 'MidnightBlue', 'DodgerBlue', 'LightSeaGreen', 'ForestGreen', 'SeaGreen', 'LimeGreen', 'MediumSeaGreen', 'Turquoise', 'RoyalBlue', 'SteelBlue', 'DarkSlateBlue', 'MediumTurquoise', 'Indigo', 'DarkOliveGreen', 'CadetBlue', 'CornflowerBlue', 'RebeccaPurple', 'MediumAquaMarine', 'SlateBlue', 'OliveDrab', 'MediumSlateBlue', 'LawnGreen', 'Chartreuse', 'Aquamarine', 'Maroon', 'Purple', 'Olive', 'SkyBlue', 'LightSkyBlue', 'BlueViolet', 'DarkRed', 'DarkMagenta', 'SaddleBrown', 'DarkSeaGreen', 'LightGreen', 'MediumPurple', 'DarkViolet', 'PaleGreen', 'DarkOrchid', 'YellowGreen', 'Sienna', 'Brown', 'LightBlue', 'GreenYellow', 'PaleTurquoise', 'LightSteelBlue', 'PowderBlue', 'FireBrick', 'DarkGoldenRod', 'MediumOrchid', 'RosyBrown', 'DarkKhaki', 'MediumVioletRed', 'IndianRed', 'Peru', 'Chocolate', 'Tan', 'Thistle', 'Orchid', 'GoldenRod', 'PaleVioletRed', 'Crimson', 'Gainsboro', 'Plum', 'BurlyWood', 'LightCyan', 'Lavender', 'DarkSalmon', 'Violet', 'PaleGoldenRod', 'LightCoral', 'Khaki', 'AliceBlue', 'HoneyDew', 'Azure', 'SandyBrown', 'Wheat', 'Beige', 'WhiteSmoke', 'MintCream', 'GhostWhite', 'Salmon', 'AntiqueWhite', 'Linen', 'LightGoldenRodYellow', 'OldLace', 'Red', 'Fuchsia', 'Magenta', 'DeepPink', 'OrangeRed', 'Tomato', 'HotPink', 'Coral', 'DarkOrange', 'LightSalmon', 'Orange', 'LightPink', 'Pink', 'Gold', 'Silver']
nameColors = {'Admin':colors[len(colors)-1]}


@app.route("/")
@app.route("/index")
def getIndex():
    return render_template("index.html")

@socketio.on('connect', namespace='/chat')
def chatConnect():
    print("New Connection")
    emit('response', {'time': datetime.datetime.now().strftime('%H:%M:%S'), 'data':' Connected to Chat', 'login':"<span style='color:" + nameColors['Admin'] +"'>" +'Admin' + "</span>"})

@socketio.on('newUser', namespace='/chat')
def newUser(msg):
    print("New User")
    nameColors[msg['login']] = colors[random.randint(0,len(colors)-2)]
    emit('response', {'time': datetime.datetime.now().strftime('%H:%M:%S'), 'data':'New User: '+ "<span style='color:" + nameColors[msg['login']] +"'>" + msg['login'] + "</span>", 'login':"<span style='color:" + nameColors['Admin'] +"'>" + 'Admin' + "</span>"}, broadcast=True)

@socketio.on('newMsg', namespace='/chat')
def recievedMsg(msg):
    print("New Message", msg)
    emit('response', {'time': datetime.datetime.now().strftime('%H:%M:%S'),'data':msg['message'], 'login':"<span style='color:" + nameColors[msg['login']] +"'>" +msg['login'] + "</span>"}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')