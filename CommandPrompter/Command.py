# Command.py
# MIT License
# Copyright (c) 2025 scutiii2

from abc import ABC, abstractmethod
from .Prompt_Result import Prompt_Result
from typing import Type
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

class Command(ABC):
    dirname: str = "commands"
    registry = []
    __initialized = False
    _cmdprefix: str = "/"
    
    def __init_subclass__(cls, **kwargs):
        """
        Saves a child if it is a command.

        Args:
            kwargs (dict[str: str]): Flags of a command initialization

        Returns:
            None.
        """
        super().__init_subclass__(**kwargs)
        if cls.__name__[:3] == "CMD":
            Command.registry.append(cls)
    
    def __look(prompt_result: Prompt_Result):
        """
        Checks if a prompt is a command or a message.
        Returns the command if exists.

        Args:
            prompt_result (Prompt_Result): Prompted data.

        Returns:
            Any | None: Founded command.
        """
        if type(prompt_result) != Prompt_Result: return None
        if prompt_result.type != "command" or prompt_result.command == None: return None
        for reg in Command.registry:
            if reg.__name__[3:].lower() == prompt_result.command:
                return reg
        return None
    
    @abstractmethod
    def _run(*args, **kwargs):
        """
        Main executable process.

        Args:
            args (str): Positionals prompted
            kwargs (dict[str: str]): Flags prompted

        Returns:
            None.
        """
        pass
    
    @classmethod
    def execute(cls, prompt_result: Prompt_Result):
        """
        Checks if a prompt is a command or a message.
        Executes the command if exists.

        Args:
            args (str): Positionals prompted
            kwargs (dict[str: str]): Flags prompted

        Returns:
            None.
        """
        if not cls.__initialized: return
        if type(prompt_result) != Prompt_Result: return
        child: Type[Command] = Command.__look(prompt_result)
        if child != None:
            child._run(*prompt_result.positionals, **prompt_result.flags)

    @classmethod
    def initialize(cls, cmdpath: str = "", cmdprefix = "/"):
        """
        Gets all of the Commands in the preferred directory.

        Args:
            cmdpath (str): Path of the commands directory. Default [executed script file]/commands

        Returns:
            None.
        """
        cls._cmdprefix = cmdprefix
        print("== Loading Commands ====================================")
        path = [Path(cmdpath), Path.cwd() / cls.dirname][cmdpath == ""]
        if not path.is_dir():
            print("No Commands Found.")
            return

        hits = list(path.glob("CMD*.py"))
        if len(hits) == 0:
            print("No Commands Found.")
            return
        num_width = len(str(len(hits)))
        
        loads = 0
        for i, file in enumerate(hits):
            try:
                name = Path(file.name).stem.removeprefix("CMD")
                spec = spec_from_file_location(file.stem, file)
                module = module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"[{(i+1):0{num_width}}] Successfully Loaded: {name} ({file.name})")
                loads += 1
            except Exception as _:
                print(f"[{(i+1):0{num_width}}] Failed to Loaded   : {name} ({file.name})")
        print(f"Commands Loaded    {" " * (3 + num_width)}: {loads} of {len(hits)}")
        print("========================================================\n")
        cls.__initialized = True
        return cls
    