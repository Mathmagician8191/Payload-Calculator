# note: rotation speed is unscaled and this does not effect orbit delta-v estimates
SCALE = 3.2

# adjust/remove launcher orbit estimates as well if changing the solar system scale
ORBIT_ESTIMATE = 5500

# Indices
RADIUS = 0
GRAVITY = 1
GM = 2
ROTATION = 3

def load_planet(radius, gravity, rotation):
  gm = radius ** 2 * 1000 * gravity
  return (radius, gravity, gm, rotation)

KERBIN = load_planet(600 * SCALE, 9.81, 373.1)

# TODO: rotation
MUN = load_planet(200 * SCALE, 1.63, 0)
MINMUS = load_planet(60 * SCALE, 0.491, 0)
KERBOL = load_planet(261600 * SCALE, 17.1, 0)

LOW_ORBIT = 120
MUN_HEIGHT = 11400 * SCALE
MINMUS_HEIGHT = 46400 * SCALE

DEFAULT = KERBIN
