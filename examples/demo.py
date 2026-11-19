"""End-to-end demo: generate -> verify -> simulate a wrong answer ->
classify the misconception -> route to the intervention node.

Run:  python examples/demo.py
"""
from mathboss.classifier import MISCONCEPTIONS, classify
from mathboss.generator import generate_many
from mathboss.graph import SkillGraph
from mathboss.verifier import assert_shippable


def simulate_error(problem):
    """Produce a *patterned* wrong answer (what a struggling kid would write)."""
    if problem.op == "*":
        return (problem.a - 1) * problem.b  # near-miss fact
    if problem.op == "-":
        # digit-wise smaller-from-larger (borrowing ignored)
        digits = zip(map(int, str(problem.a)), map(int, str(problem.b)))
        return int("".join(str(abs(x - y)) for x, y in digits))
    return problem.answer + 1  # off-by-one


def main() -> None:
    graph = SkillGraph.load()
    for template in ("add_carry_2d", "sub_borrow_2d", "mult_table"):
        print(f"--- {template} ---")
        for p in generate_many(template, 3, difficulty=2, seed=42):
            assert_shippable(p)  # raises if the problem could not ship
            wrong = simulate_error(p)
            labels = classify(p, wrong)
            route = graph.route_intervention(labels[0]) if labels else "-"
            print(f"{p.render():>9} = ?   kid writes {wrong:>3}   {labels}   -> {route}")
    print("\nKnown v1 patterns:")
    for code, desc in MISCONCEPTIONS.items():
        print(f"  {code:20} {desc}")


if __name__ == "__main__":
    main()
