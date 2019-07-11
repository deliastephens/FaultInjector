# FaultInjector
A Python-TKinter application with the capability to connect to running SITL
instances, create its own, load WayPoint missions, inject instrumentation failures,
and run multiple simulations in succession for in-depth, efficient fault testing
of the ArduPilot software.

Forked from Jayson Boubin's [FaultInjector](https://github.com/boubinjg/FaultInjector),
developed for AFIT in 2016 (original notes [here](http://jaysonboubin.com/faultinjection.html)),
this version of FaultInjector adds much-needed functionality and modernizes the
software for Python3.

With this UAV Fault Injection, it is easy to test many mission scenarios in varied
environments, making it a robust UAV testing and verification tool.

### Running
To run FaultInjector, simply download all of the required programs and packages,
navigate to the folder that contains `FaultInjector.py` in a Command Prompt, and
type
```
python3 FaultInjector.py
```

## Requirements
### Python and Packages
FaultInjector requires [Python3](https://www.python.org/download/releases/3.0/)
or greater, and the following packages:

`os, signal, psutil, dronekit, tkinter, time, __thread,
sys, struct, curses, pymavlink, pymavlink.dialects.v10`

To get these packages, it's easiest to use `pip3` with Python3.

### ArduPilot
FaultInjector makes use of [ArduPilot SITL](http://ardupilot.org/dev/docs/sitl-simulator-software-in-the-loop.html). I have a custom version of ArduPilot that uses different
locations as its default and would recommend cloning [my fork](https://github.com/deliastephens/ardupilot) if you're at CICATA.

## Features
### SITL
To start a new instance of MavLink's SITL, simply press 'Start SITL' in the
upper left toolbar. This will run `sim_vehicle.py` with the default options in
the location specified by the text box. (Note: this process is somewhat slow.
Optimizations incoming).

To add a named location to ArduPilot, simply navigate to
`your_ardupilot_folder/Tools/autotest` and modify the `locations.txt` file
in the specified manner. Restart FaultInjector to be able to enter that location
in the box.

### Missions
To load custom missions in FaultInjector, there are two options:
put your Mission File (saved as MP Waypoint.txt) in the following formta (insert picture)

### FaultInjection
