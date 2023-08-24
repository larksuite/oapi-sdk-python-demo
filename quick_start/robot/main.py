from flask import Flask
from lark_oapi.adapter.flask import *

from config import *
from quick_start.robot.im import *

app = Flask(__name__)

# 创建告警群并拉人入群
chat_id = create_alert_chat()
print(f"chat_id: {chat_id}")

# 发送告警通知
send_alert_message(chat_id)

# 注册事件回调
event_handler = lark.EventDispatcherHandler.builder(ENCRYPT_KEY, VERIFICATION_TOKEN, lark.LogLevel.DEBUG) \
    .register_p2_im_message_receive_v1(do_p2_im_message_receive_v1) \
    .build()

# 注册卡片回调
card_handler = lark.CardActionHandler.builder(ENCRYPT_KEY, VERIFICATION_TOKEN, lark.LogLevel.DEBUG) \
    .register(do_interactive_card) \
    .build()


@app.route("/event", methods=["POST"])
def event():
    resp = event_handler.do(parse_req())
    return parse_resp(resp)


@app.route("/card", methods=["POST"])
def card():
    resp = card_handler.do(parse_req())
    return parse_resp(resp)


if __name__ == "__main__":
    app.run(port=7777)
