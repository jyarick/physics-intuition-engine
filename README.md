# Physics Intuition Engine v1

A symbolic physics interpretation tool that reads second-order linear ODEs, extracts their structure, identifies characteristic scales and regimes, and generates intuition-oriented summaries.

## What it does

Given an equation such as

$$
m\ddot{x} + b\dot{x} + kx = F_0 \cos(\omega t),
$$

the engine:

- parses the equation into canonical form
- classifies its mathematical structure
- extracts coefficients and forcing terms
- computes characteristic quantities such as
  - discriminant
  - natural frequency
  - damping ratio
  - damping timescale
- identifies regime conditions such as
  - overdamped
  - critically damped
  - underdamped
  - low-frequency forcing
  - near resonance
  - high-frequency forcing
- generates both
  - a mathematical summary
  - a physics / intuition summary

## Current v1 scope

This version is intentionally scoped to:

$$
a\,x'' + b\,x' + c\,x = f(t)
$$

with emphasis on **second-order linear constant-coefficient ODEs**.

Supported examples include:

- undamped oscillator
- damped oscillator
- driven damped oscillator
- constant forcing cases

The engine also provides validation warnings when an equation falls outside the current supported family.

## Project structure

```text
physics_intuition_engine/
├── intuition_engine/
│   ├── __init__.py
│   ├── schemas.py
│   ├── examples.py
│   ├── parser.py
│   ├── classifier.py
│   ├── extractors.py
│   ├── regimes.py
│   ├── validation.py
│   ├── explain.py
│   └── pipeline.py
├── notebooks/
│   └── v1_engine_playground.ipynb
├── tests/
│   └── test_v1_cases.py
├── requirements.txt
└── README.md