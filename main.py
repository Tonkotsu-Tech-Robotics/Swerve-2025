import asyncio
from swerve.SwerveDrive import SwerveDrive

async def main(swerve_drive: SwerveDrive = None):
    while True:
        await swerve_drive.testFunction()  # Call the test function in SwerveDrive
        
        await asyncio.sleep(0.005)  # Sleep for 5 milliseconds

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