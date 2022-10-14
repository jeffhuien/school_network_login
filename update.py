# -*- coding: utf-8 -*-
# Author: GAO--HUI
# Date: 2022-10-02 16:19:05
# LastEditors: GAO--HUI
# LastEditTime: 2022-10-14 22:34:35
# FilePath: \新版本\update.py


from cmath import inf
import configparser
import os
from xml.dom.minidom import parse

import bs4
import requests


def getlocalversion() -> str:
    """获取本地浏览器的版本号"""
    dom = parse(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.VisualElementsManifest.xml")
    rootNode = dom.documentElement
    data = rootNode.getElementsByTagName("VisualElements")
    for i in data:
        version = i.getAttribute("Square150x150Logo")
    version = version.split("\\")
    return version[0]


def get_new_version():
    """获取最新同大版本的小版本"""

    url = "https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/"
    html = requests.get(url)
    html.encoding = "utf-8"
    soup = bs4.BeautifulSoup(html.text, "html.parser")
    f = soup.select(".driver-download__meta")
    for i in f:
        if getlocalversion()[0:3] in str(i):
            a = i
            break

    return a.text.split(":")[1][1::]


def check():
    """检查是否有驱动"""
    for i, j, k in os.walk(os.getcwd()):
        if "msedgedriver.exe" not in k:
            return False
        else:
            return True


def download(url, filename):
    """下载驱动文件"""
    data = requests.get(url, stream=True)

    with open(filename, "wb") as f:
        for i in data.iter_content(8):
            f.write(i)


def update(checked=False):
    """检查更新并下载"""
    url = f"https://msedgedriver.azureedge.net/{get_new_version()}/edgedriver_win64.zip"
    info = configparser.ConfigParser()
    info.read("userinfo.ini")
    now_version = info.get("driver_version", "version")
    version = get_new_version()

    print("now_version:", now_version)

    if now_version != version or checked:
        print("版本不一致")
        print()
        print()
        print()
        print("更新中：请勿关闭窗口")

        update_link = url
        download(update_link, filename="edgedriver_win64.zip")
        print("更新完成")

        info.set("driver_version", "version", version)

        info.write(open("userinfo.ini", "r+", encoding="utf-8"))
        print("new_version:", version)
        unzip()


def unzip():
    """解压文件"""
    import zipfile

    with zipfile.ZipFile("edgedriver_win64.zip") as zf:
        zf.extractall()

    os.remove("edgedriver_win64.zip")
