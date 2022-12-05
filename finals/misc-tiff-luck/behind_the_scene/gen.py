from PIL import Image, ImageFont
import numpy as np
from enum import Enum
import io
import re 
from utils import *

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

class Spiral:

    """Deconstruct the array in to set of lines, 
    in spiral order (starting by the first row, going clockwise)"""

    def __init__(self, array):
        self.array = array
        self.dir = Direction.UP

    def __iter__(self):
        return self

    def __next__(self):
        if self.array.size == 0:
            raise StopIteration
         
        match self.dir:
            case Direction.UP:
                result = self.array[0]
                result = result.reshape(1,result.size)
                self.array = self.array[1:]
            
            case Direction.DOWN:
                result = self.array[-1]
                result = result.reshape(1,result.size)
                self.array = self.array[:-1]

            case Direction.RIGHT:
                result = self.array[:,-1]
                result = result.reshape(result.size,1)
                self.array = self.array[:,:-1]

            case Direction.LEFT:
                result = self.array[:,0]
                result = result.reshape(result.size,1)
                self.array = self.array[:,1:]

        self.dir = Direction((self.dir.value + 1) % len(Direction))
        return result


flag = 'EPFL{d1dn7_u53_71FF_for_4_r3as0n}'

def create_flag_img(flag=flag, name='flag.png'):
    offset = 4
    #maybe load from file, to ascii art maybe?
    #font = ImageFont.load_default()
    font = ImageFont.truetype('FreeSerif.ttf', 20) # at /usr/share/fonts/truetype/freefont/
    text_width, text_height = font.getsize(flag)


    # create a blank canvas with extra space between lines
    img = Image.new('1', (text_width + 2*offset, text_height + 2*offset), "white")
    
    mask = font.getmask(flag, mode='1')
    d = Image.core.draw(img.im, 0)
    d.draw_bitmap((offset, offset), mask, 0)
    #resulting flag
    img.save(name)


def create_challenge(flag_path='flag.png', dst_name = 'challenge'):
    img = Image.open(flag_path)
    np_array = to_array(img)
    
    #print(np_array.shape)
    res = b''
    formats = [f for f in Format]
    for i,line in enumerate(Spiral(np_array)):
        data = to_data(line, formats[i%len(Format)])
        
        # Uncomment to see imperfections in repair 
        #if repair(data[:-2]) != data:
        #    print(formats[i%len(Format)], line.shape,repair(data[:-2])[-2:] , data[-2:])
        #else:
        #    print(formats[i%len(Format)])
        #if formats[i%len(Format)] == Format.WEBP:
        #    print(i, formats[i%len(Format)], data[-2:])
        res += data[:-2]

    with open(dst_name, 'wb') as f:
        f.write(res)

create_flag_img()
create_challenge()


