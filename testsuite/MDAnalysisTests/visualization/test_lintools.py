import pytest
from MDAnalysis.visualization.lintools import create_clock_diagram
from MDAnalysisTests.datafiles import (ALA_191, GLY_932, DSPC_None)


@pytest.mark.parametrize("resname, resid, values, expected", (
    [
        "ALA", "191", [0.1], ALA_191
    ], [
        "GLY", "932", [0.3, 0.5, 0.6], GLY_932
    ], [
        "DSPC", None, [0.5, 0.6, 0.6], DSPC_None
    ],
))
def test_create_clock_diagram(resname, resid, values, expected):
    clock_diagram = create_clock_diagram(resname, resid, values)
    clock_diagram.seek(0)
    actual = clock_diagram.readlines()
    actual_with_no_date = actual[0:8] + actual[9:]
    with (open(expected)) as f:
        expected_contents = f.readlines()
    expected_with_no_date = expected_contents[0:8] + expected_contents[9:]
    assert expected_with_no_date == actual_with_no_date


def test_create_clock_diagram_non_normalised_values():
    with pytest.raises(ValueError) as e:
        create_clock_diagram("test", "123", [1, 3])
        assert e.value == "The value list must contain normalised values between 0 and 1."


def test_create_clock_diagram_gt_5_values():
    with pytest.raises(ValueError) as e:
        create_clock_diagram("test", "123", [0.1, 0.2, 0.1, 0.3, 0.4, 0.6])
        assert e.value == "The value list has to contain no more than 5 items."
