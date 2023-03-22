import keyboard
import time 

while True:
    if keyboard.is_pressed('w'):
        print('Forward')
    elif keyboard.is_pressed('s'):
        print('Backward')
    elif keyboard.is_pressed('a'):
        print('Left')
    elif keyboard.is_pressed('d'):
        print('Right')
    elif keyboard.is_pressed('del'):
        print('del')
    elif keyboard.is_pressed('q'):
        print('Quit!')
        break
