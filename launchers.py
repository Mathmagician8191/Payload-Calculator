import pyjson5
import os

launcher_groups = ["misc_launchers","american_launchers","soviet_launchers"]

launchers = []

for group in launcher_groups:
  with open(f"rockets/{group}.json5") as file:
    launchers += pyjson5.load(file)

stage_library = {}

for path in os.listdir("stages"):
  with open(f"stages/{path}") as file:
    json_stages = pyjson5.load(file)
    for stage in json_stages:
      stage_library[stage["name"]] = stage

def lcf(number):
  for x in range(2, number + 1):
    if number % x == 0: return x

def get_stage(stage):
  if isinstance(stage, str):
    data = stage_library[stage]
    return data["wet_mass"], data["dry_mass"], data["isp"], data["thrust"]
  else: return stage

def configuations(launcher):
  min_stages = launcher["min_stages"]
  stages = launcher["stages"]
  name = launcher["name"]
  launch_thrust = launcher["launch_thrust"]
  stage_count_required = len(stages) != min_stages
  results = []
  for stage_count in range(min_stages, len(stages) + 1):
    sub_stages = stages[:stage_count]
    variant_name = f"{name} ({stage_count} stages)" if stage_count_required else name
    results.append([launcher, stage_count, None, 0])
    if "boosters" in launcher:
      _, _, isp, thrust = get_stage(sub_stages[0])
      mass_flow = thrust / isp
      #core_stage, *others = sub_stages
      for booster in launcher["boosters"]:
        for count in launcher["booster_counts"]:
          results.append([launcher, stage_count, booster, count])
  return results

def configuration_data(configuration):
  if len(configuration) == 4:
    launcher, stage_count, booster, count = configuration
  elif len(configuration) == 2:
    launcher, stage_count = configuration
    booster, count = None, 0
  else:
    print("Unsupported format for rocket configuration")
    quit()
  min_stages = launcher["min_stages"]
  stages = launcher["stages"]
  name = launcher["name"]
  launch_thrust = launcher["launch_thrust"]
  stage_count_required = len(stages) != min_stages
  stages = stages[:stage_count]
  variant_name = f"{name} ({stage_count} stages)" if stage_count_required else name
  if booster is not None:
    _, _, isp, thrust = get_stage(stages[0])
    mass_flow = thrust / isp
    booster_details = stage_library[booster]
    is_asparagus = "asparagus" in booster_details and booster_details["asparagus"]
    wet_mass = booster_details["wet_mass"]
    dry_mass = booster_details["dry_mass"]
    booster_isp = booster_details["isp"]
    booster_thrust = booster_details["thrust"]
    booster_mass_flow = booster_thrust / booster_isp
    booster_launch_thrust = booster_details["launch_thrust"]
    launch_thrust = launch_thrust + booster_launch_thrust * count
    variant_name += f" ({count}x {booster})"
    if is_asparagus:
      group_size = lcf(count)
      group_count = count // group_size
      new_stages = []
      total_thrust = thrust
      total_mass_flow = mass_flow
      for x in range(group_count):
        total_thrust += booster_thrust * group_size
        total_mass_flow += booster_mass_flow * group_size
        total_isp = total_thrust / total_mass_flow
        new_stages.append([wet_mass * group_size, dry_mass * group_size, total_isp, total_thrust])
      new_stages.reverse()
      stages = new_stages + stages
    else:
      core_stage, *others = stages
      core_flow_rate = launcher["core_flow_rate"] if "core_flow_rate" in launcher else 1
      thrust *= core_flow_rate
      mass_flow *= core_flow_rate
      total_thrust = thrust + booster_thrust * count
      total_mass_flow = mass_flow + booster_mass_flow * count
      total_isp = total_thrust / total_mass_flow
      core_mass_flow = (wet_mass - dry_mass) * mass_flow / booster_mass_flow
      core_wet, core_dry, core_isp, core_thrust = get_stage(core_stage)
      core_wet -= core_mass_flow
      first_stages = [
        (core_mass_flow + wet_mass * count, dry_mass * count, total_isp, total_thrust),
        (core_wet, core_dry, core_isp, core_thrust),
      ]
      stages = first_stages + others
  return {
    "name" : variant_name,
    "stages" : stages,
    "launch_thrust" : launch_thrust,
  }
