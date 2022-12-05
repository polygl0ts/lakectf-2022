extends Node2D

var SERVER_IP = "chall.polygl0ts.ch"
var SERVER_PORT = 4900

onready var underground = preload("res://Underground.tscn")

var pressed_key

func _ready():
# warning-ignore:return_value_discarded
	get_tree().connect("connected_to_server", self, "_connected")
# warning-ignore:return_value_discarded
	get_tree().connect("connection_failed", self, "_connection_failed")	
# warning-ignore:return_value_discarded
	get_tree().connect("server_disconnected", self, "_server_disconnected")
	pressed_key = [false, false, false, false]
	
	_connect()
	
func _process(_delta):
	if true in pressed_key:
		Globals.key_pressed(pressed_key)
		pressed_key = [false, false, false, false]
	
func _connect():
	var peer = NetworkedMultiplayerENet.new()
	peer.create_client(SERVER_IP, SERVER_PORT)
	get_tree().network_peer = peer

func _connected():
	set_network_master(1)
	
	var node = underground.instance()
	add_child(node)

func _connection_failed():
	pass

func _server_disconnected():
	get_tree().quit()

func _input(_event):
	pressed_key = [
		Input.is_action_just_pressed(("ui_left")),
		Input.is_action_just_pressed(("ui_right")),
		Input.is_action_just_pressed(("ui_up")),
		Input.is_action_just_pressed(("ui_down"))
	]
