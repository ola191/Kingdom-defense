class ButtonNavigator:
    def __init__(self, buttons):
        self.buttons = buttons
        self.current_index = 0
        self.brightness_delta = 20
        self.old_index = self.current_index

    def get_current(self):
        return self.buttons[self.current_index]

    def get_buttons(self):
        return self.buttons

    def next(self):
        self._update_index((self.current_index + 1) % len(self.buttons))

    def previous(self):
        self._update_index((self.current_index - 1) % len(self.buttons))

    def _update_index(self, new_index):
        self.current_index = new_index

        old_button = self.buttons[self.old_index]
        old_button.change_brightness(old_button.brightness + self.brightness_delta)

        self.old_index = self.current_index
        self.current_index = new_index

        new_button = self.buttons[self.current_index]
        new_button.change_brightness(new_button.brightness - self.brightness_delta)
