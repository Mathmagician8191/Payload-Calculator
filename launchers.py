import pyjson5

with open("rockets/irl.json5") as file:
  launchers = pyjson5.load(file)
