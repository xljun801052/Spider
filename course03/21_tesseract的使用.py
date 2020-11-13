"""
    一、现在没有哪个页面不需要验证码、滑块拖动。点击验证等验证信息。面对此类网页登录就是个难题，如何解决？
        前提：以下所有步骤操作是在同一个session会话下，为啥呢？考虑多个用户登录情况就知道了!
            1.tesseract使用背景和流程
                ①获取登录页面(登录页面中含有验证码等链接URL)
                ②获取验证码
                ③处理验证码(方式有多种)
                    ①手动处理填写
                    ②使用图像识别技术：Tesseract ocr【Google开源的一款图像识别工具】
                        ①GitHub【需下载安装使用】：https://github.com/xljun801052/tesseract
                            【tesseract-ocr语言包库地址：https://github.com/tesseract-ocr/tessdata/blob/master/eng.traineddata。使用的话下载后放到安装根目录下的tessdata目录下即可】
                        ②command：tesseract 输入文件名 输出文件名
                        ③当然原生的tesseract OCR识别能力有限，容易受到干扰，识别度较低。
                         但是可以通过文字训练【tesseract OCR训练】来提高识别能力 ， 这个数据人工智能方向了...
                    ③使用云打码平台进行识别(人工+技术识别)
                ④构造登录参数信息
                    username
                    password
                    code
                    ....
                ⑤发送登录请求

            2.python中使用tesseract的demo
                ①安装软件
                    【win平台】安装tesseract软件，并配置环境变量：
                        i:Path中配置tesseract-ocr根路径--->>>D:\software\Tesseract-OCR
                        ii:新建环境变量’TESSDATA_PREFIX‘并配置tesseract-ocr根路径下的tessdata目录--->>>D:\software\Tesseract-OCR\tessdata
                    【unix平台】安装tesseract-ocr
                        sudo apt install tesseract-ocr
                        sudo apt install libtesseract-dev

                ②安装库
                    pip install pytesseract

                ③引入后使用
                    import pytesseract
                    from PIL import Image

            3.【如遇pycharm使用tesseract-ocr意外报错】
                命令行输入:SET TESSDATA_PREFIX=D:\tesseract\Tesseract-OCR
                【参考：https://blog.csdn.net/weixin_42812527/article/details/81908674】
"""
import pytesseract
from PIL import Image

for i in range(1, 4):
    image = Image.open('../testdata/yzm{}.jpg'.format(i))
    code = pytesseract.image_to_string(image)
    print('验证码'+str(i)+':'+code)
    # 验证码1:
    # 验证码2:6 2290
    #
    #
    # 验证码3:7 3 6 4
