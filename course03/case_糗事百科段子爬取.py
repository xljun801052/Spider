"""
    一、利用之前所学爬取一部分糗事百科中的段子数据：https://www.qiushibaike.com/text/【本次是全站段子爬取】
        1.明确目标数据，构造请求，获取数据
        2.分析页面结构(响应数据结构)，确定需要的数据结构层
        3.书写正则匹配需要的数据进行提取
            ①断点调试书写正则
            ②修改完善正则，利用evaluate功能查看提取结果
        4.将结果数据写入文件中
"""
import random
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import time
import os
from lxml import etree


def download_pda(i, base_url, dz_page_urls, dz_filepath):
    """
    将一页中的段子都下载下来
    :param base_url: 主站地址
    :param dz_page_urls: 一页中段子的链接汇总
    :return:
    """
    print('正在下载第{}页段子...'.format(str(i)))
    dz_page_url_list = []
    for dz_page_url in dz_page_urls:
        dz_page_url_list.append(base_url + dz_page_url)
    # 解析数据并存入文本
    with open(dz_filepath + '\\qsbk_dz.txt', 'ab') as f:
        for dz_page_url in dz_page_url_list:
            try:
                print('正在请求：'+dz_page_url)
                dz_page_response = urlopen(Request(dz_page_url, headers={
                    'User-Agent': UserAgent().chrome,
                    'origin': 'https://www.qiushibaike.com',
                    'referer': 'https://www.qiushibaike.com/'
                }))
            except Exception as e:
                print('获取段子详情失败...')
                print(e)
            time.sleep(random.randint(10, 15))
            dz_page_html = etree.HTML(dz_page_response.read().decode())
            dz_info = dz_page_html.xpath('//div[@class="content"]')[0].xpath('string(.)')
            f.write(dz_info.encode())
            # 每个段子间至少隔两行
            f.write(b'\n\n\n')
        f.close()


# 构造请求
base_url = 'https://www.qiushibaike.com'
dz_links_url = base_url + '/text'
headers = {
    'User-Agent': UserAgent().chrome
}
request = Request(dz_links_url, headers=headers)

# 发送请求，得到段子总页面
response = urlopen(request)
time.sleep(5)
html_info = etree.HTML(response.read().decode())
# print(html_info)

# 这里默认第一页段子【后面的页面的段子稍后取】
dz_page_urls = html_info.xpath('//div[@class="col1 old-style-col1"]/div/a[1]/@href')
# 判断一共多少页
try:
    total_page_count = int(html_info.xpath('//div[@class="col1 old-style-col1"]/ul/li[last()-1]/a/span/text()')[0])
    print('一共有{}页段子！'.format(str(total_page_count)))
except Exception as e:
    print('获取总页码出错')
    print(e)

# 创建文件路径
dz_filepath = r'G:\python爬虫实战结果\text'
if not os.path.exists(dz_filepath):
    os.makedirs(dz_filepath)

# 段子获取
for i in range(1, total_page_count + 1):
    try:
        response = urlopen(Request(dz_links_url + '/page/' + str(i), headers={
            'User-Agent': UserAgent().chrome,
            'origin': 'https://www.qiushibaike.com',
            'referer': 'https://www.qiushibaike.com/'
        }))
    except Exception as e:
        print('获取段子链接汇总页失败...')
        print(e)
    time.sleep(8)
    dz_page_html = etree.HTML(response.read().decode())
    dz_page_urls = dz_page_html.xpath('//div[@class="col1 old-style-col1"]/div/a[1]/@href')
    print('第'+str(i)+'页链接汇总如下：')
    print(dz_page_urls)
    download_pda(i, dz_links_url, dz_page_urls, dz_filepath)
