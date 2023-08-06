import json
import os

from chariotCore import VERSION
from chariotCore.tools import *
from chariotCore.templates import *
import traceback
import tarfile
import docker


def generate(work_path: str, file_path: str):
    """
    #   生成插件
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    file_path:str,    #   插件定义文件相对路径

    #   生成失败时显示错误log，并返回
    """

    log("info", f"正在使用千乘插件开发工具 v{VERSION} 生成插件")

    modules = [
        "actions",
        "triggers",
        "alarm_receivers",
        "indicator_receivers",
        "asset_receivers"
    ]

    try:

        #   读取插件定义文件
        data = readGenerateFile(work_path, file_path)

        #   生成基础文件
        generateBaseFile(work_path)

        #   生成tests文件夹
        tests_path = os.path.join(work_path, "tests")
        if not os.path.exists(tests_path):
            os.mkdir(tests_path)

        #   检测旧版本
        updateModuleFile(work_path)

        #   生成自定义类
        types = data.get("types")
        if types:
            #   生成自定义类的校验数据
            types_model = generateTypesModel(types)
        else:
            types_model = ""
            log("attention", "未检测到自定义类型，跳过自定义类型校验数据的生成")

        #   生成connection
        connection_params = data.get("connection")
        #   connection不存在也要生成一份校验数据，因为所有功能执行前默认跑一次连接器
        if not connection_params:
            connection_params = {}
        #   生成连接器的校验数据
        connection_model = generateConnectionModel(connection_params)
        #   获取参数列表，用于生成功能文件
        connection_keys = list(connection_params.keys())

        modules_list_dict = {
            "actions": [],
            "triggers": [],
            "alarm_receivers": [],
            "indicator_receivers": [],
            "asset_receivers": []
        }

        #   生成组件以及组件属下的功能
        for module in modules:
            func_class_name_list = generateModule(data, module, types_model, connection_model, connection_keys)
            modules_list_dict[module] = func_class_name_list

        #   生成入口文件 main.py
        plugin_name = data.get("name")
        generateMainFile(work_path, plugin_name, modules_list_dict)

        #   生成帮助文件
        generateHelpFile(data)

        #   生成通用文件存储的文件夹
        generateUtilFile(work_path)

        #   生成存储热更新包的文件夹
        generateUpdateFile(work_path)

    except Exception as error:
        log("error", f"{error}\n{traceback.format_exc()}")
        return

    log("info", "所有插件文件生成完成")


def autoGenerate(work_path, file_path: str):
    """
    #   生成插件
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    file_path:str,    #   特殊定义文件相对路径

    #   生成失败时显示错误log，并返回
    """

    modules = [
        "actions",
        "triggers",
        "alarm_receivers",
        "indicator_receivers",
        "asset_receivers"
    ]

    try:

        log("info", "读取插件数据中")

        try:
            file_read = open(os.path.join(work_path, file_path), "r", encoding="utf-8").read()
            if file_path.endswith(".sdkc") or file_path.endswith(".json"):
                data = json.loads(file_read)
            elif file_path.endswith(".yaml"):
                data = yaml.load(file_read, Loader=yaml.FullLoader)
            else:
                data = json.loads(file_read)
        except Exception as error:
            raise Exception(f"读取插件数据失败\n  失败原因：{error}")

        log("info", "读取完成")

        #   生成tests文件夹
        tests_path = os.path.join(work_path, "tests")
        if not os.path.exists(tests_path):
            os.mkdir(tests_path)

        #   生成自定义类
        types = data.get("types")
        if types:
            #   生成自定义类的校验数据
            types_model = generateTypesModel(types)
        else:
            types_model = ""
            log("attention", "未检测到自定义类型，跳过自定义类型校验数据的生成")

        #   生成connection
        connection_params = data.get("connection")
        #   connection不存在也要生成一份校验数据，因为所有功能执行前默认跑一次连接器
        if not connection_params:
            connection_params = {}
        #   生成连接器的校验数据
        connection_model = generateConnectionModel(connection_params)
        #   获取参数列表，用于生成功能文件
        connection_keys = list(connection_params.keys())

        modules_list_dict = {
            "actions": [],
            "triggers": [],
            "alarm_receivers": [],
            "indicator_receivers": [],
            "asset_receivers": []
        }

        #   删除老旧文件
        deleteOldFile(modules_list_dict)

        #   生成组件以及组件属下的功能
        for module in modules:
            func_class_name_list = generateModule(data, module, types_model, connection_model, connection_keys)
            modules_list_dict[module] = func_class_name_list

        #   生成入口文件 main.py
        plugin_name = data.get("name")
        generateMainFile(work_path, plugin_name, modules_list_dict)

        #   生成帮助文件
        generateHelpFile(data)

        #   生成通用文件存储的文件夹
        generateUtilFile(work_path)

        #   生成存储热更新包的文件夹
        generateUpdateFile(work_path)

    except Exception as error:
        log("error", f"{error}\n{traceback.format_exc()}")
        return 1

    log("info", "所有插件文件生成完成")
    return 0


def generateYaml(work_path: str):
    """
    #   在当前工作目录下生成一个yaml模板文件
    参数说明：
    work_path:str,    #   当前工作区绝对路径

    """
    try:
        #   获取res文件夹
        res_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "res")
        #   获取plugin.spec.yaml模板文件
        yaml_template = os.path.join(res_dir, "plugin.spec.yaml")
        #   生成位置
        file_path = os.path.join(work_path, "plugin.spec.yaml")

        #   若文件存在则跳过生成
        if os.path.exists(file_path):
            log("attention", rf"\plugin.spec.yaml 已存在，跳过生成")
            return
        else:
            shutil.copy2(yaml_template, file_path)
        log("info", rf"\plugin.spec.yaml 生成完成")
    except Exception as error:
        raise Exception(rf"\plugin.spec.yaml 生成失败，错误未知：" + f"\n{error}")


def run(work_path: str, test_path: str):
    """
    #   运行插件指定功能
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    test_path:str,    #   测试用的数据文件的相对路径

    """

    log("info", f"正在根据 {test_path} 的数据运行功能")

    main_path = os.path.join(work_path, "main.py")

    test_path = os.path.join(work_path, test_path)

    if not os.path.exists(test_path):
        raise Exception(f"测试文件路径错误：\n{test_path}")

    else:
        cmd = f"python {main_path} run {test_path}"
        os.system(cmd)


def http(work_path: str, workers: int = 4):
    """
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    workers:int,    #   工作进程数量
    """
    main_path = os.path.join(work_path, "main.py")

    cmd = f"python {main_path} http {workers}"
    os.system(cmd)


def test(work_path: str, tests: str):
    """
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    tests:str,    #   测试用的数据文件的相对路径

    """
    main_path = os.path.join(work_path, "main.py")
    test_path = os.path.join(work_path, tests)

    if not os.path.exists(test_path):
        log("error", f"请正确输入路径")

    cmd = f"python {main_path} test {test_path}"
    os.system(cmd)


def tarball(work_path: str):
    """
    参数说明：
    work_path:str,    #   当前工作区绝对路径
    """
    log("info", "创建在线包中")

    tarballOnlinePack()

    log("info", "创建完成")


def mkimg(os_arch: str):
    """
    参数说明：
    os_arch:str,    #   平台，不填默认根据目前开发环境进行选择，例如：linux/386，linux/arm64，linux/arm/v7
    """
    log("info", "创建离线包中")

    work_path = os.getcwd()

    #   builds文件夹用于放置构建好的包
    builds_dir_path = os.path.join(work_path, "builds")

    #   需要打包的文件
    #   以元组形式放入 (相对目录, 打包后在压缩包内的文件名)
    #   打包后在压缩包内的文件名为千乘后端规定的
    files_to_tar = [
        ("plugin.spec.yaml", "plugin.spec.yaml"),
        ("icon.png", "icon.png"),
        ("help.md", "help.md"),
    ]

    #   临时镜像文件名
    temp_image = "temp_image.tar.gz"
    files_to_tar.append(
        (os.path.join("builds", temp_image), "plugin.tar.gz")
    )

    #   临时在线包文件名
    temp_tar = "temp_plugin.tar.gz"

    #   创建临时在线包
    #   这里调用此方法是为了利用打包在线包时的忽略不必要文件功能
    #   并通过RUN将在线包解压至容器内的工作目录
    data = tarballOnlinePack(temp_tar)

    #   获取插件定义文件中的元数据
    vendor = data["vendor"]
    name = data["name"]
    version = data["version"]

    #   创建Docker环境
    docker_client = docker.from_env()

    #   镜像标签
    tag = f"{vendor}/{name}:{version}"

    temp_plugin_tar = open(os.path.join(builds_dir_path, "temp_plugin.tar.gz"), "rb")

    log("info", "创建镜像中")
    docker_client.images.build(fileobj=temp_plugin_tar, pull=True, tag=tag, custom_context=True, platform=os_arch)
    log("info", "创建完成")

    temp_plugin_tar.close()

    log("info", "缓存镜像至本地")
    try:
        temp_image_path = os.path.join(builds_dir_path,temp_image)
        #   清除可能的残留文件
        if os.path.exists(temp_image_path):
            os.remove(temp_image_path)
        #   根据tag获取镜像
        image = docker_client.images.get(tag)
        image_data = image.attrs
        #   暂存镜像文件
        with open(temp_image_path, "wb") as file:
            for chunk in image.save(named=True):
                file.write(chunk)
    except Exception as error:
        raise Exception(f"缓存失败\n{error}")
    log("info", "缓存完成")

    log("info", "创建临时插件结构文件")
    plugin = {
        "plugin_data": data,
        "plugin_code": getAllModulesCode()
    }
    with open(os.path.join(work_path, "plugin.construction.json"), "w", encoding="utf-8") as file:
        json.dump(plugin, file, ensure_ascii=False)
        files_to_tar.append(("plugin.construction.json", "plugin.construction.json"))
    log("info", "创建完成")

    #   离线包文件名
    offline_name = f"{vendor}-" \
                   f"{name}-" \
                   f"{version}-" \
                   f"{(image_data['Os'] + '-') if image_data.get('Os') else ''}" \
                   f"{(image_data['Architecture'] + '-') if image_data.get('Architecture') else ''}" \
                   f"{(image_data['Variant'] + '-') if image_data.get('Variant') else ''}" \
                   f"offline.tar.gz"

    log("info", "打包必要文件")

    try:
        offline_tar_path = os.path.join(builds_dir_path,offline_name)
        #   清除可能的残留文件
        if os.path.exists(offline_tar_path):
            os.remove(offline_tar_path)
        with tarfile.open(offline_tar_path, "w:gz", format=tarfile.GNU_FORMAT) as tar:
            for file in files_to_tar:
                file_path = os.path.join(work_path, file[0])
                if os.path.exists(file_path):
                    tar.add(file_path, arcname=file[1])
                else:
                    raise Exception(f"{file}缺失")
    except Exception as error:
        raise Exception(f"打包失败\n{error}")

    log("info", "打包完成")
    log("info", "创建离线包完成")

    log("info", "清理临时文件中")
    clear_files = [
        os.path.join("builds", temp_image),
        os.path.join("builds", temp_tar),
        "plugin.construction.json"
    ]
    for file in clear_files:
        file_path = os.path.join(work_path, file)
        if os.path.exists(file_path) and not os.path.isdir(file_path):
            os.remove(file)
    log("info", "清理完成")
    return
