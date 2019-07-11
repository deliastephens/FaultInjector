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

![](https://raw.githubusercontent.com/deliastephens/FaultInjector/master/res/FaultInjector.PNG)

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
![](https://raw.githubusercontent.com/deliastephens/FaultInjector/master/res/connect_toolbar.PNG)
This version of FaultInjector inclues the ability to start and stop
Software-in-the-Loop Simulations (SITL).

To start a new instance of MavLink's SITL, simply press 'Start SITL' in the
upper left toolbar. This will run `sim_vehicle.py` with the default options in
the location specified by the text box. After a while, a MAVProxy window should
appear running the simulation with the default parameters.

![](https://raw.githubusercontent.com/deliastephens/FaultInjector/master/res/MAVProxy.PNG)
To connect to the simulation, simply press 'Connect' and you'll be good to go.

To add a named location to ArduPilot, simply navigate to
`your_ardupilot_folder/Tools/autotest` and modify the `locations.txt` file
in the specified manner. Restart FaultInjector to be able to enter that location
in the box.

### Missions
![](https://raw.githubusercontent.com/deliastephens/FaultInjector/master/res/mission_toolbar.PNG)
This version of FaultInjector allows for custom missions to be loaded.

To load custom missions in FaultInjector, there are two options:
put your Mission File (saved as MP Waypoint.txt) in the following format (insert picture)
into the `missions` folder.

FaultInjector will automatically recenter the mission around the home point of
the drone itself.

### FaultInjection
