import moteus
import moteus_pi3hat

class TestMotor:
    def __init__(self, motorID, transport, accel_limit=10.0, velocity_limit=12.0):
        """
        :param motorID: Moteus controller ID.
        :param transport: Transport object.
        :param accel_limit: Acceleration limit in rev/s².
        :param velocity_limit: Velocity limit in rev/s.
        """
        self.accel_limit = accel_limit
        self.velocity_limit = velocity_limit
        self.motor = moteus.Controller(id=motorID, transport=transport)

    async def setAngle(self, angle_deg):
        """
        Move to a target angle in degrees.
        Returns boolean and retrived position after rotation
        :param angle_deg: An angle in degrees
        """

        try:
            angle_rev = angle_deg / 360.0
            
            degAngle = await self.getPos() * 360

            if degAngle == None:
                raise TypeError("Degree angle in setAngle function returned as type None")
        
            adjustedAngle = angle_rev # temp angle for now, have the calculations for now

            await self.motor.set_position(
                position=(self.getPos() + adjustedAngle),
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit
            )

            return [True, self.getPos()]
        except Exception as e:
            print("Error caught in setAngle function:" + e)
            return [False, None]


    async def addToCurrentPos(self, position_val):
        """
        Move to a position in revolutions
        Moves in relation to current position
        """
        return await self.motor.set_position(
            position=(position_val + self.getPos()),
            accel_limit=self.accel_limit,
            velocity_limit=self.velocity_limit
        )

    async def setPos(self, position_val):
        """
        Move to a position in revolutions 
        """
        return await self.motor.set_position(
            position=position_val,
            accel_limit=self.accel_limit,
            velocity_limit=self.velocity_limit
        )

    async def getPos(self):
        """
        Returns the motor position (either in revolutions or None)
        """

        # Query the motor for its current state
        result = await self.motor.set_position(query=True)

        # Extract the position from the result
        return result.values.get('position', None)

    async def setPosWaitComplete(self, position_val):
        """
        Moves to a position in revolutions
        Waits until command is complete before moving onto the next command
        """
        return await self.motor.set_position_wait_complete(
            position=position_val,
            velocity=0,
            accel_limit=self.accel_limit,
            velocity_limit=self.velocity_limit
        )

    async def stop(self):
        """
        Stop the motor.
        """
        await self.motor.set_stop()
