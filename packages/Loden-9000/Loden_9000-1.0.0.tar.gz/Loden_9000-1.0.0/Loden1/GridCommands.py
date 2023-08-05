#!/usr/bin/env python3
# Mission: Provide a reusable set of grid-management operations.

__all__ = ["CmdHelp","CmdValues","CmdOpen","CmdClose",
           "CmdEvents","CmdEvent",]

from AbsGrid import aGrid
from AbsCommand import aCommand, NoCommand, BadParam

class Command(aCommand):
    def __init__(self, key):
        self.key = key
    
    def execute(self, a_grid, full_command) -> str():
        Validate.validate(self, a_grid, full_command)
        return self.key 


class Validate:
    @staticmethod
    def validate(a_cmd, a_grid, full_command):
        if not isinstance(a_cmd, Command):
            raise NoCommand("Error: Command child required.")
        Validate.check_prefix(a_cmd.key, full_command)
        Validate.check_instance(a_grid)
    
    ''' Common parameter validations. '''
    @staticmethod
    def check_instance(a_grid):
        ''' Verif a_grid existance & type. '''
        if not a_grid:
            raise NoCommand("Error: No grid provided.")
        if not isinstance(a_grid, aGrid):
            raise BadParam("Error: Unsupported Object.")

    @staticmethod
    def check_prefix(dot_name, full_command):
        ''' Full commands must begin with the dot_name. '''
        if not full_command.lower().startswith(dot_name.lower()):
            raise NoCommand("Error: Command mismatch.")


class CmdHelp(Command):
    def __init__(self, key):
        super().__init__(key)
    
    def execute(self, a_grid, full_command) -> str():
        return super().execute(a_grid, full_command)   

class CmdValues(Command):
    def __init__(self, key):
        super().__init__(key)
    
    def execute(self, a_grid, full_command) -> str():
        return super().execute(a_grid, full_command)    

class CmdOpen(Command):
    def __init__(self, key):
        super().__init__(key)
    
    def execute(self, a_grid, full_command) -> str():
        return super().execute(a_grid, full_command)    

class CmdClose(Command):
    def __init__(self, key):
        super().__init__(key)
    
    def execute(self, a_grid, full_command) -> str():
        return super().execute(a_grid, full_command)    

class CmdEvents(Command):
    def __init__(self, key):
        super().__init__(key)
    
    def execute(self, a_grid, full_command) -> str():
        return super().execute(a_grid, full_command)
    
class CmdEvent(Command):
    def __init__(self, key):
        super().__init__(key)
    
    def execute(self, a_grid, full_command) -> str():
        return super().execute(a_grid, full_command)

