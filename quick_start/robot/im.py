import time

import lark_oapi as lark
from lark_oapi.api.im.v1 import *

from client import client

user_open_ids = ["ou_a79a0f82add14976e3943f4deb17c3fa", "ou_33c76a4cbeb76bd66608706edb32508e"]


# 获取会话历史消息
def list_chat_history(chat_id: str) -> None:
    request = ListMessageRequest.builder() \
        .container_id_type("chat") \
        .container_id(chat_id) \
        .build()

    response = client.im.v1.message.list(request)

    if not response.success():
        raise Exception(
            f"client.im.v1.message.list failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")

    f = open(f"./chat_history.txt", "w")
    for i in response.data.items:
        sender_id = i.sender.id
        create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i.create_time) / 1000))
        content = i.body.content

        msg = f"chatter({sender_id}) at {create_time} send: {content}"
        f.write(msg + "\n")

    f.close()


# 创建报警群并拉人入群
def create_alert_chat() -> str:
    request = CreateChatRequest.builder() \
        .user_id_type("open_id") \
        .request_body(CreateChatRequestBody.builder()
                      .name("P0: 线上事故处理")
                      .description("线上紧急事故处理")
                      .user_id_list(user_open_ids)
                      .build()) \
        .build()

    response = client.im.v1.chat.create(request)

    if not response.success():
        raise Exception(
            f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")

    return response.data.chat_id


# 发送报警消息
def send_alert_message(chat_id: str) -> None:
    request = CreateMessageRequest.builder() \
        .receive_id_type("chat_id") \
        .request_body(CreateMessageRequestBody.builder()
                      .receive_id(chat_id)
                      .msg_type("interactive")
                      .content(_build_card("跟进处理"))
                      .build()) \
        .build()

    response = client.im.v1.chat.create(request)

    if not response.success():
        raise Exception(
            f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")


# 上传图片
def _upload_image() -> str:
    file = open("alert.png", "rb")
    request = CreateImageRequest.builder() \
        .request_body(CreateImageRequestBody.builder()
                      .image_type("message")
                      .image(file)
                      .build()) \
        .build()

    response = client.im.v1.image.create(request)

    if not response.success():
        raise Exception(
            f"client.im.v1.image.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")

    return response.data.image_key


# 获取会话信息
def get_chat_info(chat_id: str) -> GetChatResponseBody:
    request = GetChatRequest.builder() \
        .chat_id(chat_id) \
        .build()

    response = client.im.v1.chat.get(request)

    if not response.success():
        raise Exception(
            f"client.im.v1.chat.get failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")

    return response.data


# 更新会话名称
def update_chat_name(chat_id: str, chat_name: str):
    request: UpdateChatRequest = UpdateChatRequest.builder() \
        .chat_id(chat_id) \
        .request_body(UpdateChatRequestBody.builder()
                      .name(chat_name)
                      .build()) \
        .build()

    response: UpdateChatResponse = client.im.v1.chat.update(request)

    if not response.success():
        raise Exception(
            f"client.im.v1.chat.update failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")


# 处理消息回调
def do_p2_im_message_receive_v1(data: P2ImMessageReceiveV1) -> None:
    msg = data.event.message
    if "/solve" in msg.content:
        request = CreateMessageRequest.builder() \
            .receive_id_type("chat_id") \
            .request_body(CreateMessageRequestBody.builder()
                          .receive_id(msg.chat_id)
                          .msg_type("text")
                          .content("{\"text\":\"问题已解决，辛苦了!\"}")
                          .build()) \
            .build()

        response = client.im.v1.chat.create(request)

        if not response.success():
            raise Exception(
                f"client.im.v1.chat.create failed, code: {response.code}, msg: {response.msg}, log_id: {response.get_log_id()}")

        chat_info = get_chat_info(msg.chat_id)
        name = chat_info.name
        if name.startswith("[跟进中]"):
            name = "[已解决]" + name[5:]
        elif not name.startswith("[已解决]"):
            name = "[已解决]" + name

        update_chat_name(msg.chat_id, name)


# 处理卡片回调
def do_interactive_card(data: lark.Card) -> Any:
    if data.action.value.get("key") == "follow":
        chat_info = get_chat_info(data.open_chat_id)
        name = chat_info.name
        if not name.startswith("[跟进中]") and not name.startswith("[已解决]"):
            name = "[跟进中] " + name
        update_chat_name(data.open_chat_id, name)

        return _build_card("跟进中")


# 构建卡片
def _build_card(button_name: str) -> str:
    image_key = _upload_image()
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "template": "red",
            "title": {
                "tag": "plain_text",
                "content": "1 级报警 - 数据平台"
            }
        },
        "elements": [
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": "**🕐 时间：**\n2021-02-23 20:17:51"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": "**🔢 事件 ID：**\n336720"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": "**📋 项目：**\nQA 7"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": "**👤 一级值班：**\n<at id=all>所有人</at>"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": "**👤 二级值班：**\n<at id=all>所有人</at>"
                        }
                    },
                ]
            },
            {
                "tag": "img",
                "img_key": image_key,
                "alt": {
                    "tag": "plain_text",
                    "content": " "
                },
                "title": {
                    "tag": "lark_md",
                    "content": "支付方式 支付成功率低于 50%："
                }
            },
            {
                "tag": "note",
                "elements": [
                    {
                        "tag": "plain_text",
                        "content": "🔴 支付失败数  🔵 支付成功数"
                    }
                ]
            },
            {
                "tag": "action",
                "actions": [
                    {
                        "tag": "button",
                        "text": {
                            "tag": "plain_text",
                            "content": button_name
                        },
                        "type": "primary",
                        "value": {
                            "key": "follow"
                        },
                    },
                    {
                        "tag": "select_static",
                        "placeholder": {
                            "tag": "plain_text",
                            "content": "暂时屏蔽"
                        },
                        "options": [
                            {
                                "text": {
                                    "tag": "plain_text",
                                    "content": "屏蔽10分钟"
                                },
                                "value": "1"
                            },
                            {
                                "text": {
                                    "tag": "plain_text",
                                    "content": "屏蔽30分钟"
                                },
                                "value": "2"
                            },
                            {
                                "text": {
                                    "tag": "plain_text",
                                    "content": "屏蔽1小时"
                                },
                                "value": "3"
                            },
                            {
                                "text": {
                                    "tag": "plain_text",
                                    "content": "屏蔽24小时"
                                },
                                "value": "4"
                            },
                        ],
                        "value": {
                            "key": "value"
                        }
                    }
                ]
            },
            {
                "tag": "hr"
            },
            {
                "tag": "div",
                "text": {
                    "tag": "lark_md",
                    "content": "🙋🏼 [我要反馈误报](https://open.feishu.cn/) | 📝 [录入报警处理过程](https://open.feishu.cn/)"
                }
            }
        ]
    }

    return lark.JSON.marshal(card)
