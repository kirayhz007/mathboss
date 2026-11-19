import pytest

from mathboss.graph import SkillGraph


def test_load_and_traverse():
    g = SkillGraph.load()
    assert "counting-to-10" in g.nodes

    unlocked = g.unlocked_by({"counting-to-10"})
    assert "addition-within-10" in unlocked
    assert "counting-to-20" in unlocked
    # addition-within-20 needs addition-within-10 first
    assert "addition-within-20" not in unlocked


def test_intervention_routing():
    g = SkillGraph.load()
    assert g.route_intervention("NEAR_MISS_FACT") == "multiplication-tables-to-10"
    assert g.route_intervention("SMALLER_FROM_LARGER") == "place-value-tens"


def test_unknown_intervention_fails_loud():
    g = SkillGraph.load()
    with pytest.raises(KeyError):
        g.route_intervention("NOT_A_THING")


def test_cycle_is_a_hard_load_error():
    nodes = {
        "a": {"grade": 1, "concept": "a", "prerequisites": ["b"], "mastery": {}},
        "b": {"grade": 1, "concept": "b", "prerequisites": ["a"], "mastery": {}},
    }
    with pytest.raises(ValueError, match="cycle"):
        SkillGraph(nodes, {})
