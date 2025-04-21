import asyncio
import moteus
# import the moteus pi 3 hat module
import moteus_pi3hat

async def main():
    transport = moteus_pi3hat.Pi3HatTransport()

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
    main()