# Setup Guide

Follow the moteus install docs available at

https://github.com/mjbots/pi3hat/blob/master/docs/reference.md#usage-with-client-side-tools

In the rasp pi, run these commands to get started with running any of the python files

```
sudo bash # Important since you'll have to run the python files in root
cd Swerve-2025
source moteus-venv/bin/activate # If moteus-venv does not exist, follow moteus guide on creating venv and installing required libraries
```

# Motor setup

You will have to figure out what motors you have first (as well as their ids) before doing any calibration. You can run this command to do that.

```
python3 -m moteus.moteus_tool --info
```

NOTE: If you have more than one motor you want to tune, you will have to adjust their IDs individually.

After figuring out what motors you have, run this command:

```
python3 -m moteus_gui.tview -t [motor id]
```

NOTE: If you want to have multiple motors, it can be dash-separated for a range or comma-separated for individual motors. Examples are given below.

Comma-separated values for tview in ids 11 and 12
```
python3 -m moteus_gui.tview -t 11,12
```

Dash-separated for tview in ids 1 through 15
```
python3 -m moteus_gui.tview -t 1-15
```

Dash-separated values can be useful for calibration, motor id lookup and looking at the values for multiple motors.

Comma-separated values can be useful for looking at the stats of a single motor at a time.

# Calibration

To properly calibrate motors for code running, run this command in the shell AFTER you have sourced into the virtual environment

IMPORTANT: While calibrating, make sure any motor that is being calibrated can freely spin!

If you want to calibrate multiple motors (on different can busses), [motor id here] should be comma-separated

```
python3 -m moteus.moteus_tool -t [motor id here] --calibrate
```

Ex for 2 motors:
```
python3 -m moteus.moteus_tool -t 1,2 --calibrate
```

# Starting the motors

There are several example files that should work fine after calibration, the one that should be used is wait_complete.py.

https://github.com/mjbots/moteus/blob/main/lib/python/examples/wait_complete.py

Before starting motors, make sure to disable servopos position min/max (You only have to do this the first time setting up from the Raspberry Pi). You can do this by first going into tview

```
python3 -m moteus_gui.tview -t [all your motor ids, comma separated]
```

Then, in the command bar at the bottom of the GUI, running

```
[motor id]>conf set servopos.position_min nan
```
```
[motor id]>conf set servopos.position_max nan
```

then running this command to save the configurations

```
[motor id]>conf write
```

Setting servo pos max/min to NaN will disable the check that requires the motor position to start within a specific range (from -1 to 1), and this can screw up the motors if you don't have a command that moves the motors into their original starting position.

# Additional Notes

Running the tview GUI will also allow you to graph and track motor telemetry data such as current position, velocity, among other points, making it easier to debug

SUPER IMPORTANT!!!!!! In any motor.set_position() or motor.set_position_wait_command() function, ALWAYS have a velocity_limit and accel_limit parameter or else ur motor go bye bye :D An example of such is provided down below.

```
await controller.set_position( # Same thing with controller.set_position_wait_complete()
    position=1.0,
    velocity=2.0,
    velocity_limit=5.0,
    accel_limit=4.0
)
```
