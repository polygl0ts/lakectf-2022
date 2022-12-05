extends Node2D

onready var h_open = preload("res://img/door_h_open.png")
onready var h_close = preload("res://img/door_h_closed.png")
onready var v_open = preload("res://img/door_v_open.png")
onready var v_close = preload("res://img/door_v_closed.png")

var open = false
var horizontal
var pos

func _ready():
# warning-ignore:return_value_discarded
	Globals.connect("trigger_door", self, "change_state")

func init(h, p):
	horizontal = h
	pos = p
	position.x = p.x * Globals.unit
	position.y = p.y * Globals.unit

func change_state(target):
	if target.hash() == pos.hash():
		open = not open

func _process(_x):
	if horizontal:
		$Sprite.set_texture(h_open if open else h_close)
	else:
		$Sprite.set_texture(v_open if open else v_close)
