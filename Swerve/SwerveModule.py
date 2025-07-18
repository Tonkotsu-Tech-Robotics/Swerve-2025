import moteus
import moteus_pi3hat
from wpimath.controller import PIDController
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState
from wpimath.kinematics import SwerveModulePosition
from wpimath.geometry import Rotation2d
import math
from Swerve.SwerveMotor import SwerveMotor
from Utils.Constants import DRIVE_MOTOR_GEAR_RATIO, WHEEL_DIAMETER


class SwerveModule:
    def __init__(self, drive_id: int, steer_id: int, transport):
        self.drive = SwerveMotor(drive_id, transport)
        self.steer = SwerveMotor(steer_id, transport)

        # Initial position and state
        self.swerve_module_position = SwerveModulePosition(0.0, Rotation2d())
        self.state = SwerveModuleState(0.0, Rotation2d())

    async def getPosition(self) -> SwerveModulePosition:
        drive_position = await self.drive.position()  # revolutions
        steer_position = await self.steer.position()  # revolutions

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
        # Set angle natively takes degrees 
        await self.steer.setAngle(angle_deg, transport)
        await self.drive.setVelocity(speed, transport)

        # Map the steer angle list and drive velocity list to a dictionary
        return {
            "steer_angle": self.steer.position,
            "drive_velocity": self.drive.velocity
        }

    # Stops the swerve module
    async def stop(self):
        """
        Stops the swerve module by stopping both the drive and steer motors.
        """

        await self.drive.stop()
        await self.steer.stop()
