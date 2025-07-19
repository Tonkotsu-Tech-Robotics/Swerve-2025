import asyncio
import moteus
import moteus_pi3hat
import math
from Utils.Controller import Controller
from Swerve.SwerveModule import SwerveModule
from wpimath.geometry import Rotation2d
from wpimath.kinematics import SwerveModuleState
# from Swerve.SwerveMotor import SwerveMotor


async def main():
    transport = moteus_pi3hat.Pi3HatRouter(
        servo_bus_map = {
            1:[11,12]
        }
    )


    controller = Controller()
    swerve_module = SwerveModule(drive_id=11, steer_id=12, transport=transport)

    await swerve_module.stop()
    # Example usage of named bindings:
    #   LEFT_X, LEFT_Y: left joystick axes
    #   RIGHT_X, RIGHT_Y: right joystick axes
    #   BUTTON_A: A button, etc.
    # See Controller.py for full mapping.
    while True:
        try:
            # await transport.cycle([
            #     servos[11].make_position(
            #         position=math.nan,
            #         # Use named constant for left joystick Y axis, scaled to -10..10
            #         velocity=controller.get_axis(Controller.LEFT_Y) * 15,
            #         accel_limit=30,
            #         velocity_limit=15,
            #         watchdog_timeout=5,
            #     )
            # ])

            # await transport.cycle([
            #     servos[12].make_position(
            #         position=math.nan,
            #         # Use named constant for left joystick Y axis, scaled to -10..10
            #         velocity=controller.get_axis(Controller.LEFT_X) * 15,
            #         accel_limit=30,
            #         velocity_limit=15,
            #         watchdog_timeout=5,
            #     )
            # ])
            # # Example: check if A button is pressed
            # if controller.get_button(Controller.BUTTON_A):
            #     print("Button A pressed!")

            #ttest swerve module code
            left_x = controller.get_axis(Controller.LEFT_X)
            left_y = controller.get_axis(Controller.LEFT_Y)

            # use setstate and getstate methods from SwerveModule
            # Example: set the speed and angle of a swerve module

            await swerve_module.setState(SwerveModuleState(left_y, Rotation2d.fromDegrees(left_x * 180)), transport)
            

        except KeyboardInterrupt:
            print("Program interrupted by user. Stopping all modules.")
            await swerve_module.stop()
            exit(0)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            await swerve_module.stop()
    


if __name__ == '__main__':
    asyncio.run(main())
