# CommandPrompter.py
# MIT License
# Copyright (c) 2025 scutiii2

from .Command import Command
from .Prompter import Prompter

class CommandPrompter(Command):
    __prompter: Prompter = None
    
    @classmethod
    def initialize(cls, cmdpath = "", cmdprefix="/"):
        cls.__prompter = Prompter(cmdprefix = "/")
        return super().initialize(cmdpath, cmdprefix)
    
    
    @classmethod
    def execute(cls, prompt: str):
        return super().execute(cls.__prompter.input(prompt))