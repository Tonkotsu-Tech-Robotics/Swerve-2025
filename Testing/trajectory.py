import asyncio
import moteus
import time

async def main():
    qr = moteus.QueryResolution()
    # Sets 
    qr._extra = {
        moteus.Register.CONTROL_POSITION : moteus.F32,
        moteus.Register.CONTROL_VELOCITY : moteus.F32,
        moteus.Register.CONTROL_TORQUE : moteus.F32,
        moteus.Register.POSITION_ERROR : moteus.F32,
        moteus.Register.VELOCITY_ERROR : moteus.F32,
        moteus.Register.TORQUE_ERROR : moteus.F32,
    }

    controller = moteus.Controller(
        id=1,
        query_resolution = qr
    )

    await controller.set_stop()

    current_pos = 5

    for i in range(10):
        # Alternates between position 5 and -5 every 3 seconds.
        if (current_pos == -5):
            current_pos = 5
        else:
            current_pos = -5
        

        # Accerlation and velocity can be set in tview using
        # `servo.default_accel_limit` and `servod.default_velocity_limit`
        # Regardless of setting, override them in case anything bad happens :D
        results = await controller.set_position_wait_complete(
            position=current_pos,
            velocity=0.0,
            accel_limit=8.0,
            velocity_limit=8.4079,
            query=True
        )

        print(results)

if __name__ == '__main__':
    asyncio.run(main())