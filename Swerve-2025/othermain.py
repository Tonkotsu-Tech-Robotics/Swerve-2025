import asyncio
import moteus

async def main():
    # transport = moteus_pi3hat.Pi3HatRouter(
    #     servo_bus_map={
    #         1: [1],  # Bus 1 → Motor ID 1
    #     },
    # )
    # print("It got here")

    motor = moteus.Controller()

    # Stop motors if fault detected
    await motor.set_stop()

    # Spin motor at 1 m/s with a max acceleration of 2 rev/s²
    state = await motor.set_position(
        position=0.0,  # Position in revolutions
        velocity=1.0,  # Velocity in revolutions per second
        accel_limit=2.0,  # Acceleration limit in rev/s²
        query=True  # Wait for the command to complete
    )
    print("Motor is spinning at 1 m/s, current state is: ")
    print(state)

    await asyncio.sleep(5)

    await motor.set_stop()  # Stop the motor
    print("Motor stopped")
    print("Position: " + str(state.values[moteus.Register.POSITION]))  # Get the current position

if __name__ == '__main__':
    asyncio.run(main())