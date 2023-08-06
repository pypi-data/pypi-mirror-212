import os
import yaml
from fastapi import FastAPI, File, Request
from fastapi.responses import JSONResponse
import uvicorn
import typing
import multiprocessing
from . import VERSION
from .models import *
from .base import *
from importlib import reload
from signal import SIGINT

####
#
#   插件的API服务
#   全局变量前面请加下划线，这些变量应该只被web.py内方法调用
#   --预计在将来某一个版本中被另外一种方法替代-- (这行划去)
#   计划总赶不上变化不是吗
#
####

_rest_server = FastAPI(title="千乘插件API接口", version=VERSION, description="")


@_rest_server.post("/actions/{action_name}", tags=["动作"])
async def actions(action_name, plugin_stdin: typing.Optional[ACTION_TEST_MODEL]):
    """
    #   动作接口
    """
    clearLog(clear_size=1)

    action = loadModule(action_name, "actions")

    if not action:
        log("error", f"无法导入功能：{action_name}")
        content = {
            "msg": f"无法导入功能：{action_name}",
            "status": "False"
        }
        return JSONResponse(content=content, status_code=400)

    #   取出body
    data = plugin_stdin.dict()
    checkModel(data, PLUGIN_TEST_MODEL)
    data_body = data.get("body")

    #   获取input
    input_data = data_body.get("input")
    connection_data = data_body.get("connection")

    #   执行 run 相关操作
    output = action._run(input_data, connection_data, data_body.get("config"))

    if output["body"]["status"] != "True":
        return JSONResponse(content=output, status_code=500)
    else:
        return output


@_rest_server.post("/actions/{action_name}/test", tags=["动作"])
async def actions_test(action_name: str, plugin_stdin: typing.Optional[ACTION_TEST_MODEL]):
    """
    #   动作连接器测试接口
    """
    return rest_test("actions", action_name, plugin_stdin)


@_rest_server.post("/triggers/{trigger_name}", tags=["触发器"])
async def triggers(trigger_name: str, plugin_stdin: typing.Optional[TRIGGER_TEST_MODEL]):
    """
    #   触发器接口
    """
    return createReceivers("triggers", trigger_name, plugin_stdin)


@_rest_server.post("/triggers/{trigger_name}/test", tags=["触发器"])
async def trigger_test(trigger_name: str, plugin_stdin: typing.Optional[TRIGGER_TEST_MODEL]):
    """
    #   触发器连接器测试接口
    """
    return rest_test("triggers", trigger_name, plugin_stdin)


@_rest_server.post("/alarm_receivers/{alarm_receiver_name}", tags=["告警接收器"])
async def alarm_receivers(alarm_receiver_name: str, plugin_stdin: typing.Optional[ALARM_RECEIVER_TEST_MODEL]):
    """
    #   告警接收器接口
    """
    return createReceivers("alarm_receivers", alarm_receiver_name, plugin_stdin)


@_rest_server.post("/alarm_receivers/{alarm_receiver_name}/test", tags=["告警接收器"])
async def alarm_receivers_test(alarm_receiver_name: str,
                               plugin_stdin: typing.Optional[ALARM_RECEIVER_TEST_MODEL]):
    """
    #   告警接收器连接器测试接口
    """
    return rest_test("alarm_receivers", alarm_receiver_name, plugin_stdin)


@_rest_server.post("/indicator_receivers/{indicator_receiver_name}", tags=["情报接收器"])
async def indicator_receivers(indicator_receiver_name: str,
                              plugin_stdin: typing.Optional[INDICATOR_RECEIVER_TEST_MODEL]):
    """
    #   情报接收器接口
    """
    return createReceivers("indicator_receivers", indicator_receiver_name, plugin_stdin)


@_rest_server.post("/indicator_receivers/{indicator_receiver_name}/test", tags=["情报接收器"])
async def indicator_receivers_test(indicator_receiver_name: str,
                                   plugin_stdin: typing.Optional[INDICATOR_RECEIVER_TEST_MODEL]):
    """
    #   情报接收器连接器测试接口
    """
    return rest_test("indicator_receivers", indicator_receiver_name, plugin_stdin)


@_rest_server.post("/asset_receivers/{asset_receiver_name}", tags=["资产接收器"])
async def asset_receivers(asset_receiver_name: str,
                          plugin_stdin: typing.Optional[ASSET_RECEIVER_TEST_MODEL]):
    """
    #   资产接收器接口
    """
    return createReceivers("asset_receivers", asset_receiver_name, plugin_stdin)


@_rest_server.post("/asset_receivers/{asset_receiver_name}/test", tags=["资产接收器"])
async def asset_receivers_test(asset_receiver_name: str,
                               plugin_stdin: typing.Optional[ASSET_RECEIVER_TEST_MODEL]):
    """
    #   资产接收器连接器测试接口
    """
    return rest_test("asset_receivers", asset_receiver_name, plugin_stdin)


@_rest_server.post("/shutdown_receivers", tags=["插件编辑"])
async def shutdown_receivers():
    """
    #   关闭接收器
    """
    try:
        pid_data = getLocalCache("receiver_pid")
        os.kill(pid_data["pid"], SIGINT)
        log("info", "退出完成")

        setLocalCache({"pid": None}, "receiver_pid")

        content = {
            "msg": "退出完成"
        }
        return JSONResponse(content=content, status_code=200)

    except Exception as error:
        log("warning", "退出失败，可能没有接收器正在运行？")

        setLocalCache({"pid": None}, "receiver_pid")

        content = {
            "msg": "退出失败，可能没有接收器正在运行？"
        }
        return JSONResponse(content=content, status_code=404)


@_rest_server.post("/update_plugin", tags=["插件热更新"])
async def update_plugin(update_pack: bytes = File()):
    """
    #   上传更新包
    """
    try:
        save_update_pack(update_pack)
        update_result = hotUpdate("http")
        clearUpdateFile()
        if update_result:
            return {
                "msg": "更新完成"
            }
        else:
            return {
                "msg": "更新失败"
            }
    except Exception as error:
        clearUpdateFile()
        content = {
            "msg": f"更新失败 - {error}"
        }
        return JSONResponse(content=content, status_code=500)


@_rest_server.post("/editor/plugin", tags=["插件编辑"])
async def post_plugin(plugin_construction: PLUGIN_CONSTRUCTION_MODEL):
    """
    #   初始化插件
    """

    clearLog(clear_size=1)

    work_path = os.getcwd()

    plugin_construction = plugin_construction.dict()

    plugin_data = plugin_construction["plugin_data"]

    yaml_path = os.path.join(work_path, "plugin.spec.yaml")

    with open(yaml_path, "w", encoding="utf-8") as file:
        yaml.dump(plugin_data, file, encoding="utf-8",
                  allow_unicode=True, sort_keys=False)

    result = os.system("chariot-plugin -ag plugin.spec.yaml")

    if result:
        content = {
            "msg": "插件初始化失败，请查看日志以排除错误"
        }
        return JSONResponse(content=content, status_code=400)

    codes = plugin_construction["plugin_code"]

    error_dict = {}

    dir_and_code = []

    #   先遍历检查一遍，防止重复或错误操作
    #   遍历要更新的组件列表的方法和代码
    for module, func_list in codes.items():
        #   遍历要更新的方法
        for func in func_list:
            module_file_path = os.path.join(work_path, module, (func["func_id"] + ".py"))
            #   当方法不存在时记录在案
            if not os.path.exists(module_file_path):
                try:
                    error_dict[module].append(func["func_id"])
                except:
                    error_dict[module] = []
                    error_dict[module].append(func["func_id"])
            else:
                dir_and_code.append((module_file_path, func["func_code"]))

    #   当有方法不存在时就放弃所有更新
    if error_dict:
        content = {
            "msg": "部分功能未记录在定义文件，已结束插件初始化",
            "not_found": error_dict
        }
        return JSONResponse(content=content, status_code=400)

    try:
        for func_path, func_code in dir_and_code:
            with open(func_path, "w", encoding="utf-8") as file:
                file.write(func_code)
        return {
            "msg": "插件生成完成"
        }
    except Exception as error:
        content = {
            "msg": f"代码写入失败 - {error}"
        }
        return JSONResponse(content=content, status_code=500)


@_rest_server.get("/editor/plugin", tags=["插件编辑"])
async def get_plugin():
    clearLog(clear_size=1)

    work_path = os.getcwd()

    modules_dir = ["actions", "triggers", "alarm_receivers", "indicator_receivers", "asset_receivers"]

    modules_dict = {}

    try:

        for temp_module in modules_dir:

            modules_dict[temp_module] = []

            modules_dir_path = os.path.join(work_path, temp_module)

            if not os.path.exists(modules_dir_path):
                continue

            module_files = os.listdir(modules_dir_path)

            ignore_files = ["models.py", "__init__.py", "__pycache__"]

            for ignore_file in ignore_files:
                if ignore_file in module_files:
                    module_files.pop(module_files.index(ignore_file))

            for module_file in module_files:
                module_file_path = os.path.join(modules_dir_path, module_file)

                with open(module_file_path, "r", encoding="utf-8") as module_file_code:
                    modules_dict[temp_module].append({
                        "func_id": module_file.replace(".py", ""),
                        "func_code": module_file_code.read()
                    })
    except Exception as error:
        content = {
            "msg": f"功能代码读取失败 - {error}"
        }
        return JSONResponse(content=content, status_code=500)

    plugin_data = getPluginData()

    if not plugin_data:
        log("error", "插件定义数据不存在")
        content = {
            "msg": "插件定义数据不存在"
        }
        return JSONResponse(content=content, status_code=404)

    return {
        "plugin_data": plugin_data,
        "plugin_code": modules_dict
    }


@_rest_server.get("/sdk_version", tags=["插件信息"])
async def sdk_version():
    """
    #   获取SDK版本
    """
    return {
        "sdk_version": VERSION
    }


@_rest_server.get("/plugin_data", tags=["插件信息"])
async def get_plugin_data():
    """
    #   获取插件定义数据接口
    """

    plugin_data = getPluginData()

    if plugin_data:
        return plugin_data

    else:
        log("error", "插件定义数据不存在")
        content = {
            "error": "插件定义数据不存在"
        }
        return JSONResponse(content=content, status_code=404)


@_rest_server.post("/transpond", tags=["转发数据接收"])
async def receive_transpond(request: Request):
    """
    #   测试用接口，用于接收转发的数据
    """
    try:
        data = await request.body()
        log("attention", f"获得转发数据：\n {json.loads(data.decode())}")
        resp_data = {
            "msg": "接收成功",
            "error": ""
        }
        return JSONResponse(content=resp_data)
    except Exception as error:
        resp_data = {
            "msg": "接收失败",
            "error": str(error)
        }
        return JSONResponse(content=resp_data, status_code=500)


def loadModule(func_id, module):
    """
    #   尝试重载各个组件
    参数说明
    func_id:str,      #   方法名
    module:str,         #   组件

    如果无法找到方法或组件则返回None
    """

    if module == "actions":
        #   在生成插件之后有actions就能成功import了
        try:
            import actions
            #   先初始化并释放一次功能类，以清空缓存
            actions.modules_dict()[func_id]()
            #   清空完再reload
            reload(actions)
            return actions.modules_dict()[func_id]()
        except:
            log("error", traceback.format_exc())

    elif module == "triggers":
        #   通过接口创建的接收器进程会重新加载文件，所以无需reload和清缓存
        try:
            import triggers
            return triggers.modules_dict()[func_id]()
        except:
            log("error", traceback.format_exc())

    elif module == "alarm_receivers":
        try:
            import alarm_receivers
            return alarm_receivers.modules_dict()[func_id]()
        except:
            log("error", traceback.format_exc())

    elif module == "indicator_receivers":
        try:
            import indicator_receivers
            return indicator_receivers.modules_dict()[func_id]()
        except:
            log("error", traceback.format_exc())

    elif module == "asset_receivers":
        try:
            import asset_receivers
            return asset_receivers.modules_dict()[func_id]()
        except:
            log("error", traceback.format_exc())

    return None


def rest_test(module, func_id, plugin_stdin):
    """
    #   通用的连接器测试方法
    参数说明：
    module:str,         #   组件，module = action,trigger,alarm_receiver,indicator_receiver,asset_receiver
    func_id:str,  #   方法id
    plugin_stdin:str,   #   接口传入数据

    因为测试连接器流程一样
    所有使用一个通用方法进行维护
    """

    clearLog(clear_size=1)

    func = loadModule(func_id, module)

    if not func:
        log("error", f"无法导入功能：{func_id}")
        content = {
            "msg": "无法导入功能：{func_id}"
        }
        return JSONResponse(content=content, status_code=400)

    #   取出body
    data = plugin_stdin.dict()
    data_body = data.get("body")

    connection_data = data_body.get("connection")

    if data_body.get("config"):
        log("info", "获取请求中配置信息")
        loadConfig(data_body["config"])
    else:
        log("info", "请求中无配置信息，使用默认配置")
        loadConfig()

    output = func._test(connection_data)

    if output["body"]["status"] != "True":
        return JSONResponse(content=output, status_code=500)
    else:
        return output


def createReceivers(module, receiver_name, plugin_stdin):
    """
    #   通用接收器方法
    参数说明：
    module:str,         #   组件，module = trigger,alarm_receiver,indicator_receiver,asset_receiver
    receiver_name:str,  #   接收器名称
    plugin_stdin:str,   #   接口传入数据

    因为触发器、告警接收器、情报接收器、资产接收器代码重复率极高（或者可以说一模一样的），
    因此使用一个通用方法进行维护
    """

    clearLog(clear_size=1)

    module_dict = {
        "triggers": "触发器",
        "indicator_receivers": "情报接收器",
        "alarm_receivers": "告警接收器",
        "asset_receivers": "资产接收器"
    }

    data = plugin_stdin.dict()

    try:

        plugin_data = getPluginData()

        if not plugin_data.get(module, {}).get(receiver_name):
            log("error", f"无法在{module_dict[module]}下找到该功能：{receiver_name}")
            content = {
                "msg": f"无法在{module_dict[module]}下找到该功能：{receiver_name}"
            }
            return JSONResponse(content=content, status_code=404)

        process = multiprocessing.Process(target=receiverProcess, args=(module, receiver_name, data))

        process.start()

        #   先鲨了之前创建的接收器，千乘只允许一个容器跑一个接收器
        log("attention", "尝试退出之前创建的接收器")
        try:
            pid_data = getLocalCache("receiver_pid")
            os.kill(pid_data["pid"], SIGINT)
            log("info", "退出完成")
            log("info", "缓存本次接收器信息")
            setLocalCache({"pid": process.pid}, "receiver_pid")
        except:
            log("warning", "退出失败，第一次创建接收器请忽略此警告")
            log("info", "缓存本次接收器信息")
            setLocalCache({"pid": process.pid}, "receiver_pid")

    except Exception as error:

        from .base import _log_data

        log("error", f"{error}")

        content = {
            "version": "v1",
            "type": data["type"],
            "body": {
                "status": "False",
                "log": _log_data,
                "error_trace": traceback.format_exc(),
                "msg": f"{module_dict[module]}创建失败"
            }
        }

        return JSONResponse(content=content, status_code=500)

    from .base import _log_data

    content = {
        "version": "v1",
        "type": data["type"],
        "body": {
            "status": "True",
            "log": _log_data,
            "error_trace": "",
            "msg": f"{module_dict[module]}已创建完成"
        }
    }

    return JSONResponse(content=content, status_code=201)


def receiverProcess(module, receiver_name, data):
    """
    #   此方法用于创建各类接收器进程
    参数说明：
    module:str,         #   组件，module = trigger,alarm_receiver,indicator_receiver,asset_receiver
    receiver_name:str,  #   接收器名称
    data:dict,  #   接收的数据
    """

    receiver = loadModule(receiver_name, module)
    if not receiver:
        log("error", f"无法导入功能：{receiver_name}")
        content = {
            "msg": f"无法导入功能：{receiver_name}"
        }
        return JSONResponse(content=content, status_code=400)

    #   data中的body部分
    data_body = data.get("body")
    #   run输入参数
    input_data = data_body.get("input")
    #   连接器参数
    connection_data = data_body.get("connection")
    #   转发地址
    dispatcher_url = data_body.get("dispatcher").get("url")
    #   缓存地址
    cache_url = data_body.get("dispatcher").get("cache_url")

    receiver._run(input_data, connection_data, dispatcher_url, cache_url, data_body.get("config"))


def runserver(workers):
    """
    #   启动api服务
    参数说明：
    workers:int,    #   工作进程数量
    """
    log("attention", "在浏览器内输入 http://127.0.0.1:10001/docs 以进行接口测试")
    uvicorn.run("SDK.web:_rest_server", host="0.0.0.0", port=10001, workers=workers)
