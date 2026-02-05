import tkinter as tk
from typing import Callable

class Command:
    def __init__(self,
                initialize : Callable[[None], None] = lambda: None,
                execute : Callable[[None], None] = lambda: None, 
                is_finished : Callable[[None],bool] = lambda: False, 
                end : Callable[[bool],None] = lambda inturrepted: None):
        
        self.initialize = initialize
        self.execute = execute
        self.is_finished = is_finished
        self.end = end
        self.active = False
        self.ID = CommandScheduler.register_command(self)
    
    def activate(self):
        self.active = True
        self.initialize()

    def deactivate(self, interrupted):
        self.active = False
        self.end(interrupted)

class CommandScheduler:
    def __init__(self, root: tk.TK, period = 10):
        self.root = root
        self.period = period
        self.commands = []

    def schedule(self, command: Command):
        command.activate()

    def register_command(self, command: Command):
        self.commands.append(command)
        return len(self.commands)
    
    def periodic(self):
        # iterate only over active commands
        for command in self.commands[:]:
            if not command.active:
                continue

            if command.is_finished():
                command.deactivate(False)
            else:
                command.execute()


        self.root.after(self.period, self.periodic)


    
