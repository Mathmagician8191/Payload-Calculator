import os
import pyjson5
from math import log

stage_library = {}

for path in os.listdir("stages"):
  with open(f"stages/{path}") as file:
    json_stages = pyjson5.load(file)
    for stage in json_stages:
      stage_library[stage["name"]] = stage

# returns None if the rocket fails conditions
def delta_v(payload, stages, required_deltav, min_acceleration=0):
  margin = -required_deltav
  wet_mass = payload
  for stage in stages[::-1]:
    if isinstance(stage, str):
      data = stage_library[stage]
      wet = data["wet_mass"]
      dry = data["dry_mass"]
      isp = data["isp"]
      thrust = data["thrust"]
    else: wet, dry, isp, thrust = stage
    dry_mass = wet_mass + dry
    wet_mass += wet
    if thrust / wet_mass < min_acceleration:
      return None, wet_mass
    margin += isp * 9.81 * log(wet_mass / dry_mass)
  return margin, wet_mass
