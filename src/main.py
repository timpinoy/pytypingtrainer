import pyray as pr
import math
import os

from settings import *
from wordlist import WordList


class App:
    def __init__(self) -> None:
        pr.init_window(WIN_WIDTH, WIN_HEIGHT, "PY Typing Trainer")
        pr.set_target_fps(TARGET_FPS)
        self.delta_time: float = 0.0
        self.type_mode: TypeMode = TypeMode(self)
    
    def update(self) -> None:
        self.delta_time = pr.get_frame_time()
        self.type_mode.update()
    
    def draw(self) -> None:
        pr.begin_drawing()
        pr.clear_background(BG_COLOR)
        pr.draw_fps(10, 10)
        self.type_mode.draw()
        pr.end_drawing()

    def run(self) -> None:
        while not pr.window_should_close():
            self.update()
            self.draw()
        pr.close_window()

class TypeMode():
    def __init__(self, app: App) -> None:
        self._app = app
        self._load_word_list()
        self.word_time: float = 15.0
        self.remaining_word_time: float = self.word_time
        self.current_line: str = self.wl.get_word_line(40)

    def update(self) -> None:
        self.remaining_word_time -= self._app.delta_time
        if self.remaining_word_time < 0:
           self.remaining_word_time = self.word_time 
           self.current_line = self.wl.get_word_line(40)

    def draw(self) -> None:
        text_width = pr.measure_text(self.current_line, FONT_SIZE)
        text_start = (WIN_WIDTH - text_width) // 2
        pr.draw_text(f"{math.ceil(self.remaining_word_time)}", 20, 80, FONT_SIZE, FONT_COLOR)
        pr.draw_text(f"{self.current_line}", text_start, 140, FONT_SIZE, FONT_COLOR)
        pr.draw_line(text_start,
                     200, 
                     text_start + text_width,
                     200,
                     pr.BLACK)
    
    def _load_word_list(self) -> None:
        filepath = os.path.abspath(os.path.join(
            os.path.dirname( __file__ ), 
            *WORDS_FOLDER,
            "english.json"
            ))
        self.wl = WordList(filepath)




def load_words() -> WordList:
    filepath = os.path.abspath(os.path.join(
        os.path.dirname( __file__ ), 
        *WORDS_FOLDER,
        "english.json"
        ))
    return WordList(filepath)

def main():

    wl: WordList = load_words()
    
    word_time: float = 5.0
    remaining_word_time: float = word_time
    current_line: str = wl.get_word_line(50)
    int_char_pressed: int = 0

    pr.init_window(WIN_WIDTH, WIN_HEIGHT, "PY Typing Trainer")

    pr.set_target_fps(TARGET_FPS)

    # main loop
    while not pr.window_should_close():
        #update
        remaining_word_time -= pr.get_frame_time()
        if remaining_word_time < 0:
           remaining_word_time = word_time 
           current_line = wl.get_word_line(50)

        pr.measure_text("some text", pr.get_font_default().baseSize)
        
        int_char_pressed = pr.get_char_pressed()
        while int_char_pressed > 0:
            if int_char_pressed >= 32 and int_char_pressed < 125:
                print(chr(int_char_pressed))
            int_char_pressed = pr.get_char_pressed()

        # draw
        pr.begin_drawing()

        pr.clear_background(BG_COLOR)

        pr.draw_fps(10, 10)

        text_width = pr.measure_text(current_line, FONT_SIZE)
        text_start = (WIN_WIDTH - text_width) // 2
        pr.draw_text(f"{math.ceil(remaining_word_time)}", 20, 80, FONT_SIZE, FONT_COLOR)
        pr.draw_text(f"{current_line}", text_start, 140, FONT_SIZE, FONT_COLOR)
        pr.draw_line(text_start,
                     200, 
                     text_start + text_width,
                     200,
                     pr.BLACK)

        char = pr.get_char_pressed()

        # end draw
        pr.end_drawing()

    # de-initialization
    pr.close_window()


if __name__ == "__main__":
    app = App()
    app.run()