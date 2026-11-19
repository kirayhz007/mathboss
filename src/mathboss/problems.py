"""Core problem representation shared by generator, verifier and classifier."""
from __future__ import annotations

from dataclasses import dataclass

OPS = ("+", "-", "*")


@dataclass(frozen=True)
class Problem:
    a: int
    b: int
    op: str  # one of OPS
    template: str  # generator template that produced this problem
    grade: int

    def __post_init__(self) -> None:
        if self.op not in OPS:
            raise ValueError(f"unknown op {self.op!r}")

    @property
    def answer(self) -> int:
        if self.op == "+":
            return self.a + self.b
        if self.op == "-":
            return self.a - self.b
        return self.a * self.b

    def render(self) -> str:
        return f"{self.a} {self.op} {self.b}"
