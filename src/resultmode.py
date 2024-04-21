import pyray as pr
from typing import Dict
from settings import *
from typemode import TypeMode

class ResultMode():
    def __init__(self, result: Dict) -> None:
        self.back_to_menu = False
        self._typing_result = result

    def update(self):
        if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            self.back_to_menu = True

    def draw(self):
        pr.draw_text(f'Entered Characters: {self._typing_result["entered_count"]}', 20, 40, FONT_SIZE, FONT_COLOR)
        pr.draw_text(f'WPM: {self._typing_result["wpm"]}', 20, 80, FONT_SIZE, FONT_COLOR)
        pr.draw_text(f'Raw WPM: {self._typing_result["raw_wpm"]}', 20, 120, FONT_SIZE, FONT_COLOR)
        pr.draw_text(f'Accuracy: {self._typing_result["acc"]:.2f}', 20, 160, FONT_SIZE, FONT_COLOR)
        text = "press enter to go back to the menu"
        text_width = pr.measure_text(text, FONT_SIZE)
        text_start_pos = (WIN_WIDTH - text_width) // 2
        pr.draw_text(text, text_start_pos, 240, FONT_SIZE, FONT_COLOR)