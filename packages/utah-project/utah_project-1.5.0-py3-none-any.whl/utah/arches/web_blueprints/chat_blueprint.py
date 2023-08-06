from flask import Blueprint, render_template, request, session
import json
from datetime import datetime
import time
from utah.core.authorize import uri_authorized

class Msg():
    def __init__(self,text,timestamp,handle):
        self.text=text
        self.timestamp=timestamp
        self.handle=handle

app = Blueprint('chat', __name__,url_prefix="/chat")

counter = 0
chatData = []

@app.route("communicate", methods=['GET'])
@uri_authorized()
def get_queue():
    return render_template("chat.html", handle=session["user_id"], text="", messages=chatData)

@app.route("communicate", methods=['POST'])
@uri_authorized()
def postToQueue():
    handle = request.form["handle"].rstrip()
    text = request.form["text"].rstrip()

    if handle and text:
        message = Msg(text, timeStamp(), request.form["handle"])
        chatData.append(message)
        trimList(chatData, 10)
        text = ""

    return render_template("chat.html", handle=session["user_id"], text=text, messages=chatData)


def trimList(chat,max):
    if len(chat) > max:
        chat.pop(0)


def timeStamp():
    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min
    second = time.localtime().tm_sec
    if (hour/10) < 1:
        hour = "0"+str(hour)+":"
    else:
        hour = str(hour)+":"
    if (minute/10) < 1:
        minute = "0"+str(minute)+":"
    else:
        minute = str(minute)+":"
    if (second/10) < 1:
        second = "0"+str(second)
    else:
        second = str(second)
    return hour+minute+second