from config import system

match system:
  case "rss":
    from rss_bodies import *
  case "ksp":
    from ksp_bodies import *
  case x:
    print(f"Invalid system {x}")
