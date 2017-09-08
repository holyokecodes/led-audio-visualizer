import keyboard

def test():
    print("space")
    
keyboard.add_hotkey('space', lambda: test())

while True:
    pass
