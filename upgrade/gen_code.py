# coding:utf8

import time
import base64

str_time = str(time.time())

code = base64.b64encode(str_time.encode('utf-8')).decode('utf-8')

print(code)
