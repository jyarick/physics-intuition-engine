import sympy as sp
from sympy.parsing.sympy_parser import parse_expr

from intuition_engine.schemas import ParsedEquation


def build_symbol_dict():
    """
    Create the allowed symbol/function namespace for parsing user equations.
    We keep this constrained on purpose for v1.
    """
    t = sp.symbols("t", real=True)
    x = sp.Function("x")

    # Common symbolic parameters for canonical examples
    m, b, k, F0, omega, c = sp.symbols("m b k F0 omega c", real=True)

    local_dict = {
        "sp": sp,
        "t": t,
        "x": x,
        "m": m,
        "b": b,
        "k": k,
        "c": c,
        "F0": F0,
        "omega": omega,
        "diff": sp.diff,
        "cos": sp.cos,
        "sin": sp.sin,
        "exp": sp.exp,
        "sqrt": sp.sqrt,
        "pi": sp.pi,
    }
    return local_dict


def split_equation(equation_str: str) -> tuple[str, str]:
    """
    Split an equation string into left-hand side and right-hand side.
    Requires exactly one '=' sign.
    """
    if equation_str.count("=") != 1:
        raise ValueError("Equation must contain exactly one '=' sign.")

    lhs_str, rhs_str = equation_str.split("=")
    lhs_str = lhs_str.strip()
    rhs_str = rhs_str.strip()

    if not lhs_str or not rhs_str:
        raise ValueError("Both left-hand side and right-hand side must be non-empty.")

    return lhs_str, rhs_str


def parse_side(expr_str: str, local_dict: dict) -> sp.Expr:
    """
    Parse one side of the equation into a SymPy expression.
    """
    try:
        expr = parse_expr(expr_str, local_dict=local_dict, evaluate=True)
    except Exception as e:
        raise ValueError(f"Could not parse expression: {expr_str}\nOriginal error: {e}")
    return sp.simplify(expr)


def parse_equation(equation_str: str) -> ParsedEquation:
    """
    Parse a full equation string like:
        m*diff(x(t), t, 2) + b*diff(x(t), t) + k*x(t) = F0*cos(omega*t)

    Returns a ParsedEquation dataclass with:
    - lhs
    - rhs
    - canonical_expr = lhs - rhs
    - dependent_function = x
    - independent_variable = t
    """
    local_dict = build_symbol_dict()
    lhs_str, rhs_str = split_equation(equation_str)

    lhs = parse_side(lhs_str, local_dict)
    rhs = parse_side(rhs_str, local_dict)
    canonical_expr = sp.simplify(lhs - rhs)

    dependent_function = local_dict["x"]
    independent_variable = local_dict["t"]

    return ParsedEquation(
        raw_input=equation_str,
        lhs=lhs,
        rhs=rhs,
        canonical_expr=canonical_expr,
        dependent_function=dependent_function,
        independent_variable=independent_variable,
    )