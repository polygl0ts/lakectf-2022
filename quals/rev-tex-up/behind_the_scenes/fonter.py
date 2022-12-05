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
    #return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))
def find_center(x1, y1, x2, y2, r, sweep):
    #print()
    #print(x1,y1,x2,y2,r)
    x11 = (x1 - x2)/2
    y11 = (y1 - y2)/2
    #print("wtf", (x11**2+y11**2)/r**2)
    #print(x11,y11)
    #print((r**4 - r**2 * y11**2 - r**2 * x11**2),(r**2 * y11**2 + r**2 * x11**2))
    scaler = math.sqrt((r**4 - r**2 * y11**2 - r**2 * x11**2)/(r**2 * y11**2 + r**2 * x11**2))
    #print(scaler)
    if not sweep: #sweep!= False = large_arc
        scaler *= -1
    cx1 = scaler * r*y11/r
    cy1 = -scaler * r*x11/r
    #print("scaler", scaler)
    #print(f"cx1 {cx1} cy1 {cy1}")
    cx = cx1 + (x1+x2)/2
    cy = cy1 + (y1+y2)/2
    #print(f"cx {cx} cy {cy}")
    return cx,cy

def get_path(c:chr, offset, scale = 0.1, isStr:bool=False):
    path, _ = pathtools.svg2paths(f"font/{c}.svg")
    s = ""
    xmin, xmax, ymin, ymax = path[0].bbox()
    #print(ymin,ymax)
    max = -1000 *scale
    #print(path[0])
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
            #print(length([start.real-cx, start.imag-cy]), length([end.real-cx, end.imag-cy]))
            #print(f"cp: ({cx, cy})")
            #print(f"endp: ({end.real, end.imag})")
            #print()
            #print(f"start:{math.degrees(start_angle)},end:{math.degrees(end_angle)}")
            if abs(end_angle-start_angle)>math.pi and not c.large_arc:
                if end_angle-start_angle<0:
                    end_angle+=2*math.pi
                else:
                    start_angle+=2*math.pi
               
            #start_angle,end_angle = end_angle, start_angle
            #if end_angle<0:
            #    end_angle+=2*math.pi
            #start_angle += math.pi
            #start_angle = math.atan2(start.imag,start.real)
            #end_angle = math.atan2(end.imag,end.real)
            #print(radius, math.sqrt())
            #start_angle = math.atan((start.imag/radius.imag)/(start.real/radius.real))
            #end_angle = math.atan((end.imag/radius.imag)/(end.real/radius.real))
            #s += f"\\draw ({scale*start.real}, {-scale*start.imag}) arc [ start angle= {start_angle} r, end angle= {end_angle} r, x radius={scale*radius.real}, y radius = {scale * radius.imag}];\n"
            #s += f"\\draw ({scale*start.real}, {-scale*start.imag}) arc [ start angle= {start_angle} r, end angle= {end_angle} r, radius={scale*radius.real}];\n"
            #s += f"\\filldraw[black] (0,0) circle (20pt);\n"
            #s += f"\\filldraw[black] ({cx},{cy}) circle (20pt);\n"
            #s += f"\\filldraw[black] ({cx},{-cy}) circle (4pt);\n"
            #s += f"\\filldraw[red] ({scale*start.real+ offset}, {-scale*start.imag}) circle (4pt);\n"
            #s += f"\\filldraw[black] ({scale*end.real+ offset}, {-scale*end.imag}) circle (4pt);\n"
            #s += f"\\draw[green] ({scale*start.real}, {-scale*start.imag}) arc ({end_angle} r: {start_angle} r:{scale*radius.real});\n"
            #s += f"\\draw[green] ({scale*start.real}, {-scale*start.imag}) arc ({math.pi} r: {3*math.pi/2} r:{scale*radius.real});\n"
            #color = "red" if sweep else "green"
            #s += f"\\draw[{color}] ({scale*start.real+ offset}, {-scale*start.imag}) -- ({scale*end.real+ offset},{-scale*end.imag});\n" 
            if isStr:
                s += f"\\draw[ultra thick] ({scale*start.real} + {offset}, {-scale*start.imag}) arc ({-start_angle} r: {-end_angle} r:{scale*radius.real});\n"
            else:
                s += f"\\draw[ultra thick] ({scale*start.real+offset}, {-scale*start.imag}) arc ({-start_angle} r: {-end_angle} r:{scale*radius.real});\n"
            
            

            #s += f"\\draw ({scale*start.real}, {scale*start.imag}) arc ({start_angle} r: {end_angle} r:{scale*radius.real});\n"
            #s += f"\\filldraw[red] ({scale*start.real+ offset}, {scale*start.imag}) -- ({cx},{cy});\n"
            #s += f"\\filldraw[red] ({scale*start.real+ offset}, {scale*start.imag}) circle (4pt);\n"
            #s += f"\\filldraw[black] ({scale*end.real+ offset}, {scale*end.imag}) circle (4pt);\n"
            #s += f"\\draw[{color}] ({scale*start.real+ offset}, {scale*start.imag}) -- ({scale*end.real+ offset},{scale*end.imag});\n" 
            #s += f"\\draw ({scale*start.real}, {scale*start.imag}) arc ({start_angle} r: {end_angle} r:{scale*radius.real});\n"
            #s += f"\\draw[blue] ({scale*start.real+ offset}, {scale*start.imag}) -- ({scale*end.real+ offset},{scale*end.imag});\n" 
            #s += f"\\draw[blue] ({cx+ offset}, {cy}) -- ({scale*end.real+ offset},{scale*end.imag});\n" 
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
    



#with open(f"test.tex",'w') as f:
#        f.write(template.format(draw=s))