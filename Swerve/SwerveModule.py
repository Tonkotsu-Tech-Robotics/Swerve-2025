import moteus
import moteus_pi3hat
from wpimath.controller import PIDController
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState
from wpimath.geometry import Rotation2d
import math

class SwerveModule:
    def __init__(self, drive_id, steer_id, transport):
        self.drive = moteus.Controller(id=drive_id, transport=transport)
        self.steer = moteus.Controller(id=steer_id, transport=transport)

    # Sets the speed and angle of the swerve module
    async def set(self, speed, angle_deg):
        angle_rev = angle_deg / 360.0

        # BE AWARE OF CONVERSIONS

        await self.steer.set_position(position=angle_rev, query=True)
        await self.drive.set_position(velocity=speed, query=True)

    # Stops the swerve module
    async def stop(self):
        await self.drive.set_stop()
