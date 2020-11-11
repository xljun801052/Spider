"""
    一、proxy代理：隐藏"自己"身份的一种方式，使用代理服务器代替我们进行访问网络资源

        1.实现原理：
            urlopen()底层还是opener的open()方法。在opener对象构建时中可以传入一个代理处理器，那么生成的opener便
            具备了处理代理的请求的功能。随后使用这个opener.open(request)方法即可
            # 以下是build_opener(handler)的部分源码
                opener = OpenerDirector()
                default_classes = [ProxyHandler, UnknownHandler, HTTPHandler,
                                   HTTPDefaultErrorHandler, HTTPRedirectHandler,
                                   FTPHandler, FileHandler, HTTPErrorProcessor,
                                   DataHandler]
                if hasattr(http.client, "HTTPSConnection"):
                    default_classes.append(HTTPSHandler)
                skip = set()
                for klass in default_classes:
                    for check in handlers:
                        if isinstance(check, type):
                            if issubclass(check, klass):
                                skip.add(klass)
                        elif isinstance(check, klass):
                            skip.add(klass)

        2.使用代理处理的代码样例：
            # demo:以下的ip、port均为代理服务器的对应ip、代理port
                # 鉴于代理有分有无【用户名&密码】参数的区别，所以也有了两种写法
                    # ①无【用户名&密码】
                    from urllib.request import ProxyHandler

                    handler = ProxyHandler({'http': 'xxx.xxx.xxx.xxx:port'})
                    opener = build_opener(handler)
                    response = opener.open(request)

                    # ①有【用户名&密码】
                    from urllib.request import ProxyHandler

                    handler = ProxyHandler({'http': 'username：password@ip:port'})
                    opener = build_opener(handler)
                    response = opener.open(request)

        3.工具
            ①免费代理网站（获取代理ip、port）：快代理
                https://www.kuaidaili.com/free/

            ②代理结果测试网站
                http://httpbin.org/get【可以返回当前的一些发起该请求的客户端的一些信息】
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

url = 'http://httpbin.org/get'
headers = {
    'User-agent': UserAgent().chrome
}
request = Request(url, headers=headers)
# 不使用代理时："origin": "180.165.133.145"
# opener = build_opener()
# response = opener.open(request)
# print(response.read().decode())
# {
#   "args": {},
#   "headers": {
#     "Accept-Encoding": "identity",
#     "Host": "httpbin.org",
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1467.0 Safari/537.36",
#     "X-Amzn-Trace-Id": "Root=1-5fab81ce-11faf2b03ed614a34bedf4c5"
#   },
#   "origin": "180.165.133.145",
#   "url": "http://httpbin.org/get"
# }

# 使用代理时："origin": "139.224.18.116"
# 两种写法：分别支持有用户名和密码的以及无用户名和密码的
# handler = ProxyHandler({'http': 'username：password@ip:port'})  # 有用户名和密码的代理使用方式
handler = ProxyHandler({'http': '139.224.18.116:80'})  # 无用户名和密码的代理使用方式
opener = build_opener(handler)
response = opener.open(request)
print(response.read().decode())
# 这里的免费代理结果都不太好用，只测试成功了一个！
# {
#   "args": {},
#   "headers": {
#     "Accept-Encoding": "identity",
#     "Host": "httpbin.org",
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
#     "X-Amzn-Trace-Id": "Root=1-5fab83c2-7911cda84d4f8bb653c46af3"
#   },
#   "origin": "139.224.18.116",
#   "url": "http://httpbin.org/get"
# }