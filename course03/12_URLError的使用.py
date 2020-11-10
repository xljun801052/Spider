"""
    一、有时候我们的请求会因为网页地址变更或者服务器域名变换导致出现爬取出错：URLError/HTTPError。如何捕获呢？怎么样才是完整的代码...
        1.我们在确知错误的情况下可以用try...except...根据具体的异常类型捕获
        2.根据捕获的异常code来给出更加详细的提示
"""
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
from urllib.error import URLError,HTTPError

demo_err_url1 = 'https://mbd.baidu.com/newspagess'
demo_err_url2 = 'www.baidu111.com'
headers = {
    'User-agent': UserAgent().chrome
}
try:
    response = urlopen(Request(demo_err_url1, headers=headers))
    print(response.read()[:500])
except URLError as e:
    print(e)  # code 404
    print('页面失踪...')
except HTTPError as e:
    print(e)
    print('域名出错...')
except ValueError as e:
    print(e)
    print('页面失踪2...')
print("访问完成")
