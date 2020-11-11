"""

    手写第一个爬虫程序：
        1.使用urllib库
        2.获取响应相关信息：
            ① 读取响应内容
                info = response.read()
            ② 获取请求状态码
                status_code = response.getcode()
            ③ 获取真实url,防止重定向导致url变化
                true_url = response.geturl()
            ④ 获取响应头
                headers = response.info()
"""
from urllib.request import urlopen

url1 = 'https://item.jd.com/10021937750949.html'  # 小黑裙商品页面
url2 = 'https://passport.jd.com/uc/login?ReturnUrl=http%3A%2F%2Fitem.jd.com%2F10021937750949.html'  # 登录页面
url3 = 'https://www.baidu.com'  # baidu首页
# 发送请求
response = urlopen(url3)
# 读取响应内容
info = response.read()
print('======={}========'.format('响应内容'))
print(info)
# 对响应内容进行编码
info.decode()  # 默认utf8
print('======={}========'.format('编码(utf-8)后响应内容'))
print(info)
# 获取请求状态码
status_code = response.getcode()
print('======={}========'.format('状态码'))
print(status_code)
# 获取真实url,防止重定向导致url变化
true_url = response.geturl()
print('======={}========'.format('真实url'))
print(true_url)
# 获取响应头
headers = response.info()
print('======={}========'.format('响应头'))
print(headers)


