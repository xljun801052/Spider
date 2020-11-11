"""
    一、针对有些具体的网页需要我们登录之后才能浏览，如何爬取？肯定要先模拟登录呀，拥有了登录状态才能进行下去呀...
        这里主要使用cookie解决。【至于session包括selenium等解决方案后续研究】

            0.Cookielib库的使用
                cookielib模块的主要作用是提供可存储cookie的对象，以便于与urllib模块配合使用来访问Internet资源。
                Cookielib模块非常强大，我们可以利用本模块的CookieJar类的对象来捕获cookie并在后续连接请求时重新发送，
                比如可以实现模拟登录功能。该模块主要的对象有CookieJar、FileCookieJar、MozillaCookieJar、LWPCookieJar


        两种方法：

            1.页面登录，获取登录状态下浏览网页需要发送的cookie，然后request携带cookie进行爬取网页数据

            2.代码直接模拟登录获取登录状态下浏览网页需要的cookie，然后后续request携带对应cookie进行爬取网页数据
                ①构造登录headers和data数据
                ②发送请求
                ③保存请求响应时返回的cookie：两种方法
                    i:直接将cookie保存在内存中，发送请求时随调随用
                        HTTPCookieProcessor,build_opener两者结合可以构建保存cookie的opener，使用opener的open()方法发送请求便可以携带对应的cookie了
                        原理是HTTPCookieProcessor内部有用来保存cookie的CookieJar类

                        # HTTPCookieProcessor部分源码
                            class HTTPCookieProcessor(BaseHandler):
                                def __init__(self, cookiejar=None):
                                    import http.cookiejar
                                    if cookiejar is None:
                                        cookiejar = http.cookiejar.CookieJar()
                                    self.cookiejar = cookiejar

                                def http_request(self, request):
                                    self.cookiejar.add_cookie_header(request)
                                    return request

                    ii:将cookie保存到本地文件中，然后发送请求时从文件中获取并添加到请求中
                        ①利用到MozillaCookieJar

"""
from urllib.request import Request, urlopen
from fake_useragent import UserAgent
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener

url1 = 'https://mail.126.com/fgw/da-login-api/listLoginInfo?limit=1&1603785999122'  # 查看网易邮箱登录信息
url2 = 'https://order.jd.com/lazy/getOrderProductInfo.action'  # 查看京东个人购物车信息
url4 = 'https://order.jd.com/center/list.action'  # 查看全部订单
headers = {
    'User-agent': UserAgent().chrome,
    # 'Cookie': 'nts_mail_user=xlys_000@126.com:-1:1; locale=; face=js6; mail_upx_nf=; mail_idc=""; secu_info=1; mail_host=mail.126.com; mail_uid=xlys_000@126.com; mail_style=js6; ANTICSRF=cleared; starttime=; NTES_SESS=D57edgFxRgAtcFJD_V65tobh8mo0excLjqxW6aUYHYo6ybvYyrnuZzo1vb98CCYjBjtx0tFWuUMC.1O5i5psACy702XMP2Lpd2REQtNIotK3Xhgl9necs1ln5mmYRDR1.UdMHJF1l9kl0doqpHJSTxxSifpFA7qVTNtmMEOMuPq6UBGRDECVrre_yyMrZWKRvesbAw21zADYTc3jP_zLHkEQVbDlgt_JRDHcaR8JHU9qc; S_INFO=1603769486|0|#3&80#|xlys_000@126.com; P_INFO=xlys_000@126.com|1603769486|0|mail126|00&99|shh&1603769161&caldav#shh&null#10#0#0|173034&0|urs&mail126&note_client|xlys_000@126.com; df=mail163_letter; mail_upx=t7hz.mail.126.com|t8hz.mail.126.com|t1hz.mail.126.com|t2hz.mail.126.com|t3hz.mail.126.com|t4hz.mail.126.com|t3bj.mail.126.com|t4bj.mail.126.com|t1bj.mail.126.com|t2bj.mail.126.com; Coremail=b5399a950c3cc%PAVuriYQZQmoUvZcCPQQXBUHHtSGkKCe%g2a15.mail.126.com; cm_last_info=dT14bHlzXzAwMCU0MDEyNi5jb20mZD1odHRwcyUzQSUyRiUyRm1haWwuMTI2LmNvbSUyRmpzNiUyRm1haW4uanNwJTNGc2lkJTNEUEFWdXJpWVFaUW1vVXZaY0NQUVFYQlVISHRTR2tLQ2Umcz1QQVZ1cmlZUVpRbW9VdlpjQ1BRUVhCVUhIdFNHa0tDZSZoPWh0dHBzJTNBJTJGJTJGbWFpbC4xMjYuY29tJTJGanM2JTJGbWFpbi5qc3AlM0ZzaWQlM0RQQVZ1cmlZUVpRbW9VdlpjQ1BRUVhCVUhIdFNHa0tDZSZ3PWh0dHBzJTNBJTJGJTJGbWFpbC4xMjYuY29tJmw9LTEmdD0tMSZhcz10cnVl; MAIL_SESS=D57edgFxRgAtcFJD_V65tobh8mo0excLjqxW6aUYHYo6ybvYyrnuZzo1vb98CCYjBjtx0tFWuUMC.1O5i5psACy702XMP2Lpd2REQtNIotK3Xhgl9necs1ln5mmYRDR1.UdMHJF1l9kl0doqpHJSTxxSifpFA7qVTNtmMEOMuPq6UBGRDECVrre_yyMrZWKRvesbAw21zADYTc3jP_zLHkEQVbDlgt_JRDHcaR8JHU9qc; MAIL_SINFO=1603769486|0|#3&80#|xlys_000@126.com; MAIL_PINFO=xlys_000@126.com|1603769486|0|mail126|00&99|shh&1603769161&caldav#shh&null#10#0#0|173034&0|urs&mail126&note_client|xlys_000@126.com; mail_entry_sess=0da4131f493a45daeb959159b31491c7f45bca39ae649ac3cfbc6fbb363e88ec5b33a3c98bf37656a80965b40e29f49a480c75a447ba1727c9ed40922bcd09ab70938dd310c135e06eb05331ab718d91277b5bce56f477edf6c7f6816abe8942195c7abe4ae810e69f02bf74e1be9bb56fe69d9c23014a60f4748dfa3f2e14bce50d42cbbe1de06a978d0444a0c0150e57750c36d759a30d7b5dc9ae9e1dedc24e3cf66a1f70d2e4e4bb8b90ecaf092fdb376908ba96c96840e77c8106f122de; Coremail.sid=PAVuriYQZQmoUvZcCPQQXBUHHtSGkKCe; JSESSIONID=54C6C3D60C87F0F665DAB78D3F416CA5'
    # 'Cookie': 'unpl=V2_ZzNtbUVUShMmX0UEex9ZAWJXE18RXkUWdAlOByxLCAM1ABcKclRCFnQUR1xnGlQUZwAZWUZcQRxFCEdkexhdBWUKE1tLV3MlRQtGZHopXAJmAxBZRlVBHXQORlR%2fEVoAYgcaX0NncxJ1AXZkME0DUydHQgIfDxxcKDhGU3MfWg1vAhBeclZzFX0OQ1J9HVgMZzNZM0MaQxJ0CERQfxteDWYFEl1GX0UQcAxOVnopXARmAhNdRlJLEkUL; __jdv=76161171|direct|-|none|-|1603786288099; __jdu=16013553390711597445930; areaId=2; shshshfpa=2b07cd14-7e61-1a7a-4ddc-026c48dcba84-1603786290; shshshfpb=zDWFYbDAcpGoDEv99CzNGBw%3D%3D; __jda=122270672.16013553390711597445930.1601355339.1601355339.1603786288.1; __jdc=122270672; shshshfp=d3f3c6eb335df4189a8f2dcfd088887d; 3AB9D23F7A4B3C9B=I7SCN6LU6ZSKFPCP7JJHC7YEIONK6U6OY5WFWGV3EO5FHTBZSSWFTUTRN7LZM2SB5Y4XGD5SPO3ZVDV4TTPD6D3DGU; ipLoc-djd=2-2830-51803-0; wlfstk_smdl=lo5z7o2z3q02chk665m35sbbnbyyg2z2; TrackID=1UqvFscqnZKE2TdwhOQDcIzaRTfowpXgXuQz_cNsdlPcv0QpWhNRuMAdh62zMj2SYKrZhicbqE__aomkx8MOR5j4wjgL2WrlyTVBjuqsTPio; thor=97AFBBB39581FE0B6BA59BC174A1FB79181DA7881366095EFDC2FDDED6BD3642604015AE647D0DF217F996B378B74E1D88A466BD2451CB7AD8FE5270D0F9640773BD4DF1BF9F9F03ADE2EEA4E5F47929571BDEEB2CFC8B6BCA61C6C7A06BE29F64FCFEF4DA349E41EF95A6FB4C36B55ABE26BB65C58AA33BF506614DECB1AF20219966D92B8B601E6D7DA8AA8608F1B9BA93B5292E41DA2BB46CDD38AEDAE73B; pinId=p62zwICsQ-sFdno56nLZ1Q; pin=jd_hiZKLSLHhwVu; unick=jd_hiZKLSLHhwVu; ceshi3.com=000; _tp=gfCVmPlDc7hBle9zLUDvtg%3D%3D; _pst=jd_hiZKLSLHhwVu; shshshsID=b64f20f5e440f41bf508e3be9e456a36_5_1603786369048; __jdb=122270672.12.16013553390711597445930|1.1603786288'
    'Cookie': 'unpl=V2_ZzNtbUVUShMmX0UEex9ZAWJXE18RXkUWdAlOByxLCAM1ABcKclRCFnQUR1xnGlQUZwAZWUZcQRxFCEdkexhdBWUKE1tLV3MlRQtGZHopXAJmAxBZRlVBHXQORlR%2fEVoAYgcaX0NncxJ1AXZkME0DUydHQgIfDxxcKDhGU3MfWg1vAhBeclZzFX0OQ1J9HVgMZzNZM0MaQxJ0CERQfxteDWYFEl1GX0UQcAxOVnopXARmAhNdRlJLEkUL; __jdv=76161171|direct|-|none|-|1603786288099; __jdu=16013553390711597445930; areaId=2; shshshfpa=2b07cd14-7e61-1a7a-4ddc-026c48dcba84-1603786290; shshshfpb=zDWFYbDAcpGoDEv99CzNGBw%3D%3D; __jda=122270672.16013553390711597445930.1601355339.1601355339.1603786288.1; __jdc=122270672; shshshfp=d3f3c6eb335df4189a8f2dcfd088887d; 3AB9D23F7A4B3C9B=I7SCN6LU6ZSKFPCP7JJHC7YEIONK6U6OY5WFWGV3EO5FHTBZSSWFTUTRN7LZM2SB5Y4XGD5SPO3ZVDV4TTPD6D3DGU; ipLoc-djd=2-2830-51803-0; wlfstk_smdl=lo5z7o2z3q02chk665m35sbbnbyyg2z2; TrackID=1UqvFscqnZKE2TdwhOQDcIzaRTfowpXgXuQz_cNsdlPcv0QpWhNRuMAdh62zMj2SYKrZhicbqE__aomkx8MOR5j4wjgL2WrlyTVBjuqsTPio; thor=97AFBBB39581FE0B6BA59BC174A1FB79181DA7881366095EFDC2FDDED6BD3642604015AE647D0DF217F996B378B74E1D88A466BD2451CB7AD8FE5270D0F9640773BD4DF1BF9F9F03ADE2EEA4E5F47929571BDEEB2CFC8B6BCA61C6C7A06BE29F64FCFEF4DA349E41EF95A6FB4C36B55ABE26BB65C58AA33BF506614DECB1AF20219966D92B8B601E6D7DA8AA8608F1B9BA93B5292E41DA2BB46CDD38AEDAE73B; pinId=p62zwICsQ-sFdno56nLZ1Q; pin=jd_hiZKLSLHhwVu; unick=jd_hiZKLSLHhwVu; ceshi3.com=000; _tp=gfCVmPlDc7hBle9zLUDvtg%3D%3D; _pst=jd_hiZKLSLHhwVu; shshshsID=b64f20f5e440f41bf508e3be9e456a36_5_1603786369048; __jdb=122270672.12.16013553390711597445930|1.1603786288'
}

data2 = {
    "orderWareIds": 39992041300,
    "orderWareTypes": 0,
    "orderIds": 133917395720,
    "orderTypes": 22,
    "orderSiteIds": 0,
    "sendPays": 0
}
# request = Request(url2, headers=headers, data=urlencode(data2).encode())
request = Request(url2, headers=headers, data=urlencode(data2).encode())
response = urlopen(request)
print(response.read().decode('gbk'))
# ==================网易邮箱信息=====================
# {
#     "code":200,
#     "desc":"DONE",
#     "success":"false",
#     "result":{
#         "list":[
#             {
#                 "type":"DS",
#                 "addrInfo":{
#                     "country":"中国",
#                     "province":"上海市",
#                     "city":"上海市"
#                 },
#                 "loginTime":1603775998000,
#                 "loginWay":"邮箱大师"
#             }
#         ]
#     }
# }

# ================JD商城购物车信息=============================
# [
#     {
#         "extTagMapWare":null,
#         "mainProductId":0,
#         "wareType":0,
#         "yb":false,
#         "jiFen":0,
#         "stock":5,
#         "cardKey":null,
#         "discountPrice":0,
#         "stockName":null,
#         "singleShouldPrice":null,
#         "jingDouNum":0,
#         "cid":0,
#         "isShowHuiShouJiuJiLink":0,
#         "showSellForMoneyLink":0,
#         "cxlFlag":0,
#         "dynamicIcon":0,
#         "giftWare":false,
#         "frontExtMap":{
#
#         },
#         "price":null,
#         "imgPath":"//img10.360buyimg.com/N6/s60x60_jfs/t1/26265/30/2196/129757/5c19fdb9Ed39968d8/2b6dbd59af8f61f4.jpg",
#         "productId":39992041300,
#         "num":0,
#         "categoryString":"1315;1345;9748",
#         "secondHandNameAndUrl":null,
#         "snCode":null,
#         "wareUrl":"//item.jd.com/39992041300.html",
#         "color":null,
#         "name":"秋款开裆丝袜女肉色加绒保暖打底裤袜加厚连裤袜免脱开档袜子 肤色2双 2条加厚加薄绒(10-20℃)",
#         "state":1
#     }
# ]
