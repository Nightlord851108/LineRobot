from flask import Flask, request, abort
import json

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

from src.message import Message

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('ZtmdrSOL3jYcjtNFpoAWNnmFbRivHNUR8U+w3ftRnNF0ODl5G5w+aT3X1LEm6616qnHvJlxQBr3N9YhXRp1XyqSlWWOQRb1W9lx0UPX2FMPbVNNCIhIBwsXKRt0lvz+1hOa+Qe+IhMX7hfcenFWIJwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('62eb9886562f78d9402b8ba72a4f57f4')


def checkKey(message):
    keywordList = ['Language', 'profile', 'project', 'team work', 'Lab']
    for i in keywordList:
        if i == message:
            return True
    return False

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    print("*****Input details in body*****")
    print(body)
    if (checkKey(json.loads(body)['events'][0]['message']['text'])):
        return 'OK'
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("*****Input Message In handle_message*****")
    print(event)
    inputMessage = event.message.text
    ms = Message(inputMessage)
    replyMessage = ms.getOutput()
    message = TextSendMessage(text=replyMessage)
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
