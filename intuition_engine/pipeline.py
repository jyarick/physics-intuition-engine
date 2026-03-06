from intuition_engine.schemas import AnalysisReport
from intuition_engine.parser import parse_equation
from intuition_engine.classifier import classify_equation
from intuition_engine.validation import validate_classification
from intuition_engine.extractors import extract_features
from intuition_engine.regimes import build_regime_insights
from intuition_engine.explain import build_full_summaries
from intuition_engine.scaling import extract_scaling_features

def analyze_equation(equation_str: str) -> AnalysisReport:
    """
    End-to-end analysis pipeline for the v1 Physics Intuition Engine.
    """
    parsed = parse_equation(equation_str)
    classification = classify_equation(parsed)
    validation = validate_classification(classification)
    features = extract_features(parsed)
    scaling = extract_scaling_features(features)
    regimes = build_regime_insights(features)
    math_summary, physics_summary = build_full_summaries(
        parsed=parsed,
        classification=classification,
        features=features,
        regimes=regimes,
    )

    return AnalysisReport(
        parsed=parsed,
        classification=classification,
        validation=validation,
        features=features,
        scaling=scaling,
        regimes=regimes,
        math_summary=math_summary,
        physics_summary=physics_summary,
    )