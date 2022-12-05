import warnings
from utils import *

class DeSpiral:

    """Undo the Spiral, by filling array by array"""

    def __init__(self, first, second):
        #print("filling")
        self.array = np.zeros((second.shape[0] + 1, first.shape[1]))
        self.height, self.width = self.array.shape
        if self.height == self.width:
            warnings.warn("Same height as width: DeSpiral middle line will be degenerate")

        self.fill(first)
        self.fill(second)


    def fill(self, array):
        if array.size == 0:
            return
        height, width = array.shape

        if (width != 1 and self.height < self.width) or (height == 1 and self.height >= self.width):
            #line 
            width_offset = self.width - width
            diag = width_offset//2
            if width_offset % 2 == 0:
                #UP
                for i,n in enumerate(array[0]):
                    #print(i,n)
                    self.array[diag, diag + i] = n

            else:
                #DOWN
                for i,n in enumerate(array[0]):
                    #print(i,n)
                    self.array[-(1 + diag), diag + i] = n

        else:
            #column             
            height_offset = self.height - height
            diag = (height_offset + 1)//2 
            
            if height_offset % 2 == 0:
                #LEFT
                for i,n in enumerate(array[:,0]):
                    #print(i,n)
                    self.array[diag+i, diag-1] = n

            else:
                #RIGHT
                for i,n in enumerate(array[:,0]):
                    #print(i,n)
                    self.array[diag+i, -diag] = n

    
    def result(self):
        return self.array

def to_arrays(bytes:bytes) -> list[np.ndarray]:
    pattern = b'|'.join([f.magic_num for f in Format])

    starts = [(m.start(0)) for m in re.finditer(pattern, bytes)]
    starts.append(len(bytes))
    res = []
    i = 0
    while i < len(starts)-1:
        #print(i)
        if get_format(bytes[starts[i]:]) == Format.XBM:
            res.append(to_array(Image.open(io.BytesIO(repair(bytes[starts[i]:starts[i+2]])))))
            i+=1
        else:
            res.append(to_array(Image.open(io.BytesIO(repair(bytes[starts[i]:starts[i+1]])))))
        i+=1
    return res

def solve_challenge(chall_path='challenge'):
    with open(chall_path, 'rb') as f:
        bytes = f.read()#
        arrays = to_arrays(bytes)
        d = DeSpiral(arrays[0], arrays[1])
        for a in arrays[2:]:
            d.fill(a)
        array = d.result()
        img = to_image(array)
        img.save('solved.png')

solve_challenge()