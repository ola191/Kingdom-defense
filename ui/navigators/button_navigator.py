import pygame

class Navigator:
    def __init__(self, elements):
        self.elements = elements
        self.current_index = 0
        self.brightness_delta = 20
        self.old_index = self.current_index

    def update_selection(self):
        for i, element in enumerate(self.elements):
            element.selected = (i == self.current_index)

    def get_current(self):
        return self.elements[self.current_index]

    def get_buttons(self):
        return self.elements

    def next(self):
        self._update_index((self.current_index + 1) % len(self.elements))

    def previous(self):
        self._update_index((self.current_index - 1) % len(self.elements))

    def _update_index(self, new_index):
        self.current_index = new_index

        old_button = self.elements[self.old_index]
        old_button.selected = False
        old_button.change_brightness(100)

        self.old_index = self.current_index

        new_button = self.elements[self.current_index]
        new_button.selected = True
        new_button.change_brightness(80)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.current_index = (self.current_index + 1) % len(self.elements)
                self.update_selection()
            elif event.key == pygame.K_UP:
                self.current_index = (self.current_index - 1) % len(self.elements)
                self.update_selection()
            elif event.key == pygame.K_RETURN:
                return self.elements[self.current_index].action()