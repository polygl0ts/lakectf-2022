extends Node2D

onready var up = preload("res://img/lever_up.png")
onready var down = preload("res://img/lever_down.png")

var pos
var state = false

func _ready():
# warning-ignore:return_value_discarded
	Globals.connect("pull_the_lever", self, "pull")

func init(p):
	pos = p.duplicate(true)

func pull(target):
	if pos and target.hash() == pos.hash():
		state = not state
		$Sprite.set_texture(down if state else up)
