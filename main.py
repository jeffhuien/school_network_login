# -*- coding: utf-8 -*-
# Author: GAO--HUI
# Date: 2022-09-01 18:19:30
#LastEditors: GAO--HUI
#LastEditTime: 2022-09-16 11:33:30
#FilePath: \自动登录校园网\main.py


import os
import sys
import time
import configparser

# from func_timeout import func_set_timeout

# import selenium  # 第三方库  pip install selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# 驱动更新
# https://msedgedriver.azureedge.net/105.0.1343.42/edgedriver_win64.zip


def read():
    # 创建管理对象
    conf = configparser.ConfigParser()
    # 读ini文件
    conf.read("acc.ini", encoding="utf-8")  # python3
    items = conf.items("acc_data")

    return items


# @func_set_timeout(5)
def submit(Uname, Upsd, Uway):
    # 实例化浏览器对象
    # option = Options()
    # option.page_load_strategy = "eager"
    url = "http://10.1.1.1"
    drive = webdriver.Edge(service=Service(executable_path="msedgedriver.exe"))
    # drive = webdriver.Chrome(service=Service(executable_path="chromedriver.exe"))
    drive.get(url)
    print(drive.title)

    drive.find_element(by=By.XPATH, value="/html/body/div[2]/form/div/div[1]/input[1]").send_keys(Uname)
    drive.find_element(by=By.XPATH, value="/html/body/div[2]/form/div/div[2]/input").send_keys(Upsd)
    drive.find_element(by=By.XPATH, value=f"/html/body/div[2]/form/div/div[4]/span[{Uway}]/label/input").click()
    # print("单击了运营商")
    drive.find_element(by=By.XPATH, value="/html/body/div[2]/form/div/div[5]/input").click()
    # print("单击了提交按钮")
    print(drive.title)
    drive.quit()


items = read()
Uname = items[0][1]
Upsd = items[1][1]
Uway = items[2][1]


submit(Uname, Upsd, Uway)

# os._exit()
