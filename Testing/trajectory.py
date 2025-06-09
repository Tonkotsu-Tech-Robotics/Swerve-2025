import asyncio
import moteus
import time

async def main():
    controller = moteus.Controller(
        id=2,
    )

    await controller.set_stop()

    current_pos = 100

    for i in range(10):
        # Alternates between position 5 and -5 every 3 seconds.
        if (current_pos == -100):
            current_pos = 100
        else:
            current_pos = -100
        

        # Accerlation and velocity can be set in tview using
        # `servo.default_accel_limit` and `servod.default_velocity_limit`
        # Regardless of setting, override them in case anything bad happens :D
        results = await controller.set_position_wait_complete(
            position=current_pos,
            velocity=0.0,
            accel_limit=8.0,
            velocity_limit=8,
            query=True
        )

        print(results)

if __name__ == '__main__':
    asyncio.run(main())