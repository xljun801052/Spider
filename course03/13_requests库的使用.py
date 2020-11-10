"""
    一、介绍一个和urllib功能类似的请求库requests
        1.安装：pip install requests
        2.使用对应的get/post/put/delete/head/options方法发送请求
            ①get():参数是字典，我们也可以传递json类型的参数
            ②post():参数是字典，我们也可以传递json类型的参数
            ③均支持设置请求超时时间(单位：秒)：response = requests.xxx(xxx_url,timeout=0.001)
            ④支持自定义头：response = requests.xxx(xxx_url, headers=headers_xxx)【headers_xxx为字典数据，定义请求头信息】
                headers_xxx = {
                    'User-agent': UserAgent().chrome
                }
            ⑤支持代理proxy:response = requests.xxx(xxx_url, proxies=proxies_xxx)【proxies_xxx为字典数据，定义请求代理信息】
                proxies_xxx = {
                    'http':'http://10.10.0.10:3128',
                    'https':'https://10.10.0.10:1080'
                }
            ⑥支持session自动保存cookies【可以保持会话,利用session取代requests即可】:
                demo：
                    # 创建一个session对象
                    s = requests.Session()
                    # 使用此session对象发送请求，设置cookies
                    s.get('http://www.jd.com')
            ⑦支持ssl验证(选择忽略验证CA证书):使用verify=False即可
                demo:
                    # 禁用安全请求警告
                    requests.packages.urllib3.disable_warnings()  # 不影响，只不过是一种优化
                    response = requests.xxx(xxx_url, verify=False)
            ⑧response内容介绍：
                response.json()以json字符串形式获取响应内容
                response.text:以字符串形式获取响应内容
                response.content:以字节形式获取响应内容
                response.headers:获取响应头内容
                response.url:获取访问地址
                response.encoding:获取网页编码
                response.request.headers:获取请求头内容
                response.cookie:获取cookie
"""
import requests
from fake_useragent import UserAgent

# get()
get_url = 'http://www.baidu.com/s'
params = {
    'wd': '数学危机1'
}
headers_get = {
    'User-agent': UserAgent().chrome
}
response = requests.get(get_url, params=params, headers=headers_get)
print(response.url)  # http://www.baidu.com/s?wd=%E6%95%B0%E5%AD%A6%E5%8D%B1%E6%9C%BA1
response.encoding = 'utf-8'
html_content = response.text
# print(html_content)

# post()
post_url = 'http://www.sxt.cn/index/login/login'
data = {
    'account': 'xxxx',
    'password': 'yyyyyy'
}
headers_post = {
    'User-agent': UserAgent().mozilla
}
response = requests.get(post_url, data=data, headers=headers_post)
print(response.url)
response.encoding = 'utf-8'
html_content2 = response.text
print(response.request.headers['User-agent'])
