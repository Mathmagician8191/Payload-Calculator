from math import log
from launchers import get_stage

# returns None if the rocket fails conditions
def delta_v(payload, stages, required_deltav, min_acceleration=0):
  margin = -required_deltav
  wet_mass = payload
  for stage in stages[::-1]:
    wet, dry, isp, thrust = get_stage(stage)
    dry_mass = wet_mass + dry
    wet_mass += wet
    if thrust / wet_mass < min_acceleration:
      return None, wet_mass
    margin += isp * 9.81 * log(wet_mass / dry_mass)
  return margin, wet_mass
