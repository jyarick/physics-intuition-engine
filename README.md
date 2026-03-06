# Physics Intuition Engine v1

A symbolic equation-reading tool for second-order linear ODEs that extracts structure, characteristic scales, regime conditions, and intuition-oriented summaries.

## Demo

![Physics Intuition Engine demo](assets/physics-intuition-engine-demo.png)

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

## Current limitations

This is a v1 tool focused on second-order linear constant-coefficient ODEs.

Known limitations:
- support is intentionally restricted to a narrow equation family
- regime thresholds are simplified in some places for clarity
- forcing-frequency detection is basic
- the current interface is notebook-based

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
│   ├── scaling.py
│   ├── validation.py
│   ├── explain.py
│   └── pipeline.py
├── notebooks/
│   └── v1_engine_playground.ipynb
├── tests/
│   └── test_v1_cases.py
├── requirements.txt
└── README.md

## Installation

```bash
python3 -m pip install -r requirements.txt
```
## Why this project exists

Many students learn how to manipulate equations without learning how to read them physically. 
This project aims to bridge that gap by turning equations into structured intuition.