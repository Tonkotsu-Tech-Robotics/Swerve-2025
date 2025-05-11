import asyncio
import moteus_pi3hat
from Test_motor import TestMotor

async def main():
    transport = moteus_pi3hat.Pi3HatRouter(
        servo_bus_map={
            1: [11],  # Bus 1 → Motor ID 11
        },
    )

    motor = TestMotor(motorID=11, transport=transport, accel_limit=2.0)


    await motor.setSpeed(1.0)

    await asyncio.sleep(5)


    await motor.stop()

if __name__ == '__main__':
    asyncio.run(main())
