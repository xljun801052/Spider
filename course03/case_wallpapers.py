from lxml import etree
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import time
import os

""""
    问题：
        1.首页使用代码无法访问
        2.数量太大，数据内容太多，考虑多线程
        3.嵌套循环请求次数太多了，考虑休眠或者其他方法同等优化，不要被封禁
"""

# 主站地址
base_url = 'https://10wallpaper.com'

request = Request(base_url, headers={
    # 'User-Agent': UserAgent().chrome
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
})
try:
    # 发送请求拿到主页所有的分类名称和分类后主页的url,并根据名称建立文件夹用于存储
    response = urlopen(request)
    time.sleep(3)
    homepage_html = etree.HTML(response.read().decode())
    # 全站一共7W+张，按1920x1020分辨率大约要70G存储,先拿一个相册出来看看
    # 共计16个分类：风景、人物、...
    category_names = homepage_html.xpath('//div[@id="content"]/div/div/ul[2]')
    category_page_urls = homepage_html.xpath('//div[@id="content"]/div/div/ul[2]/li/a/@href')
    for category_name, category_page_url in zip(category_names, category_page_urls):
        try:
            category_filepath = '../testdata/' + category_name
            if not os.path.exists(category_filepath):
                os.makedirs(category_filepath)
            # 请求相册集页面：这里默认进来是分类后【相册集页面】的第一页
            category_page_response = urlopen(Request(base_url + category_page_url, headers={
                'User-Agent': UserAgent().chrome
            }))
            time.sleep(3)
            category_page_html = etree.HTML(category_page_response.read().decode())
            # 取出每页中的相册集的链接
            album_info_urls = category_page_html.xpath('//div[@id="pics-list"]/p/a/@href')
            # 取出相册集中的相册集名字
            album_names = category_page_html.xpath('//div[@id="pics-list"]/p/a/span/text()')
            for album_info_url, alnum_name in zip(album_info_urls, album_names):
                try:
                    album_path = category_filepath + '/' + alnum_name
                    if not os.path.exists(album_path):
                        os.makedirs(album_path)
                    # 拿到相册集详情页中每张壁纸链接
                    alnum_detail_info_page_response = urlopen(Request(base_url + album_info_url, headers={
                        'User-Agent': UserAgent().chrome
                    }))
                    time.sleep(3)
                    detail_html = etree.HTML(alnum_detail_info_page_response.read().decode())
                    # 每张壁纸详情页链接
                    wp_page_urls = detail_html.xpath('//div[@id="pics-list"]/p/a/@href')
                    for wp_page_url in wp_page_urls:
                        try:
                            wp_response = urlopen(Request(base_url + wp_page_url, headers={
                                'User-Agent': UserAgent().chrome
                            }))
                            time.sleep(3)
                            wp_html = etree.HTML(wp_response.read().decode())
                            # 这里a的集合涵盖了不同分别率的链接，下载对应的即可
                            wp_url = wp_html.xpath('//div[@class="pic-left"]/div/span[3]/a[11]/@href')
                            wp_name = wp_url.split('/')[len(wp_url.split('/')) - 1]
                            whole_wp_url = base_url + wp_url
                            wp = urlopen(Request(whole_wp_url, headers={
                                'User-Agent': UserAgent
                            }))
                            time.sleep(3)
                            with open(album_path + wp_name, 'wb') as f:
                                f.write(wp.read())
                                f.flush()
                            f.close()
                        except Exception as e:
                            print('壁纸下载处理异常...')
                            print(e)
                except Exception as e:
                    print('相册集处理异常...')
                    print(e)
                # 每一页的相册集处理完后，处理下一页相册
                # while category_page_html.xpath('//div[@class="pg_pointer"]/a[last()]/text()') == '>>':
        except Exception as e:
            print('分类处理异常...')
            print(e)
except Exception as e:
    print('主站处理异常...')
    print(e)
