from intuition_engine.ode.schemas import EquationClassification, ValidationResult


def validate_classification(classification: EquationClassification) -> ValidationResult:
    if classification.family is not None:
        return ValidationResult(is_supported=True, warnings=[])
    warnings = []
    if classification.order not in (1, 2):
        warnings.append(f"Expected a first- or second-order equation, but detected order {classification.order}.")
    if not classification.is_linear:
        warnings.append("Equation is nonlinear in the dependent function or its derivatives.")
    if not classification.has_constant_coefficients:
        warnings.append("Equation does not have constant coefficients with respect to the independent variable.")
    if classification.family is None:
        warnings.append("Equation is outside the currently recognized families of the engine.")
    return ValidationResult(is_supported=False, warnings=warnings)
