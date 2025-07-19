import moteus
import moteus_pi3hat
import asyncio
import math

"""
A swerve motor class

Defines all the functions required for motor movement using the moteus library.
"""
class SwerveMotor:
    def __init__(self,
                 motorID: int,
                 transport: moteus_pi3hat.Pi3HatRouter,
                 accel_limit: float=20.0,
                 velocity_limit: float=20.0,
                 watchdog_timeout: float=0.5):
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

    @property
    async def position(self):
        """
        Gives the current absolute motor position (relative to position 0).

        :return float: The current absolute motor position in revolutions.
        """

        # Query the motor for its current state
        result = await self.motor.set_position(position=math.nan, query=True)

        print(f"Motor {self.motor.id} position register is of type {type(result.values[moteus.Register.POSITION])}")

        # Extract the position from the result
        return result.values[moteus.Register.POSITION]

    @property
    async def velocity(self) -> float:
        """
        Gives the current velocity

        :return float: The current velocity of the motor in rev/s.
        """

        # Query the motor for its current state
        result = await self.motor.set_position(position=math.nan, query=True)

        # Extract the position from the result
        return result.values[moteus.Register.VELOCITY]
    
    @property
    async def values(self) -> list:
        """
        Gives a list of properties exposed by the moteus library for reading or writing.
        The full list can be found here:
        https://github.com/mjbots/moteus/blob/main/lib/python/moteus/moteus.py#L149 (class code)
        https://github.com/mjbots/moteus/blob/main/docs/reference.md#a2b-registers (descriptors)
        
        :returns [any]: A list of Register object properties
        """
        result = await self.motor.set_position(query=True)

        return result.values

    async def setAngle(self, angle_deg: float, transport: moteus.Transport) -> bool:
        """
        A position mode function.
        
        Move to a target angle in degrees.
        Returns boolean and retrived position after rotation

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().
        It is better if you implement this yourself IF you have more than 1 motor.

        :param angle_deg (float): An angle in degrees to move to. Will be converted to revolutions. Motor will move  to this angle relative to its current position, and with a max speed of what is set in self.velocity_limit in rev/s. It will reach this max speed in self.accel_limit in rev/s².
        :param transport (moteus.Transport): The transport object to use for communication. Should be the same transport used in every motor.

        :return bool: True if the angle was set successfully, False otherwise.
        """

        try:
            angle_rev = angle_deg / 360.0

            # degAngle = await self.position * 360

            # if degAngle == None:
            #     raise TypeError(
            #         "Degree angle in setAngle function returned as type None")

            # adjustedAngle = angle_rev  # temp angle for now, add calculations in later

            await transport.cycle([self.motor.make_position(
                position=angle_rev,
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=self.watchdog_timeout
            )])

            return True
        except Exception as e:
            print(f"Error caught in setAngle function: {e}")
            await self.emergency_stop(f"Error caught in setAngle function: {e}")
            return False

    async def addToCurrentPos(self, position_val: float, transport: moteus.Transport) -> bool:
        """
        Move to a position in revolutions relative to current position.

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().
        It is better if you implement this yourself IF you have more than 1 motor.

        :param position_val (float): The position target to move to in revolutions. This will be added to the current position of the motor, not set as an absolute position.
        :param transport (moteus.Transport): The transport object to use for communication. Should be the same transport used in every motor.

        :return bool: True if the position was set successfully, False otherwise.
        """
        try:
            await transport.cycle([self.motor.make_position(
                position=(position_val + self.position),
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=self.watchdog_timeout)
            ])

            return True
        except Exception as e:
            print(f"Error caught in addToCurrentPosition function: {e}")
            await self.emergency_stop(f"Error caught in addToCurrentPosition function: {e}")
            return False

    async def setPosition(self, position_val: float, transport: moteus.Transport ) -> bool:
        """
        A position mode function.

        Move to an absolute position in revolutions.

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().
        It is better if you implement this yourself IF you have more than 1 motor that you want to run.

        :param position_val (float): The position target to move to in revolutions.
        :param transport (moteus.Transport): The transport object to use for communication.

        :return bool: True if the position was set successfully, False otherwise.
        """
        try:
            await transport.cycle([self.motor.make_position(
                position=position_val,
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=self.watchdog_timeout)
            ])

            return True
        except Exception as e:
            print(f"Error caught in setPos function: {e}")
            await self.emergency_stop(f"Error caught in setPos function: {e}")
            return False

    async def setVelocity(self, velocity_val: float, transport: moteus.Transport) -> bool:
        """
        A velocity control mode function.

        Sets the velocity of the motor in revolutions/sec.

        NOTE: If the wait_time parameter is not set, set_position will not fully run unless you manually implement asyncio.sleep().
        It is better if you implement this yourself IF you have more than 1 motor that you want to run.

        
        :param velocity_val The velocity target in revolutions per second.

        :return bool: True if the velocity was set successfully, False otherwise.
        """

        try:
            await transport.cycle([self.motor.make_position(
                position=math.nan,
                velocity=velocity_val,
                accel_limit=self.accel_limit,
                velocity_limit=self.velocity_limit,
                watchdog_timeout=self.watchdog_timeout)
            ])

            return True
        except Exception as e:
            print(f"Error caught in setVelocity function: {e}")
            await self.emergency_stop(f"Error caught in setVelocity function: {e}")
            return False

    async def stop(self) -> None:
        """
        Stop the motor and clears all outstanding faults.
        """
        await self.motor.set_stop()

    async def emergency_stop(self, error_message: str) -> None:
        """
        Stops the motor, clears all outstanding faults.
        Exits out of the program with a critical error.

        :params error_message (any): An error message to be displayed before quitting the program.
        """
        await self.motor.set_stop()

        if error_message is not None:
            print(f"A critical error has occurred and the program needs to quit. Error message: {error_message}")
        else:
            print("An unknown error has occurred and the program needs to quit.")

        exit(1)