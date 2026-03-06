from dataclasses import dataclass, field
from typing import Optional, List, Any
import sympy as sp


@dataclass
class ParsedEquation:
    raw_input: str
    lhs: sp.Expr
    rhs: sp.Expr
    canonical_expr: sp.Expr          # lhs - rhs
    dependent_function: sp.Function
    independent_variable: sp.Symbol


@dataclass
class EquationClassification:
    order: Optional[int]
    is_linear: bool
    has_constant_coefficients: bool
    is_forced: bool
    family: Optional[str]
    notes: List[str] = field(default_factory=list)


@dataclass
class ExtractedFeatures:
    a: Optional[sp.Expr] = None
    b: Optional[sp.Expr] = None
    c: Optional[sp.Expr] = None
    forcing: Optional[sp.Expr] = None
    discriminant: Optional[sp.Expr] = None
    natural_frequency: Optional[sp.Expr] = None
    damping_ratio: Optional[sp.Expr] = None
    damping_timescale: Optional[sp.Expr] = None
    forcing_frequency: Optional[sp.Expr] = None
    characteristic_polynomial: Optional[sp.Expr] = None
    roots: Optional[List[sp.Expr]] = None


@dataclass
class RegimeInsight:
    label: str
    condition: Any
    meaning: str

@dataclass
class ValidationResult:
    is_supported: bool
    warnings: List[str] = field(default_factory=list)

@dataclass
class ScalingFeatures:
    natural_frequency: Optional[sp.Expr] = None
    damping_ratio: Optional[sp.Expr] = None
    forcing_ratio: Optional[sp.Expr] = None
    notes: List[str] = field(default_factory=list)

@dataclass
class AnalysisReport:
    parsed: ParsedEquation
    classification: EquationClassification
    validation: ValidationResult
    features: ExtractedFeatures
    scaling: ScalingFeatures
    regimes: List[RegimeInsight]
    math_summary: str
    physics_summary: str