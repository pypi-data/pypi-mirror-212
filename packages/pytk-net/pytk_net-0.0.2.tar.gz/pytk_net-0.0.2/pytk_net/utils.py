import json
from hashlib import md5
from os import path
from typing import Dict

from PIL import ImageFont, Image, ImageDraw
from PIL import ImageTk
from PIL.ImageTk import PhotoImage


def fpath(name):
    """
    解决打包后图片找不到的问题
    """
    new_path = path.abspath(path.join(path.dirname(__file__), name))
    return new_path


ICON_FONT_PATH = fpath("./icons/bootstrap-icons.woff")

"""
存放打开的图片
"""
img_obj_dic: Dict[str, PhotoImage] = {}


def load_image(img_path, width, height):
    """
    加载图片
    """
    global img_obj_dic
    key = img_path + str(width) + str(height)
    key = key.encode("utf-8")
    key = md5(key).hexdigest()
    if key in img_obj_dic.keys():
        return img_obj_dic[key]
    img = ImageTk.PhotoImage(image=Image.open(img_path).resize((width, height)))
    img_obj_dic.update({key: img})
    return img_obj_dic[key]


def uni_2_png(val, img_size, color):
    font = ICON_FONT_PATH
    img = Image.new("RGBA", (img_size, img_size))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(font, int(img_size * 0.95))

    val = chr(val)
    x, y = draw.textsize(val, font=font)
    draw.text(((img_size - x) // 2, (img_size - y) // 2), val, font=font, fill=color)
    return img


def load_font_icon(val, size=512, color="#000"):
    """
    加载图标
    """
    global img_obj_dic
    key = "icon_" + str(val) + str(size) + color
    key = key.encode("utf-8")
    key = md5(key).hexdigest()
    if key in img_obj_dic.keys():
        return img_obj_dic[key]
    img = ImageTk.PhotoImage(image=uni_2_png(val, size, color))
    img_obj_dic.update({key: img})
    return img_obj_dic[key]


def get_icon_val(name):
    f = open(fpath("static/bootstrap-icons.json"), mode='r', encoding='utf-8')
    icons = json.load(f)
    f.close()
    return icons[name]
