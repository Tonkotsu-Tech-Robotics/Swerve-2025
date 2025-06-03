import asyncio
import moteus

async def main():
    # Construct a default controller at id 1.
    c = moteus.Controller()

    # Clear any outstanding faults.
    await c.set_stop()

    # This will periodically command and poll the controller until
    # the target position achieves the commanded value.

    result = await c.set_position_wait_complete(
        position=0.5, accel_limit=2.0)
    print(result)

    # Then go back to zero, and eventually try again.
    result = await c.set_position_wait_complete(
        position=0.0, accel_limit=2.0)
    print(result)


if __name__ == '__main__':
    asyncio.run(main())