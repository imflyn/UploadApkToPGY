import json
import os
import requests

workspace = "C:\\Users\\Flyn\\.jenkins\\workspace\\Android Employee"

apk_path = workspace + "\\employee\\build\outputs\\apk"


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
                    print("apk 文件上传成功 链接为：https://www.pgyer.com/" + json.loads(response)['data']['buildShortcutUrl'])
                else:
                    print("apk 文件上传到蒲公英失败！！")


if __name__ == '__main__':
    upload_file(apk_path)
