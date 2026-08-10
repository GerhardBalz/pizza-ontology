# Canonical coherent Pizza reasoning module

This directory is the repository-owned **Track 4 — Reason** artifact for Pizza Ontology 2.0.

The historical ontology is intentionally preserved unchanged and contains unsatisfiable tutorial classes. The artifact here is therefore a **derived coherent module**, not a replacement ontology and not a repaired Pizza 2.0.

## Semantic question

Can OWL reasoning infer:

```text
AmericanHot SubClassOf SpicyPizza
```

without asserting that classification directly?

The module contains the semantic chain needed for the inference:

```text
AmericanHot
    ├── SubClassOf NamedPizza
    │       └── SubClassOf Pizza
    │
    └── hasTopping some JalapenoPepperTopping
            │
            ├── SubClassOf PepperTopping
            │       └── SubClassOf PizzaTopping
            │
            └── hasSpiciness some Hot

SpicyTopping ≡
    PizzaTopping
    and hasSpiciness some Hot

SpicyPizza ≡
    Pizza
    and hasTopping some SpicyTopping
```

HermiT can therefore derive:

```text
AmericanHot SubClassOf SpicyPizza
```

## Asserted versus inferred

The regression is deliberately two-sided:

1. `verify-not-asserted.sparql` proves the classification is **not asserted** in the module.
2. HermiT classifies the module.
3. `verify-spicy.sparql` proves the classification is present in the **reasoned artifact**.
4. ROBOT produces an explanation for the inferred axiom.

This makes the knowledge status explicit rather than presenting asserted and derived knowledge as equivalent.

## Provenance

The module is derived from the preserved source:

```text
src/ontology/pizza-edit.owl
```

The runner pins that source to Git blob:

```text
397492e484de5560f8a7e048ce8999b707d94388
```

If the source blob changes, the reasoning runner fails until the module and its provenance are reviewed explicitly.

Machine-readable provenance is in [`provenance.ttl`](provenance.ttl).

The semantic content copied/selected from Pizza Ontology 2.0 retains its upstream **CC BY 3.0** licensing and attribution boundary.

## Run

Requirements:

- Java 17+
- `curl`
- `git`

From the repository root:

```bash
bash artifacts/reasoning/run.sh
```

The runner pins ROBOT 1.9.10 and uses HermiT.

Generated files are written below `artifacts/reasoning/results/` and are not committed.

## Architectural boundary

```text
Pizza Ontology 2.0
    full preserved teaching ontology
            │
            │ selected semantic knowledge
            ▼
coherent reasoning module
            │
            │ OWL reasoning
            ▼
HermiT
            │
            ├── inferred classification
            ├── verification
            └── explanation
```

The coherent module is a stable **domain semantic artifact** owned by `pizza-ontology`. Downstream projects such as ESKA may consume it, but should not become the accidental owner of the Pizza semantics it contains.
