import sympy as sp

from intuition_engine.schemas import ExtractedFeatures, RegimeInsight


def build_regime_insights(features: ExtractedFeatures) -> list[RegimeInsight]:
    """
    Generate conditional regime-level insights from extracted features.
    Conditions are stored as SymPy relational expressions when possible.
    """
    insights: list[RegimeInsight] = []

    a = features.a
    b = features.b
    c = features.c
    forcing = features.forcing
    disc = features.discriminant
    wn = features.natural_frequency
    zeta = features.damping_ratio
    tau_d = features.damping_timescale
    wf = features.forcing_frequency

    # Damping regimes
    if disc is not None:
        insights.append(
            RegimeInsight(
                label="Overdamped regime",
                condition=disc > 0,
                meaning="Two distinct real characteristic roots; motion returns without oscillating."
            )
        )
        insights.append(
            RegimeInsight(
                label="Critical damping",
                condition=sp.Eq(disc, 0),
                meaning="Repeated real root; fastest return to equilibrium without oscillation."
            )
        )
        insights.append(
            RegimeInsight(
                label="Underdamped regime",
                condition=disc < 0,
                meaning="Complex-conjugate roots; decaying oscillations occur."
            )
        )

    # Natural scale
    if wn is not None:
        insights.append(
            RegimeInsight(
                label="Natural timescale",
                condition=sp.Eq(sp.Symbol("omega_n"), wn),
                meaning="Sets the system's intrinsic oscillation scale when damping and forcing do not dominate."
            )
        )

    # Damping strength
    if zeta is not None:
        insights.append(
            RegimeInsight(
                label="Weak damping",
                condition=sp.Symbol("zeta") < 1,
                meaning="Oscillations persist for many cycles before decaying significantly."
            )
        )
        insights.append(
            RegimeInsight(
                label="Strong damping",
                condition=sp.Symbol("zeta") > 1,
                meaning="Dissipation dominates over oscillatory behavior."
            )
        )

    # Transient decay
    if tau_d is not None:
        t = sp.Symbol("t", real=True)
        insights.append(
            RegimeInsight(
                label="Transient decay",
                condition=t > tau_d,
                meaning="Initial-condition-driven transients are strongly suppressed at late times."
            )
        )

    # Forced-response regimes
    if forcing is not None and forcing != 0 and wn is not None and wf is not None:
        insights.append(
            RegimeInsight(
                label="Low-frequency forcing",
                condition=wf < wn,
                meaning="Response tends to track the drive quasi-statically."
            )
        )
        insights.append(
            RegimeInsight(
                label="Near resonance (weak damping)",
                condition=sp.Eq(wf, wn),
                meaning="Response amplitude is enhanced because the drive matches the system's natural scale."
            )
        )
        insights.append(
            RegimeInsight(
                label="High-frequency forcing",
                condition=wf > wn,
                meaning="Inertia suppresses displacement response; the system cannot follow the drive efficiently."
            )
        )

    # Long-time forced behavior
    if forcing is not None and forcing != 0 and tau_d is not None:
        t = sp.Symbol("t", real=True)
        insights.append(
            RegimeInsight(
                label="Steady-state dominance",
                condition=t > tau_d,
                meaning="The long-time behavior is dominated by the driven steady-state response rather than the transient homogeneous solution."
            )
        )

    return insights