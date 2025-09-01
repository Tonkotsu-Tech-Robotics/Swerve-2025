import moteus
import moteus_pi3hat
import asyncio
from Swerve.SwerveModule import SwerveModule
import Utils.Constants as Constants
import wpimath.estimator as estimator
from wpimath.geometry import Pose2d, Rotation2d
import wpimath.kinematics 
from wpimath.geometry import Pose3d, Rotation3d
import math
import wpilib
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
        self.controller = Controller()
        self.modules = []
        # pose_estimator: estimator.SwerveDrive4PoseEstimatorBase | None = None
        # pose_estimator_3d: estimator.SwerveDrive4PoseEstimator3dBase | None = None

        # states = [wpimath.kinematics.SwerveModuleState() for _ in range(4)]
        # set_states = [wpimath.kinematics.SwerveModuleState() for _ in range(4)]

        # self.pose_estimator = self.initialize_pose_estimator()
        # self.pose_estimator_3d = self.initialize_pose_estimator_3d()
        # self.field = wpilib.Field2d()

        # self.robot_pos = Pose2d(0.0, 0.0, Rotation2d.fromDegrees(0.0))
        # self.robot_pos_3d = Pose3d(0.0, 0.0, 0.0, Rotation3d(0.0, 0.0, 0.0))

    # this is not my code maybe delete later
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
    
    async def getControllerSpeeds(self):
        """
        Uses the controller to set the speeds of the swerve modules based on joystick input.
        """
        forward_speed = self.controller.get_axis(Controller.LEFT_X)
        left_speed = self.controller.get_axis(Controller.LEFT_Y)
        turn_speed = self.controller.get_axis(Controller.RIGHT_X)

        return [forward_speed, left_speed, turn_speed]


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
    
    # async def initialize_pose_estimator(self):
    #     return estimator.SwerveDrive4PoseEstimator(
    #         Constants.kinematics,
    #         Rotation2d.fromDegrees(self.get_heading()), #<- needs to be updated
    #         self.get_module_positions(), #<- allso wrong change later
    #         Pose2d(0.0, 0.0, Rotation2d.fromDegrees(0.0)),
    #         np.array([[0.02], [0.02], [math.radians(5)]]),
    #         np.array([[0.3], [0.3], [math.radians(10)]])
    #     )
    
    # async def initialize_pose_estimator_3d(self):
    #     return estimator.SwerveDrive4PoseEstimator3d(
    #         Constants.kinematics,
    #         self.get_rotation_3d_function, #<- needs to be updated
    #         self.get_module_positions(), #<- wrong change later
    #         Pose3d(0.0, 0.0, 0.0, Rotation3d(0.0, 0.0, 0.0))
    # )

    async def swerve_drive_periodic(self):
        # await self.update_pos() 
        return

        #idk why its white 
        # self.pose_estimator.update(self.get_pidgey_rotation(), self.get_module_positions()) #fix more stuff dummy
        # self.pose_estimator_3d.update(self.pidgey.getRotation3d(), self.get_module_positions()) # needs to change the rotation functions here

        # self.robot_pos = self.pose_estimator.getEstimatedPosition()
        # self.robot_pos_3d = self.pose_estimator_3d.getEstimatedPosition()

    # async def update_pos(self):
        # return #no idea how to do this shit rn
    
    async def set_drive_speeds(self, forward_speed, left_speed, turn_speed, is_field_oriented = False):
        # Convert to chassis speeds the robot understand?s
        speeds = None
        if is_field_oriented:
            speeds = wpimath.kinematics.ChassisSpeeds.fromFieldRelativeSpeeds
            (forward_speed, left_speed, turn_speed, self.get_heading_rotation2d())
            #fix get heading

        else: 
            speeds = wpimath.kinematics.ChassisSpeeds(forward_speed, left_speed, turn_speed)

        speeds = wpimath.kinematics.ChassisSpeeds.discretize(speeds, 0.02)

        new_states = Constants.kinematics.toSwerveModuleStates(speeds)

        new_states = wpimath.kinematics.SwerveDrive4Kinematics.desaturateWheelSpeeds(new_states, Constants.MAX_SPEED)
        await self.set_swerve_module_states(new_states)

    async def reset_heading(self):
        #reset the heading
        return

    async def get_swerve_module_states(self) -> wpimath.kinematics.SwerveModuleState:
        current_module_state = wpimath.kinematics.SwerveModuleState()
        for i in range(4):
            current_module_state[i] = self.states[i]
        
        return current_module_state
    
    async def set_swerve_module_states(self, states):
        set_states = states
        for i in range (4):
            self.modules[i].set_states(set_states[i])

    
    async def get_swerve_module_positions(self) -> wpimath.kinematics.SwerveModulePosition:
        current_module_position = wpimath.kinematics.SwerveModulePosition[4]
        for i in range(4):
            current_module_position[i] = await self.modules.get_position()
        
        return current_module_position
    
    async def stop_modules(self):
        for i in range(4):
            await self.modules[i].stop()
    
    async def reset_drive_positions(self):
        for i in range(4):
            await self.modules.reset_drive_positions()

    
    async def get_heading(self) -> float:
        result = await self.transport.cycle([], request_attitude=True)
        imu_result = [
            x for x in result
            if x.id == -1 and isinstance(x, moteus_pi3hat.CanAttitudeWrapper)][0]

        return imu_result.euler_rad.yaw * 180.0 / math.pi  # Convert radians to degrees

    
    async def get_heading_rotation2d(self) -> float:
        return Rotation2d.fromDegrees(await self.get_heading())

