import asyncio
import math
import moteus
import moteus_pi3hat

async def main():
    transport = moteus_pi3hat.Pi3HatRouter(
        servo_bus_map = {
            1:[11, 12],
        }
    )

    c1 = moteus.Controller(id = 11),
    c2 = moteus.Controller(id = 12)

    while True:
        print(await transport.cycle(
            c1.make_position(position=math.nan, query=True),
            c2.make_position(position=math.nan, query=True),
        ))

asyncio.run(main())