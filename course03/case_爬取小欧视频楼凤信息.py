"""
    小欧视频地址：https://cn.qhr128.xyz
    小欧视频楼凤模块：https://cn.qhr128.xyz/loufeng/
        ①摘取发布标题、发布时间、地区信息、年龄信息、颜值水平信息、消费水平信息、服务项目、图片、妹子描述
        ②图片保存文件夹中

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql
import os
import requests
from fake_useragent import UserAgent

base_url = "https://cn.qhr128.xyz"
loufeng_url = "https://cn.qhr128.xyz/loufeng/"
headers = {
    "User-agent": UserAgent().chrome
}
chrome = webdriver.Chrome()
chrome.get(loufeng_url)
time.sleep(5)
# 获取首页所有的标签链接生成商品详情页链接
mn_abstract_info_els = chrome.find_elements(By.XPATH, "//div[@class='col-md-4 loufeng']//a")
mn_detail_url_list = []
i = 0
while i < len(mn_abstract_info_els):
    mn_detail_url_list.append(mn_abstract_info_els[i].get_attribute("href"))
    i += 1

# 单个打开每个链接，获取详情数据并保存
for url in mn_detail_url_list:
    # print(url)
    chrome1 = webdriver.Chrome()
    chrome1.get(url)
    time.sleep(3)
    title = chrome1.find_elements(By.XPATH, "//div[@class='panel-heading']//h1")[0].text
    release_time = chrome1.find_elements(By.XPATH, "//div[@class='panel-heading']//p//span[1]")[0].text
    release_person = chrome1.find_elements(By.XPATH, "//div[@class='panel-heading']//p//span[2]")[0].text
    mn_area = chrome1.find_elements(By.XPATH, "//div[@class='panel lfdetail'][1]//div[@class='panel-body']//div[1]")[
        0].text
    mn_num = chrome1.find_elements(By.XPATH, "//div[@class='panel lfdetail'][1]//div[@class='panel-body']//div[2]")[
        0].text
    mn_age = chrome1.find_elements(By.XPATH, "//div[@class='panel lfdetail'][1]//div[@class='panel-body']//div[3]")[
        0].text
    mn_facial_score = \
        chrome1.find_elements(By.XPATH, "//div[@class='panel lfdetail'][1]//div[@class='panel-body']//div[4]")[0].text
    consume_level = \
        chrome1.find_elements(By.XPATH, "//div[@class='panel lfdetail'][1]//div[@class='panel-body']//div[5]")[0].text
    service_item = \
        chrome1.find_elements(By.XPATH, "//div[@class='panel lfdetail'][1]//div[@class='panel-body']//div[6]")[0].text
    mn_img_els = chrome1.find_elements(By.XPATH, "//div[@class='desc']//div[1]//p//img")
    # 滚动加载图片
    # js = "window.scrollTo(0,3000)"
    # chrome1.execute_script(js)
    mn_imgurl_list = []
    for mn_img_el in mn_img_els:
        mn_imgurl_list.append(mn_img_el.get_attribute("src"))
        # 下载图片到指定基础文件夹中
        img_directory = "../data/img/loufeng/" + title + '/'
        if not os.path.exists(img_directory):
            os.makedirs(img_directory)
        # 文件名：先用src的最后一段命名吧
        img_name = mn_img_el.get_attribute("src").split('_')[len(mn_img_el.get_attribute("src").split('_')) - 1]
        response = requests.get(mn_img_el.get_attribute("src"), headers=headers)
        with open(img_directory + img_name, 'wb') as f:
            f.write(response.content)
            f.flush()
            f.close()

    # 组装数据
    mn_info_tuple = (title, release_time, release_person, mn_area, mn_num, mn_age, mn_facial_score, consume_level, service_item,",".join(mn_imgurl_list))

    # 进行数据库的链接存储
    db = pymysql.connect(host="127.0.0.1", user="root", password="123789Xlys!@#$", database="datacollection", port=3306)
    cursor = db.cursor()
    loufeng_add_sql1 = """insert into t_loufeng_info (title,release_time,release_person,area,mn_numb,mn_age,mn_facial_score,consume_level,service_item,mn_img_urls) values 
                                                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        cursor.execute(loufeng_add_sql1, mn_info_tuple)
        db.commit()
        print("小姐姐信息入库成功...")
    except Exception as e:
        print("小姐姐信息插入数据库异常!")
        db.rollback()
        print(e)
    finally:
        db.close()
    # 一次循环结束后把处理好的页面关闭
    chrome1.close()
    # 这里停10秒也还是会被检测到...后续优化吧
    time.sleep(10)
