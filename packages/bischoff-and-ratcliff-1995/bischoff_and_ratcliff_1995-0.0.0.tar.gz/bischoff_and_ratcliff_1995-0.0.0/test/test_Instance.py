import json

import bischoff_and_ratcliff_1995 as br95


def expected(case_name):
    with open(f"test/data/{case_name}.json", "r") as file:
        expected = json.load(file)
    return expected


def test_case_1():
    actual = br95.Instance(
        C={"length": 587, "width": 233, "height": 220},
        n=8,
        a=[30, 25, 20],
        b=[120, 100, 80],
        L=2,
        s=2507305,
    )
    assert actual.to_dict() == expected("case_1")
    return


def test_case_2():
    actual = br95.Instance(
        C={"length": 587, "width": 233, "height": 220},
        n=10,
        a=[30, 25, 20],
        b=[120, 100, 80],
        L=2,
        s=2508405,
    )
    assert actual.to_dict() == expected("case_2")
    return


def test_case_3():
    actual = br95.Instance(
        C={"length": 587, "width": 233, "height": 220},
        n=12,
        a=[30, 25, 20],
        b=[120, 100, 80],
        L=2,
        s=2506505,
    )
    assert actual.to_dict() == expected("case_3")
    return


def test_case_4():
    actual = br95.Instance(
        C={"length": 587, "width": 233, "height": 220},
        n=8,
        a=[30, 25, 20],
        b=[120, 100, 80],
        L=2,
        s=2506105,
    )
    assert actual.to_dict() == expected("case_4")
    return


def test_case_5():
    actual = br95.Instance(
        C={"length": 587, "width": 233, "height": 220},
        n=10,
        a=[30, 25, 20],
        b=[120, 100, 80],
        L=2,
        s=2504605,
    )
    assert actual.to_dict() == expected("case_5")
    return


def test_case_6():
    actual = br95.Instance(
        C={"length": 587, "width": 233, "height": 220},
        n=12,
        a=[30, 25, 20],
        b=[120, 100, 80],
        L=2,
        s=2502605,
    )
    assert actual.to_dict() == expected("case_6")
    return


def test_case_7():
    # this is the first case of the BR1 instances
    actual = br95.Instance(
        C={"length": 587, "width": 233, "height": 220},
        n=3,
        a=[30, 25, 20],
        b=[120, 100, 80],
        L=2,
        s=2502505,
    )
    assert actual.to_dict() == expected("case_7")
    return
