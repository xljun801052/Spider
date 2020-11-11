"""
    案例demo:
        目标：爬取http://www.bt46.xyz/网页内容并存入文件中
            url：http://www.bt46.xyz/index.php?page=1

"""
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from fake_useragent import UserAgent
import os


def get_html(url):
    # 构建headers
    headers = {
        'User-agent': UserAgent().chrome
    }
    response = urlopen(Request(url, headers=headers))
    return response.read()


def save_html(file, content):
    with open(file, 'wb') as f:
        f.write(content)


def main():
    end_pn = int(input("【请输入需要下载的页数(默认从1开始】:"))
    base_url = 'http://www.bt46.xyz/index.php?page={}'
    # 构建页数
    for pn in range(end_pn):
        url = base_url.format(pn + 2)
        html_content = get_html(url)
        data_save_dir = 'e:/test/'
        if not os.path.exists(data_save_dir):
            os.makedirs(data_save_dir)
        file = data_save_dir+'第' + str(pn) + '页.html'
        save_html(file, html_content)


if __name__ == '__main__':
    main()
