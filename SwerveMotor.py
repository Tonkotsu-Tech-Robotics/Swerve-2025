import moteus
import asyncio
import math

class SwerveMotor:
    def __init__(self, motorID, transport, accel_limit=16.0, velocity_limit=16.0, watchdog_timeout=math.inf):
        """
        Constructs a swerve motor instance

        :param motorID (int): Moteus controller ID.
        :param transport (Pi3HatRouter): Transport object.
        :param accel_limit (float): Acceleration limit in rev/s².
        :param velocity_limit (float): Velocity limit in rev/s.
        :param watchdog_timeout (float): Timeout before function stops running (if you don't know how this param works, better not touch it).
        """
        self.accel_limit = accel_limit
        self.velocity_limit = velocity_limit
        self.watchdog_timeout = watchdog_timeout
        self.motor = moteus.Controller(id=motorID, transport=transport)

    @property
    async def pos(self):
        """
        Gives the current absolute motor position (relative to position 0).

        :return float: The current absolute motor position in revolutions.
        """

        # Query the motor for its current state
        result = await self.motor.set_position(query=True)

        # Extract the position from the result
        return result.values.get('position', None)

    @property
    async def velocity(self):
        """
        Gives the current velocity

        :return float: The current velocity of the motor in rev/s.
        """

        # Query the motor for its current state
        result = await self.motor.set_position(query=True)

        # Extract the position from the result
        return result.values.get('velocity', None)


    async def setAngle(self, angle_deg, wait_time=0):
        """
        Move to a target angle in degrees.
        Returns boolean and retrived position after rotation

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().
        
        :param angle_deg (float): An angle in degrees
        :param wait_time (float): The time to wait for the set_position function to complete.
        
        :return [boolean, float, any]: A completion boolean, position after the command has complete, set_position returned value
        """

        try:
            angle_rev = angle_deg / 360.0
            
            degAngle = await self.getPos() * 360

            if degAngle == None:
                raise TypeError("Degree angle in setAngle function returned as type None")
        
            adjustedAngle = angle_rev # temp angle for now, have the calculations for now

            command1 = await self.motor.set_position(
                position=(self.getPos() + adjustedAngle),
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=math.inf
            )

            asyncio.sleep(wait_time)

            return [True, self.getPos(), command1]
        except Exception as e:
            print(f"Error caught in setAngle function: {e}")
            return [False, None, None]


    async def addToCurrentPos(self, position_val, wait_time=0):
        """
        Move to a position in revolutions relative to current position.

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().
        
        :param position_val (float): The position to move to in revolutions.
        :param wait_time (float): The time to wait for the set_position function to complete.
        
        :return [boolean, float, any]: A completion boolean, position after the command has complete, set_position returned value
        """
        try:
            command1 = await self.motor.set_position(
                position=(position_val + self.getPos()),
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=math.inf
            )

            asyncio.sleep(wait_time)

            return [True, self.getPos(), command1]
        except Exception as e:
            print(f"Error caught in addToCurrentPosition function: {e}")
            return [False, None, None]

    async def setPos(self, position_val, wait_time):
        """
        Move to an absolute position in revolutions.

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().

        :param position_val (float): The position to move to in revolutions.
        :param wait_time (float): The time to wait for the set_position function to complete.
        
        :return [boolean, float, any]: A completion boolean, position after the command has complete, set_position returned value
        """
        try:
            command1 = await self.motor.set_position(
                position=position_val,
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=math.inf
            )

            asyncio.sleep(wait_time)

            return [True, self.getPos(), command1]
        except Exception as e:
            print(f"Error caught in addToCurrentPosition function: {e}")
            return [False, None, None]


    async def setPosWaitComplete(self, position_val):
        """
        Moves to a position in revolutions
        Waits until command is complete before moving onto the next command
        """
        return await self.motor.set_position_wait_complete(
            position=position_val,
            velocity=0,
            accel_limit=self.accel_limit,
            velocity_limit=self.velocity_limit,
            watchdog_timeout=math.inf
        )

    async def setVelocity(self, velocity_val):
        """
        Sets the velocity of the motor
        :param velocity_val The velocity value in revolutions per second
        """
        return await self.motor.set_position(
            position=math.nan,
            velocity=velocity_val,
            accel_limit=self.accel_limit,
            velocity_limit=self.velocity_limit,
            watchdog_timeout=math.inf
        )
    
    async def setVelocityWaitComplete(self, velocity_val):
        """
        Moves to a velocity in revolutions
        Waits until command is complete before moving onto the next command
        """
        return await self.motor.set_position_wait_complete(
            position=math.nan,
            velocity=velocity_val,
            accel_limit=self.accel_limit,
            velocity_limit=self.velocity_limit,
            watchdog_timeout=math.inf
        )


    async def stop(self):
        """
        Stop the motor.
        """
        await self.motor.set_stop()
