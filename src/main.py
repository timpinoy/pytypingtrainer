import pyray as pr
import math
import os

from typing import List
from settings import *
from wordlist import WordList


class App:
    def __init__(self) -> None:
        pr.init_window(WIN_WIDTH, WIN_HEIGHT, "PY Typing Trainer")
        pr.set_target_fps(TARGET_FPS)
        self.delta_time: float = 0.0
        self.round_time: float = 60.0
        self.remaining_time: float = self.round_time
        self.type_mode: TypeMode = TypeMode(self)
    
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

class TypeMode():
    def __init__(self, app: App) -> None:
        self._app = app
        self._char_width = pr.measure_text(" ", FONT_SIZE)
        self._load_word_list()
        self._text_lines: List[TextLine] = []
        self.reset()

    def update(self) -> None:
        int_char = pr.get_char_pressed()
        while int_char > 0:
            if int_char >= 32 and int_char <= 125:
                input_char = chr(int_char)
                if self._text_lines[self._current_line].update(input_char):
                #if self._text_lines[self._current_line].input_char(input_char):
                    self._set_active_line(self._current_line + 1)
            int_char = pr.get_char_pressed()

        if pr.is_key_pressed(pr.KeyboardKey.KEY_BACKSPACE):
            #self._text_lines[self._current_line].backspace()
            self._text_lines[self._current_line].update("", is_backspace=True)

    def draw(self) -> None:
        for i in range(len(self._text_lines)):
            self._text_lines[i].draw(140 + (FONT_SIZE + 2) * i)
    
    def _load_word_list(self) -> None:
        filepath = os.path.abspath(os.path.join(
            os.path.dirname( __file__ ), 
            *WORDS_FOLDER,
            "english.json"
            ))
        self._world_list = WordList(filepath)
    
    def _set_active_line(self, active_index: int) -> None:
        if active_index >= len(self._text_lines):
            self.reset()
            return
        self._current_line: int = active_index
        print(active_index)
        for i in range(len(self._text_lines)):
            if i == active_index:
                self._text_lines[i].is_active = True
            else:
                self._text_lines[i].is_active = False

    def _update_line(self) -> None:
        pass

    def reset(self) -> None:
        self._text_lines: List[TextLine] = [TextLine(self._world_list, MAX_LINE_LENGTH) for _ in range(NUM_LINES)]
        self._set_active_line(0)

class TextLine:
    def __init__(self, word_list: WordList, max_length: int) -> None:
        self._word_list: WordList = word_list
        self._max_length: int = max_length
        self._current_char: int = 0
        self.is_active: bool = False
        self._text: str = self._word_list.get_random_word()
        word = self._word_list.get_random_word()
        while len(self._text) + len(word) <= self._max_length:
            self._text = f"{self._text} {word}"
            word = self._word_list.get_random_word()
        self._text: str = f"{self._text} "
        self._text_len: int = len(self._text)
        self._characters: List[str] = list(self._text)
        self._typed_characters: List[str] = []
        self._typed_characters_history: List[str] = []

        self._cursor_position: int = 0
        self._entered: List[str] = []
        self._matched_characters = []
    
    def update(self, input_char, is_backspace: bool = False) -> None:
        if is_backspace:
            self._entered.pop()
        else:
            self._entered.append(input_char)
        self._cursor_position = 0
        self._matched_characters = []

        for c in self._entered:
            if c == " ":
                for i in range(self._cursor_position, len(self._characters)):
                    if self._characters[i] == " ":
                        break
                    else:
                        self._matched_characters.append((self._characters[i], False, False))
                        self._cursor_position += 1
                self._cursor_position += 1
                self._matched_characters.append((" ", True, True))
            elif c == self._characters[self._cursor_position]:
                self._matched_characters.append((c, True, True))
                self._cursor_position += 1
        
        if self._cursor_position >= self._text_len:
            return True
        return False

    def draw(self, y_offset: int):
        # centering text so need to calculate how wide the text line will be
        text_width: int = pr.measure_text(self._text, FONT_SIZE)
        text_start_pos = (WIN_WIDTH - text_width) // 2
        x_offset = text_start_pos
        pr.draw_text(self._text, x_offset, y_offset + 30, FONT_SIZE, FONT_COLOR)

        for i in range(self._text_len):
            current_char_width = pr.measure_text(self._characters[i], FONT_SIZE)
            if i == self._cursor_position and self.is_active:
                pr.draw_rectangle(x_offset, y_offset, current_char_width, FONT_SIZE, pr.PINK)

            pr.draw_text(self._characters[i],
                        x_offset,
                        y_offset,
                        FONT_SIZE,
                        FONT_COLOR)

            x_offset += current_char_width + CHAR_SPACING

        # matching chars
        x_offset = text_start_pos
        for i in range(len(self._entered)):
            current_char_width = pr.measure_text(self._entered[i], FONT_SIZE)
            pr.draw_text(self._entered[i],
                        x_offset,
                        y_offset + 60,
                        FONT_SIZE,
                        FONT_COLOR)
            x_offset += current_char_width + CHAR_SPACING

        # entered matching chars
        x_offset = text_start_pos
        for i in range(len(self._matched_characters)):
            current_char_width = pr.measure_text(self._matched_characters[i][0], FONT_SIZE)
            color = FONT_COLOR
            if self._matched_characters[i][1] == False:
                color = pr.RED
            pr.draw_text(self._matched_characters[i][0],
                        x_offset,
                        y_offset + 90,
                        FONT_SIZE,
                        color)
            x_offset += current_char_width + CHAR_SPACING

    def get_text(self) -> str:
        return self._text

    def input_char(self, char: str) -> bool:
        self._typed_characters.append(char)
        print(char)
        #self._characters[self._current_char] = char
        self._current_char += 1
        if self._current_char == self._text_len:
            self._current_char = self._text_len - 1
            return True
        return False

    def backspace(self) -> None:
        if len(self._typed_characters) > 0:
            self._typed_characters.pop()


if __name__ == "__main__":
    app = App()
    app.run()