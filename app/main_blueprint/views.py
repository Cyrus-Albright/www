# -*- coding:utf-8 -*-
from flask import render_template, send_from_directory, send_file, \
    request, make_response, current_app
from flask import __version__ as flask_version
import requests
import os
import json
from time import time
## 从项目顶层导入包，不能使用相对路径（...tools.tools），需使用绝对路径，或直接导入对应名称
from tools.tools import struct_time, get_readable_file_size
from . import main


## Get Configuration
FILECACHEDIR = current_app.config.get("FILECACHEDIR")


if not os.path.exists(FILECACHEDIR):
    os.mkdir(FILECACHEDIR)


@main.route("/", methods=["GET"])
def index():
    return render_template("index.html")


## 云端后台下载，Pythonanywhere免费账号只用来下载github文件
@main.route("/clouddownload", methods=["POST"])
def clouddownload():
    url = request.form.get("url")
    print(f"[云端下载]开始下载:{url}")
    # 取消SSL验证，避免下载github文件错误
    req = requests.get(url, verify=False)
    # 获取远端文件名称
    if "Content-Disposition" in req.headers and req.headers["Content-Disposition"]:
        filename = req.headers["Content-Disposition"].split(";")[
            1].split("=")[1]
    else:
        filename = os.path.basename(url)
    if not filename:
        ## 未找到文件名，就用时间戳代替
        filename = str(int(time()))
    filepath = os.path.join(FILECACHEDIR, filename)
    with open(filepath, "wb") as f:
        f.write(req.content)
    print(f"[云端下载]下载完成:{url}")
    return f"[云端下载]下载完成:{url}", 200


## 列示FILECACHEDIR文件夹下的所有文件
@main.route("/listfile", methods=["GET"])
def listfile():
    filelist = os.listdir(FILECACHEDIR)
    fileinfolist = []
    for filename in filelist:
        filestat = os.stat(os.path.join(FILECACHEDIR, filename))
        ## 获取文件大小，以可读格式KB/MB/GB展示
        filesize = get_readable_file_size(filestat.st_size)
        ## 获取文件最后修改时间
        filectime = struct_time(filestat.st_ctime)
        fileinfo = {"filename": filename,
                    "lastmodified": filectime, "size": filesize}
        fileinfolist.append(fileinfo)
    ## 以json格式返回响应
    response = make_response(json.dumps({"fileinfolist": fileinfolist}))
    response.headers["Content-Type"] = "text/json"
    return response


## 从服务器FILECACHEDIR文件夹下载文件
@main.route("/download", methods=["GET", "POST"])
def downloadfile():
    print("[Route:download()]Start...")
    filename = request.args.get("filename")
    if not os.path.exists(os.path.join(FILECACHEDIR, filename)):
        return "No such file", 404
    ## 获取文件完整路径
    absfilepath = os.path.join(os.path.abspath(FILECACHEDIR), filename)
    print(f"dir:{FILECACHEDIR}, filename:{filename}, abspath:{absfilepath}")
    # print("isfile:{}".format(os.path.isfile(absfilepath)))
    try:
        ## send_from_directory函数中的文件名参数，在flask2.x版本中是path=文件名称，在flask1.x中是filename=完整文件路径
        if flask_version.startswith("2."):
            response = make_response(send_from_directory(
                directory=FILECACHEDIR, path=filename, as_attachment=True))
        elif flask_version.startswith("1."):
            ## (python3.7 flask1.0) test ok:
            response = make_response(send_from_directory(
                directory=FILECACHEDIR, filename=filename, as_attachment=True))
        else:
            # send_file有安全隐患，使用send_from_directory确保只从指定的文件夹发送文件
            response = send_file(absfilepath, as_attachment=True)
        ## 添加中文文件名支持
        response.headers["Content-Disposition"] = "attachment; filename={}".format(
            filename.encode().decode('latin-1'))
        return response
    except Exception as e:
        print(f"Exception occured: {str(e)}")
        return f"Exception occured: {str(e)}", 500


## 删除服务器FILECACHEDIR中的文件
@main.route("/deletefile", methods=["POST"])
def deletefile():
    print(f"[Route:deletefile()]Start...")
    filename = request.form.get("filename")
    ## 获取文件完整路径
    absfilepath = os.path.join(os.path.abspath(FILECACHEDIR), filename)
    print(
        f"[Route:deletefile()]dir:{FILECACHEDIR}, filename:{filename}, abspath:{absfilepath}")
    ## 判断文件是否存在
    if not os.path.exists(absfilepath):
        return "No such file", 404
    ## 尝试删除文件
    try:
        os.remove(absfilepath)
    except Exception as e:
        return "[Route:deletefile()]Exception occured: File Remove Error", 500
    ## 删除完成返回文件名作为响应
    print(f"[Route:deletefile()]file:{filename} has been deleted!")
    return make_response(json.dumps({"filename": filename}))

