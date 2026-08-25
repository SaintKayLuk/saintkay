#!/usr/bin/python
#-*- coding: utf-8 -*-

# 发送消息到企业微信机器人
import requests
import sys
import json
 
 
#发送消息
msgsend_url='https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b0416691-710e-4cea-ad7d-a9be4edfac1f'

#脚本参数
touser=sys.argv[1]
subject=sys.argv[2]
message=sys.argv[3]

params={
        "msgtype": "text",
        "text": {
                "content": message,
                "mentioned_mobile_list":[touser]
        }
}
 
req=requests.post(msgsend_url, json=params)
print(req.text);
