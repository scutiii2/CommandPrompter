# Prompt_Result.py
# MIT License
# Copyright (c) 2025 scutiii2

from dataclasses import dataclass

@dataclass
class Prompt_Result:
    type: str
    tokens: list[str]
    command: str | None
    flags: dict[str, str]
    positionals: list[str]