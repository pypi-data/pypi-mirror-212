#!/usr/bin/env python3
'''
Mission: Provide a Tkinter implementation suitable
for paradigm testing, demonstration, as well as re-use.

Note: This particular demonstration also features a
time-based callback operation, so the whimsical __main__
herein can (ahem) "make faces, in time."

'''

from AbsGrid import aGrid, GridParams
import tkinter as tk
from tkinter import font

class GridT(aGrid):

    def __init__(self, params=GridParams()):
        super().__init__(params)
        self._win = None
        self._cells = []
        self._time_lapse = 1000 # milisecond default
        self._times = 0
    
    def _init_win(self):
        self.close()
        self._win = tk.Tk()
        self._win.title("Loden")
        zpane = tk.Frame(self._win)
        zfont = font.nametofont('TkFixedFont')
        zfont.configure(size=self.params.font_size)
        zfont.configure(weight=font.BOLD)
        self._win.geometry(f"+{50}+{50}")
        self._win['bg'] =self.params.color_border
        self._win['borderwidth'] = 2 # margin nsew
        for yhigh in range(self.params.cells_wide):
            for xwide in range(self.params.cells_high):
                a_wgt = tk.Button(
                    zpane,
                    font=zfont,
                    bg=self.params.color_back,
                    fg=self.params.color_fore,
                    width=self.params.font_wide,
                    height=self.params.font_high,
                    relief=tk.SOLID
                    )
                a_wgt.grid(row=xwide,column=yhigh)
                self._cells.append(a_wgt)
        zpane.pack(expand=True)
        self.zpane = zpane

    @staticmethod
    def Create(params):
        ''' Factory - requesite '''
        result = GridT(params)
        result._init_win()
        return result
    
    def back(self, color):
        '''
        Update & distribute a default cell color
        over the entire grid, preserving previous
        contents, if any.
        '''
        for cell in self._cells:
            a_wgt = self._win.nametowidget(cell)
            a_wgt.config(bg=color)
        self.params.color_back = color    

    def fore(self, color):
        '''
        Update & distribute a default foreground color
        over the entire grid, preserving previous
        contents, if any.
        '''
        for cell in self._cells:
            a_wgt = self._win.nametowidget(cell)
            a_wgt.config(fg=color)
        self.params.color_fore = color    

    def set_color(self, cellx, celly, color) -> bool:
        '''
        Set the color of the 0's based cell location.
        Colors to be a stringified color as per Tkinter.
        '''
        a_wgt = self.get_cell(cellx, celly)
        if a_wgt:
            a_wgt.config(bg=color)
            return True
        return False

    def cls(self, color=None):
        '''
        Clear the screen to the desired color.
        Resets the default text content to empty.
        Default color to be platform defined.
        '''
        if not color:
            color = self.params.color_back
        for cell in self._cells:
            a_wgt = self._win.nametowidget(cell)
            a_wgt['text'] = ' '
            a_wgt.config(bg=color)

    def set_char(self, cellx, celly, a_char) -> bool:
        '''
        Set the content of a cell to the string.
        String size to be a multiple of font_wide.
        '''
        a_wgt = self.get_cell(cellx, celly)
        if a_wgt:
            a_wgt['text'] = a_char
            return True
        return False
    
    def close(self):
        '''
        Close the window and / exit the program.
        '''
        if self._win:
            try:
                self._win.destroy()
            except:
                pass
            finally:
                self._win = None

    def ticker(self, mili_sec=None):
        '''
        Beschedule the very NEXT callback to .tick()
        '''
        if not mili_sec:
            mili_sec = self._time_lapse
        self.zpane.after(mili_sec, self.tick)
        self._time_lapse = mili_sec
        self._times += 1

    def tick(self):
        '''
        To activate one must first call .ticker().
        One must also re-sechedule using the same,
        as demonstrated herein.
        '''
        import random
        r = hex(random.randrange(0, 255))[2:]
        g = hex(random.randrange(0, 255))[2:]
        b = hex(random.randrange(0, 255))[2:]
        acolor = f'#{r:<02}{g:<02}{b:<02}'
        x = random.randrange(0, self.params.cells_wide)
        y = random.randrange(0, self.params.cells_high)
        if self._times % (len(self._cells)/2) == 0:
            self.cls(acolor)
        else:
            face = random.randrange(0x1f600, 0x1f619)
            self.set_char(x, y, chr(face))
            self.set_color(x, y, acolor)
        self.ticker()

    def get_cell(self, xloc, yloc):
        '''
        Handy way to get the representational widget.
        Returns None if none found.
        '''
        max_ = (yloc * self.params.cells_wide) + xloc
        if len(self._cells) > max_:
            a_wgt = self._cells[max_]
            return self._win.nametowidget(a_wgt)


if __name__ == '__main__':
    params = GridParams(20,10)
    params.font_wide = 3
    params.font_high = 1
    params.font_size = 28
    w = GridT.Create(params)
    w.set_color(0, 0, 'red')
    w.set_char(0, 0, '#')
    w.set_color(4, 4, '#ee00ee')
    w.set_char(4, 4, '!')
    w.ticker(150)
    print("You can now use 'w.' (e.g. w.close()), as well.")

