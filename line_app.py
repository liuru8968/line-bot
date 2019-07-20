from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('nJEws5PICIZlm8kbfSPuEegBYoFwMUPAO/6KiguxExLytLGkOIwzuErm/ybm5Jk10JgOntsPYT3qoQOzB10KbJQ4+MSqbA1kAYDr8x497h8P47vR8Y0/5w5wLb3L6lhO0Cqspg9mCj7KAZ/XxgOjtQdB04t89/1O/w1cDnyilFU=')
#頻道訪問令牌(Channel access token (long-lived) )
handler = WebhookHandler('f55a7519943f011bd900cbb66c0bbaee')#你的頻道秘密(Channel secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()