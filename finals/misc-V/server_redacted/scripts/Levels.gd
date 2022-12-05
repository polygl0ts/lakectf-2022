extends Node

# Map site
const SIZE = 10

# Special levels identifiers
const BASE = -1
const FIVE = -1
const FMAPa = -1
const FMAPb = -1
const FMAPc = -1
const END = -1

# Level configuartion example
const IN1 = {"x": 1, "y": 4}
var EXAMPLE = [
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
	[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]
var example_config = {
	"in": IN1,
	"out": {"x": SIZE - 1, "y": 5},
	"levers": [],
	"doors": [],
	"doors_state": [],
	"map": EXAMPLE,
	"enemies": [],
	"id": 1,
	"info": "",
}

# Level generating functions placeholders
func base():
	return example_config.deuplicate(true)

func next_level(prev, pos=Globals._pos(0,0)):
	return example_config.duplicate(true)
