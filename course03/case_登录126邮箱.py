from urllib.request import urlopen, Request
from fake_useragent import UserAgent
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener
from http import cookiejar

# 登录表单提交地址
url = 'https://passport.126.com/dl/l'

# 请求头
headers = {
    'User-Agent': UserAgent().chrome,
    # 'Cookie': '_ihtxzdilxldP8_=30; THE_LAST_LOGIN=xlys_000@126.com; nts_mail_user=xlys_000@126.com:-1:1; gdxidpyhxdE=bDQHWbR%2FBcMuZsyrwgX5CDBCnnYS0Thry7RK1bxVx6A58dJytIesMwbq3YJSMGC939Qxuyjex%5CgUdMEmkNZIi4DJCvfiDwUDS3CvalaxwwBz0yuLE3a6J7MMgPXW60qr37Ie9e99C8gAh94iqJcnBqzfgvoZH%2BwQ%5Cc3OiJCMVZX9VyVk%3A1603770294168; _9755xjdesxxd_=32; YD00000710348764%3AWM_NI=KQy%2FuDntUCYwpqrKky%2BqnSRXDgoJusvA5CFhOWXN6Mlges4BUYWnIWIxfBFOGKErUV01FiFPL3euBkTuBw6%2BhnBN5Dl%2FkO%2BkZM4QV9ztFpmRBVy%2FCbI%2Fc4Z91TxWwtWOYXI%3D; YD00000710348764%3AWM_NIKE=9ca17ae2e6ffcda170e2e6eeacfc6393a787a2c25a8c928ea2c54e879a9faaf142bbee9eb6f763fb9299afb62af0fea7c3b92a898fb7d0f850aeac9ba4dc7db4afbeacea73e9afa2b4d15488b9a1abf879b69ffba4c5648d8998afb547b0b9ab94b74a9787998fcc5d8ba8aaa3c54585958b93d85ef4ef8a8ac55c90edab96c16198ab8e98b521acb28eafb850b0f1a5b0aa619a93fcb2d533baac8a91f05a828ab7d0c26a8bf1add5d933f38cb8b8f680959197b9cc37e2a3; YD00000710348764%3AWM_TID=3f8OpVhjxBhBBFRUVANvN3nBA8m9MCZ7; P_INFO=xlys_000@126.com|1603849996|0|mail126|00&99|shh&1603792842&mail_client#shh&null#10#0#0|173034&0|urs&mail126&note_client|xlys_000@126.com; JSESSIONID-WYTXZDL=JuHJbP%2F5%5C4S%2Fjel3srTdGU%5C1aX5ppdHX9qMp%5CwIKmc8Ks85mb%2FTheDN%2BFvY1mNwYqQBttE7NS%2BEtOyUfdU6ZoAx%5Cy2L3s1xJ7v0dwSNtaWL63ALf5WkJTjJP2ROPe3csltrYVW4ud7T%2FGyPTht%2B01v%2FTPaSSFdrThw9%5CKMPldeSk%2Bt5I%3A1605086114446; utid=NgHmdCJvnkB1zhgAgW2c4JqWcY9FVCtQ; l_s_mail126QdQXWEQ=55835D327313F36E6F208A63B108DBD4AE517ADAEE37DC874856B83A2FBEB4E340B18C14AEB7ED4EFF01E556909CA0ED7E6BF61C05FC9090EFFDF40AA4B32DB65E6E1FEA876EDA63B96EE91D649A541AE56351F0EE2E0A14116804B8323F24F2E8E71432A3CA7E0C12D451A319DE8B6D'
}

# 携带载荷数据
payload = {
    'channel': 0,
    'd': 10,
    'domains': "163.com",
    'l': 0,
    'pd': "mail126",
    'pkid': "QdQXWEQ",
    'pw': "tit3IzQ/SadRu1oDl1A5GSpsKLYrbY2YnWy3QrBzvJ9ElLyR+CfDcJeOACxraZH0PCcgHUc2duXoHY+LIpZ4ctoAY3z5PFboRjW6GQlvHh0bgl0TIyRKlbUnOraqrZ3X5xWfKf/DIhKAhgNCUb3CL/TlYgkBBJLghG3KiDlEBpQ=",
    'pwdKeyUp': 1,
    'rtid': "YQRj2WWptMwb0wsnBlGDHzNi7YJIQm0c",
    't': 1605085543661,
    'tk': "a8105c6030f99e4cde63133cd653a664",
    'topURL': "https://mail.126.com/",
    'un': "xlys_000@126.com"
}

# 请求的data数据是bytes类型?后续研究...
# print(type(payload))  # <class 'dict'>
# print(type(urlencode(payload)))  # <class 'str'>
# print(type(urlencode(payload).encode()))  # <class 'bytes'>

# 构造请求
request = Request(url, headers=headers, data=urlencode(payload).encode())

# 利用HTTPCookieProcessor和build_opener()构造可以保存cookie的opener：原理是HTTPCookieProcessor内部有用来保存cookie的CookieJar类
opener = build_opener(HTTPCookieProcessor(cookiejar.CookieJar()))
response = opener.open(request)
print(response.read().decode())
