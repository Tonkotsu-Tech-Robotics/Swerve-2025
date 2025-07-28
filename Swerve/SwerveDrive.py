import moteus
import moteus_pi3hat
import asyncio
from Swerve.SwerveModule import SwerveModule
from utils.Constants import kinematics
import wpimath.estimator.SwerveDrivePoseEstimator
import wpimath.estimator.SwerveDrivePoseEstimator3d
from wpimath.geometry import Pose2d, Rotation2d
from wpimath.kinematics import SwerveDriveKinematics
from wpimath.geometry import Pose3d, Rotation3d
import math
import numpy as np


from Utils.Controller import Controller

class SwerveDrive:
    def __init__(self):
        self.transport: moteus.Transport = moteus_pi3hat.Pi3HatRouter(
            servo_bus_map={
                1: [11, 12], # Bus 1, Motor ids 11 and 12
                2: [13, 14], # Bus 2, Motor ids 13 and 14
                3: [15, 16], # Bus 3, Motor ids 15 and 16
                4: [17, 18],  # Bus 4, Motor ids 17 and 18
            }
        )

        #need to add controller
        self.modules = []
        pose_estimator: SwerveDrivePoseEstimator | None = None
        pose_estimator_3d: SwerveDrivePoseEstimator3d | None = None
        field: Field2d | None = None

        states = [SwerveModuleState() for _ in range(4)]
        set_states = [SwerveModuleState() for _ in range(4)]
        
        self.modules = self.initialize_modules()


    
    
    async def stop(self):
        """
        Stops all swerve modules.
        """
        [
            await module.stop() for module in self.modules
        ]

    async def setAll(self, speeds, angles):
        """
        Sets the speed and angle of each swerve module.
        """
        [
            await module.set(speed, angle, self.transport)
            for module, speed, angle in zip(self.modules, speeds, angles)
        ]

    async def setModule(self, index, speed, angle):
        """
        Sets the speed and angle of a specific swerve module.
        """
        await self.modules[index].set(speed, angle, self.transport)

    async def getModulePosition(self, index):
        """
        Gets the position of a specific swerve module.
        """
        return await self.modules[index].getPosition()
    
    async def setMotorSpeeds(self):
        """
        Uses the controller to set the speeds of the swerve modules based on joystick input.
        """

        left_x = self.controller.get_axis(Controller.LEFT_X)
        left_y = self.controller.get_axis(Controller.LEFT_Y)
        right_x = self.controller.get_axis(Controller.RIGHT_X)
        right_y = self.controller.get_axis(Controller.RIGHT_Y)

        # Calculate speeds and angles for each module
        speeds = [left_y, left_y, right_y, right_y]
        angles = [left_x, left_x, right_x, right_x]

        await self.setAll(speeds, angles)


    # NEW CODE

    async def initialize_modules(self):
        return [
            SwerveModule(
               drive_id=11, steer_id=12, transport=self.transport
            ),
            SwerveModule(
                drive_id=13, steer_id=14, transport=self.transport
            ),
            SwerveModule(
                drive_id=15, steer_id=16, transport=self.transport
            ),
            SwerveModule(
                drive_id=17, steer_id=18, transport=self.transport
            )
        ]
    
    async def initialize_pose_estimator(self):
        return SwerveDrivePoseEstimator(
            kinematics,
            Rotation2d.fromDegrees(self.get_heading()), #<- needs to be updated
            self.get_module_positions(),
            Pose2d(0.0, 0.0, Rotation2d.fromDegrees(0.0)),
            np.array([[0.02], [0.02], [math.radians(5)]]),
            np.array([[0.3], [0.3], [math.radians(10)]])
        )
    
    async def initialize_pose_estimator_3d(self):
        return SwerveDrivePoseEstimator3d(
            kinematics,
            #get rotation 3d function,
            self.get_module_positions(),
            Pose3d(0.0, 0.0, 0.0, Rotation3d(0.0, 0.0, 0.0))
    )

    async def swerve_drive_periodic(self):
        await self.update_pos() 

        self.pose_estimator.update(self.get_pidgey_rotation(), self.get_module_positions())
        self.pose_estimator_3d.update(self.pidgey.getRotation3d(), self.get_module_positions()) # needs to change the rotation functions here

        self.field.setRobotPose(self.pose_estimator.getEstimatedPosition())
        self.robot_pos = self.pose_estimator.getEstimatedPosition()

    async def update_pos(self):
        return #no idea how to do this shit rn
    
    async def set_drive_speeds(self, forward_speed, left_speed, turn_speed, is_field_oriented):
        # Convert to chassis speeds the robot understands
        if is_field_oriented:
            speeds = self.from_field_relative_speeds(
                forward_speed, left_speed, turn_speed, self.get_pidgey_rotation()
            )
        else:
            speeds = ChassisSpeeds(forward_speed, left_speed, turn_speed)

        speeds = self.discretize(speeds, 0.02)

        new_states = kinematics.toSwerveModuleStates(speeds)

        self.desaturate_wheel_speeds(new_states, self.MAX_SPEED)
        self.set_module_states(new_states)

    
