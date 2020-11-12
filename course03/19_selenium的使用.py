"""
    Selenium的文档见有道云笔记
    此节介绍具体使用：模拟126邮箱登录
"""
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

# 发送请求
chrome.get(login_page_url)
# chrome.save_screenshot(r'E:\Pythonlearning\PythonProjects\Spider_learning\Spider\testdata\shot.jpg')
# print(chrome.page_source)

# 拿到响应后定位元素并填充值
# 获取iframe嵌套页面src地址:此嵌套页面是真正的登录输入表单
# iframe_url = chrome.find_element(By.XPATH, '//div[@class="loginForm"]/div[1]/div[1]/iframe').get_attribute('src')
# print(iframe_url)
iframe = chrome.find_element(By.XPATH, '//div[@class="loginForm"]/div[1]/div[1]/iframe')
chrome.switch_to.frame(iframe)
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
chrome.switch_to_window(chrome.window_handles[-1])
print(chrome.window_handles)
# print(chrome.page_source)

# 获取登录后的页面cookie
cookies_for_126email = chrome.get_cookies()
cookies = {}
for cookie in cookies_for_126email:
    # 这里我们仅仅保存cookie重要的name和value
    cookies[cookie['name']] = cookie['value']

# 利用 pickle 存储相关的cookies信息，下次可以直接调用。
# pickle 是Python特有的序列化工具，能够快速高效存储Python数据类型，反序列化读取后返回的仍是原先的python数据类型。
# 而.txt 等都是字符串类型，需要转换。
cookies_output = open('../testdata/cookies_126.pickle', 'wb')
pickle.dump(cookies_for_126email, cookies_output)
cookies_output.close()

# 提取所有邮件
emails_info_url = 'https://mail.126.com/js6/s?sid=nAdBTFjFZtVzncxzcjFFdCxpEIPudaVB&func=mbox:listMessages'
loaded_cookies = pickle.load('../testdata/cookies_126.pickle', 'rb')
chrome.add_cookie()
chrome.close()
