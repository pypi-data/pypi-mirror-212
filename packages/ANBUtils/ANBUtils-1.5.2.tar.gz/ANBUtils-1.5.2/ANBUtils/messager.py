# -*- coding: utf-8 -*-
import os

import requests

message_mark_0: str = 'Message'
message_mark_A: str = '[脑暴]'
message_mark_B: str = '[赞]'
message_mark_C: str = '[加油]'
message_mark_D: str = '[算账]'

msg_text = '''{
    "msgtype": "text",
    "text": {
        "content": "%s"
    }
}'''


def dingtalk_message(data):
    webhook = os.environ.get('DINGTALK_WEBHOOK')
    headers = {
        'Content-Type': 'application/json',
    }
    response = requests.post(webhook, headers=headers, data=data.encode("UTF-8"))
    return response.text


def dingtalk_text_message(text: str):
    """钉钉文本消息发送"""
    dingtalk_message(msg_text % text)
