# Setup Guide

Follow the moteus install docs available at

https://github.com/mjbots/pi3hat/blob/master/docs/reference.md#usage-with-client-side-tools

In the rasp pi, run these commands to get started with running any of the python files

```
sudo bash # Important since you'll have to run the python files in root
cd Swerve-2025
source moteus-venv/bin/activate # If moteus-venv does not exist, follow moteus guide on creating venv and installing required libraries
```

# Calibration

To properly calibrate motors for code running, run this command in the shell AFTER you have sourced into the virtual environment

IMPORTANT: While calibrating, make sure any motor that is being calibrated can freely spin!

```
python3 -m moteus.moteus_tool -t [motor id here] --calibrate --cal-motor-poles 14
```

- Addendum 1: The value for cal motor poles must be correct, however for our motors it should be 14, and if it is wrong then it will tell you the correct number to use in the argument.
- Addendum 2: It may be optional, so someone needs to check whenever they have the time.

# Starting the motors

There are several example files that should work fine after calibration, the one that should be used is wait_complete.py.

https://github.com/mjbots/moteus/blob/main/lib/python/examples/wait_complete.py

Before starting motors, make sure to disable servopos position min/max (You only have to do this the first time setting up from the Raspberry Pi). You can do this by first going into tview

```
sudo moteus-venv/bin/tview
```

Then, in the command bar at the bottom of the GUI, running

```
conf set servopos.position_min nan
```
```
conf set servopos.position_max nan
```

then running this command to save the configurations

```
conf write
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
