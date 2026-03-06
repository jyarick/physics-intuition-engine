from intuition_engine.schemas import EquationClassification, ValidationResult


def validate_classification(classification: EquationClassification) -> ValidationResult:
    """
    Validate whether the classified equation is fully supported by the current v1 engine.

    v1 target family:
        second-order linear ODE with constant coefficients
        a*x'' + b*x' + c*x = f(t)
    """
    warnings = []

    if classification.order != 2:
        warnings.append(
            f"Expected a second-order equation, but detected order {classification.order}."
        )

    if not classification.is_linear:
        warnings.append(
            "Equation is nonlinear in the dependent function or its derivatives."
        )

    if not classification.has_constant_coefficients:
        warnings.append(
            "Equation does not have constant coefficients with respect to the independent variable."
        )

    if classification.family != "second_order_linear_constant_coeff_ode":
        warnings.append(
            "Equation is outside the current v1 family: second-order linear constant-coefficient ODEs."
        )

    return ValidationResult(
        is_supported=(len(warnings) == 0),
        warnings=warnings,
    )