import moteus
import moteus_pi3hat
from wpimath.controller import PIDController
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState
from wpimath.kinematics import SwerveModulePosition
from wpimath.geometry import Rotation2d
import math
from SwerveMotor import SwerveMotor
from constants import DRIVE_MOTOR_GEAR_RATIO, WHEEL_DIAMETER


class SwerveModule:
    def __init__(self, drive_id: int, steer_id: int, transport):
        self.drive = SwerveMotor(drive_id, transport)
        self.steer = SwerveMotor(steer_id, transport)

        # Initial position and state
        self.swerve_module_position = SwerveModulePosition(0.0, Rotation2d())
        self.state = SwerveModuleState(0.0, Rotation2d())

    async def getPosition(self) -> SwerveModulePosition:
        drive_position = await self.drive.pos()  # revolutions
        steer_position = await self.steer.pos()  # revolutions

        angle = Rotation2d.fromRotations(steer_position)
        distance = (drive_position / DRIVE_MOTOR_GEAR_RATIO) * WHEEL_DIAMETER * math.pi

        self.swerve_module_position = SwerveModulePosition(distance, angle)
        return self.swerve_module_position


    # Sets the speed and angle of the swerve module (in motor revolutions)
    async def set(self, speed: float, angle_deg: float, transport: moteus.Transport) -> list:
        """
        Sets the speed and angle of the swerve module.

        :param speed (float): The speed of the swerve module in revolutions per second.
        :param angle_deg (float): The angle of the swerve module in degrees.
        
        :return list: A list containing the results of setting the speed and angle.
        """
        # Convert the angle from degrees to revolutions
        # 1 revolution = 360 degrees, so we divide by 360
        angle_rev = angle_deg / 360.0

        # BE AWARE OF CONVERSIONS
        steer_angle = await self.steer.setAngle(angle_rev, transport)
        drive_velocity = await self.drive.setVelocity(speed, transport)

        # Map the steer angle list and drive velocity list to a dictionary
        return {
            "steer_angle": steer_angle
        }

    # Stops the swerve module
    async def stop(self):
        """
        Stops the swerve module by stopping both the drive and steer motors.
        """

        await self.drive.stop()
        await self.steer.stop()
