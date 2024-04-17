import pyray as pr
import math
import os

from settings import *
from typing import List
from typemode import TypeMode

class App:
    def __init__(self) -> None:
        pr.init_window(WIN_WIDTH, WIN_HEIGHT, "PY Typing Trainer")
        pr.set_target_fps(TARGET_FPS)
        self.delta_time: float = 0.0
        self.round_time: float = 60.0
        self.remaining_time: float = self.round_time
        self.type_mode: TypeMode = TypeMode()
    
    def update(self) -> None:
        self.delta_time = pr.get_frame_time()
        self.remaining_time -= self.delta_time
        if self.remaining_time < 0:
           self.remaining_time = self.round_time 
           self.type_mode.reset()
        self.type_mode.update()
    
    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(BG_COLOR)
        pr.draw_fps(10, 10)
        pr.draw_text(f"{math.ceil(self.remaining_time)}", 20, 80, FONT_SIZE, FONT_COLOR)
        self.type_mode.draw()
        pr.end_drawing()

    def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
        pr.close_window()


if __name__ == "__main__":
    app = App()
    app.run()