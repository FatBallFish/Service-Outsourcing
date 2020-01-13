from Hotel import settings
# 导入图形模块，随机数模块
from PIL import Image,ImageDraw,ImageFont
from extral_apps import MD5
import random
import logging,sys
import os
import io,base64
# path=""
code_str = ""
webpath = ""
fonts_list = []
log_img = logging.getLogger("ImgCaptcha")

def Initialize(main_path:str):
    """
ImgCaptcha 模块初始化，此函数应在所有函数之前调用
    :param cfg_path: 配置文件地址。
    :param main_path: 程序主目录地址。
    """
    global Main_filepath
    Main_filepath = main_path
    # print(Main_filepath)
    log_img.info("Module ImgCaptcha loaded")
    print("【ImgCaptcha】Module ImgCaptcha loaded")

def LoadFontsFile(filepath):
    global fonts_list
    fonts_list.clear()
    path_list =  os.listdir(filepath)
    for filename in path_list:
        if os.path.splitext(filename)[1] in ['.ttf',".TTF",".otf",".OTF"]:
            # print("Fonts:",filename)
            fonts_list.append(os.path.join(filepath,filename))
            # print(os.path.join(filepath,filename))

def CreatCode()->tuple:
    """
创建一个验证码图片文件，返回验证码图片base64数据（*.png）
    :param font: 字体文件名
    :return: 元组，(验证码内容，验证码图片base64数据)
    """
    global code_str
    global webpath,path
    try:
        LoadFontsFile(os.path.join(Main_filepath,"fonts"))
    except Exception as e:
        log_img.error(e)
        print("UnknownError:",e)
        log_img.info("Program Ended")
        sys.exit()
    font_num = len(fonts_list)
    # print("字体个数总共有",font_num,"个")
    font = fonts_list[random.randint(0,font_num-1)]
    code_str = ""
    # 定义使用image类实例化一个长为120px，宽为30px，基于RGB的（255，255，255）颜色的图片
    img1 = Image.new(mode="RGB",size=(120,30),color=(255,255,255))
    # 实例化一支画笔
    draw1 = ImageDraw.Draw(img1,mode="RGB")
    # 定义要使用的字体,第一个参数表示字体的路径,第二个参数表示字体大小
    try:
        font1 = ImageFont.truetype(font,28)
    except:
        log_img.error("Failed to load font [%s]",font)
        print("Failed to load font [%s]" % font)
        return "Error",""

    for i in range(5):
        # 每循环一次，从a到z中随机生成一个字母或数字
        # 使用ASCII码，A-Z为65-90，a-z为97-122，0-9为48-57,使用chr把生成的ASCII码转换成字符
        # str 把生成的数字转换成字符串
        char1 = random.choice([chr(random.randint(65,90)),chr(random.randint(48,57)),chr(random.randint(97,122))])
        code_str += char1
        # 每循环一次重新生成随机颜色
        color1 = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
        # 把生成的字母或者数字添加到图片上
        # 图片长度为120px，要生成5个数字或字母则每添加一个，其位置就要向后移动24px
        if random.randint(0,1):
            draw1.line((0,random.randint(0,30),120,random.randint(0,30)),color1,0)
        draw1.text([i*20+10,0],char1,color1,font1)
    #print(code_str)
    # 把生成的图片保存为“pic.png”格式，文件名通过加盐获得

    # file_name = "%s.png"%MD5.md5(code_str)
    # file_path = os.path.join(path,file_name)
    try:
        img_crop = img1.crop()
        img_ByteArr = io.BytesIO()
        img_crop.save(img_ByteArr,format="png")
        img_ByteData = img_ByteArr.getvalue()
        img_b64_byte = base64.b64encode(img_ByteData)
        img_b64_str = bytes.decode(img_b64_byte)
        log_img.info("Created a captcha [%s]",code_str)
        return (code_str,img_b64_str)
    except:
        log_img.error("Failed to translate img to base64  data")
        return "Error",""
def GetCodeText()->str:
    """
返回验证码内容
    :return: 验证码内容
    """
    return code_str

# def GetCodePath()->str:
#     """
# 返回验证码保存目录
#     :return: 验证码保存目录
#     """
#     return path

if __name__ == "__main__":
    CreatCode()