import asyncio
import moteus_pi3hat
import moteus

async def main():
    # Construct a default controller at id 1.
    transport = moteus_pi3hat.Pi3HatRouter(
        servo_bus_map={
            1: [11]
        }
    )

    c = moteus.Controller(id=1, transport=transport)

    # Clear any outstanding faults.
    await c.set_stop()

    # This will periodically command and poll the controller until
    # the target position achieves the commanded value.

    result = await c.set_position_wait_complete(
        position=500, 
        accel_limit=8.0,
        velocity_limit=8.0
    )
    
    print(result)


    # Then go back to zero, and eventually try again.
    result = await c.set_position_wait_complete(
       position=0, 
       accel_limit=8.0,
       velocity_limit=8.0
    )

    print(result)


if __name__ == '__main__':
    asyncio.run(main())