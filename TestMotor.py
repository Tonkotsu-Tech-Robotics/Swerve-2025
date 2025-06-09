import moteus
import moteus_pi3hat

class TestMotor:
    def __init__(self, motorID, transport, accel_limit=8.0, velocity_limit=8.0):
        """
        :param motorID: Moteus controller ID.
        :param transport: Transport object.
        :param accel_limit: Acceleration limit in rev/s².
        :param velocity_limit: Velocity limit in rev/s.
        """
        self.accel_limit = accel_limit
        self.velocity_limit = velocity_limit
        self.motor = moteus.Controller(id=motorID, transport=transport)

    # async def setPos(self, angle_deg):
    #     """
    #     Move to a target angle in degrees.
    #     """
    #     angle_rev = angle_deg / 360.0
    #     await self.motor.set_position(
    #         position=angle_rev,
    #         accel_limit=self.accel_limit,
    #         query=True
    #     )

    async def setPos(self, position_val):
        """
        Move to a position in revolutions 
        """
        await self.motor.set_position(
            
        )

    async def setSpeed(self, speed):
        """
        Set velocity in revolutions per second.
        """
        await self.motor.set_position(
            position=speed,
            accel_limit=self.accel_limit,
            query=True
        )

    async def stop(self):
        """
        Stop the motor.
        """
        await self.motor.set_stop()
