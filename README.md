# MathBoss

> A math game where wrong answers are the product.

Every math app on the store tracks right vs. wrong and dials difficulty up and down.
MathBoss classifies **how** the answer is wrong — borrowing errors, off-by-one
counting, smaller-digit-from-larger subtraction, near-miss multiplication facts —
and routes the student to the intervention level for that *exact* broken mental
model. **Adaptive diagnosis, not adaptive difficulty.**

## Why this is different

| Everyone else | MathBoss |
|---|---|
| Answer wrong → retry easier problems | Answer wrong → classified error *pattern* → targeted intervention node |
| Content hand-authored, QA'd after the fact | Every generated problem passes a symbolic verifier **before** a kid can see it |
| Monetizes parents | Telemetry compounds into a labeled error dataset — the game is the acquisition strategy, the data is the moat |

## What is real in this repo (v0)

This repo is the **core engine**, built test-first:

- `skill_graph.yaml` — concept DAG (grades 1–6 target, v0 sample nodes), with
  mastery criteria and **misconception → intervention routing**.
- `src/mathboss/classifier.py` — deterministic rule engine labeling *how*
  answers are wrong (4 published error patterns in v0).
- `src/mathboss/generator.py` — template-based problem generation,
  parameterized by concept and difficulty.
- `src/mathboss/verifier.py` — symbolic verification stage: invariant-breaking
  problems are **structurally unshippable**, not caught in QA.
- Property-style tests + CI on three Python versions.

Concrete examples the tests assert:

- `7 × 8 = 54` → classified `NEAR_MISS_FACT` (54 is the neighbouring fact 6 × 9)
- `52 − 37 = 25` → classified `SMALLER_FROM_LARGER` (digit-wise `|5−3||2−7|`, borrowing ignored)
- `23 − 17 = 40` → classified `WRONG_OPERATION` (added instead of subtracted)

## Quickstart

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the five core systems, data flow,
stack decisions (Godot 4 web-first client, FastAPI backend, Postgres), and the
milestone plan.

## Built agent-first

The boring-but-verifiable work in this repo — graph scaffolding, template +
verifier pairs, property tests, CI — is delegated to coding agents (Devin),
with human review on every merge. That division of labor is the whole point:
agents are good at generating and checking closed-form arithmetic; humans
decide what's worth learning and what's fun.

## Roadmap

- [ ] v0.1 — this repo: engine core with verified generation
- [ ] v0.2 — Godot 4 web client: boss-encounter presentation layer
- [ ] v0.3 — FastAPI service + telemetry loop (labeled error data starts compounding)
- [ ] v0.4 — skill graph v1: ~200 nodes, grades 1–6
- [ ] v0.5 — homework mode: photograph the worksheet → tonight's homework becomes tomorrow's boss fights

## License

MIT
