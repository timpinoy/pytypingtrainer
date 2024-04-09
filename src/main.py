import pyray as pr
import cffi as cffi
import math
import os

from wordlist import WordList

def load_words() -> WordList:
    filepath = os.path.abspath(os.path.join(
        os.path.dirname( __file__ ), 
        "..", 
        "resources", 
        "languages", 
        "english.json"
        ))
    return WordList(filepath)

def main():

    wl: WordList = load_words()
    
    screen_width: int = 800
    screen_height: int = 600
    target_fps: int = 60
    word_time: float = 10.0
    remaining_word_time: float = word_time
    current_word: str = wl.get_random_word()

    pr.init_window(screen_width, screen_height, "PY Typing Trainer")

    pr.set_target_fps(target_fps)

    # main loop
    while not pr.window_should_close():
        #update
        remaining_word_time -= pr.get_frame_time()
        if remaining_word_time < 0:
           remaining_word_time = word_time 
           current_word = wl.get_random_word()

        # draw
        pr.begin_drawing()

        pr.clear_background(pr.LIGHTGRAY)

        pr.draw_fps(10, 10)

        pr.draw_text(f"{current_word}", 10, 40, 20, pr.BLACK)
        pr.draw_text(f"{math.ceil(remaining_word_time)}", 10, 60, 20, pr.BLACK)

        # end draw
        pr.end_drawing()

    # de-initialization
    pr.close_window()


main()