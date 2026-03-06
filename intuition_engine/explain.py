import sympy as sp

from intuition_engine.schemas import (
    ParsedEquation,
    EquationClassification,
    ExtractedFeatures,
    RegimeInsight,
)


def _fmt(expr) -> str:
    """
    Safe string formatter for SymPy expressions / None values.
    """
    if expr is None:
        return "None"
    return sp.sstr(expr)


def build_math_summary(
    parsed: ParsedEquation,
    classification: EquationClassification,
    features: ExtractedFeatures,
    regimes: list[RegimeInsight],
) -> str:
    """
    Build a compact technical summary of the equation structure and extracted features.
    """
    lines = []

    lines.append("Mathematical Summary")
    lines.append("--------------------")
    lines.append(f"Canonical form: {_fmt(parsed.canonical_expr)} = 0")
    lines.append(f"Order: {classification.order}")
    lines.append(f"Linear: {classification.is_linear}")
    lines.append(f"Constant coefficients: {classification.has_constant_coefficients}")
    lines.append(f"Forced: {classification.is_forced}")
    lines.append(f"Recognized family: {classification.family}")

    lines.append("")
    lines.append("Extracted coefficients:")
    lines.append(f"  a = {_fmt(features.a)}")
    lines.append(f"  b = {_fmt(features.b)}")
    lines.append(f"  c = {_fmt(features.c)}")
    lines.append(f"  forcing = {_fmt(features.forcing)}")

    lines.append("")
    lines.append("Derived quantities:")
    lines.append(f"  discriminant = {_fmt(features.discriminant)}")
    lines.append(f"  natural_frequency = {_fmt(features.natural_frequency)}")
    lines.append(f"  damping_ratio = {_fmt(features.damping_ratio)}")
    lines.append(f"  damping_timescale = {_fmt(features.damping_timescale)}")
    lines.append(f"  forcing_frequency = {_fmt(features.forcing_frequency)}")
    lines.append(f"  characteristic_polynomial = {_fmt(features.characteristic_polynomial)}")
    lines.append(f"  roots = {_fmt(features.roots)}")

    if classification.notes:
        lines.append("")
        lines.append("Classifier notes:")
        for note in classification.notes:
            lines.append(f"  - {note}")

    if regimes:
        lines.append("")
        lines.append("Regime map:")
        for r in regimes:
            lines.append(f"  - {r.label}: if {r.condition}")

    return "\n".join(lines)


def build_physics_summary(
    parsed: ParsedEquation,
    classification: EquationClassification,
    features: ExtractedFeatures,
    regimes: list[RegimeInsight],
) -> str:
    """
    Build an intuition-first summary.
    This stays generic ('inertial-like', 'restoring-like') unless a domain overlay is added later.
    """
    lines = []

    lines.append("Physics / Intuition Summary")
    lines.append("---------------------------")

    if classification.family != "second_order_linear_constant_coeff_ode":
        lines.append(
            "This equation is not fully inside the current v1 family, so the physical interpretation may be incomplete."
        )
        return "\n".join(lines)

    a = features.a
    b = features.b
    c = features.c
    forcing = features.forcing
    wn = features.natural_frequency
    zeta = features.damping_ratio
    tau_d = features.damping_timescale
    wf = features.forcing_frequency

    lines.append(
        "The equation has the archetypal second-order balance between an inertial-like term, a dissipative term, a restoring term, and an optional external drive."
    )

    lines.append("")
    lines.append("Term roles:")
    lines.append(f"  - {_fmt(a)} * x''  -> inertial-like contribution")
    lines.append(f"  - {_fmt(b)} * x'   -> damping / dissipation-like contribution")
    lines.append(f"  - {_fmt(c)} * x    -> restoring / stiffness-like contribution")

    if forcing is not None and forcing != 0:
        lines.append(f"  - {_fmt(forcing)} -> external input / drive")
    else:
        lines.append("  - No external forcing term detected")

    if wn is not None:
        lines.append("")
        lines.append(
            f"The natural oscillation scale is set by omega_n = {_fmt(wn)}."
        )

    if zeta is not None:
        lines.append(
            f"The damping ratio zeta = {_fmt(zeta)} compares dissipation against oscillatory tendency."
        )

    if tau_d is not None:
        lines.append(
            f"A transient decay timescale is roughly tau_d ~ {_fmt(tau_d)}."
        )

    if forcing is not None and forcing != 0:
        lines.append("")
        lines.append(
            "Because the system is driven, the long-time behavior is generally a competition between transient decay and forced steady-state response."
        )

        if wf is not None and wn is not None:
            lines.append(
                f"When the drive frequency {_fmt(wf)} is far below {_fmt(wn)}, the system tends to follow the drive quasi-statically."
            )
            lines.append(
                f"When the drive frequency {_fmt(wf)} is near {_fmt(wn)}, response enhancement becomes possible."
            )
            lines.append(
                f"When the drive frequency {_fmt(wf)} is far above {_fmt(wn)}, inertia tends to suppress the displacement response."
            )

    lines.append("")
    lines.append("Behavioral interpretation:")
    for r in regimes:
        lines.append(f"  - {r.label}: {r.meaning}")

    return "\n".join(lines)


def build_full_summaries(
    parsed: ParsedEquation,
    classification: EquationClassification,
    features: ExtractedFeatures,
    regimes: list[RegimeInsight],
) -> tuple[str, str]:
    """
    Convenience wrapper returning (math_summary, physics_summary).
    """
    math_summary = build_math_summary(parsed, classification, features, regimes)
    physics_summary = build_physics_summary(parsed, classification, features, regimes)
    return math_summary, physics_summary