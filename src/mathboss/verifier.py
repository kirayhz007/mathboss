"""Symbolic verification stage.

Every generated problem must pass these invariants BEFORE it can be shown to
a student. The point is not "we tested the engine after the fact" — it is
that a malformed problem is structurally unable to leave the pipeline.

Template invariants:
  add_within_10 : a,b >= 1 and a + b <= 10
  add_within_20 : a,b >= 1 and a + b <= 20
  sub_within_10 : 1 <= b <= a <= 10 (no negative results in grade 1)
  add_carry_2d  : a,b >= 10 and units digits sum >= 10 (carry required)
  sub_borrow_2d : a > b >= 10 and a's unit digit < b's unit digit (borrow required)
  mult_table    : 2 <= a,b <= 10

Global invariants: operands and answer are non-negative integers.
"""
from __future__ import annotations

from .problems import Problem

INVARIANTS = {
    "add_within_10": lambda p: p.a >= 1 and p.b >= 1 and p.a + p.b <= 10,
    "add_within_20": lambda p: p.a >= 1 and p.b >= 1 and p.a + p.b <= 20,
    "sub_within_10": lambda p: 1 <= p.b <= p.a <= 10,
    "add_carry_2d": lambda p: p.a >= 10 and p.b >= 10 and (p.a % 10) + (p.b % 10) >= 10,
    "sub_borrow_2d": lambda p: p.a > p.b >= 10 and (p.a % 10) < (p.b % 10),
    "mult_table": lambda p: 2 <= p.a <= 10 and 2 <= p.b <= 10,
}


def verify(p: Problem) -> list[str]:
    """Return the list of violated invariants ([] == safe to ship)."""
    violations: list[str] = []
    if p.a < 0 or p.b < 0 or p.answer < 0:
        violations.append("non_negative")
    check = INVARIANTS.get(p.template)
    if check is None:
        violations.append(f"unknown_template:{p.template}")
    elif not check(p):
        violations.append(f"template_invariant:{p.template}")
    return violations


def assert_shippable(p: Problem) -> None:
    violations = verify(p)
    if violations:
        raise ValueError(f"problem {p.render()} failed verification: {violations}")
