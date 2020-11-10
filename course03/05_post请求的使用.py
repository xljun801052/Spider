"""
    一、post请求：就是在构建Request对象时加一个data参数
        0.使用场景：
            ①最常用就是登陆网页！
            ②请求数据！【此时还要观察请求的参数还有哪些隐藏的，在构造post请求时不要忘了！】
        1.这个data参数是经历字典--->字符串--->字节类型变化：
            首先我们通过key-value构建字典形式的数据data,然后因为构建url时对特殊字符(中文等)需要进行编码所以转换成str字符串形式，urlencode()的返回值即是str类型
            最后在请求时因为Request对象对于data要求是bytes，所以还要一层转换变成bytes。encode()返回值即是bytes类型
"""
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from fake_useragent import UserAgent

data = {
    'key1': 'value1',
    'name': '夏李逸笙'
}
headers = {
    'User-Agent': UserAgent().firefox
}
response = urlopen(Request('http://www.xxx.com', data=urlencode(data).encode(), headers=headers))
print(response.read().decode())
