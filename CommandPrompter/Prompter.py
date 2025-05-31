# Prompter.py
# MIT License
# Copyright (c) 2025 scutiii2

import shlex
from .Prompt_Result import Prompt_Result

class Prompter:
    # Defaults
    __wrappers = [('"', '"'), ('[', ']'), ('(', ')'), ('<', '>')]
    __flag_prefixes = ["=", ":"]
    __cmd_prefixes = ["/", "!"]
    
    def __init__(self, *_, **kwargs):
        self.cmd_prefix = kwargs.get("cmdprefix", self.__cmd_prefixes[0])
        self.cmd_prefix = [self.__cmd_prefixes[0], self.cmd_prefix][self.cmd_prefix in self.__cmd_prefixes]
        self.flag_prefix = kwargs.get("flagprefix", self.__flag_prefixes[0])
        self.flag_prefix = [self.__flag_prefixes[0], self.flag_prefix][self.flag_prefix in self.__flag_prefixes]
    
    def __normalize_token(self, token: str):
        if token and ((token[0], token[-1]) in self.__wrappers):
            return token[1:-1].strip()
        return token

    def __is_command(self, s: str):
        return s.strip().startswith(self.cmd_prefix)

    def __parse_flags_and_positionals(self, tokens) -> tuple[dict, list]:
        flags = {}
        positionals = []

        for token in tokens:
            if token.startswith('--'):
                if '=' in token:
                    key, value = token[2:].split(self.flag_prefix, 1)
                    flags[key.strip()] = self.__normalize_token(value.strip())
                else:
                    flags[token[2:].strip()] = ""
            else:
                positionals.append(self.__normalize_token(token))

        return flags, positionals

    def input(self, input_string: str) -> Prompt_Result:
        """
        Gets prompt and analyzes if it is a command or a message.

        Args:
            input_string (str): Prompted text

        Returns:
            Prompt_Result.
        """
        result = Prompt_Result( type="empty", tokens=[], command=None, flags={}, positionals=[] )
        input_string = input_string.strip()
        if not input_string: return result

        tokens = shlex.split(input_string)
        result.tokens = tokens
        result.type = "message"
        if not self.__is_command(input_string): return result
        
        result.type = "command"
        result.flags, result.positionals = self.__parse_flags_and_positionals(tokens[1:])
        result.command = tokens[0].removeprefix("/")
        return result