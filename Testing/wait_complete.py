import asyncio
import moteus_pi3hat
import moteus

async def main():
    # Construct a default controller at id 1.
    transport = moteus_pi3hat.Pi3HatRouter(
        servo_bus_map={
            1: [11],
            2: [12]
        }
    )

    servos = {
        servo_id: moteus.Controller(id=servo_id, tranposrt=transport)
        for servo_id in [11, 12]
    }

    # Clear any outstanding faults.
    await transport.cycle([x.make_stop() for x in servos.values()])

    # This will periodically command and poll the controller until
    # the target position achieves the commanded value.

    initial_pos=120
    final_pos=0 # should be equal to 0

    commands = [
        servos[11].set_position_wait_complete(
            position=initial_pos, 
            accel_limit=8.0,
            velocity_limit=12.0
        ),
        servos[12].set_position_wait_complete(
            position=initial_pos, 
            accel_limit=8.0,
            velocity_limit=12.0
        ),
    ]

    results = await transport.cycle(commands)

    print(", ".join(
        f"({result.arbitration_id})" +
        f"{result.values[moteus.Register.POSITION]}" +
        f"{result.values[moteus.Register.VELOCITY]}"
        for result in results
    ))

    # Then go back to zero, and eventually try again.
    commands = [
        servos[11].set_position_wait_complete(
            position=final_pos, 
            accel_limit=8.0,
            velocity_limit=12.0
        ),
        servos[12].set_position_wait_complete(
            position=final_pos, 
            accel_limit=8.0,
            velocity_limit=12.0
        ),
    ]

    print(", ".join(
        f"({result.arbitration_id})" +
        f"{result.values[moteus.Register.POSITION]}" +
        f"{result.values[moteus.Register.VELOCITY]}"
        for result in results
    ))

if __name__ == '__main__':
    asyncio.run(main())