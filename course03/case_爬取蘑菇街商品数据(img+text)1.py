"""
    一、爬取蘑菇街商品数据->做项目(supermall)测试数据使用
        urls = [
          上衣:https://list.mogu.com/book/clothing?ptp=31.vOv15b.0.0.LE5ImV3v
          裙子:https://list.mogu.com/book/skirt?ptp=31.Gfr19.0.0.6yEIM1l3
          裤子:https://list.mogu.com/book/trousers?ptp=31.vOv15b.0.0.qrLfWY2l
          内衣:https://list.mogu.com/book/neiyi?ptp=31.nv1qD.0.0.ODFz1NvA
          鞋子:https://list.mogu.com/book/shoes?ptp=31.ebrCK.0.0.MoR6fMBl
        ]

        1.明确目标数据，构造请求，获取数据
        2.分析页面结构(响应数据结构)，确定需要的数据结构层
        3.书写正则匹配需要的数据进行提取
            ①断点调试书写正则
            ②修改完善正则，利用evaluate功能查看提取结果
        4.将结果数据写入数据库(mysql8)中
"""

##################################################selenium获取数据##################################################################################
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import datetime
import pymysql

# step1:构建浏览器
chrome = webdriver.Chrome()

# step2：构建请求
target_url = "https://list.mogu.com/book/clothing?ptp=31.vOv15b.0.0.LE5ImV3v"
chrome.get(target_url)
chrome.maximize_window()
# 这个地方四个列表数据量不一致...先不管了，向下滚动20屏，以后再研究吧~
js = "window.scrollTo(0,2000000)"
for i in range(1, 100):
    chrome.execute_script(js)
    time.sleep(3)

# step3:记录所有的原始价格、折后价格、图片标题、图片链接
origin_price_element_list = chrome.find_elements(By.XPATH, '//div[@class="iwf goods_item ratio3x4"]/a[3]/div/b')
discount_price_element_list = chrome.find_elements(By.XPATH, '//div[@class="iwf goods_item ratio3x4"]/a[3]/div/p')
img_title_element_list = chrome.find_elements(By.XPATH, '//div[@class="iwf goods_item ratio3x4"]/a[3]/p')
img_src_element_list = chrome.find_elements(By.XPATH, '//div[@class="iwf goods_item ratio3x4"]/a[2]')
favorite_num_element_list = chrome.find_elements(By.XPATH, '//div[@class="iwf goods_item ratio3x4"]/a[3]/div/span')
# origin_price_list = []
# discount_price_list = []
# img_title_list = []
# img_src_list = []
# favorite_num_list = []


all_length_list = [len(origin_price_element_list), len(discount_price_element_list), len(img_title_element_list),
                   len(img_src_element_list), len(favorite_num_element_list)]
print(all_length_list)

data_list = []
create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
for i in range(1, min(all_length_list)):
    # print(origin_price_list[i].text)
    # origin_price_list.append(origin_price_element_list[i].text)
    # discount_price_list.append(discount_price_element_list[i].text)
    # img_title_list.append(img_title_element_list[i].text)
    # img_src_list.append(img_src_element_list[i].get_attribute('img-src'))
    # favorite_num_list.append(favorite_num_element_list[i].text)
    data_list.append((origin_price_element_list[i].text, discount_price_element_list[i].text,
                      img_title_element_list[i].text, img_src_element_list[i].get_attribute('img-src'),
                      favorite_num_element_list[i].text, create_time))
# print(origin_price_list)
# print(discount_price_list)
# print(img_title_list)
# print(img_src_list)
# print(favorite_num_list)
print(data_list)
chrome.close()

# step4:插入数据库
conn = pymysql.connect(host="127.0.0.1", user="root", password="123789Xlys!@#$", database="dataCollection", port=3306)
cursor = conn.cursor()

# python中的datetime.datetime.now().strftime("%Y-%m-%d %H:%i:%s")对应mysql中datetime类型
# TypeError: not enough arguments for format string：主要是字符串中包含了%号，python 认为它是转移符，而实际我们需要的就是%， 这个时候，可以使用%%来表示
sql = """insert into t_supermall_home_goods_info (origin_price,discount_price,money_type,img_title,img_src,favorite,create_time,valid_flag) values (%s,%s,1,%s,%s,%s,str_to_date(%s,'%%Y-%%m-%%d %%H:%%i:%%s'),1)"""
try:
    cursor.executemany(sql, data_list)
    conn.commit()
    print("插入数据成功!")
except Exception as e:
    print(e)
    conn.rollback()
    print("插入数据异常!")
finally:
    cursor.close()
    conn.close()

# step5:根据img_src下载图片插入数据库
# conn = pymysql.connect(host="127.0.0.1", user="root", password="123789Xlys!@#$", database="dataCollection", port=3306)
# cursor = conn.cursor()
# sql = """select good_id, img_src from t_supermall_home_goods_info"""
# try:
#     cursor.execute(sql)
#     img_urls_info = cursor.fetchall()
#     for img_url_info in img_urls_info:
#         print(str(img_url_info[0])+"--->"+img_url_info[1])
# except Exception as e:
#     print("图片处理过程出现异常!")
#     print(e)
# finally:
#     cursor.close()
#     conn.close()