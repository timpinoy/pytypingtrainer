import pyray as pr
from typing import List
from settings import *

class MenuMode:
    def __init__(self) -> None:
        self._time_options: List[int] = [30, 60, 120, 180]
        self._selected_time: int = 0
        self.start_typing: bool = False
    
    def update(self) -> None:
        if pr.is_key_pressed(pr.KeyboardKey.KEY_LEFT):
            self._change_selected_time(self._selected_time - 1)
        if pr.is_key_pressed(pr.KeyboardKey.KEY_RIGHT):
            self._change_selected_time(self._selected_time + 1)
        if pr.is_key_pressed(pr.KeyboardKey.KEY_ENTER):
            self.start_typing = True

    def draw(self) -> None:
        text = "select the number of seconds (arrow keys)"
        text_width = pr.measure_text(text, FONT_SIZE)
        text_start_pos = (WIN_WIDTH - text_width) // 2
        pr.draw_text(text, text_start_pos, 170, FONT_SIZE, FONT_COLOR)

        time_str = " ".join(str(i) for i in self._time_options)
        text_width = pr.measure_text(" ".join(str(i) for i in self._time_options), FONT_SIZE)
        text_start_pos = (WIN_WIDTH - text_width) // 2
        pr.draw_text(time_str, text_start_pos, 200, FONT_SIZE, FONT_COLOR)

        selected_time_str = str(self._time_options[self._selected_time])
        line_width = pr.measure_text(selected_time_str, FONT_SIZE)
        if self._selected_time == 0:
            previous_times_width = 0
        else:
            previous_times_str = " ".join(str(i) for i in self._time_options[:self._selected_time]) + " "
            # not sure why this is off and has to be corrected by 4
            previous_times_width = pr.measure_text(previous_times_str, FONT_SIZE) + 4
        line_start_x = text_start_pos + previous_times_width
        pr.draw_line(line_start_x, 234, line_start_x + line_width, 234, pr.RED)

        text = "press enter to start"
        text_width = pr.measure_text(text, FONT_SIZE)
        text_start_pos = (WIN_WIDTH - text_width) // 2
        pr.draw_text(text, text_start_pos, 240, FONT_SIZE, FONT_COLOR)

    def _change_selected_time(self, time_index: int) -> None:
        if time_index <= 0:
            self._selected_time = 0
        elif time_index >= len(self._time_options):
            self._selected_time = len(self._time_options) - 1
        else:
            self._selected_time = time_index

    def get_selected_time(self) -> int:
        return self._time_options[self._selected_time]