"""Compute general (symbolic) solution of ODEs and systems. No initial/boundary values."""

import sympy as sp

from intuition_engine.ode.schemas import ParsedEquation


def solve_ode(parsed: ParsedEquation):
    """Return general solution of the ODE as Eq or list of Eq; None or error message if unsolved."""
    try:
        t = parsed.independent_variable
        func = parsed.dependent_function(t)
        sol = sp.dsolve(parsed.canonical_expr, func)
        if sol is not None:
            return sol
    except Exception:
        pass
    return None


def solve_system(parsed_system):
    """Return general solution of the system as list of Eq; None if unsolved."""
    try:
        t = parsed_system.independent_variable
        eqs = [
            sp.Eq(sp.diff(f(t), t), rhs)
            for f, rhs in parsed_system.equations
        ]
        funcs = [f(t) for f in parsed_system.state_vars]
        try:
            from sympy.solvers.ode.systems import dsolve_system
            sol_list = dsolve_system(eqs, funcs=funcs, t=t)
        except ImportError:
            sol_list = sp.dsolve(eqs, funcs)
        if sol_list is not None and len(sol_list) > 0:
            first = sol_list[0]
            return first if isinstance(first, (list, tuple)) else sol_list
    except Exception:
        pass
    return None
