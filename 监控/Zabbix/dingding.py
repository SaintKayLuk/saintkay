#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import time
import hmac
import hashlib
import base64
import urllib.parse
import json
import urllib.request

# ===== 钉钉机器人配置 =====
ACCESS_TOKEN = "你的access_token"
SECRET = "SECxxxxxxxxxxxxxxxxxxxxxxxx"
WEBHOOK_URL = "https://oapi.dingtalk.com/robot/send"

# ===== Zabbix 传参 =====
# $1 Send to（可不用）
# $2 Subject
# $3 Message
to = sys.argv[1] if len(sys.argv) > 1 else ""
subject = sys.argv[2] if len(sys.argv) > 2 else "Zabbix Alert"
message = sys.argv[3] if len(sys.argv) > 3 else ""

# ===== 时间戳（毫秒）=====
timestamp = str(int(time.time() * 1000))

# ===== 生成签名 =====
string_to_sign = f"{timestamp}\n{SECRET}"
hmac_code = hmac.new(
    SECRET.encode("utf-8"),
    string_to_sign.encode("utf-8"),
    hashlib.sha256
).digest()

sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))

# ===== 完整 URL =====
url = (
    f"{WEBHOOK_URL}"
    f"?access_token={ACCESS_TOKEN}"
    f"&timestamp={timestamp}"
    f"&sign={sign}"
)

# ===== 消息体 =====
payload = {
    "msgtype": "markdown",
    "markdown": {
        "title": subject,
        "text": message
    }
}

data = json.dumps(payload).encode("utf-8")

# ===== 发送请求 =====
req = urllib.request.Request(
    url=url,
    data=data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = resp.read().decode("utf-8")
        print(result)
except Exception as e:
    print("ERROR:", e)
    sys.exit(1)