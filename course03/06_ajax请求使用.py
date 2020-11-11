"""
    一、ajax请求

        0.ajax请求的注意点：
            对于动态网页爬取数据（也称为非定向爬虫），我们最主要是观察数据加载方式。这个时候浏览器上的url就只是页面框架url，并非真实数据的url链接。
            我们要想获得想要爬取的数据的链接，就要去捕获ajax请求发送的真实数据url链接--->>>打开开发者模式，F12中捕获XHR请求链接。

        1.ajax请求的判别：
            ①在请求的header中观察是否有X-Requested-With：XMLHttpRequest属性和对应值，一般ajax请求都会有
            ②查看网页源代码，一般我们想要的内容不在源代码里面的话基本都是ajax请求去获取到数据填充进来的

        2.模仿ajax请求时可以优化的点：
            ①减少请求次数，一次数据量相对多些！【但是不能很多，导致服务器一次处理数据量过大崩溃或者响应时间很长】
            ②动态请求：将请求的url通过参数构造动态化获取数据，而不是写死的url获取固定少量数据

        3.爬取豆瓣电影案例：
            ajax-url:https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start=20&limit=20

"""
from urllib.request import urlopen, Request
from utils.request_utils import get_random_ua
import time
import random
import os

base_url = 'https://movie.douban.com/j/chart/top_list?type=13&interval_id=100%3A90&action=&start={}&limit=20'

file_save_path = 'e:/test'
if not os.path.exists(file_save_path):
    os.makedirs(file_save_path)

i = 1
while True:
    request = Request(base_url.format(i * 20), headers=get_random_ua())
    response = urlopen(request)
    # time.sleep(random.randint(2, 5))
    page_info = response.read()
    # if page_info == "" or page_info is None:
    # 实际获得的是bytes类型的空的json数组【b'[]'】--->>>所以改变判空逻辑
    if page_info.decode() == "[]" or page_info.decode() is None:
        break
    else:
        print("第" + str(i) + "页正在下载...")
        with open(file_save_path+'/doubanmovies_rank_total.txt', 'ab') as f:
            f.write(page_info)
            # 每页数据都是json数组，换行隔开!同时需要将str转成bytes
            f.write('\n\n'.encode())
            f.flush()
        i += 1
