# Rule Engine Philosophy

## Why Rules Exist

The platform should not ask AI to infer product fit, backup capability, expansion viability, or installation implications from vague prompts. Those judgments should emerge from explicit compatibility rules and deterministic calculations.

## Desired Rule Characteristics

- Rules should produce structured outputs, not prose-only results.
- Rules should explain why a condition matters.
- Rules should suggest remedy paths and associated tradeoffs.
- Rules should separate hard blockers from guidance and cautionary signals.

## Current Status

The scaffold includes a compatibility explanation structure:

- `issue`
- `why_it_matters`
- `possible_solutions`
- `tradeoff`
- `severity`
- `category`

This is the contract future rule evaluators should honor.

