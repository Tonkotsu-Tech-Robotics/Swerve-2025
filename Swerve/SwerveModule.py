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

    # Sets the speed and angle of the swerve module (in motor revolutions)
    async def set(self, speed: float, angle_deg: float):
        """
        Sets the speed and angle of the swerve module.

        :param speed (float): The speed of the swerve module in revolutions per second.
        :param angle_deg (float): The angle of the swerve module in degrees.
        """
        # Convert the angle from degrees to revolutions
        # 1 revolution = 360 degrees, so we divide by 360
        angle_rev = angle_deg / 360.0

        # BE AWARE OF CONVERSIONS

        await self.steer.setAngle(angle_rev)
        await self.drive.setVelocity(speed)

    # Stops the swerve module
    async def stop(self):
        """
        Stops the swerve module by stopping both the drive and steer motors.
        """

        await self.drive.stop()
        await self.steer.stop()