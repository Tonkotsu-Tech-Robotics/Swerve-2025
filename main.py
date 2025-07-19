import asyncio
from Swerve.SwerveDrive import SwerveDrive

async def main(swerve_drive: SwerveDrive = None):
    while True:
        await swerve_drive.setMotorSpeeds()

if __name__ == '__main__':
    # Initialize SwerveDrive instance
    swerve_drive = SwerveDrive()

    try:
        asyncio.run(main(swerve_drive))
    except KeyboardInterrupt:
        print("Program interrupted by user. Stopping all modules.")
        asyncio.run(swerve_drive.stop())
        exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        asyncio.run(swerve_drive.stop())