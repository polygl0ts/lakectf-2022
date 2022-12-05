extends Node

# Signals
signal setup
signal move
signal render_enemies
signal pull_the_lever
signal trigger_door

# Game info
var unit = 75
var V = 0

# Incoming RPCs
puppet func setup(map, pos, info):
	emit_signal("setup", map, pos, info)

puppet func move(key):
	emit_signal("move", key)
	
puppet func render_enemies(pos):
	emit_signal("render_enemies", pos)

puppet func kronk(pos):
	emit_signal("pull_the_lever", pos)

puppet func trigger_door(pos):
	emit_signal("trigger_door", pos)

puppet func open_video(url):
# warning-ignore:return_value_discarded
	OS.shell_open(url)
	
puppet func set_V(v):
	V = v

# Outgoing RPCs
func key_pressed(key):
	rpc_id(1, "key_pressed", key)
