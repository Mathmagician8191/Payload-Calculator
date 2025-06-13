import json
import os

SYSTEM = "rss"
SCALE = 1
DAY_SCALE = 1
LOW_ORBIT = 200
ORBIT_ESTIMATE = 9400

# Indices
RADIUS = 0
GRAVITY = 1
GM = 2
ROTATION = 3
PARENT = 4
HEIGHT = 5

def load_planet(radius, gravity, rotation, parent, height):
  radius *= SCALE
  rotation *= SCALE / DAY_SCALE
  gm = radius ** 2 * 1000 * gravity
  return (radius, gravity, gm, rotation, parent, height * SCALE)

filepath = f"solar-systems/{SYSTEM}.json"

if not os.path.isfile(filepath):
  print(f"Invalid solar system: {SYSTEM}")
  quit()

systems = {}

with open(filepath) as file:
  data = json.load(file)
  for body in data["bodies"]:
    name = body["name"]
    systems[name] = load_planet(body["radius"], body["gravity"], body["rotation"], body["parent"], body["height"])
  DEFAULT = systems[data["default"]]
