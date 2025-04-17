Rocket launch vehicle performance comparison tool

Programs included in this repository:

`payload.py` - calculate the launchers capable of launching a given payload mass into a given orbit, or calculate the maximum payload capacity of each launcher to a given orbit

`graph.py` - graph launcher payload vs delta-v or C3 values

These programs contain configuration options

Configuration files:

`celestial_bodies.py` - contains information about celestial bodies, add more if required

`launchers.py` - contains specifications of launch vehicles, edit or add more as necessary, or remove launchers if you don't want the scripts to consider them

Other files to look at:

`orbits.py` -  contains functions for calculating delta-v of some transfer types, useful reference to set up the delta-v for reaching a given orbit correctly
