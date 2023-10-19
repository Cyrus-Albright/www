from random import randint
from time import strftime, localtime
import os


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


# 查询剩余空间，查询downloadfile文件夹大小
def diskspaceusage(dir):
    if not os.path.isdir(dir):
        return "Not Avaliable Directory"
    return os.path.getsize(dir)


def downloadfile_dir_usage():
    return os.path.getsize("/home/cyrus/project/www/downloadfile")


def user_dir_usage():
    return os.path.getsize("/home/cyrus")
