# ReDroid-AI — Phase 2

Phase 2 enriches Phase 1 static analysis output with
security-focused reasoning and risk assessment.

## Goals
- Convert raw static signals into meaningful findings
- Apply deterministic security rules before AI reasoning
- Produce analyst-style explanations and risk scores

## Components
- engine/   : Orchestrates Phase 2 analysis
- rules/    : Security heuristics and detection logic
- schemas/  : JSON input/output contracts
- ai/       : AI-based reasoning (later stage)

Phase 2 consumes Phase 1 JSON and outputs
risk-enriched, explainable results.