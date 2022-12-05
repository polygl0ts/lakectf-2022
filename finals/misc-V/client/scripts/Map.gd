extends Node2D

onready var f = preload("res://Floor.tscn")
onready var w = preload("res://Wall.tscn")
onready var l = preload("res://Lever.tscn")
onready var d = preload("res://Door.tscn")
onready var tnt = preload("res://TNT.tscn")

func build(map):
	for i in range(len(map)):
		for j in range(len(map[i])):
			var nodes = []
			if map[i][j]:
				nodes.append(f.instance())
				match map[i][j]:
					3:
						var node = l.instance()
						node.init({"x": j, "y": i})
						nodes.append(node)
					4:
						nodes.append(f.instance())
						var door = d.instance()
						door.init(true, {"x": j, "y": i})
						add_child(door)
					5:
						nodes.append(f.instance())
						var door = d.instance()
						door.init(false, {"x": j, "y": i})
						add_child(door)
					7:
						var node = tnt.instance()
						node.position.x = j * Globals.unit
						node.position.y = i * Globals.unit
						nodes.append(node)
			else:
					nodes.append(w.instance())
			
			for node in nodes:
				node.position.x = j * Globals.unit
				node.position.y = i * Globals.unit
				node.hide()
				add_child(node)
				
func _process(_v):
	match Globals.V:
		0:
			for x in get_children():
				x.show()
		_:
			pass
