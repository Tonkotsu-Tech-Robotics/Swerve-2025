import moteus
import moteus_pi3hat
from wpimath.controller import PIDController
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState
from wpimath.geometry import Rotation2d
import math
from SwerveMotor import SwerveMotor

class SwerveModule:
    def __init__(self, drive_id, steer_id, transport):
        self.drive = SwerveMotor(drive_id, transport)
        self.steer = SwerveMotor(steer_id, transport)

    # Sets the speed and angle of the swerve module
    async def set(self, speed, angle_deg):
        angle_rev = angle_deg / 360.0

        # BE AWARE OF CONVERSIONS

        await self.steer.setAngle(angle_rev)
        await self.drive.setVelocity(speed)

    # Stops the swerve module
    async def stop(self):
        await self.drive.stop()