import lark_oapi as lark

from config import *

client = lark.Client.builder() \
    .app_id(APP_ID) \
    .app_secret(APP_SECRET) \
    .log_level(lark.LogLevel.DEBUG) \
    .build()
