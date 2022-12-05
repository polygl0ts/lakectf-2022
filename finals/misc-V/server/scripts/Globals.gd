extends Node

######################################
### Signals
######################################
signal disconnect_client

######################################
### Variables  
######################################
var history = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
const TNT_ACTIVATION_CODE = 926156497
const TIMEOUT = 120.0
var clients = {}

######################################
### Utils
######################################
func _pos(x, y):
	return {"x": x, "y": y}

func init_client(id):
	clients[id] = {
		"level": Levels.next_level(0),
	}

######################################
# Boolean checks
######################################
func bound_check(id, pos):
	if clients.has(id):
		var map = clients[id].level.map
		return pos.x >= 0 and pos.y >= 0 and pos.y < len(map) and pos.x < len(map[0])

func door_check(id, pos):
	if clients.has(id):
		var l = clients[id].level
		for i in range(len(l.doors)):
			if pos.hash() == l.doors[i].hash():
				return l.doors_state[i]
		return true

func validate_position(id, pos, enemy=false):
	if clients.has(id):
		var map = clients[id].level.map
		return bound_check(id, pos) and map[pos.y][pos.x] and door_check(id, pos) and (not enemy or not lever(id, pos))
	
func level_completed(id, old, new):
	if clients.has(id):
		return old.hash() == clients[id].level.out.hash() and not bound_check(id, new)
	
func trigger(id, pos):
	if clients.has(id):
		var c = clients[id]
		return c.level.map[pos.y][pos.x] == 2 and len(c.level.enemies) == 0

func lever(id, pos):
	if clients.has(id):
		return clients[id].level.map[pos.y][pos.x] == 3
	
func tnt(id, pos):
	if clients.has(id):
		return clients[id].level.map[pos.y][pos.x] == 7

func TNT_enabled(id, pos):
	if clients.has(id):
		return clients[id].level.map[pos.y][pos.x] == 9 and history.hash() == TNT_ACTIVATION_CODE

func captured(id):
	if clients.has(id):
		var px = clients[id].position.x 
		var py = clients[id].position.y
		
		for e in clients[id].level.enemies:
			if px == e.x and py == e.y:
				return true
		
		return false 

######################################
### Enemies logic
######################################
func enemy_spawn(id):
	if clients.has(id):
		for e in clients[id].level.spawn.duplicate():
			clients[id].level.enemies.append(e)
		
		rpc_id(id, "render_enemies", clients[id].level.enemies)
	
func move_enemies(id):
	if clients.has(id):
		var px = clients[id].position.x 
		var py = clients[id].position.y 
		
		for e in clients[id].level.enemies:
			var dx = px - e.x
			var dy = py - e.y
			var moved = false
			
			if abs(dx) > abs(dy):
				if dx != 0:
					var x = e.x + 1 if dx > 0 else e.x -1
					if validate_position(id, _pos(x, e.y), true):
						e.x = x
						moved = true
						
				if not moved and dy != 0:
					var y = e.y + 1 if dy > 0 else e.y - 1
					if validate_position(id, _pos(e.x, y), true):
						e.y = y
						moved = true
			else:
				if dy != 0:
					var y = e.y + 1 if dy > 0 else e.y - 1
					if validate_position(id, _pos(e.x, y), true):
						e.y = y
						moved = true
						
				if not moved and dx != 0:
					var x = e.x + 1 if dx > 0 else e.x -1
					if validate_position(id, _pos(x, e.y), true):
						e.x = x
						moved = true
		
		rpc_id(id, "render_enemies", clients[id].level.enemies)

######################################
### Client
######################################
func client_init_level(id):
	if clients.has(id):
		var c = clients[id]
		rpc_id(id, "setup", c.level.map, c.level.in, c.level.info)
		c.position = c.level.in
		
		if c.level.id >= 100 and c.level.id < Levels.BASE and c.level.id < Levels.END:
			rpc_id(id, "set_V", 1) 

func client_move(id, key):
	if clients.has(id):
		rpc_id(id, "move", key)
		
		history.pop_back()
		history.push_front(key.find(true))

master func key_pressed(key):
	var id = get_tree().get_rpc_sender_id()
	if not clients.has(id):
		emit_signal("disconnect_client", id)
		return
	
	var c = clients[id]
	
	if not key or len(key) != 4:
		#emit_signal("disconnect_client", id)
		return
	
	var new_pos = c.position.duplicate()
	if key[0]:
		new_pos.x -= 1
	if key[1]:
		new_pos.x += 1
	if key[2]:
		new_pos.y -= 1
	if key[3]:
		new_pos.y += 1
	
	if c.level.id == Levels.FIVE:
		if new_pos.hash() == c.level.triggers[c.level.k].hash():
			match c.level.k:
				0:
					c.level.map = Levels.FMAPa
					c.level.k +=1
					c.level.in = c.position
				1:
					c.level.map = Levels.FMAPb
					c.level.k +=1
					c.level.in = c.position
				2:
					c.level.map = Levels.FMAPc
					c.level.k +=1
					c.level.in = c.position
				3:
					c.level = Levels.base()
					c.position = c.level.in.duplicate(true)
			client_init_level(id)
			
			rpc_id(id, "kronk", new_pos)
			return
	
	if validate_position(id, new_pos):	
		if lever(id, new_pos):
			if (c.level.id == Levels.END or TNT_enabled(id, c.position)) and not c.level.done:
				c.level.done = true
				rpc_id(id, c.level.call, c.level.arg)
				c.level.info = c.level.flag
				c.level.in = c.position
				client_init_level(id)
				
				yield(get_tree().create_timer(TIMEOUT), "timeout")
				emit_signal("disconnect_client", id)
			
			var l = c.level
			for i in range(len(l.levers)):
				if new_pos.hash() == l.levers[i].hash():
					rpc_id(id, "trigger_door", l.doors[i])
					l.doors_state[i] = not l.doors_state[i]
			rpc_id(id, "kronk", new_pos)
			
			if len(c.level.enemies) != 0:
				move_enemies(id)
			if captured(id):
				emit_signal("disconnect_client", id)
			return
		
		client_move(id, key)
		c.position = new_pos
		
		if captured(id) or tnt(id, new_pos):
			emit_signal("disconnect_client", id)
			return
		
		if trigger(id, new_pos):
			enemy_spawn(id)
	
	elif level_completed(id, c.position, new_pos):
		c.level = Levels.next_level(c.level.id, c.level.out)
		c.position = c.level.in.duplicate()
		client_init_level(id)
		
	if len(c.level.enemies) != 0:
		move_enemies(id)
		
	if captured(id):
		emit_signal("disconnect_client", id)
		return
