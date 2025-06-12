import moteus
import asyncio
import math

"""
A swerve motor class

Defines all the functions required for motor movement using the moteus library.
"""
class SwerveMotor:
    def __init__(self,
                 motorID,
                 transport,
                 accel_limit=16.0,
                 velocity_limit=16.0,
                 watchdog_timeout=math.inf):
        """
        Constructs a swerve motor instance.

        :param motorID (int): Moteus controller ID.
        :param transport (Pi3HatRouter): Transport object.
        :param accel_limit (float): Acceleration limit in rev/s².
        :param velocity_limit (float): Velocity limit in rev/s.
        :param watchdog_timeout (float): Timeout before function stops running (if you don't know how this param works, better not touch it).
        """

        # Set the local properties to be accessible from within the class.
        self.accel_limit = accel_limit
        self.velocity_limit = velocity_limit
        self.watchdog_timeout = watchdog_timeout
        self.motor = moteus.Controller(id=motorID, transport=transport)

        # ALWAYS call stop to the motor when starting and ending a program.
        asyncio.run(self.motor.set_stop())

    @property
    async def pos(self):
        """
        Gives the current absolute motor position (relative to position 0).

        :return float: The current absolute motor position in revolutions.
        """

        # Query the motor for its current state
        result = await self.motor.set_position(query=True)

        # Extract the position from the result
        return result.values[moteus.Register.POSITION]

    @property
    async def velocity(self):
        """
        Gives the current velocity

        :return float: The current velocity of the motor in rev/s.
        """

        # Query the motor for its current state
        result = await self.motor.set_position(query=True)

        # Extract the position from the result
        return result.values[moteus.Register.VELOCITY]
    
    @property
    async def values(self):
        """
        Gives a list of properties exposed by the moteus library for reading or writing.
        The full list can be found here:
        https://github.com/mjbots/moteus/blob/main/lib/python/moteus/moteus.py#L149 (class code)
        https://github.com/mjbots/moteus/blob/main/docs/reference.md#a2b-registers (descriptors)
        
        :returns [any]: Array of Register object properties
        """
        result = await self.motor.set_position(query=True)

        return result.values

    async def setAngle(self, angle_deg, wait_time=0):
        """
        A position mode function.
        
        Move to a target angle in degrees.
        Returns boolean and retrived position after rotation

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().
        It is better if you implement this yourself IF you have more than 1 motor.
        
        :param angle_deg (float): An angle in degrees
        :param wait_time (float): The time to wait for the set_position function to complete.
        
        :return [boolean, float, any]: A completion boolean, position after the command has complete, set_position returned value
        """

        try:
            angle_rev = angle_deg / 360.0

            degAngle = await self.pos * 360

            if degAngle == None:
                raise TypeError(
                    "Degree angle in setAngle function returned as type None")

            adjustedAngle = angle_rev  # temp angle for now, add calculations in later

            command1 = await self.motor.set_position(
                position=(self.pos + adjustedAngle),
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=self.watchdog_timeout)

            asyncio.sleep(wait_time)

            return [True, self.pos, command1]
        except Exception as e:
            print(f"Error caught in setAngle function: {e}")
            return [False, None, None]

    async def addToCurrentPos(self, position_val, wait_time=0):
        """
        Move to a position in revolutions relative to current position.

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().
        It is better if you implement this yourself IF you have more than 1 motor.

        :param position_val (float): The position target to move to in revolutions.
        :param wait_time (float): The time to wait for the set_position function to complete.
        
        :return [boolean, float, any]: An array of 3 items, described down below.
        :return boolean: A boolean for execution, True if function has properly executed.
        :return float: The current position value after running the command.
        :return any: An object returned by the set_position function.
        """
        try:
            command1 = await self.motor.set_position(
                position=(position_val + self.pos),
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=self.watchdog_timeout)

            asyncio.sleep(wait_time)

            return [True, self.pos, command1]
        except Exception as e:
            print(f"Error caught in addToCurrentPosition function: {e}")
            return [False, None, None]

    async def setPos(self, position_val, wait_time):
        """
        A position mode function.

        Move to an absolute position in revolutions.

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().
        It is better if you implement this yourself IF you have more than 1 motor that you want to run.

        :param position_val (float): The position target to move to in revolutions.
        :param wait_time (float): The time to wait for the set_position function to complete.
        
        :return [boolean, float, any]: An array of 3 items, described down below.
        :return boolean: A boolean for execution, True if function has properly executed.
        :return float: The current position value after running the command.
        :return any: An object returned by the set_position function.
        """
        try:
            command1 = await self.motor.set_position(
                position=position_val,
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=self.watchdog_timeout)

            asyncio.sleep(wait_time)

            return [True, self.pos, command1]
        except Exception as e:
            print(f"Error caught in addToCurrentPosition function: {e}")
            return [False, None, None]

    async def setPosWaitComplete(self, position_val):
        """
        A position mode function.

        Moves to an absolute position in revolutions.
        Waits until command is complete before moving onto the next command.
        
        NOTE: This function cannot be overridden when called on, use it cautiously.
        Once called, no other motors can also run at the same time.

        :param position_val (float): The position target to move to to in revolutions.

        :return [boolean, float, any]: An array of 3 items, described down below.
        :return boolean: A boolean for execution, True if function has properly executed.
        :return float: The current position value after running the command.
        :return any: An object returned by the set_position function.
        """
        try:
            command1 = await self.motor.set_position_wait_complete(
                position=position_val,
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=self.watchdog_timeout)

            return [True, self.pos, command1]
        except Exception as e:
            print(f"Error caught in addToCurrentPosition function: {e}")
            return [False, None, None]

    async def setVelocity(self, velocity_val, wait_time=0):
        """
        A velocity control mode function.

        Sets the velocity of the motor in revolutions/sec.

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().
        It is better if you implement this yourself IF you have more than 1 motor that you want to run.

        
        :param velocity_val The velocity target in revolutions per second.
        :param wait_time (float): The time to wait for the set_position function to complete.
        
        :return [boolean, float, any]: An array of 3 items, described down below.
        :return boolean: A boolean for execution, True if function has properly executed.
        :return float: The current position value after running the command.
        :return any: An object returned by the set_position function.
        """
        try:
            command1 = await self.motor.set_position(
                position=math.nan,
                velocity=velocity_val,
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=self.watchdog_timeout)

            asyncio.sleep(wait_time)

            return [True, self.pos, command1]
        except Exception as e:
            print(f"Error caught in addToCurrentPosition function: {e}")
            return [False, None, None]

    async def setVelocityWaitComplete(self, velocity_val):
        """
        A velocity control mode function.

        Moves to a velocity in revolutions.
        Waits until command is complete before moving onto the next command.

        NOTE: This function cannot be overridden when called on, use it cautiously.
        Once called, no other motors can also run at the same time.

        :param position_val (float): The position target to move to to in revolutions.

        :return [boolean, float, any]: An array of 3 items, described down below.
        :return boolean: A boolean for execution, True if function has properly executed.
        :return float: The current position value after running the command.
        :return any: An object returned by the set_position function.
        """
        try:
            command1 = await self.motor.set_position_wait_complete(
                position=math.nan,
                velocity=velocity_val,
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=self.watchdog_timeout)

            return [True, self.pos, command1]
        except Exception as e:
            print(f"Error caught in addToCurrentPosition function: {e}")
            return [False, None, None]
        

    async def stop(self):
        """
        Stop the motor and clears all outstanding faults.
        """
        await self.motor.set_stop()