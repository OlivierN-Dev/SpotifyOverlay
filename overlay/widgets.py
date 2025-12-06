import tkinter as tk
from styles import TEXT_COLOR, TITLE_FONT, ARTIST_FONT, PROGRESS_FONT, PROGRESS_BG, PROGRESS_FG

class StyledLabel(tk.Label):
    def __init__(self, master, textvar, font, **kwargs):
        super().__init__(master, textvariable=textvar, font=font, fg=TEXT_COLOR, bg=kwargs.get("bg","black"))

class ProgressBar(tk.Canvas):
    def __init__(self, master, width=200, height=20, **kwargs):
        super().__init__(master, width=width, height=height, bg=PROGRESS_BG, highlightthickness=0)
        self.width = width
        self.height = height
        self.progress_rect = self.create_rectangle(0, 0, 0, height, fill=PROGRESS_FG, width=0)

    def update_progress(self, ratio):
        """ratio entre 0 et 1"""
        self.coords(self.progress_rect, 0, 0, self.width * ratio, self.height)

class menuMusic(tk.Label):
    def __init__(self,master,text,image,font,**kwargs):
        super().__init__(master, textvariable=text,image=image, font=font, fg=TEXT_COLOR,)
        