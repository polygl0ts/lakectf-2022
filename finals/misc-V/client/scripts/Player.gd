extends Node2D

func _ready():
# warning-ignore:return_value_discarded
	Globals.connect("move", self, "move")
	
func move(key):
	if key[0]:
		position.x -= Globals.unit
	if key[1]:
		position.x += Globals.unit
	if key[2]:
		position.y -= Globals.unit
	if key[3]:
		position.y += Globals.unit
