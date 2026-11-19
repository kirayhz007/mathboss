"""Property-style checks: every generated problem must verify at every
difficulty tier, and structural invariants (carry/borrow/range) must hold."""
import pytest

from mathboss.generator import TEMPLATES, generate_many
from mathboss.verifier import verify


@pytest.mark.parametrize("template", sorted(TEMPLATES))
def test_every_generated_problem_ships(template):
    for difficulty in (1, 2, 3):
        seed = sum(map(ord, template)) + difficulty
        for p in generate_many(template, 200, difficulty=difficulty, seed=seed):
            assert verify(p) == [], f"{p.render()} failed at difficulty {difficulty}"


@pytest.mark.parametrize(
    "template,expect",
    [
        ("add_carry_2d", lambda p: (p.a % 10) + (p.b % 10) >= 10),
        ("sub_borrow_2d", lambda p: (p.a % 10) < (p.b % 10)),
        ("add_within_10", lambda p: p.a + p.b <= 10),
        ("sub_within_10", lambda p: p.b <= p.a),
    ],
)
def test_template_invariants_hold(template, expect):
    for p in generate_many(template, 100, seed=7):
        assert expect(p)


def test_bad_problem_is_unshippable():
    from mathboss.problems import Problem
    from mathboss.verifier import assert_shippable

    # violates add_within_10 invariant (sum 12 > 10) with wrong template tag
    smuggler = Problem(7, 5, "+", "add_within_10", 1)
    with pytest.raises(ValueError, match="template_invariant"):
        assert_shippable(smuggler)
