# -*- coding: utf-8 -*-
# Author: GAO--HUI
# Date: 2022-10-02 13:27:33
# LastEditors: GAO--HUI
# LastEditTime: 2022-10-14 22:32:53
# FilePath: \新版本\login.py

import configparser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import os
from update import getlocalversion


def check():
    for i, j, k in os.walk(os.getcwd()):
        if "userinfo.ini" not in k:
            return False
        else:
            return True


def write_info():

    print("第一次运行需要输入个人信息哦~")
    print("如果后续一次连接不成功，可以再次尝试")
    username = input("请输入用户名：")
    userpassword = input("请输入密码：")
    userway = input("请输入运营商【移动输1，联通输2，电信输3】：")
    info = configparser.ConfigParser()

    info.add_section("userinfo")
    info.add_section("driver_version")

    info.set("userinfo", "username", username)
    info.set("userinfo", "userpassword", userpassword)
    info.set("userinfo", "userway", userway)
    info.set("driver_version", "version", getlocalversion())

    with open("userinfo.ini", "w", encoding="utf-8") as f:
        info.write(f)


def read_info():
    info = configparser.ConfigParser()
    info.read("userinfo.ini")
    username = info.get("userinfo", "username")
    userpassword = info.get("userinfo", "userpassword")
    userway = info.get("userinfo", "userway")

    return [username, userpassword, userway]


def tesk():
    browser = webdriver.Edge(executable_path="msedgedriver.exe")
    username, userpassword, userway = read_info()
    try:
        browser.set_page_load_timeout(2)
        browser.get("http://10.0.0.1")

        browser.find_element(By.XPATH, "/html/body/div[2]/form/div/div[1]/input[1]").send_keys(username)

        browser.find_element(By.XPATH, "/html/body/div[2]/form/div/div[2]/input").send_keys(userpassword)

        browser.find_element(By.XPATH, f"/html/body/div[2]/form/div/div[4]/span[{userway}]/label/input").click()
        browser.find_element(By.XPATH, "/html/body/div[2]/form/div/div[5]/input").click()
    except TimeoutException:
        # 报错后就强制停止加载
        # 这里是js控制
        browser.execute_script("window.stop()")
    browser.quit()
