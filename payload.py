from time import perf_counter
from delta_v import delta_v
from launchers import *
from orbits import *

start = perf_counter()

def print_margin(solution):
  _, name, margin, twr, _ = solution
  print(f"{name} Margin: {margin:.1f} m/s (Launch TWR: {twr:.2f})")

def print_payload(solution):
  _, name, payload, twr, _ = solution
  print(f"{name} Payload: {payload:.3f}t (Launch TWR: {twr:.2f})")

# if None, max payload will be calculated
payload = None

payload_stages = []

required_deltav = transfer(LOW_ORBIT, 50, "Moon")

include_orbit = True

required_margin = 0

min_launch_twr = 1.1
min_twr = 0.25

min_accel = min_twr * DEFAULT[GRAVITY]

alternate_sort = False

payload_increment = 0.001

print(f"{required_deltav:.1f} m/s required after orbit")

solutions = []

for launcher in launchers:
  orbit_deltav = (launcher["orbit_deltav"] or ORBIT_ESTIMATE) if include_orbit else 0
  launcher_deltav = orbit_deltav + required_deltav
  launcher_solutions = []
  for configuration in configuations(launcher):
    data = configuration_data(configuration)
    stages = data["stages"] + payload_stages
    name = data["name"]
    thrust = data["launch_thrust"]
    if payload is None:
      increment_count = 1
      working_increments = 0
      # binary search for maximum payload capacity
      while True:
        test_payload = increment_count * payload_increment
        margin, wet_mass = delta_v(test_payload, stages, launcher_deltav, min_accel)
        twr = thrust / wet_mass / DEFAULT[GRAVITY]
        if margin is None or margin < required_margin or twr < min_launch_twr:
          increment_count = (increment_count + working_increments) // 2
          if working_increments == increment_count:
            break
        else:
          working_increments = increment_count
          increment_count *= 2
      working_payload = working_increments * payload_increment
      _, wet_mass = delta_v(working_payload, stages, launcher_deltav)
      if working_payload > 0:
        twr = thrust / wet_mass / DEFAULT[GRAVITY]
        launcher_solutions.append((wet_mass / working_payload, name, working_payload, twr, configuration))
    else:
      margin, wet_mass = delta_v(payload, stages, launcher_deltav, min_accel)
      if margin is not None and margin >= required_margin:
        twr = thrust / wet_mass / DEFAULT[GRAVITY]
        if twr >= min_launch_twr:
          launcher_solutions.append((wet_mass, name, margin, twr, configuration))
  launcher_solutions.sort(key=lambda k : k[2], reverse=True)
  existing_solutions = []
  for solution in launcher_solutions:
    solution_config = solution[4]
    for comparison in existing_solutions:
      comparison_config = comparison[4]
      # new solution has at least as many stages
      if comparison_config[1] <= solution_config[1]:
        # old solution has no boosters
        if comparison_config[2] is None: break
        # old solution has less boosters
        if comparison_config[2] == solution_config[2] and comparison_config[3] < solution_config[3]: break
    else:
      existing_solutions.append(solution)
  solutions += existing_solutions

print_solution = print_payload if payload is None else print_margin

solutions.sort(key=lambda k: k[2 if alternate_sort else 0], reverse=alternate_sort)
for solution in solutions:
  print_solution(solution)

seconds = perf_counter() - start
print(f"{1000 * seconds:.2f}ms elapsed")
