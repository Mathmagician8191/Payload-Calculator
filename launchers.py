import pyjson5

launcher_groups = ["irl_launchers"]

launchers = []

for group in launcher_groups:
  with open(f"rockets/{group}.json5") as file:
    launchers += pyjson5.load(file)
