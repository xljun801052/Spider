"""
    一、Request使用：构建请求对象

    二、User-agent的使用：
        1.隐藏请求身份，修改User-agent实现
        2.高级：构建动态User-agent

            ①构建动态源(使用fake_useragent库或者如下写死)：
                系统	    浏览器	User-Agent字符串
                Mac	    Chrome	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36
                Mac	    Firefox	Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:65.0) Gecko/20100101 Firefox/65.0
                Mac	    Safari	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0.3 Safari/605.1.15
                Windows	Chrome	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36
                Windows	Edge	Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763
                Windows	IE	    Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko
                iOS	    Chrome	Mozilla/5.0 (iPhone; CPU iPhone OS 7_0_4 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) CriOS/31.0.1650.18 Mobile/11B554a Safari/8536.25
                iOS	    Safari	Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12F70 Safari/600.1.4
                Android	Chrome	Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36
                Android	Webkit	Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; M351 Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30

            ②利用随机choice方法
"""

from urllib.request import urlopen
from urllib.request import Request
from random import choice

url1 = 'https://item.jd.com/10021937750949.html'  # 小黑裙商品页面
url2 = 'https://passport.jd.com/uc/login?ReturnUrl=http%3A%2F%2Fitem.jd.com%2F10021937750949.html'  # 登录页面
url3 = 'https://www.baidu.com'  # baidu首页

ua_choices = [
    'Mozilla/5.0 (Linux; U; Android 4.4.4; zh-cn; M351 Build/KTU84P) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; Android 4.2.1; M040 Build/JOP40D) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
]
headers = {
    # 'User-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Mobile Safari/537.36'
    'User-agent': choice(ua_choices)
}

print(choice(ua_choices))

request = Request(url3, headers=headers)
# 发送请求
response = urlopen(request)
# 读取响应内容
info = response.read().decode('utf8')
print(info[:2000])
# <!DOCTYPE html>
# <html class=""><!--STATUS OK--><head><meta name="referrer" content="always" /><meta charset='utf-8' /><meta name="viewport"
# content="width=device-width,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no"/><meta http-equiv="x-dns-prefetch-control"
# content="on"><meta name="description" content="全球最大的中文搜索引擎、致力于让网民更便捷地获取信息，找到所求。百度超过千亿的中文网页数据库，
# 可以瞬间找到相关的搜索结果。"><link rel="dns-prefetch" href="//m.baidu.com"/><link rel="shortcut icon" href="https://sm.bdimg.com/
# static/wiseindex/img/favicon64.ico" type="image/x-icon"><link rel="apple-touch-icon-precomposed" href="https://sm.bdimg.com/
# static/wiseindex/img/screen_icon_new.png"/><meta name="format-detection" content="telephone=no"/><noscript><style type="text/
# css">#page{display:none;}</style><meta http-equiv="refresh" content="0; URL=http://m.baidu.com/?cip=116.233.59.127&amp;baidu
# id=5A01C3DA21990E60A5EF00FFF5EF3CC1&amp;from=844b&amp;vit=fps?from=844b&amp;vit=fps&amp;index=&amp;ssid=0&amp;bd_page_type=1&a
# mp;logid=11809909190986683513&pu=sz%401321_480&t_noscript=jump" /></noscript><title>百度一下</title><script>window._performanceTi
# mings=[['firstLine',+new Date()]];</script><style type="text/css" id='spa-base-style'>#search-card {display: none;}</style><styl
# e type="text/css">@font-face {font-family: 'n-icons';src: url('https://sm.bdimg.com/static/wiseindex/fonts/n-icons_ec9afed.eot')
# ;src: url('https://sm.bdimg.com/static/wiseindex/fonts/n-icons_ec9afed.eot#iefix') format('embedded-opentype'),url('https://sm.b
# dimg.com/static/wiseindex/fonts/n-icons_7bcbf44.woff') format('woff'),url('https://sm.bdimg.com/static/wiseindex/fonts/n-icons_d
# 083fee.ttf') format('truetype'),url('https://sm.bdimg.com/static/wiseindex/fonts/n-icons_1015320.svg#n-icons') format('svg');fon
# t-weight: normal;font-style: normal;}@font-face {font-family: 'icons';src: url('https://sm.bdimg.com/static/wiseindex/iconfont/i
# confont_b8e5ea1.eot');src: url('https://sm.bdimg.com/static/wiseindex/iconfont/iconfont_b8e5ea1.eot#iefix') format('embedded-opentyp
