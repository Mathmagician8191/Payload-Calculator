import os
import json
from math import log

stage_library = {}

for path in os.listdir("stages"):
  with open(f"stages/{path}") as file:
    json_stages = json.load(file)
    for stage in json_stages:
      stage_library[stage["name"]] = stage

def delta_v(payload, stages, required_deltav):
  margin = -required_deltav
  wet_mass = payload
  for stage in stages[::-1]:
    if isinstance(stage, str):
      data = stage_library[stage]
      wet = data["wet_mass"]
      dry = data["dry_mass"]
      isp = data["isp"]
    else: wet, dry, isp = stage
    dry_mass = wet_mass + dry
    wet_mass += wet
    margin += isp * 9.81 * log(wet_mass / dry_mass)
  return margin, wet_mass
