from math import sqrt, sin, cos, pi, hypot
from celestial_bodies import *

# velocity of a circular orbit at the provided height above the surface
def circular(height, planet=DEFAULT):
  height += planet[RADIUS]
  return sqrt(planet[GM] / height)

# velocity of an elliptical orbit using the vis-viva equation
def elliptical(start, sma, planet=DEFAULT):
  radius = planet[RADIUS]
  start += radius
  sma += radius
  return sqrt(planet[GM] * (2 / start - 1 / sma))

# escape velocity at the provided height above the surface
def escape(height, planet=DEFAULT):
  height += planet[RADIUS]
  return sqrt(2 * planet[GM] / height)

# delta-v to reach a specific C3 value from a circular orbit
def c3_deltav(c3, height=LOW_ORBIT, planet=DEFAULT):
  return sqrt(escape(height, planet) ** 2 + c3 * 10 ** 6) - circular(height, planet)

# transfer from a circular orbit at start to an elliptical orbit of start x end
# the first half of a hohmann transfer
def halfmann(start, end, inclination=0, planet=DEFAULT):
  inclination *= pi / 180
  sma = (start + end) / 2
  initial = circular(start, planet)
  velocity = elliptical(start, sma, planet)
  horizontal = velocity * cos(inclination)
  vertical = velocity * sin(inclination)
  final_burn = hypot((horizontal - initial), vertical)
  return final_burn

# hohmann transfer from circular orbits at start and end (above the surface)
# allows for a plane change, assumed to be part of the second burn
# splitting the plane change across both burns is more efficient, but not accounted for here
def hohmann(start, end, inclination=0, planet=DEFAULT):
  initial_burn = halfmann(start, end, 0, planet)
  return initial_burn + halfmann(end, start, inclination, planet)

# Transfer from a circular orbit around a central body to a circular orbit around the target body
def transfer(start_height, final_height, target_planet, return_trip=False, home_planet=DEFAULT):
  target_planet = systems[target_planet]
  target_height = target_planet[HEIGHT]
  final_injection = (hypot(halfmann(target_height, start_height, planet=home_planet), escape(final_height, target_planet)) - circular(final_height, target_planet))
  if return_trip:
    final_injection *= 2
  return halfmann(start_height, target_height, planet=home_planet) + final_injection

# estimate of extra delta-v penalty to launch into an inclined orbit
# assumes the launch site is at the equator
def incline(angle, height=LOW_ORBIT, planet=DEFAULT):
  angle *= pi / 180
  velocity = circular(height, planet)
  baseline = velocity - planet[ROTATION]
  horizontal = velocity * cos(angle)
  vertical = velocity * sin(angle)
  new = hypot((horizontal - planet[ROTATION]), vertical)
  return new - baseline

# plane change at the given height
def plane(angle, height, planet=DEFAULT):
  angle *= pi / 180
  velocity = circular(height, planet)
  horizontal = velocity * cos(angle)
  vertical = velocity * sin(angle)
  return hypot((velocity - horizontal), vertical)

# calculate the height of a stationary orbit
def stationary_height(planet=DEFAULT):
  radius = planet[RADIUS]
  return radius * ((1000 * planet[GRAVITY] * radius / planet[ROTATION] ** 2) ** (1 / 3) - 1)
