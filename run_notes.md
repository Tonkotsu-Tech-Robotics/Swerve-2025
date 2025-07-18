# Setup Guide

Follow the moteus install docs available at

https://github.com/mjbots/pi3hat/blob/master/docs/reference.md#usage-with-client-side-tools

(I'll put the commands down here to run if you are too lazy like I was)

```
sudo apt install python3-pyside2* python3-serial python3-can python3-matplotlib python3-qtconsole libraspberrypi-dev

python -m venv --system-site-packages moteus-venv

sudo bash

source moteus-venv/bin/activate

pip install asyncqt importlib_metadata pyelftools

pip install moteus moteus_gui moteus-pi3hat
```

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

Ex: Comma-separated values for tview in ids 11 and 12
```
python3 -m moteus_gui.tview -t 11,12
```

Ex: Dash-separated for tview in ids 1 through 15
```
python3 -m moteus_gui.tview -t 1-15
```

Dash-separated values can be useful for calibration, motor id lookup and looking at the values for multiple motors.

Comma-separated values can be useful for looking at the stats of a single motor at a time.

You may want to change the IDs so they aren't overriding each other (which can happen if there is improper configuration).

You will want to reopen tview if you have it open already (otherwise open it if you don't), but run this command instead:

```
python3 -m moteus_gui.tview -t [current motor id], [desired motor id]
```

Afterwards, go to the terminal in the bottom of tview and run the following:
```
[current id]>conf set id.id [desired id]
```
Wait for the desired ID to be set and for the terminal to reconfigure some stuff, before running this command:
```
[desired id]>conf write
```
You will know if you did it right if after running `[desired id]>conf write`, you get a console message that says `OK`. 

As an example usage of this, I have a motor on ID 3 and want to change that motor to ID 15. I will need to run the following:
```
python3 -m moteus.tview -t 3,15
```
Wait for motors to get configured up.
```
3>conf set id.id 15
```
Wait for tview to redo some configurations
```
15>conf write
```

Quick rundown of the commands we just ran:

The first command opens up tview for IDs 3 and 15. This is needed since the configuration changes right away and as soon as you change the ID to a new one, the motor will no longer be accessible on the old ID.

The second command simply calls on ID 3 to change its motor ID to 15.

The third command calls on the newly set ID 15 to write its changes so that its persistant.

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

IMPORTANT: If you have multiple motors, you will have to run this command for each individual motor in order to prevent issues. If you did it incorrectly, running any code should show error 39 in the fault section of servo_stats in tview. You can check if you did it correctly in tview by running this command in the bottom terminal of tview:

```
[motor id to check]>d stop
[motor id to check]>d pos 20 0 0.5 a5 v5
[motor id to check]>d stop
```

Example usage:
```
12>d stop
12>d pos 20 0 0.5 a5 v5
12>d stop
```

(This will set the position to 20 with an ending velocity of 0, torque of 0.5, and max accel of 5 rev/s^2 and max velocity of 5 rev/s, then stop the motor).

NOTE: In order to completely check for faults, you may want to run that more than once (2 times should be fine).

Setting servo pos max/min to NaN will disable the check that requires the motor position to start within a specific range (from -1 to 1), and this can screw up the motors if you don't have a command that moves the motors into their original starting position.

# Additional Notes

Running the tview GUI will also allow you to graph and track motor telemetry data such as current position, velocity, among other points, making it easier to debug

Viewing errors or faults can be done by going into tview, then servo_stats, and then fault.

SUPER IMPORTANT!!!!!! In any motor.set_position() or motor.set_position_wait_command() function, ALWAYS have a velocity_limit and accel_limit parameter or else ur motor go bye bye :D An example of such is provided down below.

```
await controller.set_position( # Same thing with controller.set_position_wait_complete()
    position=1.0,
    velocity=2.0,
    velocity_limit=5.0,
    accel_limit=4.0
)
```
