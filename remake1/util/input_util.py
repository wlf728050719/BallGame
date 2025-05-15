class InputUtil:
    def __init__(self, allowed_keys):
        self.allowed_keys = set(allowed_keys)   #支持的输入按键
        self.pressed_keys = set()   #所有按下
        self.released_keys = set()  #所有释放
        self.just_pressed = set()   #最新按下
        self.just_released = set()  #最新释放
    def press(self, key):
        if key in self.allowed_keys:
            if key not in self.pressed_keys:
                self.pressed_keys.add(key)
                self.just_pressed.add(key)
            if key in self.released_keys:
                self.released_keys.remove(key)
    def release(self, key):
        if key in self.allowed_keys:
            if key in self.pressed_keys:
                self.pressed_keys.remove(key)
                self.just_released.add(key)
            self.released_keys.add(key)
    def is_pressed(self, key):
        return key in self.pressed_keys
    def is_released(self, key):
        return key in self.released_keys
    def was_just_pressed(self, key):
        return key in self.just_pressed
    def was_just_released(self, key):
        return key in self.just_released
    def update(self):
        self.just_pressed.clear()
        self.just_released.clear()
    def get_pressed_keys(self):
        return self.pressed_keys.copy()