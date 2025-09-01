import asyncio
from Swerve.SwerveDrive import SwerveDrive

async def main(swerve_drive: SwerveDrive = None):
    await swerve_drive.initialize_modules()
    speeds = [0.0, 0.0, 0.0]
    while True:
        speeds = await swerve_drive.getControllerSpeeds()
        await swerve_drive.set_drive_speeds(speeds[0], speeds[1], speeds[2], False)

        
    
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