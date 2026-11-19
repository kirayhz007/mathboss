# MathBoss Architecture (v0)

## Design rule

**Generation and verification are separate stages.** No math problem reaches a
student without passing symbolic verification. The goal is not "we tested the
engine" — it is that a malformed problem is *structurally unable* to leave the
pipeline. In an educational product, an engine that accepts `7 × 8 = 54` is a
trust-killer with parents; this architecture makes that class of bug
unrepresentable in shipping paths.

## Five core systems

### 1. Skill Graph — the spine

200+ concept nodes (grades 1–6 target; v0 sample in `skill_graph.yaml`) as a
directed acyclic graph:

```
counting-to-10 → addition-within-10 → addition-within-20 ┐
counting-to-20 → place-value-tens ───────────────────────┼→ addition-with-carrying
subtraction-within-10 ────────────────────────────────────┘
                       └→ subtraction-with-borrowing
multiplication-as-repeated-addition → multiplication-tables-to-10 → division-as-sharing → fractions-as-quantities
```

- Stored as versioned YAML; the game engine just walks the graph.
- Each node carries mastery criteria and maps to level templates.
- Loads-time validation: unknown prerequisites and cycles are hard errors
  (`graph.py::_check_dag`).
- **Intervention routing** lives in the graph too: a diagnosed misconception
  maps to a specific node, so the student is routed *forward to treatment*,
  not backward to retry.

### 2. Misconception Classifier — the diagnosis layer

v1 is a deterministic rule engine (`classifier.py`): published error patterns
from mathematics-education research encoded as matchers over
`(problem, answer)` pairs.

| Pattern | Signature | Example |
|---|---|---|
| `OFF_BY_ONE` | expected ± 1 | `6 + 3 → 10` |
| `WRONG_OPERATION` | matches a different operation on the same operands | `23 − 17 → 40` (= 23 + 17) |
| `SMALLER_FROM_LARGER` | digit-wise subtraction, borrowing ignored | `52 − 37 → 25` (\|5−3\|\|2−7\|) |
| `NEAR_MISS_FACT` | neighbouring multiplication fact | `7 × 8 → 54` (= 6 × 9) |

v2 becomes statistical once telemetry accumulates; the rules engine
bootstraps the labels. This is the compounding asset: every wrong answer in
the game is labeled training data (misconception type, grade, intervention
served, outcome).

### 3. Level Generator + Symbolic Verifier — the content pipeline

- `generator.py` — templates parameterized by `(concept, difficulty 1–3)`;
  difficulty controls operand ranges and which structural property must hold
  (e.g. `add_carry_2d` *always* requires a carry, `sub_borrow_2d` *always*
  requires a borrow — the difficulty knob is meaningful, not cosmetic).
- `verifier.py` — every template has an invariant predicate; `verify()` returns
  violations, `assert_shippable()` gates the pipeline.
- Property tests hammer every template × difficulty with hundreds of seeded
  instances; CI runs on Python 3.9 / 3.11 / 3.12.

### 4. Telemetry Loop — the moat (v0.3)

Every attempt logs `(student, problem, answer, latency, classification,
intervention_served, outcome)`. Two years in, that labeled dataset is the
company; the game is the acquisition strategy.

### 5. Homework Mode — the distribution hack (v0.5)

Parent photographs the worksheet → OCR → problem extraction → the generator
rebuilds tonight's homework as tomorrow's boss encounters. Every other app
competes with Minecraft for spare screen time; MathBoss fuses into the
school's actual curriculum, and the PTA becomes the distribution channel.

## Stack

- **Client:** Godot 4 — one codebase, web build first (school districts run
  Chromebooks, not iPads), then mobile/desktop.
- **Backend:** Python / FastAPI, Postgres. The engine in this repo is
  framework-free on purpose; the service wraps it.
- **Math lives in the world:** a boss with 48 HP and 6-damage arrows *is* a
  division problem wearing armor — numbers are rules of the world, not pop
  quizzes.

## Agent division of labor

| Humans | Coding agents (Devin) |
|---|---|
| Curriculum judgments, error-pattern selection, fun | Skill-graph scaffolding from curriculum docs |
| Review + tune every template | Template + verifier pair generation |
| Product and growth decisions | Property-test suites, CI wiring |

Agents do the boring-but-verifiable work; humans own taste. The credits are
literally buying agent-hours on the left column of that table.

## Milestones

1. **v0.1 (this repo)** — engine core: graph + classifier + verified generation, all green in CI
2. **v0.2** — Godot 4 web client, one playable boss encounter driven by real generator output
3. **v0.3** — FastAPI + telemetry; diagnosis loop closes end-to-end
4. **v0.4** — skill graph v1 (~200 nodes, grades 1–6)
5. **v0.5** — homework mode (OCR → generated encounters)
