import pygame

class Controller:
    def __init__(self):
        pygame.init()
        self.joystick = None
        self._initialize_joystick()

    def _initialize_joystick(self):
        if pygame.joystick.get_count() > 0:
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()
            self.joystick.rumble(0, 0, 1000)
            print(f"Joystick initialized: {self.joystick.get_name()}")
        else:
            print("No joystick found.")

    def get_axis(self, axis):
        if self.joystick:
            return self.joystick.get_axis(axis)
        return 0.0

    def get_button(self, button):
        if self.joystick:
            return self.joystick.get_button(button)
        return False# Process event queue