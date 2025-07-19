import moteus
import moteus_pi3hat
import asyncio
from Swerve.SwerveModule import SwerveModule
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

        self.modules = [
            SwerveModule(drive_id=11, steer_id=12, transport=self.transport),
            SwerveModule(drive_id=13, steer_id=14, transport=self.transport),
            SwerveModule(drive_id=15, steer_id=16, transport=self.transport),
            SwerveModule(drive_id=17, steer_id=18, transport=self.transport),
        ]

        self.controller = Controller()
    
    

    """
    async def stop(self):
        
        Stops all swerve modules.
        
        [
            await module.stop() for module in self.modules
        ]

    async def setAll(self, speeds, angles):
        
        Sets the speed and angle of each swerve module.
        
        [
            await module.set(speed, angle, self.transport)
            for module, speed, angle in zip(self.modules, speeds, angles)
        ]

    async def setModule(self, index, speed, angle):
        
        Sets the speed and angle of a specific swerve module.
        
        await self.modules[index].set(speed, angle, self.transport)

    async def getModulePosition(self, index):
        
        Gets the position of a specific swerve module.
        
        return await self.modules[index].getPosition()
    
    async def setMotorSpeeds(self):
        
        Uses the controller to set the speeds of the swerve modules based on joystick input.
        
        left_x = self.controller.get_axis(Controller.LEFT_X)
        left_y = self.controller.get_axis(Controller.LEFT_Y)
        right_x = self.controller.get_axis(Controller.RIGHT_X)
        right_y = self.controller.get_axis(Controller.RIGHT_Y)

        # Calculate speeds and angles for each module
        speeds = [left_y, left_y, right_y, right_y]
        angles = [left_x, left_x, right_x, right_x]

        await self.setAll(speeds, angles)

        """