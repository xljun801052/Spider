"""
    一、proxy代理：隐藏自己的一种方式
        1.urlopen()底层还是opener的open()方法
            return opener.open(url, data, timeout)
        2.使用代理处理器：
            handler = ProxyHandler({'http': 'xxx.xxx.xxx.xxx:port'})
            opener = build_opener(handler)
            response = opener.open(request)
        3.工具
            http://httpbin.org/get【可以返回当前的一些浏览器请求信息】
            {
              "args": {},
              "headers": {
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Host": "httpbin.org",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
                "X-Amzn-Trace-Id": "Root=1-5f969996-3f2c3ee84d75e9f201f52f9b"
              },
              "origin": "180.165.133.145",【使用代理后可在此属性中观察ip变化】
              "url": "http://httpbin.org/get"
            }

"""
from urllib.request import Request
from urllib.request import build_opener
from fake_useragent import UserAgent
from urllib.request import ProxyHandler  # 代理处理器

url = 'https://www.baidu.com'
headers = {
    'User-agent': UserAgent().chrome
}
request = Request(url, headers=headers)
# 两种写法：分别支持有用户名和密码的以及无用户名和密码的
# handler = ProxyHandler({'http': 'username：password@ip:port'})
handler = ProxyHandler({'http': 'ip:port'})
opener = build_opener(handler)
response = opener.open(request)
print(response.read().decode()[:2000])
