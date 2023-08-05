#!/usr/bin/env python3

from abc import ABC, abstractmethod

class GridParams:

    def __init__(self,
                 cells_wide=10,cells_high=5,
                 color_back='#00ff00',color_fore='#0000ff',color_border='#000000',
                 font_wide=1,font_high=1, font_size=16):
        self.cells_wide   = cells_wide
        self.cells_high   = cells_high
        self.color_back   = color_back
        self.color_fore   = color_fore
        self.color_border = color_border
        self.font_wide    = font_wide
        self.font_high    = font_high
        self.font_size    = font_size
       
    def assign(self, params)->bool:
        if not params:
            return False
        self.cells_wide    = params.cells_wide
        self.cells_high    = params.cells_high
        self.color_back    = params.color_back
        self.color_fore    = params.color_fore
        self.color_border  = params.color_border
        self.font_wide     = params.font_wide
        self.font_high     = params.font_high
        self.font_size     = params.font_size
        return True
        

class aGrid(ABC):

    def __init__(self, params):
        self.params = GridParams()
        self.assign(params)
    
    def assign(self, params):
        self.params.assign(params)

    @staticmethod
    @abstractmethod
    def Create(params=GridParams()):
        '''Factory. 
        Regions to be based upon cells, never pixels.
        Font width is number of characters each cell can hold.
        '''
        pass
     
    @abstractmethod
    def back(self, color):
        '''
        Update & distribute a default cell color
        over the entire grid, preserving previous
        contents, if any.
        '''
        pass

    @abstractmethod
    def fore(self, color):
        '''
        Update & distribute a default foreground color
        over the entire grid, preserving previous
        contents, if any.
        '''
        pass

    @abstractmethod
    def set_color(self, cellx, celly, color) -> bool:
        '''
        Set the color of the 0's based cell location.
        Colors to be a stringified color as per Tkinter.
        '''
        pass
     
    @abstractmethod
    def cls(self, color=None):
        '''
        Clear the screen to the desired color.
        Resets the default text content to empty.
        Default color to be platform defined.
        '''
        pass
     
    @abstractmethod
    def set_char(self, cellx, celly, a_char) -> bool:
        '''
        Set the content of a cell to the string.
        String size to be a multiple of font_wide.
        '''
        pass
    
    @abstractmethod
    def close(self):
        '''
        Close the window and / exit the program.
        '''
        pass
