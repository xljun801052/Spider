"""
    一、post请求：

        0.构建：
            就是在构建Request对象时加一个data参数，【也可以指定method参数值为post，不指定也不影响】

        1.使用场景：
            ①最常用就是登陆网页！【资料：https://www.cnblogs.com/piwefei/p/11171063.html】
            ②请求数据！【此时还要观察请求的参数还有哪些隐藏的，在构造post请求时不要忘了！】

        2.这个data参数是经历字典--->字符串--->字节类型变化：
            ①首先我们通过key-value构建字典形式的数据data,
            ②然后因为构建url时对特殊字符(中文等)需要进行编码所以转换成str字符串形式，urlencode()的返回值即是str类型
            ③最后在请求时因为Request对象对于data要求是bytes，所以还要一层转换变成bytes。encode()返回值即是bytes类型
"""
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from fake_useragent import UserAgent
# 【目前没有特别简单入门的登录网页，所以先不举例了。后续结合cookie/session实现登录时补充】
headers = {
    'User-Agent': UserAgent().firefox
}
data = {
    'name': '夏李逸笙',
    'age': 20
}
response = urlopen(Request('http://www.baidu.com/s?', data=urlencode(data).encode(), headers=headers))
print(response.geturl())
print(response.read().decode())
