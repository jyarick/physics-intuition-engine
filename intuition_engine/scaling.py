import sympy as sp

from intuition_engine.schemas import ExtractedFeatures, ScalingFeatures


def extract_scaling_features(features: ExtractedFeatures) -> ScalingFeatures:
    """
    Extract key dimensionless/scaling quantities for the v1 equation family.

    Target quantities:
      omega_n = sqrt(c/a)
      zeta    = b / (2*sqrt(a*c))
      r       = omega_forcing / omega_n
    """
    wn = features.natural_frequency
    zeta = features.damping_ratio
    wf = features.forcing_frequency

    forcing_ratio = None
    notes = []

    if wn is not None:
        notes.append("Natural frequency sets the intrinsic oscillation scale.")

    if zeta is not None:
        notes.append("Damping ratio compares dissipative strength to oscillatory tendency.")

    if wf is not None and wn is not None:
        forcing_ratio = sp.simplify(wf / wn)
        notes.append("Forcing ratio compares the drive frequency to the system's natural frequency.")

        notes.append("If forcing_ratio << 1, response is quasi-static.")
        notes.append("If forcing_ratio ~ 1, the system is in the resonance region.")
        notes.append("If forcing_ratio >> 1, inertia suppresses the displacement response.")

    return ScalingFeatures(
        natural_frequency=wn,
        damping_ratio=zeta,
        forcing_ratio=forcing_ratio,
        notes=notes,
    )