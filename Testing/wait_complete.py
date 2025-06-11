import asyncio
import moteus_pi3hat
import moteus
import math

# Run two motors at the same time

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
    motor2 = moteus.Controller(id=12)
    
    await motor1.set_stop()
    await motor2.set_stop()

    await control_motor(motor1, position=math.nan, velocity=10, velocity_limit=5.0, accel_limit=5.0)
    await control_motor(motor2, position=math.nan, velocity=10, velocity_limit=5.0, accel_limit=5.0)

    # response1 = await motor1.set_position(position=math.nan, velocity=10, velocity_limit=15.0, accel_limit=5.0, maximum_torque=1, watchdog_timeout=math.inf)
    # response2 = await motor2.set_position(position=math.nan, velocity=10, velocity_limit=15.0, accel_limit=5.0, maximum_torque=1, watchdog_timeout=math.inf)

    await asyncio.sleep(10)

    # print(response1)
    # print(response2)

    await motor1.set_stop()
    await motor2.set_stop()
if __name__ == '__main__':
    asyncio.run(main())