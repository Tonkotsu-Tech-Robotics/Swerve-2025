import asyncio
import moteus
# import the moteus pi 3 hat module
import moteus_pi3hat

async def main():
    transport = moteus_pi3hat.Pi3HatRouter(   
    servo_bus_map = {
            1:[11],
            2:[12],
            3:[13],
            4:[14],
        },
    )

    while True:
        # Create a moteus client with the transport
        client = moteus.MoteusClient(transport)

        # Send a command to the moteus controller
        response = await client.command(0, 0, 0, 0)

        # Print the response
        print(response)

        # Sleep for a while before sending the next command
        await asyncio.sleep(1)

if __name__ == '__main__':
    asyncio.run(main())