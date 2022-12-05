from PIL import Image, ImageFont
import numpy as np
import re 
from PIL import Image, ImageFont
from enum import Enum
import io

class Format(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self, format, magic_num):
          self.format = format
          self.magic_num = magic_num

    JPEG = "JPEG", b"\xff\xd8\xff\xe0"
    PNG = "PNG", b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"
    #TIFF = "TIFF", b"\x49\x49\x2A\x00"
    PPM = "PPM", b"P4\n"
    BMP = "BMP", b"\x42\x4D"
    GIF = "GIF", b"GIF87a"
    XBM = "XBM", b"#define" #normally just #define
    WEBP = "WEBP" , b"RIFF"

def reduce_pixel(x,y):
    assert x==y
    if x == 0:
        return 0
    elif x == 255:
        return 255
    else :
        raise ValueError

def sharpen_pixel(x):
    if x > 126:
        return 255
    else:
        return 0

def to_array(img: Image) -> np.ndarray:
    """ Tranforms an image to a boolean np array"""
    res = np.array(img)
    if img.format ==  Format.WEBP.format: #WebP
        assert res.ndim == 3
        res = np.frompyfunc(reduce_pixel, 2,1).reduce(res, axis=2)

    if img.format == Format.JPEG.format:
        res = np.vectorize(sharpen_pixel)(res)
        
    return res.astype(bool)

def to_image(np_array) -> Image:
    """ Return an image from a given boolean array"""
    #assert(np_array.dtype==bool)
    array = (np_array*255).astype(np.uint8)
    img = Image.fromarray(array, mode='L').convert(mode='1')
    return img

def to_data(array, format:Format) -> bytes:
    """
    Given an array prints out the corresponding bytes
    """
    byte_arr = io.BytesIO()
    line = to_image(array)
    match format:
        case Format.PNG:
            line.save(byte_arr, format=format.format, compress_level=0)
        #case Format.TIFF:
        #    line.save(byte_arr, format=format.format, compression=None)
        case Format.WEBP:
            line.save(byte_arr, format=format.format, lossless=True)
        case _:
            line.save(byte_arr, format=format.format)
    return byte_arr.getvalue()


def get_format(bytes:bytes) -> Format:
    for f in Format:
        if bytes.startswith(f.magic_num):
            return f
    raise TypeError

def repair(bytes:bytes):
    match get_format(bytes):
        case Format.PNG:
            return bytes + b'\x60\x82'
        case Format.JPEG:
            return bytes + b'\xff\xd9'
        case Format.XBM:
            return bytes + b'\x3b\x0a'
        case Format.GIF:
            return bytes + b'\x00\x3b'
        #case Format.WEBP:
        #    return bytes + b'\x87\x07'
        case _:
            return bytes + b'\x00\x00'