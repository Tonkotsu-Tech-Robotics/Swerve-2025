import asyncio
import moteus
import moteus_pi3hat
import math

async def main():
    transport = moteus_pi3hat.Pi3HatRouter(
        servo_bus_map = {
            1:[11,12]
        }
    )

    servos = {
        servo_id : moteus.Controller(id=servo_id, transport=transport)
        for servo_id in [11,12]
    }

    await transport.cycle([x.make_stop() for x in servos.values()])



    await transport.cycle([
        servo.make_position(
            position=math.nan,
            velocity=5,
            accel_limit=5,
            velocity_limit=10,
            watchdog_timeout=5,
        )
        for servo in servos.values()
    ])

    await asyncio.sleep(5)

    await transport.cycle([
        servo.make_position(
            position=math.nan,
            velocity=0,
            accel_limit=5,
            velocity_limit=10,
            watchdog_timeout=5,
        )
        for servo in servos.values()
    ])

    await transport.cycle([x.make_stop() for x in servos.values()])

if __name__ == '__main__':
    asyncio.run(main())