extends Node2D

var SERVER_PORT = 4900
var MAX_PLAYERS = 256

var peer

func _ready():
	peer = NetworkedMultiplayerENet.new()
	peer.create_server(SERVER_PORT, MAX_PLAYERS)
	get_tree().network_peer = peer

# warning-ignore:return_value_discarded
	get_tree().connect("network_peer_connected", self, "_player_connected")
# warning-ignore:return_value_discarded
	get_tree().connect("network_peer_disconnected", self, "_player_disconnected")
# warning-ignore:return_value_discarded
	Globals.connect("disconnect_client", self, "_disconnect_client")

func _disconnect_client(id):
	peer.disconnect_peer(id)
	Globals.clients.erase(id)

func _player_connected(id):
	Globals.init_client(id)
	Globals.client_init_level(id)

func _player_disconnected(id):
	Globals.clients.erase(id)
