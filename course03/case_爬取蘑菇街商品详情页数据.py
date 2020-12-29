"""
    Aims：爬虫蘑菇街商品详情数据信息并保存mysql
    数据提取内容：
        1、商品介绍信息（商品展示轮播图+商品购买介绍参数）
            表：t_sell_info
                    【】
        2、商品详情（商品描述+产品规格参数+图文详情）
            【基于mysql5.7之后列的数据类型可以为json】
            表：t_category_template【用于新增商品和分类使用】--->根据分类关联商品主表的商品分类字段
            表：t_item_params【商品详情参数表】--->根据商品ID关联商品主表的商品ID字段
        3、商品评论（得分+分项计数+评论）
        4、类似商品推荐（链接）
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql
import time, datetime
import json


# 蘑菇街从缩略图中获取原图链接工具方法
def mogj_smalltobig_picurl_convert(origin_url):
    img_str_arr = origin_url.split('_')
    img_str_arr.pop()
    big_img_url = '_'.join(img_str_arr)
    return big_img_url


def get_goods_info_by_url(good_url):
    try:
        chrome = webdriver.Chrome()

        chrome.get(good_url)
        # 避免数据加载不过来空了
        time.sleep(10)

        # step0:获取商品ID
        good_id = chrome.current_url.split('/')[len(chrome.current_url.split('/')) - 1].split('?')[0]

        # step1：获取缩略图和原图--->这里有BUG，要先获取大图，因为小图可能没有，避免小图没有时大图为空的bug
        topimage_list = chrome.find_elements(By.XPATH, "//div[@id='J_SmallImgs']//div[1]//div[1]//ul//li//img")
        # 缩略图url集合
        top_small_image_url_list = []
        # 大图url集合
        top_big_image_url_list = []
        i = 0
        while i < len(topimage_list):
            # 将大图和小图的url均保存一份
            top_small_image_url_list.append(topimage_list[i].get_attribute("src"))
            top_big_image_url_list.append(mogj_smalltobig_picurl_convert(topimage_list[i].get_attribute("src")))
            i += 1
        # print(top_small_image_url_list)
        # print("......")
        # print(top_big_image_url_list)

        # step2：title 价格 颜色 尺码 库存等信息
        # 商品标题
        goods_title = chrome.find_elements(By.XPATH, "//h1[@class='goods-title']//span[2]")[0].text

        # 原价格：原价格也有为空的，所以加一下判断
        origin_price_el = chrome.find_elements(By.XPATH, "//span[@id='J_OriginPrice']")
        if len(origin_price_el) > 0:
            goods_origin_price = origin_price_el[0].text
        else:
            goods_origin_price = None

        # 折后价
        goods_now_price = chrome.find_elements(By.XPATH, "//span[@id='J_NowPrice']")[0].text

        # 评价数
        comment_count = chrome.find_elements(By.XPATH, "//span[@class='mr10']//span")[0].text

        # 累计销量
        total_sell_count = chrome.find_elements(By.XPATH, "//span[@class='num J_SaleNum']")[0].text

        # 折扣优惠信息
        discount_strategy_list = []
        discount_strategy = chrome.find_elements(By.XPATH, "//div[@class='promotions-needget']//div//span[1]")
        i1 = 0
        while i1 < len(discount_strategy):
            discount_strategy_list.append(discount_strategy[i1].text)
            i1 += 1

        # 颜色
        color_style_list = []
        color_style = chrome.find_elements(By.XPATH, "//div[@class='box']//dl[1]//dd//ol//li")
        i2 = 0
        while i2 < len(color_style):
            color_style_list.append(color_style[i2].text)
            i2 += 1

        # 尺码
        size_style_list = []
        size_style = chrome.find_elements(By.XPATH, "//div[@class='box']//dl[2]//dd//ol//li")
        i3 = 0
        while i3 < len(size_style):
            size_style_list.append(size_style[i3].text)
            i3 += 1

        # 库存量:肯定只有一个元素，所以直接取第一个就行了
        goods_stock = chrome.find_elements(By.XPATH, "//div[@id='J_GoodsNum']")[0].get_attribute("data-stock")

        # 收藏量
        collect_count = chrome.find_elements(By.XPATH, "//div[@class='fav item']//span[@class='fav-num']")[0].text

        # 服务说明:有的用a标签，有的用span标签，增加适配用*
        service_desc_list = []
        serviceDesc = chrome.find_elements(By.XPATH, "//div[@class='extra-services']//ul//li")
        i4 = 0
        while i4 < len(serviceDesc):
            service_desc_list.append(serviceDesc[i4].text)
            i4 += 1

        print("商品{}信息获取完成....".format(good_id))

        t_simage_urls = ",".join(top_small_image_url_list)
        t_bimage_urls = ",".join(top_big_image_url_list)
        discount_strategy_info = ",".join(discount_strategy_list)
        color_style_info = ",".join(color_style_list)
        size_style_info = ",".join(size_style_list)
        service_desc_info = ",".join(service_desc_list)

        # step3：商品描述 商品参数 效果图 [尺码说明 同类推荐(这两个暂时不要了)]
        # 商品描述,有的商品没有商品描述，所以要处理一下
        goods_desc_el = chrome.find_elements(By.XPATH, "//div[@id='J_Graphic_desc']//div[2]")
        if len(goods_desc_el) > 0:
            good_desc = goods_desc_el[0].text
        else:
            good_desc = None

        # 商品规格参数
        specifications = {}
        specifications_el = chrome.find_elements(By.XPATH, "//div[@id='J_Graphic_产品参数']//div[2]//table//tbody//tr//td")
        i5 = 0
        while i5 < len(specifications_el):
            specification_text = specifications_el[i5].text
            specification = specification_text.split(":")
            if len(specification) < 2:
                print("规格参数有误")
            else:
                specifications[specification[0]] = specification[1]
            i5 += 1
        json_specification = json.dumps(specifications, ensure_ascii=False)

        # 效果图【必须下拉到底后加载完成才会获取原图src信息,而且不能一次性拉倒底，否则还是*.gif，否则获取到的是*.gif图地址，会有问题的。】
        # 计算图片张数确定下拉循环次数，每次保证一张图的高度左右即可，为了可以充分加载，建议高度设置高一点
        img_count = len(chrome.find_elements(By.XPATH, "//div[ @class ='graphic-pic']//div[@ class ='pic-box']//img"))
        circulate_count = 0
        while circulate_count < img_count:
            js = "window.scrollTo(0," + str((circulate_count + 1) * 1000) + ")"
            chrome.execute_script(js)
            circulate_count += 1
            time.sleep(1)
        # 等整个循环下拉加载结束，图片地址已经全部由gif--->jpg即可获取img_url了
        img_els = chrome.find_elements_by_xpath("//div[ @class ='graphic-pic']//div[@ class ='pic-box']//img")
        i6 = 0
        img_urls = []
        # 加3是因为开头有一部分，多算几次，沸点时间可以保证数据完整性。
        while i6 < len(img_els):
            img_urls.append(img_els[i6].get_attribute("src"))
            i6 += 1
        final_img_urls = ",".join(img_urls)

        good_sell_info_tuple = (
            good_id, 'boyfriend', t_simage_urls, t_bimage_urls, goods_title, goods_origin_price, goods_now_price, int(
                comment_count),
            int(total_sell_count), discount_strategy_info, color_style_info, size_style_info, int(goods_stock),
            int(collect_count),
            service_desc_info, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0)

        good_detail_tuple = (good_id, good_desc, json_specification, final_img_urls)
        print("商品{}信息格式化完毕，准备入库...".format(good_id))
        chrome.close()

        good_sell_info = [good_sell_info_tuple, good_detail_tuple]
        return good_sell_info
    except Exception as e:
        print("获取单个商品详情数据出现异常")
        print(e)


def goods_info_into_db_one_by_one(good_info):
    db = pymysql.connect(host="127.0.0.1", user="root", password="123789Xlys!@#$", database="datacollection", port=3306)
    cursor = db.cursor()
    good_add_sql1 = """insert into t_sell_info (good_id,good_type,top_simage_urls,top_bimage_urls,title,origin_price,now_price,
                                    comment_count,total_sell_count,discount_strategy,color_style,size_style,stock,collect_count,service_style,create_time,valid_flag)values 
                                                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    good_add_sql2 = """insert into t_detail_info (good_id,goods_desc,goods_speciafications,goods_detail_imgurls) values (%s,%s,%s,%s)"""
    try:
        cursor.execute(good_add_sql1, good_info[0])
        cursor.execute(good_add_sql2, good_info[1])
        db.commit()
        print("商品{}信息入库成功...".format(good_info[0]))
    except Exception as e:
        print("商品信息插入数据库异常!")
        db.rollback()
        print(e)
    finally:
        db.close()


def goods_info_into_db_all_at_once(good_info_list):
    db = pymysql.connect(host="127.0.0.1", user="root", password="123789Xlys!@#$", database="datacollection", port=3306)
    cursor = db.cursor()
    good_add_sql = """insert into t_sell_info (good_id,top_simage_urls,top_bimage_urls,title,origin_price,now_price,comment_count,total_sell_count,discount_strategy,color_style,size_style,stock,collect_count,service_style,create_time,valid_flag)values 
                                                    (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    try:
        cursor.executemany(good_add_sql, good_info_list)
        db.commit()
        print("所有商品信息入库成功...")
    except Exception as e:
        print("商品信息插入数据库异常!")
        db.rollback()
        print(e)
    finally:
        db.close()


# url1 = "https://shop.mogu.com/detail/1m5ovm4?acm=3.ms.1_4_1m5ovm4.15.1343-102815-68998.dQSxjsk8UflsU.sd_117-swt_15-imt_6-c_1_3_588263663_0_0_3-t_dQSxjsk8UflsU-lc_3-fcid_50240-pid_180-pit_1-dit_-idx_0-dm1_5002&cparam=MTYwODg2MDg2OV8xMWtfZmU1N2VhMzkzY2MyMmNkODljNTg3ODI3ZWMwYTA0NDVfM18wXzU4ODI2MzY2M180ZjhmXzBfMF8wXzkwMF8xXzNfbG9jLTA=&ptp=31.Onv5v.0.0.ImiJ4fld"
# url2 = "https://shop.mogu.com/detail/1m1h6ms?acm=3.mce.1_4_1m1h6ms.5124.0-32450.r9fL8sk98ITX2.sd_119_115-mid_5124-pos_6-pm_009-lc_201&ptp=31.rGaCTb._rechot.1.mdIs7vpa"
# url3 = "https://shop.mogu.com/detail/1mlmpmq?acm=3.ms.1_4_1mlmpmq.15.1343-102815-68998.dQSxjsk8UflsU.sd_117-swt_15-imt_6-c_1_3_532491279_0_0_3-t_dQSxjsk8UflsU-lc_3-fcid_50240-pid_180-pit_1-dit_-idx_2-dm1_5002&cparam=MTYwODg2MDg2OV8xMWtfZmU1N2VhMzkzY2MyMmNkODljNTg3ODI3ZWMwYTA0NDVfM18wXzUzMjQ5MTI3OV80ZjhmXzBfMF8wXzgxMF8xXzNfbG9jLTA=&ptp=31.Onv5v.0.0.ImiJ4fld"
url4 = "https://shop.mogu.com/detail/1mn5puk"

# 获取分类主页地址，拿到所有商品详情页链接【不知道为啥，目前只能爬40~80条，反正做数据测试够用了，后面再研究吧】
# 上衣clothing
clothing_base_url = "https://list.mogu.com/book/clothing?ptp=31.Xnum1.0.0.H8xBcUYD"
# 裙子skirt
skirt_base_url = "https://list.mogu.com/book/skirt?ptp=31.Gfr19.0.0.T244EaJS"
# 裤子trousers
trousers_base_url = "https://list.mogu.com/book/trousers?ptp=31.vOv15b.0.0.BzV8Bf75"
# 内衣underwear
underwear_base_url = "https://list.mogu.com/book/neiyi/50025?acm=3.mce.1_10_1ko5a.132244.0.6T7ntskktbGzM.pos_876-m_482179-sd_119&ptp=31.v5mL0b._head.0.WcqTOpaZ"
# 鞋子shoes
shoes_base_url = "https://list.mogu.com/book/shoes?ptp=31.ebrCK.0.0.2VrYLg6o"
# 包包bags
bags_base_url = "https://list.mogu.com/book/bags?ptp=31.OKiTfb.0.0.0TkV8IWT"
# 男友boyfriend
boyfriend_base_url = "https://list.mogu.com/book/boyfriend?ptp=31.Gfr19.0.0.xPwXA89B"
# 母婴baby
baby_base_url = "https://list.mogu.com/book/baby?ptp=31.OifDKb.0.0.JLBZraZX"
# 家具furniture
furniture_base_url = "https://list.mogu.com/book/home/20000371?acm=3.mce.1_10_1ko5g.132244.0.6T7ntsklWJa9E.pos_879-m_482182-sd_119&ptp=31.v5mL0b._head.0.H4x8cAeh"

# 批量数据请求并操作入库
chrome = webdriver.Chrome()
# 切换商品类别 并在goods_type中修改
chrome.get(boyfriend_base_url)
clothing_goods_detail_urls = []
clothing_goods_detail_url_el_list = chrome.find_elements(By.XPATH,"//div[@id='wall_goods_box']//div[2]//div//div//a[3]")
i0 = 0
while i0 < len(clothing_goods_detail_url_el_list):
    clothing_goods_detail_urls.append(clothing_goods_detail_url_el_list[i0].get_attribute("href"))
    i0 += 1
for url in clothing_goods_detail_urls:
    good_sell_info = get_goods_info_by_url(url)
    goods_info_into_db_one_by_one(good_sell_info)
chrome.close()

# 单条数据测试
# good_sell_info = get_goods_info_by_url(url4)
# goods_info_into_db_one_by_one(good_sell_info)
print("爬取蘑菇街商品详情数据-->sell-info成功!")
# print(clothing_goods_detail_urls)
