# Pizza semantic mapping

This directory contains the source-owned artifacts for the ESKA execution mode:

```text
Mapping → transform
```

The example deliberately distinguishes **source semantic model**, **mapping semantics**, and **target semantic model**.

## Source and target

The source graph uses the historical Pizza vocabulary:

```text
pizza:Pizza
rdfs:label
pizza:hasTopping
```

The target graph uses the repository-authored Menu projection vocabulary:

```text
menu:MenuItem
menu:displayName
menu:ingredientName
```

The target vocabulary is defined in [`menu-vocabulary.ttl`](menu-vocabulary.ttl).

## Mapping artifact

[`pizza-to-menu.rq`](pizza-to-menu.rq) is a SPARQL 1.1 `CONSTRUCT` mapping. It reads the source Pizza RDF graph and constructs a new graph in the Menu projection vocabulary.

This is intentionally different from the existing Pizza rule artifact:

```text
Rule
    source-domain graph
        ↓ derive
    additional source-domain statement

Mapping
    source semantic model
        ↓ transform
    target semantic model
```

The mapping preserves the Pizza item identity but replaces source-domain classes and predicates with the target projection vocabulary. Topping entities become target-language ingredient-name literals.

## Canonical data

[`data/source-pizzas.ttl`](data/source-pizzas.ttl) contains two explicit Pizza source instances.

[`data/expected-menu.ttl`](data/expected-menu.ttl) is the canonical target graph.

The expected transformation is:

```text
Pizza RDF
    American Hot + Jalapeno Pepper
    Margherita + Mozzarella
        ↓ SPARQL CONSTRUCT
Menu RDF
    MenuItem + displayName + ingredientName
```

## Execute

```bash
python -m pip install -r artifacts/mappings/requirements.txt
python artifacts/mappings/evaluate_mapping.py
```

The regression harness:

1. parses the source RDF graph;
2. parses the target Menu semantic model;
3. executes the source-owned SPARQL mapping artifact;
4. compares the transformed graph with the canonical expected target graph;
5. verifies that Pizza classes and Pizza predicates do not leak into the target graph;
6. writes the generated target graph under `results/`.

The evaluator does not duplicate the mapping logic in Python; the transformation semantics remain in the SPARQL artifact.

## Architectural purpose

The source repository owns all domain-specific mapping semantics and test data. ESKA consumes them through an immutable commit binding and decides how source, target, and mapping semantic roles participate in a bounded Semantic Capability.

This is intended to test whether the generic ESKA core can remain small while role-specific mapping semantics stay in a mapping-specific layer until repeated cross-mode evidence justifies broader abstraction.
