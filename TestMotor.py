import moteus
import moteus_pi3hat

class TestMotor:
    def __init__(self, motorID, transport, accel_limit=2.0):
        """
        :param motorID: Moteus controller ID.
        :param transport: Transport object.
        :param accel_limit: Acceleration limit in rev/s².
        """
        self.accel_limit = accel_limit
        self.motor = moteus.Controller(id=motorID, transport=transport)

    async def setPos(self, angle_deg):
        """
        Move to a target angle in degrees.
        """
        angle_rev = angle_deg / 360.0
        await self.motor.set_position(
            position=angle_rev,
            accel_limit=self.accel_limit,
            query=True
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
