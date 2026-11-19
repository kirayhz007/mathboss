"""Skill graph loading and traversal."""
from __future__ import annotations

import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[2]
DEFAULT_GRAPH = ROOT / "skill_graph.yaml"


class SkillGraph:
    def __init__(self, nodes: dict, interventions: dict):
        self.nodes = nodes
        self.interventions = interventions
        self._check_dag()

    @classmethod
    def load(cls, path: pathlib.Path | str = DEFAULT_GRAPH) -> "SkillGraph":
        data = yaml.safe_load(pathlib.Path(path).read_text())
        return cls(data["nodes"], data.get("interventions", {}))

    def _check_dag(self) -> None:
        """Unknown prerequisites and cycles are hard load errors."""
        state: dict[str, int] = {}  # 0=unvisited 1=in-stack 2=done

        def visit(node: str) -> None:
            if state.get(node) == 1:
                raise ValueError(f"cycle in skill graph at {node!r}")
            if state.get(node) == 2:
                return
            state[node] = 1
            for pre in self.nodes[node]["prerequisites"]:
                if pre not in self.nodes:
                    raise KeyError(f"unknown prerequisite {pre!r} of {node!r}")
                visit(pre)
            state[node] = 2

        for node in self.nodes:
            visit(node)

    def unlocked_by(self, mastered: set) -> list[str]:
        """Nodes whose prerequisites are all mastered and aren't mastered yet."""
        out = []
        for name, node in self.nodes.items():
            if name in mastered:
                continue
            if set(node["prerequisites"]) <= mastered:
                out.append(name)
        return out

    def route_intervention(self, misconception: str) -> str:
        """The node a diagnosed misconception routes the student to."""
        target = self.interventions.get(misconception)
        if target is None or target not in self.nodes:
            raise KeyError(f"no intervention node for {misconception!r}")
        return target
