from random import randint
from time import strftime, localtime
import os
import subprocess
from flask import current_app


# 随机生成长度为randomlength的字符串
def generate_randomstr(randomlength=16):
    random_str = ""
    base_str = "abcdefghijklmkopqrstuvwxyz0123456789"
    length = len(base_str) - 1
    for i in range(randomlength):
        random_str += base_str[randint(0, length)]
    return random_str


# 将文件大小转换为可读格式，使用示例：
# print("可读格式文件大小：", get_readable_file_size(file_size))
def get_readable_file_size(file_size):
    # 定义文件大小单位
    units = ['B', 'KB', 'MB', 'GB', 'TB']

    # 遍历单位并将文件大小转换为相应单位
    for unit in units:
        if file_size < 1024:
            return f"{file_size:.2f} {unit}"
        file_size /= 1024

    return f"{file_size:.2f} {units[-1]}"


# 将日期转换为可读格式
def struct_time(timestr, formatstr="%Y-%m-%d %H:%M"):
    return strftime(formatstr, localtime(timestr))


# 查询占用空间，查询文件夹大小
def diskspaceusage(dir):
    if not os.path.exists(dir) or not os.path.isdir(dir):
        return "Not Avaliable Directory"
    # 使用系统du命令获取文件夹大小
    dir_size_info = subprocess.check_output(["du", "-sh", dir]).decode("utf-8")
    dir_size = dir_size_info.split("\t")[0]
    return dir_size


def get_systeminfo():
    uname = os.uname() #[sysname, nodename, release, version, machine]
    workdir = os.getcwd()
    workdir_usage = diskspaceusage(workdir)
    filecachedir = current_app.config.get("FILECACHEDIR")
    filecachedir_usage = diskspaceusage(filecachedir)
    return {"uname": uname, "workdir": workdir, "workdir_usage": workdir_usage,
        "filecachedir": filecachedir, "filecachedir_usage": filecachedir_usage}