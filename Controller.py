import pygame

class Controller:
    """
    Controller abstraction for gamepad/joystick using pygame.

    Axis and button mappings are provided as named constants for intuitive use:

    Axes:
        LEFT_X, LEFT_Y: Left joystick horizontal/vertical
        RIGHT_X, RIGHT_Y: Right joystick horizontal/vertical

    Buttons:
        BUTTON_A, BUTTON_B, BUTTON_X, BUTTON_Y, etc.

    Example usage:
        controller = Controller()
        x = controller.get_axis(Controller.LEFT_X)
        if controller.get_button(Controller.BUTTON_A):
            ...
    """

    # Common Xbox/Logitech mappings (may vary by controller)
    LEFT_X = 0
    LEFT_Y = 1
    RIGHT_X = 3
    RIGHT_Y = 4
    LEFT_TRIGGER = 2
    RIGHT_TRIGGER = 5

    BUTTON_A = 0
    BUTTON_B = 1
    BUTTON_X = 2
    BUTTON_Y = 3
    BUTTON_LB = 4
    BUTTON_RB = 5
    BUTTON_BACK = 6
    BUTTON_START = 7
    BUTTON_LEFT_STICK = 8
    BUTTON_RIGHT_STICK = 9

    def __init__(self):
        pygame.init()
        self.joystick = None
        self._initialize_joystick()

    def _initialize_joystick(self):
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            try:
                self.joystick.rumble(0, 0, 1000)
            except Exception:
                pass
            print(f"Joystick initialized: {self.joystick.get_name()}")
        else:
            print("No joystick found.")

    def get_axis(self, axis):
        """Get the value of the specified axis (use named constants)."""
        if self.joystick:
            pygame.event.pump()  # Ensure state is updated
            return self.joystick.get_axis(axis)
        return 0.0

    def get_button(self, button):
        """Get the state of the specified button (use named constants)."""
        if self.joystick:
            pygame.event.pump()
            return self.joystick.get_button(button)
        return False