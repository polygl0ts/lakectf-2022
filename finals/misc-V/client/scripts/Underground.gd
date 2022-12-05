extends Node2D

onready var map = preload("res://Map.tscn")
onready var player = preload("res://Player.tscn")
onready var enemy = preload("res://Enemy.tscn")
onready var flag = preload("res://Flag.tscn")

var enemies = []
var p
var m

func _ready():
# warning-ignore:return_value_discarded
	Globals.connect("setup", self, "_setup")
# warning-ignore:return_value_discarded
	Globals.connect("render_enemies", self, "_render_enemies")

func _setup(map_array, pos, info):
	if p:
		p.queue_free()
		p = null
		
	if m:
		for c in m.get_children():
			c.queue_free()
		m.queue_free()
		
	for e in enemies:
		e.queue_free()
	enemies = []
	
	if 'EPFL' in str(info):
		var node = flag.instance()
		node.init(info)
		add_child(node)
		return
		
	m = map.instance()
	add_child(m)
	m.build(map_array)
	
	p = player.instance()
	p.position.x = pos.x * Globals.unit
	p.position.y = pos.y * Globals.unit
	add_child(p)
	
	if len(str(info)) > 3:
		var n = get_node('Info/Label')
		n.rect_size.x = 750
		n.rect_size.y = 300
		$Info.position.y = 150
		n.bbcode_text = '[center]' + str(info) + '[/center]'
	else:
		get_node('Info/Label').bbcode_text = '[center]' + str(info) + '[/center]'
	
func _render_enemies(l):	
	var i = 0
	
	for e in l:
		if i >= len(enemies):
			var node = enemy.instance()
			add_child(node)
			enemies.append(node)
		enemies[i].position.x = e.x * Globals.unit
		enemies[i].position.y = e.y * Globals.unit
		
		i += 1
	
	while len(enemies) > len(l):
		enemies[-1].queue_free()
		enemies.erase(-1)
