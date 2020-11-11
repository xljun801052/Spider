"""
    知识拓展：
        1.请求的data数据是bytes类型?后续研究...
            # print(type(payload))  # <class 'dict'>
            # print(type(urlencode(payload)))  # <class 'str'>
            # print(type(urlencode(payload).encode()))  # <class 'bytes'>

        2.下面两种方法将data数据转成bytes类型都可以，结果一样
            # print(urlencode(payload).encode())
            # print(bytes(urlencode(payload), encoding='utf-8'))

        3.工具地址：
            http://httpbin.org/post--->可以返回该post请求的请求信息，包括头信息、请求参数、请求客户端ip等等

        4.获取当前毫秒级时间戳：
            int(round(time.time()*1000))

"""

from urllib.request import urlopen, Request
from fake_useragent import UserAgent
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener
from http import cookiejar
import json
import time

# 登录表单提交之前请求地址
step1_url = 'https://passport.126.com/dl/gt?'

# 请求头
step1_headers = {
    'User-Agent': UserAgent().chrome,
    # 这里需要带上Cookie字段，返回才会有"tk":"0b056abfda4fa46962ec1761172b1830"的值，这个’tk‘的值用于下一次提交表单请求
    'Cookie': '_ihtxzdilxldP8_=30; THE_LAST_LOGIN=xlys_000@126.com; nts_mail_user=xlys_000@126.com:-1:1; utid=Tuz4X23A20EcGeNyobIjLQHKd9s5fFdG; SID=2b1f0812-225a-420e-944b-f43b49832475; NTESwebSI=4909CDEABF636D5506F8668027E8D3E8.urs-virt20-regother25.jd.163.org-8009; ANTICSRF=cleared; P_INFO=xlys_000; NTES_OSESS=cleared; S_OINFO=; l_s_mail126QdQXWEQ=55835D327313F36E6F208A63B108DBD447297ED589CA43571BC6AB0B75DC53D8DE39F0D02CA62361FF6EA121FC15CEC8D174E5BFAE1966CF056E1DFE95B08E4D47C123A4A83104ADBEC73AE5E63C4BE9D1AA2CE0BCC5F05CF13DBB63BB0E0611BB95CAA09C2FD1F609F04F847D3B412D; JSESSIONID-WYTXZDL=hrod%2F%5CH2%2FMoLwavw%2FAKLT96wA%2FSMEZy7DfSQHacJKmrt9bJ%5CXUpgjAhH6i1%5Cgxf7dd9FGZr6l0ZgpPSZP0vqhNJ3D3EufFuuoBSDltxfpq5tHLx%2BkRHRuuBLKOM%2FFMiy9U70SSxxMyXNscGOK70VGL%5Cow4RMYHw6ZD7Al8lbhY%2Fsxxzy%3A1605109017466'
}

# 携带载荷数据
step1_payload = {
    'un': 'xlys_000@126.com',
    'pkid': 'QdQXWEQ',
    'pd': 'mail126',
    'channel': 0,
    'topURL': 'https://mail.126.com/',
    'rtid': 'YST8i3AWgPM37NtbcwUG8WAiq9q4gEoi',
    'nocache': int(round(time.time() * 1000))
}

# 构造请求
step1_data = urlencode(step1_payload)
request = Request(step1_url + step1_data, headers=step1_headers)
# 利用HTTPCookieProcessor和build_opener()构造可以保存cookie的opener：原理是HTTPCookieProcessor内部有用来保存cookie的CookieJar类
opener = build_opener(HTTPCookieProcessor(cookiejar.CookieJar()))
response = opener.open(request)
# 拿到tk的值用于构造下一次请求
print(response.read().decode())  # {"ret":"201","tk":"0b056abfda4fa46962ec1761172b1830"}

# 登录表单提交地址
step2_url = 'https://passport.126.com/dl/l'

# 请求头
step2_headers = {
    'User-Agent': UserAgent().chrome,
    'Content-Type': 'application/json',
    # 'Accept': '*/*',
    # 'Accept-Encoding': 'gzip, deflate, br',
    # 'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Cache-Control': 'no-cache',
    # 'Connection': 'keep-alive',
    'Cookie': '_ihtxzdilxldP8_=30; THE_LAST_LOGIN=xlys_000@126.com; nts_mail_user=xlys_000@126.com:-1:1; utid=Tuz4X23A20EcGeNyobIjLQHKd9s5fFdG; SID=2b1f0812-225a-420e-944b-f43b49832475; NTESwebSI=4909CDEABF636D5506F8668027E8D3E8.urs-virt20-regother25.jd.163.org-8009; ANTICSRF=cleared; P_INFO=xlys_000; NTES_OSESS=cleared; S_OINFO=; l_s_mail126QdQXWEQ=55835D327313F36E6F208A63B108DBD447297ED589CA43571BC6AB0B75DC53D8DE39F0D02CA62361FF6EA121FC15CEC8D174E5BFAE1966CF056E1DFE95B08E4D47C123A4A83104ADBEC73AE5E63C4BE9D1AA2CE0BCC5F05CF13DBB63BB0E0611BB95CAA09C2FD1F609F04F847D3B412D; JSESSIONID-WYTXZDL=hrod%2F%5CH2%2FMoLwavw%2FAKLT96wA%2FSMEZy7DfSQHacJKmrt9bJ%5CXUpgjAhH6i1%5Cgxf7dd9FGZr6l0ZgpPSZP0vqhNJ3D3EufFuuoBSDltxfpq5tHLx%2BkRHRuuBLKOM%2FFMiy9U70SSxxMyXNscGOK70VGL%5Cow4RMYHw6ZD7Al8lbhY%2Fsxxzy%3A1605109017466'
}

# 携带载荷数据
step2_payload = {
    'channel': 0,
    'd': 10,
    'domains': "163.com",
    'l': 0,
    'pd': "mail126",
    'pkid': "QdQXWEQ",
    # 这里的pw是加密过的，每次都不一样...如何获取加密结果构造请求数据呢？--->>>js代码加密？
    'pw': "tit3IzQ/SadRu1oDl1A5GSpsKLYrbY2YnWy3QrBzvJ9ElLyR+CfDcJeOACxraZH0PCcgHUc2duXoHY+LIpZ4ctoAY3z5PFboRjW6GQlvHh0bgl0TIyRKlbUnOraqrZ3X5xWfKf/DIhKAhgNCUb3CL/TlYgkBBJLghG3KiDlEBpQ=",
    'pwdKeyUp': 1,
    'rtid': "YQRj2WWptMwb0wsnBlGDHzNi7YJIQm0c",
    't': int(round(time.time() * 1000)),
    'tk': "0b056abfda4fa46962ec1761172b1830",
    'topURL': "https://mail.126.com/",
    'un': "xlys_000@126.com"
}
request2 = Request(step2_url, headers=step2_headers, data=urlencode(step2_payload).encode())
response = opener.open(request2)
print(response.read().decode())
