import svgpathtools as pathtools
import math
import numpy as np

template = """\\documentclass[tikz,border=10pt,multi]{{standalone}}

\\begin{{document}}
	\\begin{{tikzpicture}}
		
		
{draw}
        
		
	\\end{{tikzpicture}}

\\end{{document}}"""

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def det(v1,v2):
    return v1[0]*v2[1] - v1[1]*v2[0]
def angle(v1, v2):
    return math.copysign(1, det(v1,v2))*math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))

def find_center(x1, y1, x2, y2, r, sweep):
    x11 = (x1 - x2)/2
    y11 = (y1 - y2)/2
    scaler = math.sqrt((r**4 - r**2 * y11**2 - r**2 * x11**2)/(r**2 * y11**2 + r**2 * x11**2))
    if not sweep: #sweep!= False = large_arc
        scaler *= -1
    cx1 = scaler * r*y11/r
    cy1 = -scaler * r*x11/r
    cx = cx1 + (x1+x2)/2
    cy = cy1 + (y1+y2)/2
    return cx,cy

def get_path(c:chr, offset, scale = 0.1, isStr:bool=False):
    path, _ = pathtools.svg2paths(f"font/{c}.svg")
    s = ""
    xmin, xmax, ymin, ymax = path[0].bbox()
    max = -1000 *scale
    for c in path[0]:
        if type(c) is pathtools.path.Line:
            start = c.start
            end = c.end
            if isStr:
                s += f"\\draw[ultra thick] ({scale*start.real} + {offset}, {-scale*start.imag}) -- ({scale*end.real} + {offset},{-scale*end.imag});\n"
            else:
                s += f"\\draw[ultra thick] ({scale*start.real+ offset}, {-scale*start.imag}) -- ({scale*end.real+ offset},{-scale*end.imag});\n"
            #s += f"\\draw ({scale*start.real}, {-scale*start.imag}) -- ({scale*end.real},{-scale*end.imag});\n"
        elif type(c) is pathtools.path.Arc:
            #print(c)
            start = c.start
            radius = c.radius.real
            end = c.end
            sweep = c.sweep

            cx, cy = find_center(start.real, start.imag, end.real, end.imag, radius, sweep)
            start_angle = angle([1,0],[start.real-cx, start.imag-cy])
            end_angle = angle([1,0],[end.real-cx, end.imag-cy])

            #Adjust arc
            if abs(end_angle-start_angle)>math.pi and not c.large_arc:
                if end_angle-start_angle<0:
                    end_angle+=2*math.pi
                else:
                    start_angle+=2*math.pi
               
            if isStr:
                s += f"\\draw[ultra thick] ({scale*start.real} + {offset}, {-scale*start.imag}) arc ({-start_angle} r: {-end_angle} r:{scale*radius.real});\n"
            else:
                s += f"\\draw[ultra thick] ({scale*start.real+offset}, {-scale*start.imag}) arc ({-start_angle} r: {-end_angle} r:{scale*radius.real});\n"
            
        elif type(c) is pathtools.path.QuadraticBezier:
            start = c.start
            control = c.control
            end = c.end
            if isStr:
                s += f"\\draw[ultra thick] ({scale*start.real} + {offset}, {-scale*start.imag}) .. controls ({scale * control.real} + {offset},{-scale * control.imag}) .. ({scale*end.real} + {offset},{-scale*end.imag});\n"
            else:
                s += f"\\draw[ultra thick] ({scale*start.real+ offset}, {-scale*start.imag}) .. controls ({scale * control.real+ offset},{-scale * control.imag}) .. ({scale*end.real+ offset},{-scale*end.imag});\n"

    #print(template.format(draw=s))
    # Find height, width
    """
    with open(f"test.tex",'w') as f:
        f.write(template.format(draw=s))
    """
    return s, (xmax - xmin)*scale
def draw_string(word:str):
    s = ""
    h = 0
    for c in word:
        letter, offset = get_path(c,h, 0.1)
        offset = math.ceil(offset)
        s += letter
        h += offset
    return s, h 
    #print(template.format(draw=s))
    with open(f"test.tex",'w') as f:
        f.write(template.format(draw=s))

def get_offsets(word:str):
    h = 0
    res = []
    for c in word:
        res.append(h)
        _, offset = get_path(c,h, 0.1)
        offset = math.ceil(offset)
        #print(offset)
        h += offset
    res.append(h)
    return res

def get_flag_offsets(flag:str):
    return get_offsets("EPFL{"+flag+'}')[5:-2]


def draw_flag(flag:str, data:list[str])->str:
    #print(len(flag), len(data))
    assert len(flag) == len(data)
    num_offsets = get_flag_offsets(flag+'}')
    s, _ = draw_string("EPFL{")
    for c, offset in list(zip(list(flag), data)):
        letter, _ = get_path(c, offset, isStr=True)
        s+=letter
    ender, _ = get_path("}", num_offsets[-1])
    s+=ender

    return s
    
