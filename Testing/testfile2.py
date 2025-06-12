import asyncio
import moteus_pi3hat
import pygame
import moteus
import math

# Run two motors at the same time

pygame.init()
pygame.joystick.init()
JOYSTICK_DEADZONE = 0.1
OUTPUT_RANGE_MIN = -10
OUTPUT_RANGE_MAX = -10

if pygame.joystick.get_count() == 0:
    print("Error: No joystick connected.")
    exit(1)

joystick = pygame.joystick.Joystick(0)
joystick.init()
print(f"Initialized Joystick: {joystick.get_name()}")

LEFT_STICK_Y_AXIS = 1

async def stop_motor(motor):
    await motor.set_stop()

async def control_motor(motor, position, velocity, velocity_limit=5.0, accel_limit=5.0):
    await motor.set_position(position=position, velocity=velocity, velocity_limit=velocity_limit, accel_limit=accel_limit, maximum_torque=0.5, watchdog_timeout=math.inf)


async def main():
    # Construct a default controller at id 1.
    transport = moteus_pi3hat.Pi3HatRouter(
        servo_bus_map={
            1: [11, 12],
        }
    )

    # controllers = {x: moteus.Controller(x, query_resolution=qr) for x in SERVO_IDS}

    motor1 = moteus.Controller(id=11)
    # motor2 = moteus.Controller(id=12)
    
    await motor1.set_stop()
    # await motor2.set_stop()

    while True:
        raw_y_axis = -1 * joystick.get_axis(LEFT_STICK_Y_AXIS)

        mapped_y_axis = 0.0

        if abs(raw_y_axis) > JOYSTICK_DEADZONE:
            mapped_y_axis = raw_y_axis * OUTPUT_RANGE_MAX

        await control_motor(motor1, position=math.nan, velocity=mapped_y_axis, velocity_limit=15.0, accel_limit=5.0)
        # await control_motor(motor2, position=math.nan, velocity=mapped_y_axis, velocity_limit=15.0, accel_limit=5.0)

        asyncio.sleep(0.05)

if __name__ == '__main__':
    asyncio.run(main())