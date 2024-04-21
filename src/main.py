import pyray as pr
from settings import *
from typing import List
from menumode import MenuMode
from typemode import TypeMode

class App:
    def __init__(self) -> None:
        pr.init_window(WIN_WIDTH, WIN_HEIGHT, "PY Typing Trainer")
        pr.set_target_fps(TARGET_FPS)
        self._current_mode = MenuMode()
    
    def update(self) -> None:
        self._current_mode.update()
        if isinstance(self._current_mode, MenuMode):
            if self._current_mode.start_typing:
                self._current_mode = TypeMode(self._current_mode.get_selected_time())
   
    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(BG_COLOR)
        pr.draw_fps(10, 10)
        self._current_mode.draw()
        pr.end_drawing()

    def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
        pr.close_window()


if __name__ == "__main__":
    app = App()
    app.run()