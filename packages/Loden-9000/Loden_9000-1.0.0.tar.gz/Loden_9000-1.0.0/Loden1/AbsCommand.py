#!/usr/bin/env python3
# Mission: Create a command event parser, abstraction, as well as definitive event execptions.

from abc import ABC, abstractmethod

class BadParam(Exception):
    def __init__(self, message):
        super().__init__(message)

class NoCommand(Exception):
    def __init__(self, message):
        super().__init__(message)

class aCommand(ABC):
    '''Our basic command definition. '''
    @abstractmethod
    def execute(self, a_grid, full_command) -> str():
        pass
