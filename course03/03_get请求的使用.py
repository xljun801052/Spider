"""
    一、get请求的使用

        1.一般的请求都是get请求。除非显示调用post()方法或者说在method中指定post

        2.url中的中文或者特殊字符编码解决：urllib.parse中quote()或者urlencode()都可以
            ①quote(param_value):适合单个参数编码
                demo:
                    value = quote('谬论')
                    url = 'http://www.baidu.com/s?wd' + value
                    print(url)  # http://www.baidu.com/s?wd%E8%B0%AC%E8%AE%BA

            ②urlencode(param_dict)适合多个参数一起编码
                demo:
                    args = {
                        'wd': '他大姨妈四',
                        'charset': 'utf8'
                    }
                    print(urlencode(args))  # wd=%E4%BB%96%E5%A4%A7%E5%A7%A8%E5%A6%88%E5%9B%9B&charset=utf8
                    url2 = 'http://www.baidu.com?{}'.format(urlencode(args))
                    print(url2)  # http://www.baidu.com?wd=%E4%BB%96%E5%A4%A7%E5%A7%A8%E5%A6%88%E5%9B%9B&charset=utf8
"""
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from utils.request_utils import get_random_ua

# 使用quote来实现url中中文编码

value = quote('谬论')
url = 'http://www.baidu.com/s?wd=' + value
print(url)  # http://www.baidu.com/s?wd=%E8%B0%AC%E8%AE%BA
request = Request(url, headers=get_random_ua())
response = urlopen(request)
print(response.read().decode())

# <div class="c-span9 c-span-last op-bk-polysemy-piccontent">
#                     <em>谬论</em>，汉语词汇，拼音是miù lùn，指意思是荒唐、错误的言论，也指错误决狱。出自《汉书·刑法志》。
#                 </p>
#
#                 <p>

# 使用urlencode来实现url中中文编码

args = {
    'wd': '他大姨妈四',
    'charset': 'utf8'
}
print(urlencode(args))  # wd=%E4%BB%96%E5%A4%A7%E5%A7%A8%E5%A6%88%E5%9B%9B&charset=utf8
url2 = 'http://www.baidu.com?{}'.format(urlencode(args))
print(url2)  # http://www.baidu.com?wd=%E4%BB%96%E5%A4%A7%E5%A7%A8%E5%A6%88%E5%9B%9B&charset=utf8
request = Request(url2, headers=get_random_ua())
response = urlopen(request)
print(response.read().decode())
# 查看发送的真正的url
print(response.geturl())  # https://www.baidu.com/?wd=%E4%BB%96%E5%A4%A7%E5%A7%A8%E5%A6%88%E5%9B%9B&charset=utf8
