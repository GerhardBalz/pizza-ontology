# Pizza calculation artifact

This directory provides the source-owned semantic artifacts for the ESKA execution mode:

```text
Calculation → calculate
```

The example asks a deliberately small mathematical question:

> Given a circular Pizza diameter in centimetres, what is its area in square centimetres?

## Formula

[`pizza-area.openmath.xml`](pizza-area.openmath.xml) represents the formula in OpenMath:

```text
areaSquareCentimetres = π × (diameterCm / 2)²
```

The formula uses the official OpenMath content-dictionary symbols:

- `nums1:pi`
- `arith1:times`
- `arith1:divide`
- `arith1:power`

The formula contains no example Pizza identifiers and no Python-specific calculation logic.

## Domain grounding

[`calculation-vocabulary.ttl`](calculation-vocabulary.ttl) connects the mathematical variable and result to Pizza-domain engineering semantics:

```text
calc:diameterCentimetres
calc:areaSquareCentimetres
```

Both are decimal-valued properties; their names and descriptions make the expected units explicit.

This keeps the mathematical structure and domain interpretation separate:

```text
OpenMath formula
    mathematical semantics
        +
Pizza calculation vocabulary
    domain meaning / units
        ↓
source-owned calculation contract
```

## Canonical cases

[`data/cases.json`](data/cases.json) provides three deterministic cases:

| Diameter | Expected area |
| ---: | ---: |
| 20 cm | 314.159265 cm² |
| 30 cm | 706.858347 cm² |
| 40 cm | 1256.637061 cm² |

Expected values are compared at six decimal places.

## Verification

Run:

```bash
python artifacts/calculations/evaluate_calculation.py
```

The regression evaluator intentionally supports only the OpenMath subset used by this artifact:

- `OMOBJ`, `OMA`, `OMS`, `OMV`, `OMI`;
- `nums1:pi`;
- `arith1:times`, `arith1:divide`, `arith1:power`.

It verifies the OpenMath version/content-dictionary base, allowed symbol set, required `diameterCm` variable, calculation vocabulary, and all canonical numeric results.

The evaluator is a regression harness for this semantic artifact, not a general OpenMath engine.

## Architectural boundary

```text
pizza-ontology
    owns OpenMath formula + calculation vocabulary + canonical cases
        ↓ immutable commit + artifacts/manifest.ttl
ESKA
    owns Semantic Capability + calculation execution architecture
```

The historical Pizza Ontology 2.0 source is not modified by this calculation example.
