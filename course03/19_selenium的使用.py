"""
    Selenium的文档见有道云笔记
    此节介绍具体使用：
        实现目标：
            1.模拟126邮箱登录
            2.获取相应的联系人信息并保存
            3.获取相应邮件信息并保存
"""
import json
import os
import pickle
from urllib.request import Request
from urllib.parse import urlencode
from fake_useragent import UserAgent
from urllib.request import build_opener, HTTPCookieProcessor
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

username = 'xlys_000'
pwd = '80105202xlys'
# 构造请求和w无头浏览器
login_page_url = 'https://mail.126.com/'

# headers = {
#     'User-Agent': UserAgent().chrome
# }
#
# request = Request(login_page_url, headers=headers)
options = webdriver.ChromeOptions().add_argument('--headless')
chrome = webdriver.Chrome(chrome_options=options)

# -------------------------------------------------发送请求进行登录-------------------------------------------------------------------------------------
# 发送请求
chrome.get(login_page_url)
time.sleep(5)
# chrome.save_screenshot(r'E:\Pythonlearning\PythonProjects\Spider_learning\Spider\testdata\shot.jpg')
# print(chrome.page_source)

# 拿到响应后定位元素并填充值
# 获取iframe嵌套页面src地址:此嵌套页面是真正的登录输入表单
# iframe_url = chrome.find_element(By.XPATH, '//div[@class="loginForm"]/div[1]/div[1]/iframe').get_attribute('src')
# print(iframe_url)
iframe = chrome.find_element(By.XPATH, '//div[@class="loginForm"]/div[1]/div[1]/iframe')
chrome.switch_to.frame(iframe)
time.sleep(2)
# 获取iframe中的内容
# 定位账户名输入框并输入账户名
username_input_element = chrome.find_element(By.XPATH, '//div[@id="account-box"]/div[2]/input')
username_input_element.send_keys(username)
# 定位密码输入框并输入密码
pwd_input_element = chrome.find_element(By.XPATH, '//input[@name="password"]')
pwd_input_element.send_keys(pwd)
# 点击进行登录
login_btn_element = chrome.find_element(By.XPATH, '//a[@id="dologin"]')  # 点击登录
login_btn_element.click()
time.sleep(5)
# 切换到新的跳转窗口
chrome.switch_to.window(chrome.window_handles[-1])
# print(chrome.window_handles)
# print(chrome.page_source)
# ------------------------------------------------------获取cookie后访问其他需登录才能访问的网页--------------------------------------------------------------------------------
# 获取登录后的页面cookie
cookies_for_126email = chrome.get_cookies()
cookies = {}
for cookie in cookies_for_126email:
    # 这里我们仅仅保存cookie重要的name和value两个属性
    cookies[cookie['name']] = cookie['value']

# 利用 pickle 存储相关的cookies信息，下次可以直接调用。
# pickle 是Python特有的序列化工具，能够快速高效存储Python数据类型，反序列化读取后返回的仍是原先的python数据类型。
# 而.txt 等都是字符串类型，需要转换。
filepath = '../testdata/'
if not os.path.exists(filepath):
    os.makedirs(filepath)
cookies_output = open(filepath + 'cookies_126.pickle', 'wb')
pickle.dump(cookies, cookies_output)
cookies_output.close()

# 提取所有邮件
contact_info_url = 'https://mail.126.com/contacts/call.do?uid=xlys_000@126.com&sid=PApvyrPQrVjkUvUtfMQQlWFEAQSVsEnr&from=webmail&cmd=newapi.getContacts&vcardver=3.0&ctype=all&attachinfos=yellowpage,frequentContacts&freContLim=20'
# 添加cookie前要先打开一个页面。同时我们先删除所有cookie看看访问效果：应该是不可以访问的！
chrome.delete_all_cookies()
chrome.get(contact_info_url)
loaded_cookies = pickle.load(open('../testdata/cookies_126.pickle', 'rb'))
# 再把所有登录后保存的cookie加上去访问，看看效果：应该可以访问！
for cookie_key in loaded_cookies:
    chrome.add_cookie({
        'domain': 'mail.126.com',
        'httpOnly': False,
        'name': cookie_key,
        'path': '/',
        'secure': False,
        'value': loaded_cookies[cookie_key]
    })
time.sleep(5)
chrome.refresh()
# -------------------------------------------------获取联系人信息并保存-------------------------------------------------------------------------------------
result_info_json = chrome.find_element(By.XPATH, '//pre').text  # 这个联系人列表是json字符串
# 通过json.loads(json_data)将json字符串转成python对象
result_info_dict = dict(json.loads(result_info_json))
# 获得联系人信息列表并保存为文件
contacts_info = result_info_dict['data']['contacts']
contact_filepath = '../testdata/'
if not os.path.exists(contact_filepath):
    os.makedirs(contact_filepath)
open(contact_filepath + 'contacts.txt', 'wb').write(bytes(json.dumps(contacts_info), encoding='utf-8'))
time.sleep(5)
# -------------------------------------------------获取邮件信息并保存-------------------------------------------------------------------------------------
pass
chrome.close()
