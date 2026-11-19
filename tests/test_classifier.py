from mathboss.problems import Problem
from mathboss.classifier import classify


def test_correct_answer_is_unclassified():
    p = Problem(7, 8, "*", "mult_table", 3)
    assert classify(p, 56) == []


def test_near_miss_fact():
    # 7*8 = 56; 54 is the neighbouring fact 6*9
    p = Problem(7, 8, "*", "mult_table", 3)
    assert "NEAR_MISS_FACT" in classify(p, 54)


def test_smaller_from_larger():
    # 52 - 37 = 15; 25 is digit-wise |5-3||2-7| (borrowing ignored)
    p = Problem(52, 37, "-", "sub_borrow_2d", 2)
    assert "SMALLER_FROM_LARGER" in classify(p, 25)


def test_wrong_operation():
    # 23 - 17 = 6; 40 = 23 + 17
    p = Problem(23, 17, "-", "sub_borrow_2d", 2)
    assert "WRONG_OPERATION" in classify(p, 40)


def test_off_by_one():
    # 6 + 3 = 9; 10 is expected + 1
    p = Problem(6, 3, "+", "add_within_10", 1)
    assert "OFF_BY_ONE" in classify(p, 10)


def test_unclassified_wrong_answer_is_empty_not_error():
    # 7*8 -> 30: wrong, matches no v1 pattern -> empty label list
    p = Problem(7, 8, "*", "mult_table", 3)
    assert classify(p, 30) == []
