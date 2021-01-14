import keyboard

event = keyboard.record("esc")
for a in event:
    print(a)