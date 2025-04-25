import matplotlib.pyplot as plt
from time import perf_counter
from delta_v import delta_v
from launchers import *
from orbits import *

start = perf_counter()

payload_stages = []

include_orbit = True

min_twr = 1.1

min_payload = 0

selected_launchers = [
  ("Falcon 9", 2),
]

# delta-v if plotting delta-v, minimum C3 if plotting C3
min_performance = -10

# None to plot delta-v, else tuple of (planet, starting_altitude)
plot_c3 = (EARTH, 200)

payload_increment = 0.01

fig, ax = plt.subplots()

for name, stage_counts in selected_launchers:
  for launcher in launchers:
    if launcher["name"] == name:
      min_stages = launcher["min_stages"]
      stages = launcher["stages"]
      stage_count_required = len(stages) != min_stages
      orbit_deltav = (launcher["orbit_deltav"] or ORBIT_ESTIMATE) if include_orbit else 0
      thrust = launcher["launch_thrust"]
      if not hasattr(stage_counts, "__iter__"):
        stage_counts = (stage_counts,)
      for stage_count in stage_counts:
        variant_name = f"{name} ({stage_count} stages)" if stage_count_required else name
        sub_stages = stages[:stage_count] + payload_stages
        performance = []
        payload = min_payload
        while True:
          launch_performance, wet_mass = delta_v(payload, sub_stages, orbit_deltav)
          twr = thrust / wet_mass / EARTH[GRAVITY]
          if twr >= min_twr:
            if plot_c3 is not None:
              planet, altitude = plot_c3
              velocity = circular(altitude, planet=planet) + launch_performance
              escape_velocity = escape(altitude, planet=planet)
              launch_performance = (velocity ** 2 - escape_velocity ** 2) / 10 ** 6
            if launch_performance >= min_performance:
              performance.append((launch_performance, payload))
              payload += payload_increment
            else: break
          else: break
        if len(performance) > 0:
          x, y = zip(*performance)
          ax.plot(x, y, label=variant_name)
      break
  else:
    print(f"Could not find {name}")

seconds = perf_counter() - start
print(f"{1000 * seconds:.2f}ms elapsed")

plt.xlabel("Delta-v (m/s)" if plot_c3 is None else "C3 (km²/s²)")
plt.ylabel("Payload (t)")
plt.legend()
plt.show()
