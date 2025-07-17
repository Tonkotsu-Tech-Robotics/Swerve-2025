import moteus
import moteus_pi3hat
import asyncio
from SwerveModule import SwerveModule

class SwerveDrive:
    def __init__(self):
        transport = moteus_pi3hat.Pi3HatRouter(
            servo_bus_map={
                1: [11, 12], # Bus 1, Motor ids 11 and 12
                2: [13, 14], # Bus 2, Motor ids 13 and 14
                3: [15, 16], # Bus 3, Motor ids 15 and 16
                4: [17, 18],  # Bus 4, Motor ids 17 and 18
            }
        )

        self.modules = [
            SwerveModule(drive_id=11, steer_id=12, transport=transport),
            SwerveModule(drive_id=13, steer_id=14, transport=transport),
            SwerveModule(drive_id=15, steer_id=16, transport=transport),
            SwerveModule(drive_id=17, steer_id=18, transport=transport),
        ]


    async def stop(self):
        """
        Stops all swerve modules.
        """
        await asyncio.gather(*(module.stop() for module in self.modules))

    async def set(self, speeds, angles):
        """
        Sets the speed and angle of each swerve module.
        """
        await asyncio.gather(*(module.set(speed, angle) for module, speed, angle in zip(self.modules, speeds, angles)))
    
    async def setModule(self, index, speed, angle):
        """
        Sets the speed and angle of a specific swerve module.
        """
        await self.modules[index].set(speed, angle)