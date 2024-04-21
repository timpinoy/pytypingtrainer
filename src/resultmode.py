import pyray as pr
from settings import *
from typemode import TypeMode

class ResultMode():
    def __init__(self) -> None:
        pass

    def update(self):
        pass

    def draw(self):
        pr.draw_text("OVER", 20, 100, FONT_SIZE, FONT_COLOR)