import moteus
from Swerve.SwerveMotor import SwerveMotor
import moteus_pi3hat
import asyncio

async def main():
    transport = moteus_pi3hat.Pi3HatRouter(
        servo_bus_map={
            1: [11, 12]
        }
    )

    swerve_motor = SwerveMotor(motorID=11, transport=transport)

    print(f"Motor {swerve_motor.motor.id} position: {await swerve_motor.position}")

if __name__ == "__main__":
    asyncio.run(main())