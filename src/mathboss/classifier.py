"""Misconception classifier (v1: deterministic rule engine).

Labels (problem, given) pairs with the *pattern* of the error rather than a
bare wrong/right flag. Patterns follow common error taxonomies from
mathematics-education research.

An empty label list on a wrong answer means "wrong but not yet classified" —
v1 rule coverage is intentionally small; telemetry grows the taxonomy and a
statistical v2 takes over once labels accumulate.
"""
from __future__ import annotations

from .problems import Problem

MISCONCEPTIONS = {
    "OFF_BY_ONE": "Answer is expected +/- 1 (counting/sequencing slip).",
    "WRONG_OPERATION": "Answer matches a different operation on the same operands.",
    "SMALLER_FROM_LARGER": "Digit-wise subtraction ignoring borrowing (e.g. 52-37 -> 25).",
    "NEAR_MISS_FACT": "Answer is a neighbouring multiplication fact (e.g. 7x8 -> 54 = 6x9).",
}


def _wrong_operation(problem: Problem, given: int) -> bool:
    candidates = {problem.a + problem.b, problem.a - problem.b, problem.a * problem.b}
    candidates.discard(problem.answer)
    return given in candidates


def _digitwise_smaller_from_larger(a: int, b: int) -> int | None:
    """Digit-wise |a_i - b_i|; defined only for equal-width non-negative ints."""
    sa, sb = str(a), str(b)
    if len(sa) != len(sb):
        return None
    return int("".join(str(abs(x - y)) for x, y in zip(map(int, sa), map(int, sb))))


def _near_miss_fact(problem: Problem, given: int) -> bool:
    if problem.op != "*":
        return False
    a, b = problem.a, problem.b
    neighbours = {
        (a - 1) * b, (a + 1) * b, a * (b - 1), a * (b + 1),
        (a - 1) * (b + 1), (a + 1) * (b - 1),
    }
    return given in neighbours


def classify(problem: Problem, given: int) -> list[str]:
    """Return every misconception pattern matching this attempt."""
    if given == problem.answer:
        return []
    hits: list[str] = []
    if abs(given - problem.answer) == 1:
        hits.append("OFF_BY_ONE")
    if _wrong_operation(problem, given):
        hits.append("WRONG_OPERATION")
    if problem.op == "-":
        digitwise = _digitwise_smaller_from_larger(problem.a, problem.b)
        if digitwise is not None and digitwise == given:
            hits.append("SMALLER_FROM_LARGER")
    if _near_miss_fact(problem, given):
        hits.append("NEAR_MISS_FACT")
    return hits
