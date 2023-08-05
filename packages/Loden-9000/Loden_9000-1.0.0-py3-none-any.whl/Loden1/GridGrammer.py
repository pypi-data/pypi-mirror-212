#!/usr/bin/env python3
# Mission: Create a command-line grammar.

import GridCommands
from AbsCommand import NoCommand, BadParam

class Grmr01:
    ''' A grammar for the abstract grid - others to follow? '''
    def __init__(self):
        self.commands = [
            GridCommands.CmdHelp(".help"),
            GridCommands.CmdValues(".values"),
            GridCommands.CmdOpen(".open"),
            GridCommands.CmdClose(".close"),
            GridCommands.CmdEvents(".events"),
            GridCommands.CmdEvent(".event"),
        ]

    def get_command(self, string):
        ''' Check for a case-insensitive 'dot command'
        for a potentially parameterized operation.
        
        Return the primary Command instance or a domain
        exception. '''
        
        cols = string.lower().split(' ')
        for cmd in self.commands:
            if cmd.key == cols[0]:
                return cmd
        raise NoCommand(f"No '{string}'")
