import json
import os
import requests
import time
import sys
import configparser
from mail_sender import MailSender

workspace = "C:\\Users\\Flyn\\.jenkins\\workspace\\Android Consumer"

apk_path = workspace + "\\consumer\\build\outputs\\apk"

mail_sender = MailSender()
configparser = configparser.ConfigParser()
configparser.read(os.path.dirname(os.path.realpath(__file__)) + '\\config.txt')
mail_sender.to_address = configparser.get("Info", "to_address").split(",")
mail_sender.from_address = configparser.get("Info", "from_address")
mail_sender.my_name = configparser.get("Info", "my_name")
mail_sender.password = configparser.get("Info", "password")
mail_sender.smtp_server = configparser.get("Info", "smtp_server")
mail_sender.smtp_server_port = configparser.get("Info", "smtp_server_port")

date = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))

BRANCH = sys.argv[1]
BUILD_TYPE = sys.argv[2]
FLAVORS = sys.argv[3]

print("BRANCH:  " + BRANCH)
print("BUILD_TYPE:  " + BUILD_TYPE)
print("FLAVORS:  " + FLAVORS)


def upload_file(path):
    parents = os.listdir(path)
    for parent in parents:
        child = os.path.join(path, parent)
        if os.path.isdir(child):
            upload_file(child)
        else:
            if child.endswith(".apk"):
                print(child)
                result = requests.post(
                    url="https://www.pgyer.com/apiv2/app/upload",
                    data={"_api_key": "8bc2faf1cea2b0aa0b18465fd3b7ed47",
                          },
                    files={"file": open(child, "rb")}
                )
                if result.status_code < 300:
                    response = result.text
                    print(response)
                    url = "https://www.pgyer.com/" + json.loads(response)['data']['buildShortcutUrl']
                    print("apk 文件上传成功 链接为：" + url)
                    mail_sender.send(
                        "[" + date + "] Android Consumer " + BRANCH + " " + FLAVORS + " " + BUILD_TYPE + " APK 下载文件 ",
                        "APK编译时间：" + date + "\n" +
                        "APK 下载链接：" + url,
                        lambda: print("发送邮件成功！！"),
                        lambda: print("发送邮件失败！！")
                    )
                else:
                    print("apk 文件上传到蒲公英失败！！")


if __name__ == '__main__':
    upload_file(apk_path)
