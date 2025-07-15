import asyncio
import moteus
import moteus_pi3hat
import math
from Controller import Controller

async def main():
    transport = moteus_pi3hat.Pi3HatRouter(
        servo_bus_map = {
            1:[11,12]
        }
    )
        
    servos = {
        servo_id : moteus.Controller(id=servo_id, transport=transport)
        for servo_id in [11,12]
    }

    await transport.cycle([x.make_stop() for x in servos.values()])


    controller = Controller()
    # Example usage of named bindings:
    #   LEFT_X, LEFT_Y: left joystick axes
    #   RIGHT_X, RIGHT_Y: right joystick axes
    #   BUTTON_A: A button, etc.
    # See Controller.py for full mapping.
    while True:
        try:
            await transport.cycle([
                servo.make_position(
                    position=math.nan,
                    # Use named constant for left joystick Y axis, scaled to -10..10
                    velocity=controller.get_axis(Controller.LEFT_Y) * 15,
                    accel_limit=30,
                    velocity_limit=15,
                    watchdog_timeout=5,
                )
                for servo in servos.values()
            ])
            # Example: check if A button is pressed
            if controller.get_button(Controller.BUTTON_A):
                print("Button A pressed!")
        except KeyboardInterrupt:
            print("Program interrupted by user. Stopping all modules.")
            await transport.cycle([x.make_stop() for x in servos.values()])
            exit(0)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            await transport.cycle([x.make_stop() for x in servos.values()])
    


if __name__ == '__main__':
    asyncio.run(main())
