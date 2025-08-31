import pytest

from pycalc_sse.server import safe_eval


@pytest.mark.parametrize(
    "expr,expected",
    [
        ("1+2*3", 7),
        ("(1+2)*3", 9),
        ("8/4", 2),            # float -> int if integer-valued
        ("7//3", 2),
        ("7%3", 1),
        ("2**3", 8),
        ("-5 + +2", -3),
    ],
)
def test_basic_operations(expr, expected):
    assert safe_eval(expr) == expected


def test_fractional_results_are_float():
    result = safe_eval("5/2")
    assert isinstance(result, float)
    assert result == 2.5


@pytest.mark.parametrize(
    "bad_expr",
    [
        "a+1",                # variable not allowed
        "'3'+1",              # non-numeric constant
        "__import__('os')",   # call/import not allowed
        "[1,2,3]",            # list literal not allowed
        "1<<2",               # unsupported operator
    ],
)
def test_disallowed_syntax_raises(bad_expr):
    with pytest.raises(ValueError):
        safe_eval(bad_expr)

