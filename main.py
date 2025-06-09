import asyncio
import moteus_pi3hat
from SwerveMotor import TestMotor

async def main():
    transport = moteus_pi3hat.Pi3HatRouter()
    print("It got here")

    motor = TestMotor(motorID=1, transport=transport, accel_limit=2.0)

    await motor.setSpeed(1.0)

    await asyncio.sleep(5)


    await motor.stop()

if __name__ == '__main__':
    asyncio.run(main())
