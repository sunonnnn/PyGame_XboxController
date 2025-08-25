import pygame

class Signal:
    def __init__(self):
        self._callback = None

    def connect(self, func):
        self._callback = func

    def emit(self, *args, **kwargs):
        if self._callback is not None:
            self._callback(*args, **kwargs)

"""class Signal:
    def __init__(self):
        self._callback = []

    def connect(self, func):
        self._callback.append(func)

    def disconnect(self, func):
        self._callback.remove(func)

    def clear(self):
        self._callback.clear()

    def emit(self, *args, **kwargs):
        for callback in self._callback:
            callback(*args, **kwargs)"""

class Controller:
    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        if pygame.joystick.get_count() == 0:
            raise RuntimeError("No controller detected.")
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()
        self.threshold = 0.5

        self.button_index = {
            0: "A",
            1: "B",
            2: "X",
            3: "Y",
            4: "View",
            5: "Xbox",
            6: "Menu",
            7: "Left_stick",
            8: "Right_stick",
            9: "LB",
            10: "RB",
            11: "D_UP",
            12: "D_DOWN",
            13: "D_LEFT",
            14: "D_RIGHT",
            15: "Share",
        }

        self.button_press   = {name: Signal() for _, name in self.button_index.items()}
        self.button_release = {name: Signal() for _, name in self.button_index.items()}

        self.stick_move = {
            "Lstick_up": Signal(),
            "Lstick_down": Signal(),
            "Lstick_left": Signal(),
            "Lstick_right": Signal(),
            "Lstick_lr_center": Signal(),
            "Lstick_ud_center": Signal(),
            "Rstick_up": Signal(),
            "Rstick_down": Signal(),
            "Rstick_left": Signal(),
            "Rstick_right": Signal(),
            "Rstick_lr_center": Signal(),
            "Rstick_ud_center": Signal(),
            "LT_pressed": Signal(),
            "LT_released": Signal(),
            "RT_pressed": Signal(),
            "RT_released": Signal()
        }

    def get_events(self):
        for event in pygame.event.get():
            # button press
            if event.type == pygame.JOYBUTTONDOWN:
                button_name = self.button_index.get(event.button)
                if button_name:
                    sig = self.button_press.get(button_name)
                    if sig:
                        sig.emit()
                        pygame.time.wait(10)  # Debounce delay
            elif event.type == pygame.JOYBUTTONUP:
                button_name = self.button_index.get(event.button)
                if button_name:
                    sig = self.button_release.get(button_name)
                    if sig:
                        sig.emit()

            if event.type == pygame.JOYAXISMOTION:
                axis = event.axis

                # left stick
                Lstick_lr = self.controller.get_axis(0)
                Lstick_ud = self.controller.get_axis(1)
                
                if axis in [0, 1]: 
                    if Lstick_lr <= -self.threshold:
                        self.stick_move['Lstick_left'].emit()
                    elif Lstick_lr >= self.threshold:
                        self.stick_move['Lstick_right'].emit()
                    else:
                        self.stick_move['Lstick_lr_center'].emit()
                    
                    if Lstick_ud <= -self.threshold:
                        self.stick_move['Lstick_up'].emit()
                    elif Lstick_ud >= self.threshold:
                        self.stick_move['Lstick_down'].emit()
                    else:
                        self.stick_move['Lstick_ud_center'].emit()

                # right stick
                Rstick_lr = self.controller.get_axis(2)
                Rstick_ud = self.controller.get_axis(3)

                if axis in [2, 3]:
                    if Rstick_lr <= -self.threshold:
                        self.stick_move['Rstick_left'].emit()
                    elif Rstick_lr >= self.threshold:
                        self.stick_move['Rstick_right'].emit()
                    else:
                        self.stick_move['Rstick_lr_center'].emit()
                    
                    if Rstick_ud <= -self.threshold:
                        self.stick_move['Rstick_up'].emit()
                    elif Rstick_ud >= self.threshold:
                        self.stick_move['Rstick_down'].emit()
                    else:
                        self.stick_move['Rstick_ud_center'].emit()
                
                # trigger
                LT = self.controller.get_axis(4)
                RT = self.controller.get_axis(5)

                if axis == 4:
                    if LT >= self.threshold:
                        self.stick_move['LT_pressed'].emit()
                    else:
                        self.stick_move['LT_released'].emit()
                if axis == 5:
                    if RT >= self.threshold:
                        self.stick_move['RT_pressed'].emit()
                    else:
                        self.stick_move['RT_released'].emit()
                
