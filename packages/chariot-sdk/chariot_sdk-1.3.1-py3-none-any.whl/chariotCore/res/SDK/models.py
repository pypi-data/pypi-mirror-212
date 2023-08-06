from typing import List, Literal, Optional
from pydantic import BaseModel


#   执行数据验证类，用于传入插件数据的验证
class PLUGIN_TEST_MODEL(BaseModel):
    version: str
    type: str
    body: dict


#   转发地址和缓存地址
class DISPATCHER_MODEL(BaseModel):
    url: str = "http://127.0.0.1:10001/transpond"
    cache_url: str = ""


#   请求
class BODY_MODEL(BaseModel):
    meta: dict = {}
    connection: dict = {}
    dispatcher: DISPATCHER_MODEL = None
    input: dict = {}
    enable_web: bool = False
    config: dict = {}


class ACTION_TEST_BODY_MODEL(BODY_MODEL):
    action: str


class TRIGGER_TEST_BODY_MODEL(BODY_MODEL):
    trigger: str
    dispatcher: DISPATCHER_MODEL


class ALARM_RECEIVER_TEST_BODY_MODEL(BODY_MODEL):
    alarm: str
    dispatcher: DISPATCHER_MODEL


class INDICATOR_RECEIVER_TEST_BODY_MODEL(BODY_MODEL):
    receiver: str
    dispatcher: DISPATCHER_MODEL


class ASSET_RECEIVER_TEST_BODY_MODEL(BODY_MODEL):
    asset: str
    dispatcher: DISPATCHER_MODEL


class ACTION_TEST_MODEL(BaseModel):
    version: str = "v3"
    type: str = "action"
    body: ACTION_TEST_BODY_MODEL


class TRIGGER_TEST_MODEL(BaseModel):
    version: str = "v3"
    type: str = "trigger"
    body: TRIGGER_TEST_BODY_MODEL


class ALARM_RECEIVER_TEST_MODEL(BaseModel):
    version: str = "v3"
    type: str = "alarm_receiver"
    body: ALARM_RECEIVER_TEST_BODY_MODEL


class INDICATOR_RECEIVER_TEST_MODEL(BaseModel):
    version: str = "v3"
    type: str = "indicator_receiver"
    body: INDICATOR_RECEIVER_TEST_BODY_MODEL


class ASSET_RECEIVER_TEST_MODEL(BaseModel):
    version: str = "v3"
    type: str = "asset_receiver"
    body: ASSET_RECEIVER_TEST_BODY_MODEL


#   插件定义文件结构，用于初始化插件
class PLUGIN_DATA_MODEL(BaseModel):
    plugin_spec_version: str = "v3"
    name: str
    version: str
    title: dict
    sdk: str = "1.3.1"
    description: dict = None
    vendor: str = "chariot"
    tags: List[str] = []
    types: dict = None
    connection: dict = None
    actions: dict = None
    triggers: dict = None
    alarm_receivers: dict = None
    indicator_receivers: dict = None
    asset_receivers: dict = None


class FUNC_SET_MODEL(BaseModel):
    func_id: str
    func_code: str


class CODE_DICT_MODEL(BaseModel):
    actions: List[FUNC_SET_MODEL] = []
    triggers: List[FUNC_SET_MODEL] = []
    alarm_receivers: List[FUNC_SET_MODEL] = []
    indicator_receivers: List[FUNC_SET_MODEL] = []
    asset_receivers: List[FUNC_SET_MODEL] = []


class PLUGIN_CONSTRUCTION_MODEL(BaseModel):
    plugin_data: PLUGIN_DATA_MODEL
    plugin_code: CODE_DICT_MODEL
