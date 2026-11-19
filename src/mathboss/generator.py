"""Template-based problem generation.

Every template is parameterized by difficulty (1-3) and emits Problem
instances. NOTHING a kid sees skips the verifier (verifier.py): generation
and verification are separate stages by design.

Difficulty is structural, not cosmetic: e.g. add_carry_2d ALWAYS requires a
carry and sub_borrow_2d ALWAYS requires a borrow, at every difficulty —
difficulty only widens operand ranges.
"""
from __future__ import annotations

import random

from .problems import Problem


def _add_within_10(rng: random.Random, d: int) -> Problem:
    hi = (5, 8, 10)[d - 1]
    a = rng.randint(1, hi - 1)
    b = rng.randint(1, hi - a)
    return Problem(a, b, "+", "add_within_10", 1)


def _add_within_20(rng: random.Random, d: int) -> Problem:
    hi = (12, 16, 20)[d - 1]
    a = rng.randint(2, hi - 2)
    b = rng.randint(1, hi - a)
    return Problem(a, b, "+", "add_within_20", 1)


def _sub_within_10(rng: random.Random, d: int) -> Problem:
    hi = (6, 8, 10)[d - 1]
    a = rng.randint(hi // 2, hi)
    b = rng.randint(1, a)  # grade 1: never negative results
    return Problem(a, b, "-", "sub_within_10", 1)


def _add_carry_2d(rng: random.Random, d: int) -> Problem:
    a_hi, b_hi = ((49, 49), (79, 79), (99, 99))[d - 1]
    while True:
        a = rng.randint(11, a_hi)
        b = rng.randint(11, b_hi)
        if (a % 10) + (b % 10) >= 10:  # carrying genuinely required
            return Problem(a, b, "+", "add_carry_2d", 2)


def _sub_borrow_2d(rng: random.Random, d: int) -> Problem:
    a_hi = (49, 79, 99)[d - 1]
    while True:
        a = rng.randint(21, a_hi)
        b = rng.randint(11, a - 1)
        if (a % 10) < (b % 10):  # borrowing genuinely required
            return Problem(a, b, "-", "sub_borrow_2d", 2)


def _mult_table(rng: random.Random, d: int) -> Problem:
    hi = (5, 8, 10)[d - 1]
    a = rng.randint(2, hi)
    b = rng.randint(2, hi)
    return Problem(a, b, "*", "mult_table", 3)


TEMPLATES = {
    "add_within_10": _add_within_10,
    "add_within_20": _add_within_20,
    "sub_within_10": _sub_within_10,
    "add_carry_2d": _add_carry_2d,
    "sub_borrow_2d": _sub_borrow_2d,
    "mult_table": _mult_table,
}


def generate(template: str, difficulty: int = 1, seed: int | None = None) -> Problem:
    if template not in TEMPLATES:
        raise KeyError(f"unknown template {template!r}")
    if not 1 <= difficulty <= 3:
        raise ValueError("difficulty must be 1..3")
    return TEMPLATES[template](random.Random(seed), difficulty)


def generate_many(
    template: str, n: int, difficulty: int = 1, seed: int | None = None
) -> list[Problem]:
    if template not in TEMPLATES:
        raise KeyError(f"unknown template {template!r}")
    if not 1 <= difficulty <= 3:
        raise ValueError("difficulty must be 1..3")
    rng = random.Random(seed)
    return [TEMPLATES[template](rng, difficulty) for _ in range(n)]
