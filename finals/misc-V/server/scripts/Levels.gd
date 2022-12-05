extends Node

const SIZE = 10

const END = 366# RICK ROLL
const FIVE = 309 #303 FIFTH
const BASE = 1001 #1001 SHADOWS
const A = BASE + 1
const B = A + 1
const C = B + 1
const D = C + 1
const E = D + 1
const F = E + 1
const TNT = F + 1

func _pos(x, y):
	return {"x": x, "y": y}

# Starting map
const IN1 = {"x": 1, "y": 4}
const OUT1 = {"x": SIZE-1, "y": 5}
const MAP1 = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 1, 1, 1, 0, 0, 0, 0, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# FIFTH
const L303 = {"x": 0, "y": 5}
const R303 = {"x": SIZE - 1, "y": 5}
const MAP303a = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
const FMAPa = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 0, 0, 3, 0, 0, 0, 0],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
const FMAPb = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 0, 0, 3, 0, 0, 0, 0],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
const FMAPc = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 3, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 0, 0, 3, 0, 0, 0, 0],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
	[0, 0, 0, 0, 1, 0, 0, 3, 0, 0],
	[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
]
var TRIGGER303 = [_pos(5, 4), _pos(2, 3), _pos(7, 7), _pos(4, 10)]

# RICK ROLL
const MAP365 = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 3, 1, 1, 1, 0],
	[0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# SHADOWS
const SIN = {"x": 5, "y": 5}
const SOUT = {"x": SIZE - 1, "y": 5}
const MAPBASE = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

# LEVEL A
#	#0  1  2  3  4  5  6  7  8  9
var MAPA = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #2
	[0, 0, 1, 1, 1, 0, 0, 0, 0, 0], #3
	[0, 0, 1, 1, 1, 0, 0, 0, 0, 0], #4
	[1, 1, 1, 1, 1, 5, 1, 1, 1, 1], #5
	[0, 0, 1, 1, 1, 0, 0, 0, 0, 0], #6
	[0, 0, 1, 1, 1, 0, 0, 0, 0, 0], #7
	[0, 0, 0, 3, 0, 0, 0, 0, 0, 0], #8
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
]

var a_config = {
	"in": _pos(0, 5),
	"out": _pos(9,5),
	"levers": [_pos(3,8)],
	"doors": [_pos(5,5)],
	"doors_state": [false],
	"map": MAPA,
	"enemies": [],
	"info": "",
	"id": A
}

# LEVEL A
#	#0  1  2  3  4  5  6  7  8  9
var MAPB = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #2
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #3
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #4
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 0], #5
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0], #6
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0], #7
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0], #8
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0], #9
]

var b_config = {
	"in": _pos(0, 5),
	"out": _pos(3,9),
	"levers": [],
	"doors": [],
	"doors_state": [],
	"map": MAPB,
	"enemies": [_pos(8,5)],
	"info": "",
	"id": B
}

var MAPC = [
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0], #0
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0], #1
	[0, 0, 0, 1, 1, 1, 1, 1, 1, 0], #2
	[1, 1, 1, 2, 0, 0, 0, 0, 1, 0], #3
	[0, 0, 0, 1, 0, 1, 1, 1, 1, 0], #4
	[0, 0, 0, 1, 0, 1, 0, 0, 0, 0], #5
	[0, 3, 1, 1, 0, 1, 1, 1, 1, 0], #6
	[0, 0, 0, 1, 0, 0, 0, 0, 1, 0], #7
	[5, 1, 1, 1, 1, 1, 1, 1, 1, 0], #8
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
]

var c_config = {
	"in": _pos(3, 0),
	"out": _pos(0,8),
	"levers": [_pos(1,6)],
	"doors": [_pos(0,8)],
	"doors_state": [false],
	"map": MAPC,
	"enemies": [],
	"trigger": [_pos(3,2)],
	"spawn": [_pos(0,3)],
	"info": "",
	"id": C
}

# LEVEL A
#	#0  1  2  3  4  5  6  7  8  9
var MAPD = [
	[0, 0, 0, 0, 1, 0, 3, 0, 0, 0], #0
	[0, 0, 0, 0, 1, 0, 4, 0, 0, 0], #1
	[0, 3, 1, 1, 1, 1, 1, 1, 0, 0], #2
	[0, 0, 1, 0, 0, 0, 0, 1, 0, 0], #3
	[0, 0, 1, 0, 0, 0, 0, 1, 0, 0], #4
	[0, 0, 1, 0, 0, 0, 0, 1, 0, 0], #5
	[0, 0, 1, 0, 0, 0, 0, 1, 0, 0], #6
	[0, 0, 1, 1, 1, 1, 1, 1, 0, 0], #7
	[0, 0, 1, 0, 0, 0, 0, 0, 0, 0], #8
	[0, 0, 4, 0, 0, 0, 0, 0, 0, 0], #9
]

var d_config = {
	"in": _pos(4, 0),
	"out": _pos(2,9),
	"levers": [_pos(1,2), _pos(6,0)],
	"doors": [_pos(6,1), _pos(2,9)],
	"doors_state": [false, false],
	"map": MAPD,
	"enemies": [_pos(2,6)],
	"info": "",
	"id": D
}

# LEVEL A
#	#0  1  2  3  4  5  6  7  8  9
var MAPE = [
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0], #0
	[0, 0, 0, 1, 0, 0, 0, 0, 0, 0], #1
	[0, 0, 0, 1, 1, 1, 1, 1, 1, 0], #2
	[0, 0, 0, 1, 0, 0, 0, 0, 1, 0], #3
	[0, 1, 1, 2, 3, 0, 1, 1, 1, 0], #4
	[0, 0, 0, 1, 0, 0, 1, 0, 0, 0], #5
	[0, 0, 0, 1, 0, 0, 1, 1, 1, 0], #6
	[0, 0, 0, 1, 0, 0, 0, 0, 1, 0], #7
	[5, 1, 1, 1, 1, 1, 1, 1, 1, 0], #8
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
]

var e_config = {
	"in": _pos(3, 0),
	"out": _pos(0,8),
	"levers": [_pos(4,4)],
	"doors": [_pos(0,8)],
	"doors_state": [false],
	"map": MAPE,
	"enemies": [],
	"trigger": [_pos(3,4)],
	"spawn": [_pos(1,4), _pos(3,2), _pos(3,8)],
	"info": "",
	"id": E
}

# LOGIC
const MAPF =  [
	#0  1  2  3  4  5  6  7  8  9
	[0, 0, 4, 0, 0, 0, 0, 0, 0, 0], #0
	[0, 1, 1, 1, 0, 1, 1, 1, 1, 0], #1
	[0, 1, 1, 1, 0, 1, 0, 0, 1, 0], #2
	[0, 1, 0, 1, 3, 1, 0, 0, 1, 0], #3
	[0, 1, 1, 1, 0, 1, 0, 0, 1, 0], #4
	[0, 1, 0, 1, 0, 1, 0, 0, 1, 0], #5
	[0, 4, 0, 0, 0, 0, 1, 5, 1, 0], #6
	[0, 1, 1, 1, 1, 1, 1, 0, 0, 0], #7
	[0, 3, 0, 0, 0, 0, 1, 3, 0, 0], #8
	[0, 0, 0, 0, 0, 0, 1, 0, 0, 0], #9
]
var f_config = {
	"in": _pos(6, SIZE - 1),
	"out": _pos(2,0), 
	"levers": [_pos(4,3), _pos(1,8),_pos(7,8)],
	"doors": [_pos(2,0), _pos(1,6), _pos(7,6)],
	"doors_state": [false, false, false],
	"enemies": [_pos(8,1), _pos(1,7), _pos(1,3)],
	"map": MAPF,
	"info": "",
	"id": F
}

# LEVEL A
#	#0  1  2  3  4  5  6  7  8  9
var MAPTNT = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
	[0, 0, 7, 7, 7, 7, 7, 7, 7, 0], #1
	[0, 0, 7, 7, 7, 7, 7, 7, 7, 0], #2
	[0, 0, 7, 1, 7, 1, 7, 7, 7, 0], #3
	[0, 0, 1, 1, 1, 1, 1, 7, 7, 0], #4
	[0, 0, 1, 1, 1, 1, 9, 3, 7, 0], #5
	[0, 0, 1, 1, 1, 1, 1, 7, 7, 0], #6
	[0, 0, 1, 1, 1, 1, 7, 7, 7, 0], #7
	[0, 0, 1, 1, 1, 1, 1, 7, 7, 0], #8
	[0, 0, 1, 0, 0, 0, 0, 0, 0, 0], #9
]

var TNT_config = {
	"in": _pos(2, SIZE - 1),
	"out": _pos(0,0),
	"levers": [],
	"doors": [],
	"doors_state": [],
	"map": MAPTNT,
	"enemies": [],
	"info": "",
	"id": TNT,
	"call": "open_video",
	"arg": "https://youtu.be/c8UtojJT8ts?t=24",
	"flag": "EPFL{Pe0ple shouldn'7 b3 afr4id of th3ir gov3rnmen7. Governm3nt5 sh0uld be 4fra1d 0f the1r p3opl3.}",
	"done": false
}

func base():
	return {"map": MAPBASE, "in": SIN, "out": SOUT, "levers": [], "doors": [], "enemies":[], "info": "", "id": BASE}.duplicate(true)

func next_level(prev, pos=_pos(0,0)):
	var next = prev + 1
	if next == 1:
		return {"map": MAP1, "in": IN1, "out": OUT1, "levers": [], "doors": [], "enemies":[], "info": next, "id": next}
	elif next == END:
			return add_simple_entry(MAP365.duplicate(true), pos)
#	elif next == END + 1:
#			return {"map": MAP365.duplicate(true), "in": pos, "out": _pos(0,0), "levers": [], "doors": [], "enemies":[], "info": "...but you forgot\nthe 5th of\nNovember :(", "id": next}
	elif next == FIVE - 1:
		return prepare_fifth(pos, next)
	elif next == FIVE:
		if pos.x == 0:
			return {"map": MAP303a, "in": R303, "out": L303, "levers": [], "doors": [], "enemies":[], "info": next, "id": FIVE, "k": 0, "triggers": TRIGGER303}
		else:
			return {"map": MAP303a, "in": L303, "out": R303, "levers": [], "doors": [], "enemies":[], "info": next, "id": FIVE, "k": 0, "triggers": TRIGGER303}
	elif prev == BASE:
		return a_config.duplicate(true)
	elif prev == A:
		return b_config.duplicate(true)
	elif prev == B:
		return c_config.duplicate(true)
	elif prev == C:
		return d_config.duplicate(true)
	elif prev == D:
		return e_config.duplicate(true)
	elif prev == E:
		return f_config.duplicate(true)
	elif next == TNT:
		return TNT_config.duplicate(true)
	else:
			return random_map(pos, next)
			
## Random map generation
func add_simple_entry(m, pos):
	var x = pos.x
	var y = pos.y

	var e = null
		
	if x == 0:
		e = _pos(SIZE - 1, y)
	elif x == (SIZE - 1):
		e = _pos(0, y)
	elif y == 0:
		e = _pos(x, SIZE - 1)
	else:
		e = _pos(x, 0)
		
	m[e.y][e.x] = 1
			
	return {"map": m, "in": e, "out": _pos(0, 0), "levers": [], "doors": [], "enemies":[], "info": "You made it to the\nend of the year!", "id": END, "done": false, "call": "open_video", "arg": "https://youtu.be/dQw4w9WgXcQ", "flag": "...but you forgot\nthe 5th of\nNovember :("}

### Random map generation
func rnd_entry(pos):
	var x = pos.x
	var y = pos.y
	
	var walk = []
	if x == 0:
		walk += [_pos(SIZE - 1, y), _pos(SIZE - 2, y), _pos(SIZE - 3, y)]
	elif x == (SIZE - 1):
		walk += [_pos(0, y), _pos(1, y), _pos(2, y)]
	elif y == 0:
		walk += [_pos(x, SIZE - 1), _pos(x, SIZE - 2),  _pos(x, SIZE - 3)]
	else:
		walk += [_pos(x, 0), _pos(x, 1), _pos(x, 2)]
	
	return walk
	
func rnd_exit(pos):
	var x = pos.x
	var y = pos.y
	
	if x == 1:
		return _pos(0, y)
	elif x == (SIZE - 2):
		return _pos(x + 1, y)
	elif y == 1:
		return _pos(x, 0)
	else:
		return _pos(x, y + 1)
	
func random_map(pos, next):
	var walk = rnd_entry(pos)
	
	var first = walk[0]
	var last = walk[-1]
	while last.x != 1 and last.x != (SIZE - 2) and last.y != 1 and last.y != (SIZE - 2):
		match randi() % 4:
			0:
				if not first.y == 0:
					walk.append(_pos(last.x, last.y - 1))
			1:
				if not first.x == (SIZE - 1):
					walk.append(_pos(last.x + 1, last.y))
			2:
				if not first.y == (SIZE - 1):
					walk.append(_pos(last.x, last.y + 1))
			3:
				if not first.x == 0:
					walk.append(_pos(last.x - 1, last.y))
		
		last = walk[-1]
	
	walk.append(rnd_exit(last))
	
	# Initialize empty map
	var map = []
	for _i in range(SIZE):
		var row = []
		for _j in range(SIZE):
			row.append(0)
		map.append(row)
	
	# Configure map
	for w in walk:
		map[w.y][w.x] = 1
	
	return {"map": map, "in": walk[0], "out": walk[-1], "levers": [], "doors": [], "enemies":[], "info": next, "id": next}

func prepare_fifth(pos, next):
	var walk = rnd_entry(pos)
	
	# Vertical move
	var last = walk[-1]
	while last.y != 5:
		if last.y < 5:
			walk.append(_pos(last.x, last.y + 1))
		else:
			walk.append(_pos(last.x, last.y - 1))
		
		last = walk[-1]
	
	# Horizontal move
	if last.x < 5:
		while last.x != SIZE - 1:
			walk.append(_pos(last.x + 1, last.y))
			last = walk[-1]
	else:
		while last.x != 0:
			walk.append(_pos(last.x - 1, last.y))
			last = walk[-1]
	
		# Initialize empty map
	var map = []
	for _i in range(SIZE):
		var row = []
		for _j in range(SIZE):
			row.append(0)
		map.append(row)
		
	# Configure map
	for w in walk:
		map[w.y][w.x] = 1
	
	return {"map": map, "in": walk[0], "out": walk[-1], "levers": [], "doors": [], "enemies":[], "info": next, "id": next}
