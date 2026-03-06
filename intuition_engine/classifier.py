import sympy as sp

from intuition_engine.schemas import ParsedEquation, EquationClassification


def get_derivatives(parsed: ParsedEquation):
    """
    Return all Derivative objects involving the dependent function.
    """
    expr = parsed.canonical_expr
    dep_func = parsed.dependent_function(parsed.independent_variable)

    derivatives = [
        d for d in expr.atoms(sp.Derivative)
        if d.expr == dep_func
    ]
    return list(derivatives)


def get_order(parsed: ParsedEquation) -> int:
    """
    Determine the highest derivative order of the dependent function.
    Returns 0 if no derivatives appear.
    """
    derivatives = get_derivatives(parsed)
    if not derivatives:
        return 0

    t = parsed.independent_variable
    max_order = 0
    for d in derivatives:
        order = d.derivative_count
        if order > max_order:
            max_order = order
    return max_order


def is_linear_in_function(parsed: ParsedEquation) -> bool:
    """
    Check linearity with respect to x(t), x'(t), x''(t), etc.
    Strategy:
      Replace x(t) and its derivatives with dummy symbols and test total polynomial degree.
    """
    expr = sp.expand(parsed.canonical_expr)
    t = parsed.independent_variable
    x_t = parsed.dependent_function(t)

    replacements = {}
    dummy_symbols = []

    # Replace x(t)
    x0 = sp.Symbol("X0")
    replacements[x_t] = x0
    dummy_symbols.append(x0)

    # Replace derivatives
    derivatives = sorted(
        get_derivatives(parsed),
        key=lambda d: d.derivative_count
    )

    for d in derivatives:
        dn = sp.Symbol(f"X{d.derivative_count}")
        replacements[d] = dn
        dummy_symbols.append(dn)

    expr_sub = expr.subs(replacements)

    try:
        poly = sp.Poly(expr_sub, *dummy_symbols)
    except sp.PolynomialError:
        return False

    return poly.total_degree() <= 1


def has_constant_coefficients(parsed: ParsedEquation) -> bool:
    """
    Check whether coefficients of x(t), x'(t), x''(t) are independent of t.
    This is only meaningful after confirming linearity.
    """
    expr = sp.expand(parsed.canonical_expr)
    t = parsed.independent_variable
    x_t = parsed.dependent_function(t)

    basis_terms = [x_t]
    derivatives = sorted(get_derivatives(parsed), key=lambda d: d.derivative_count)
    basis_terms.extend(derivatives)

    for term in basis_terms:
        coeff = expr.coeff(term)
        if coeff.has(t):
            return False

    return True


def is_forced(parsed: ParsedEquation) -> bool:
    """
    Determine whether the equation has a nonzero forcing/input term.
    We subtract off all dependent-variable terms and see what remains.
    """
    expr = sp.expand(parsed.canonical_expr)
    t = parsed.independent_variable
    x_t = parsed.dependent_function(t)

    basis_terms = [x_t]
    derivatives = sorted(get_derivatives(parsed), key=lambda d: d.derivative_count)
    basis_terms.extend(derivatives)

    dependent_part = 0
    for term in basis_terms:
        dependent_part += expr.coeff(term) * term

    remainder = sp.simplify(expr - dependent_part)
    return remainder != 0


def classify_equation(parsed: ParsedEquation) -> EquationClassification:
    """
    Classify the parsed equation for the v1 engine.
    """
    notes = []

    order = get_order(parsed)
    linear = is_linear_in_function(parsed)

    if not linear:
        const_coeffs = False
        notes.append("Equation is not linear in the dependent function and its derivatives.")
    else:
        const_coeffs = has_constant_coefficients(parsed)

    forced = is_forced(parsed)

    family = None
    if order == 2 and linear and const_coeffs:
        family = "second_order_linear_constant_coeff_ode"
        if forced:
            notes.append("Equation matches the v1 family and includes forcing/input.")
        else:
            notes.append("Equation matches the v1 family and is homogeneous.")
    else:
        notes.append("Equation does not fully match the current v1 family.")

    return EquationClassification(
        order=order,
        is_linear=linear,
        has_constant_coefficients=const_coeffs,
        is_forced=forced,
        family=family,
        notes=notes,
    )