# PyGame_XboxController
Handles XboxController input events with the pygame library.


# How to use

```python
from xbox_controller import Controller

con = Controller()

# functions to connect
def on_A_press():
    print("A button pressed")
def on_A_release():
    print("A button released")
def on_Lstick_up():
    print("Left stick moved up")
def on_Lstick_down():
    print("Left stick moved down")
def on_Lstick_ud_center():
    print("Left stick ud centered")

# connect to joystick events
con.button_press['A'].connect(on_A_press)
con.button_release['A'].connect(on_A_release)

con.stick_move['Lstick_up'].connect(on_Lstick_up)
con.stick_move['Lstick_down'].connect(on_Lstick_down)
con.stick_move['Lstick_ud_center'].connect(on_Lstick_ud_center)

# detect events
while True:
    con.get_events()
```
