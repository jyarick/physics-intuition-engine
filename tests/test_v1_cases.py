import sympy as sp

from intuition_engine.pipeline import analyze_equation
from intuition_engine.examples import EXAMPLES


def test_driven_damped_oscillator_supported():
    eq = EXAMPLES["Driven damped oscillator"]

    report = analyze_equation(eq)

    assert report.validation.is_supported is True
    assert report.classification.order == 2
    assert report.classification.is_linear is True
    assert report.classification.has_constant_coefficients is True


def test_undamped_oscillator_features():
    eq = EXAMPLES["Undamped oscillator"]

    report = analyze_equation(eq)
    features = report.features

    m, k = sp.symbols("m k", real=True)

    assert features.a == m
    assert features.c == k
    assert features.b == 0

    assert sp.simplify(features.natural_frequency - sp.sqrt(k / m)) == 0

def test_first_order_equation_warning():
    eq = "diff(x(t), t) + x(t) = 0"

    report = analyze_equation(eq)

    assert report.validation.is_supported is False
    assert report.classification.order == 1


def test_nonlinear_equation_warning():
    eq = "diff(x(t), t, 2) + x(t)**2 = 0"

    report = analyze_equation(eq)

    assert report.validation.is_supported is False
    assert report.classification.is_linear is False


def test_time_dependent_coeff_warning():
    eq = "diff(x(t), t, 2) + t*diff(x(t), t) + x(t) = 0"

    report = analyze_equation(eq)

    assert report.validation.is_supported is False
    assert report.classification.has_constant_coefficients is False