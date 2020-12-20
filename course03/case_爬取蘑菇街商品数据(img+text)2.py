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
import random
from urllib.request import Request, urlopen, urlretrieve
from fake_useragent import UserAgent
import time
import os
from lxml import etree
import pymysql


##################################################下载图片##################################################################################
def download_img(urls):
    """
    根据链接下载图片
    :param urls: 图片链接地址
    :return: 图片二进制内容响应
    """
    headers = {
        "User-Agent": UserAgent().chrome,
        # ':authority': 's5.mogucdn.com',
        # ':method': 'GET',
        # :path: / mlcdn / c45406 / 191015_4cij00jed03d5d08dljif36g1lkk1_3556x5334.jpg
        # ': scheme': 'https',
        # accept: text / html, application / xhtml + xml, application / xml;q = 0.9, image / avif, image / webp, image / apng, * / *;q = 0.8, application / signed - exchange;v = b3;q = 0.9
        # 'accept-encoding': 'gzip,deflate,br',
        # 'accept-language': 'zh-CN,zh;q = 0.9',
        # 'cache-control': 'no-cache',
        # 'pragma': 'no-cache',
        # 'sec-fetch-dest': 'document',
        # 'sec-fetch-mode': 'navigate',
        # 'sec-fetch-site': 'none',
        # 'sec-fetch-user': '?1',
        # 'upgrade-insecure-requests': 1
    }
    img_content_list = []
    for url in urls:
        response = urlopen(Request(url, headers=headers))
        time.sleep(1)
        # 这里获取的不是单纯图片内容...后续研究吧
        img_content_list.append(response.read())
        with open('test1', 'wb') as f:
            f.write(response.read())
            f.flush()
    return img_content_list


# step5:根据img_src下载图片插入数据库
conn = pymysql.connect(host="127.0.0.1", user="root", password="123789Xlys!@#$", database="dataCollection", port=3306)
cursor = conn.cursor()
sql = """select good_id, img_src from t_supermall_home_goods_info"""
sql_insert = """insert  into t_supermall_hoem_goos_info (goods_id,img) values (%s,%s)"""
try:
    cursor.execute(sql)
    img_info = cursor.fetchall()
    img_id_list = []
    img_link_list = []
    insert_info = []
    for img_url_info in img_info:
        img_id_list.append(img_url_info[0])
        img_link_list.append(img_url_info[1])
    # 下载图片内容
    img_content_list = download_img(img_link_list)
    # 存储到数据库
    for (img_id, img_content) in zip(img_id_list, img_content_list):
        insert_info.append((img_id, img_content))
    cursor.execute(sql_insert, insert_info)
    conn.commit()
except Exception as e:
    print("图片处理过程出现异常!")
    conn.rollback()
    print(e)
finally:
    cursor.close()
    conn.close()
