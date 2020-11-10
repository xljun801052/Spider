"""
    一、HTTPS请求的使用
        1.HTTPS = HTTP + SSL（网景公司推出）
            SSL对应网站安全证书，大部分公司自己做的，这样打开页面时提示"此站点证书未受信任，是否仍要打开？"。当然也有一些
            专门做CA证书认证的，他们制作出来的CA证书一般根据浏览器预设置信任的信息来，所以可以直接打开，忽略那种告警提示信息。
        2.HTTPS:响应返回的内容是加密的，防止别人抓包窃取信息
        3.爬虫时面对需要证书验证的url，我们有时候的处理时忽略证书验证
            context = ssl._create_unverified_context()
            response = urlopen(Request(url, headers=headers), context=context)
"""
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
import ssl

url = 'https://www.12306.cn/index/'
headers = {
    'User-agent': UserAgent().chrome
}
# 构建一个context对象,选择忽略证书验证
context = ssl._create_unverified_context()
response = urlopen(Request(url, headers=headers), context=context)
info = response.read().decode()
print(info[:1000])
# <!DOCTYPE html>
# <html>
#
# <head>
#     <meta charset="utf-8">
#     <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1">
#     <title>中国铁路12306</title>
#     <script>
#         window.startTime = new Date().getTime(); //"window.onload外开始时间:",window.startTime
#     </script>
#     <link rel="shortcut icon" href="images/favicon.ico" type="image/x-icon" />
#     <!-- <link href="./css/index.css" rel="stylesheet">
#     <link href="./css/global.css" rel="stylesheet">
#     <link href="./css/public.css" rel="stylesheet"> -->
#     <link href="./fonts/iconfont.css" rel="stylesheet">
#     <!-- 日期城市控件 -->
#     <!-- <link href="./css/common/calendarNew.css" rel="stylesheet">
#     <link href="./css/common/table.css" rel="stylesheet">
#     <link href="./css/common/station.css" rel="stylesheet">
#     <link rel="stylesheet" href="./css/main.css"> -->
#     <link rel="stylesheet" href="./css/index_y_v30001.css">
# </head>
# <style>
#     .typeahead li {
#         width: 265px;
#         padding-left: 10px
