import asyncio
import moteus
import moteus_pi3hat
from Swerve.SwerveMotor import SwerveMotor

async def main():
    transport = moteus_pi3hat.Pi3HatRouter()

    motor = SwerveMotor(motorID=11, transport=transport)

    await motor.setVelocity(10.0)

    await asyncio.sleep(10)

    await motor.stop()

if __name__ == '__main__':
    asyncio.run(main())