# Pizza DMN decision artifact

This directory provides the source-owned semantic artifact for the ESKA execution mode:

```text
Decision → decide
```

The decision model is intentionally small. Its purpose is to test whether an explicit decision model can remain independently owned, executable, traceable, and consumable by ESKA without turning the ESKA core into a DMN-specific model.

## Decision

[`pizza-dietary-suitability.dmn`](pizza-dietary-suitability.dmn) is a DMN 1.5 `UNIQUE` decision table named `PizzaDietarySuitabilityDecision`.

Inputs:

```text
containsMeat : boolean
containsFish : boolean
```

Outcome relation and values are defined in [`decision-vocabulary.ttl`](decision-vocabulary.ttl):

```text
decision:dietarySuitability
    → decision:NotVegetarian
    → decision:PescatarianOnly
    → decision:Vegetarian
```

Decision table:

| containsMeat | containsFish | Outcome |
| --- | --- | --- |
| `true` | `-` | `decision:NotVegetarian` |
| `false` | `true` | `decision:PescatarianOnly` |
| `false` | `false` | `decision:Vegetarian` |

The `UNIQUE` hit policy means a valid input context must select exactly one rule.

## Why DMN?

The preceding Pizza execution mode used a SPARQL `CONSTRUCT` rule to derive a graph statement. This artifact instead models an explicit **decision with named inputs and a selected outcome**.

```text
Rule
    evaluate matching graph pattern
    → derive statement

Decision
    evaluate explicit decision inputs
    → select one outcome
```

The distinction is important for the ESKA falsification exercise.

## Test cases

[`data/cases.json`](data/cases.json) supplies three explicit contexts so every outcome is exercised:

```text
meatyPizza
    containsMeat = true
    containsFish = false
    → NotVegetarian

fishPizza
    containsMeat = false
    containsFish = true
    → PescatarianOnly

vegetarianPizza
    containsMeat = false
    containsFish = false
    → Vegetarian
```

These are **decision inputs**, not OWL inferences. The decision evaluator does not inspect the Pizza ontology to infer whether meat or fish is present.

## Execute

From the repository root:

```bash
python artifacts/decisions/evaluate_decision.py
```

The deterministic evaluator supports only the deliberately small DMN 1.5 subset used here:

- one `UNIQUE` decision table;
- boolean input expressions;
- unary tests `true`, `false`, and `-`;
- one string-valued output containing a semantic outcome IRI.

It verifies the model structure, requires exactly one matching rule for every case, checks all expected semantic outcomes, and writes generated results below `artifacts/decisions/results/`.

The evaluator is a regression harness for this canonical artifact, not a claim to implement the complete DMN specification.

## Repository boundary

```text
pizza-ontology
    owns DMN decision model
    owns outcome vocabulary
    owns canonical decision cases
        ↓ immutable commit + artifacts/manifest.ttl
ESKA
    binds/evaluates decision
        ↓
SemanticCapability
→ Execution
→ Result
→ Verification
→ PROV-O
```

The historical Pizza Ontology 2.0 source is not modified by this decision artifact.
