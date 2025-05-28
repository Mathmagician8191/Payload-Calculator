# estimate for the delta-v to reach LEO
ORBIT_ESTIMATE = 9400

# Indices
RADIUS = 0
GRAVITY = 1
GM = 2
ROTATION = 3

def load_planet(radius, gravity, rotation):
  gm = radius ** 2 * 1000 * gravity
  return (radius, gravity, gm, rotation)

# note - radius set to match Earth's GM
EARTH = load_planet(6374.3, 9.81, 465.1)
MOON = load_planet(1738.1, 1.625, 4.627)

LOW_ORBIT = 200
MOON_HEIGHT = 384000

DEFAULT = EARTH
