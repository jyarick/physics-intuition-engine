import sympy as sp

from intuition_engine.schemas import ParsedEquation, ExtractedFeatures
from intuition_engine.classifier import get_derivatives


def extract_coefficients(parsed: ParsedEquation):
    """
    Extract coefficients a, b, c from:

        a*x'' + b*x' + c*x - f(t) = 0
    """
    expr = sp.expand(parsed.canonical_expr)

    t = parsed.independent_variable
    x = parsed.dependent_function(t)

    derivatives = sorted(get_derivatives(parsed), key=lambda d: d.derivative_count)

    x2 = None
    x1 = None

    for d in derivatives:
        if d.derivative_count == 2:
            x2 = d
        if d.derivative_count == 1:
            x1 = d

    a = expr.coeff(x2) if x2 else 0
    b = expr.coeff(x1) if x1 else 0
    c = expr.coeff(x)

    return a, b, c


def extract_forcing(parsed: ParsedEquation, a, b, c):
    """
    Extract forcing term f(t).
    """
    expr = sp.expand(parsed.canonical_expr)

    t = parsed.independent_variable
    x = parsed.dependent_function(t)

    derivatives = sorted(get_derivatives(parsed), key=lambda d: d.derivative_count)

    dependent_part = a * next((d for d in derivatives if d.derivative_count == 2), 0) \
                   + b * next((d for d in derivatives if d.derivative_count == 1), 0) \
                   + c * x

    remainder = sp.simplify(expr - dependent_part)

    forcing = -remainder

    return sp.simplify(forcing)


def extract_forcing_frequency(forcing):
    """
    Detect sinusoidal forcing frequency if present.
    """
    if forcing is None:
        return None

    if forcing.has(sp.cos) or forcing.has(sp.sin):
        args = list(forcing.atoms(sp.cos, sp.sin))
        if args:
            trig = args[0]
            arg = trig.args[0]
            symbols = list(arg.free_symbols)

            if symbols:
                return symbols[0]

    return None


def compute_characteristic_polynomial(a, b, c):
    r = sp.symbols("r")
    return a * r**2 + b * r + c


def compute_roots(poly):
    r = sp.symbols("r")
    try:
        return sp.solve(poly, r)
    except Exception:
        return None


def extract_features(parsed: ParsedEquation) -> ExtractedFeatures:
    """
    Main feature extraction pipeline.
    """
    a, b, c = extract_coefficients(parsed)

    forcing = extract_forcing(parsed, a, b, c)

    discriminant = sp.simplify(b**2 - 4*a*c)

    natural_frequency = None
    if a != 0 and c != 0:
        natural_frequency = sp.sqrt(c/a)

    damping_ratio = None
    if a != 0 and c != 0:
        damping_ratio = b / (2 * sp.sqrt(a*c))

    damping_timescale = None
    if b != 0:
        damping_timescale = a / b

    forcing_frequency = extract_forcing_frequency(forcing)

    poly = compute_characteristic_polynomial(a, b, c)
    roots = compute_roots(poly)

    return ExtractedFeatures(
        a=a,
        b=b,
        c=c,
        forcing=forcing,
        discriminant=discriminant,
        natural_frequency=natural_frequency,
        damping_ratio=damping_ratio,
        damping_timescale=damping_timescale,
        forcing_frequency=forcing_frequency,
        characteristic_polynomial=poly,
        roots=roots,
    )