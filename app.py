# -*- coding:utf-8 -*-
from flask import Flask, render_template, send_from_directory, send_file, \
    request, make_response
from flask import __version__ as flask_version
import requests
import os
import json
from time import time

app = Flask(__name__)

# Configuration
app.config["filecachedir"] = "downloadfile"

# get config
filedir = app.config.get("filecachedir")
if not os.path.exists(filedir):
    os.mkdir(filedir)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/clouddownload", methods=["POST"])
def clouddownload():
    url = request.form.get("url")
    print(f"开始下载:{url}")
    # do download
    # 取消SSL验证，避免下载github文件错误
    req = requests.get(url, verify=False)
    # 获取远端文件名称
    if "Content-Disposition" in req.headers and req.headers["Content-Disposition"]:
        filename = req.headers["Content-Disposition"].split(";")[
            1].split("=")[1]
    else:
        filename = os.path.basename(url)
    if not filename:
        filename = str(int(time()))
    filepath = os.path.join(filedir, filename)
    with open(filepath, "wb") as f:
        f.write(req.content)
    print(f"下载完成:{url}")
    return f"下载完成:{url}", 200


@app.route("/listfile", methods=["GET"])
def listfile():
    filelist = os.listdir(filedir)
    # TODO: 添加文件lastmodifieddate, 文件大小size
    # fileinfolist = []
    # for filename in filelist:
    # filestate = {"filename":filename, "lastmodifieddate":lastmodifieddate, "size":size}
    # fileinfolist.append(filestate)
    # response = make_response(json.dumps(fileinfolist))
    response = make_response(json.dumps(filelist))
    response.headers["Content-type"] = "text/json"
    return response


@app.route("/download", methods=["GET", "POST"])
def downloadfile():
    print("[Route:download()]Start...")
    filename = request.args.get("filename")
    if not os.path.exists(os.path.join(filedir, filename)):
        return "No such file", 404
    # 获取文件完整路径
    absfilepath = os.path.join(os.path.abspath(filedir), filename)
    print(f"dir:{filedir}, filename:{filename}, abspath:{absfilepath}")
    # print(f"absfilepath: {absfilepath}")
    # print("isfile:{}".format(os.path.isfile(absfilepath)))
    try:
        # print(f"directory:{os.path.abspath(filedir)}, filename:{filename}")
        # send_from_directory函数中的文件名参数，在flask2.x版本中是path=文件名称，在flask1.x中是filename=完整文件路径
        if flask_version.startswith("2."):
            response = make_response(send_from_directory(
                directory=filedir, path=filename, as_attachment=True))
        elif flask_version.startswith("1."):
            response = make_response(send_from_directory(
                directory=filedir, filename=filename, as_attachment=True))
        else:
            # send_file有安全隐患，使用send_from_directory确保只从指定的文件夹发送文件
            response = send_file(absfilepath, as_attachment=True)
        # python3.7 flask1.0 test ok:
        # response = send_from_directory(
        #     directory=filedir, filename=filename, as_attachment=True)
        # 添加中文文件名支持
        response.headers["Content-Disposition"] = "attachment; filename={}".format(
            filename.encode().decode('latin-1'))
        return response
    except Exception as e:
        print(f"Exception occured: {str(e)}")
        return f"Exception occured: {str(e)}", 500


@app.route("/deletefile", methods=["POST"])
def deletefile():
    print(f"[Route:deletefile()]Start...")
    filename = request.form.get("filename")
    # 获取文件完整路径
    absfilepath = os.path.join(os.path.abspath(filedir), filename)
    print(
        f"[Route:deletefile()]dir:{filedir}, filename:{filename}, abspath:{absfilepath}")

    if not os.path.exists(absfilepath):
        return "No such file", 404

    try:
        os.remove(absfilepath)
    except Exception as e:
        return "[Route:deletefile()]Exception occured: File remove error", 500

    print(f"[Route:deletefile()]file:{filename} has been deleted!")
    return make_response(json.dumps({"filename": filename}))


if __name__ == "__main__":
    app.run("0.0.0.0", 8000)
