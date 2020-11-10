"""
    一、get请求的使用
        1.中文编码解决：urllib.parse中quote或者urlencode都可以
            quote适合单个参数编码
            urlencode适合多个参数一起编码

"""
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:16.0.1) Gecko/20121011 Firefox/21.0.1'
}

# 使用quote来实现url中中文编码
value = quote('谬论')
url = 'http://www.baidu.com/s?wd' + value
print(url)  # http://www.baidu.com/s?wd%E8%B0%AC%E8%AE%BA

# 使用urlencode来实现url中中文编码
args = {
    'wd': '他大姨妈四',
    'charset': 'utf8'
}
print(urlencode(args))  # wd=%E4%BB%96%E5%A4%A7%E5%A7%A8%E5%A6%88%E5%9B%9B&charset=utf8
url2 = 'http://www.baidu.com?{}'.format(urlencode(args))
print(url2)  # http://www.baidu.com?wd=%E4%BB%96%E5%A4%A7%E5%A7%A8%E5%A6%88%E5%9B%9B&charset=utf8

# request = Request(url, headers=headers)
# response = urlopen(request)
# 查看发送的真正的url
