from client.backend import AppBackend
from client.commands.basic_commands import CommandScheduler

class ControllerInterface:
    def __init__(self, backend, scheduler):
        self.m_backend = backend
        self.m_scheduler = scheduler

    def backend(self) -> AppBackend:
        return self.m_backend
    
    def scheduler(self) -> CommandScheduler:
        return self.m_scheduler