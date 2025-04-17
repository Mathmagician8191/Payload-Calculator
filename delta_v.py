from math import log

def delta_v(payload, stages, required_deltav):
  margin = -required_deltav
  wet_mass = payload
  for wet, dry, isp in stages[::-1]:
    dry_mass = wet_mass + dry
    wet_mass += wet
    margin += isp * 9.81 * log(wet_mass / dry_mass)
  return margin, wet_mass
