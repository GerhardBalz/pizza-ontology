# Pizza OpenAPI Semantic Projection

## Purpose

This is the second implementation projection from the preserved Pizza Ontology 2.0 semantic model.

It targets an **OpenAPI 3.1 application contract** rather than a checked-in concept catalog:

```text
Pizza Ontology 2.0
    authoritative semantic model
        ↓ shared OAK-verified source extraction
selected Pizza semantic slice
        ↓ target-specific projection policy
OpenAPI 3.1 application contract
        ↓
API implementation / clients
```

The OpenAPI document is **not** the ontology, not a new ontology version, and not a competing semantic source of truth.

## Files

```text
projections/
├── common/
│   └── pizza_source.py
├── pizza-concepts/
│   ├── projection-config.json
│   ├── projection.schema.json
│   ├── pizza-concepts.json
│   └── project.py
└── pizza-openapi/
    ├── openapi-config.json
    ├── pizza-concepts.openapi.json
    ├── project.py
    ├── requirements.txt
    └── README.md
```

`projections/common/pizza_source.py` owns the reusable OAK source-access boundary. Both implementation projections use it, so target-specific code does not duplicate OWL interpretation logic.

`openapi-config.json` contains API-projection identity and API-specific path/title choices.

`pizza-concepts.openapi.json` is the checked-in OpenAPI 3.1 contract.

`project.py` regenerates and validates that contract against the current Pizza source ontology.

## Why this target is materially different

The first projection in `projections/pizza-concepts/` is **content-first**:

```text
selected OWL semantics
    ↓
checked-in JSON concept catalog
```

It carries concrete projected concept records for application consumption.

This second projection is **schema/interface-first**:

```text
selected OWL semantics
    ↓
OpenAPI paths + response schemas + identifier domains
```

It specifies an interface that an implementation can expose. It does not embed the complete projected concept catalog as response examples.

This difference is intentional because the architecture experiment is not "can we serialize the same JSON twice?" It is whether a stable projection contract survives across different target responsibilities.

## Semantic fields

The API response schema carries the same selected semantic boundary as the first projection:

- Pizza concept CURIE;
- historical Pizza entity IRI;
- application-facing display label;
- selected direct named superclass references;
- selected `hasTopping some X` existential targets;
- traceability statements describing where those projected relations came from.

`requiredToppings` still means:

```text
hasTopping some X
```

or, operationally:

> at least one topping of type `X` is required.

It does **not** mean that the listed toppings form a closed or complete recipe.

## API-owned concerns

The following are introduced by the OpenAPI projection and are **not Pizza ontology semantics**:

- `/concepts` and `/concepts/{conceptId}` paths;
- HTTP `GET` operations;
- `q` and `requiredTopping` query parameters;
- `200` and `404` response contracts;
- collection and error envelopes;
- OpenAPI operation identifiers;
- JSON Schema implementation structure.

The projection deliberately contains no `servers` entry. Runtime host/base URL/deployment binding is a separate operational concern and should not be confused with the semantic or API contract.

## Source-derived API constraints

The current OpenAPI contract includes source-verified identifier domains:

```text
PizzaConceptId
    pizza:AmericanHot
    pizza:Margherita

ToppingId
    union of topping targets actually projected from those selected concepts
```

These enums are not maintained by hand. `project.py --check` rebuilds them from Pizza OWL through the shared OAK extraction boundary and fails if the checked-in OpenAPI contract drifts.

## Projection policy

The OpenAPI document records the projection policy in the `x-pizza-projection` extension.

### Preserved

- historical Pizza entity IRIs;
- selected asserted named superclass relationships;
- selected `hasTopping` existential relationship targets.

### Transformed

- OWL identifiers become CURIE + full IRI fields;
- selected OWL relationships become response-schema fields;
- existential restrictions become `requiredToppings` references.

### Introduced

- application display-label choice;
- HTTP paths and operations;
- query parameters;
- response status/envelope structure;
- OpenAPI / JSON Schema interface structure.

### Omitted

- universal topping closure restrictions;
- country-of-origin restrictions;
- inferred classifications;
- disjointness;
- object-property characteristics and broader OWL axioms;
- unrelated annotations;
- runtime deployment/server location.

## Validation

Install dependencies and run:

```bash
python -m pip install -r projections/pizza-openapi/requirements.txt
python projections/pizza-openapi/project.py --check
```

The verifier:

1. reads the shared Pizza projection selection configuration;
2. extracts the selected semantic slice directly from `src/ontology/pizza-edit.owl` through OAK;
3. builds the OpenAPI 3.1 contract;
4. validates it with `openapi-spec-validator`;
5. verifies source-derived concept and topping identifier domains;
6. verifies that runtime deployment information has not leaked into the contract;
7. compares the generated contract with `pizza-concepts.openapi.json`.

To intentionally regenerate after reviewing a projection-policy or source-selection change:

```bash
python projections/pizza-openapi/project.py --write
```

## Comparison with the first projection

The two implementation targets now provide the following evidence.

| Concern | JSON concept catalog | OpenAPI contract | Common? |
|---|---|---|---|
| explicit source semantic model | yes | yes | **yes** |
| shared source selection | yes | yes | **yes** |
| source access through OAK | yes | yes | **yes** |
| preserve entity identity | yes | yes | **yes** |
| select superclass semantics | yes | yes | **yes** |
| select existential topping semantics | yes | yes | **yes** |
| explicit preserved/transformed/introduced/omitted policy | yes | yes | **yes** |
| source-regression check | yes | yes | **yes** |
| target remains non-authoritative | yes | yes | **yes** |
| checked-in concept content | yes | no | target-specific |
| JSON Schema catalog contract | yes | embedded differently | target-specific |
| HTTP paths/operations/status | no | yes | target-specific |
| query/filter interface | no | yes | target-specific |

## Architecture finding

Two materially different targets now support a stable **implementation-projection pattern**:

```text
source semantic model
    ↓ explicit source selection
source-verified semantic slice
    ↓ explicit semantic-loss / transformation policy
implementation projection
    ↓ target-specific contract
consumer
```

The common invariants are stronger than after the first projection alone:

1. source semantic identity is explicit;
2. selected semantics are explicit;
3. semantic preservation/transformation/omission is explicit;
4. target-specific additions are explicit;
5. traceability to the source remains machine-verifiable;
6. the target does not become a second semantic authority.

However, this does **not** yet justify using the unqualified generic word `Projection` for every semantic transformation. ESKA Mapping still demonstrates a materially different pattern:

```text
implementation projection
    semantic model → narrower application representation/contract

semantic transformation / Mapping
    source semantic model → mapping semantics → target semantic model
```

The evidence therefore strengthens **Implementation Projection** as a candidate reusable Semantic Modeling concept while preserving the #51 caution around a generic `Projection` class.

## Boundary to future architecture work

This issue intentionally does not create a Semantic Modeling ontology.

The next Track 9 reassessment can now ask whether the pair:

```text
SemanticModel
ImplementationProjection
```

is sufficiently precise and useful to justify the first small reusable Semantic Modeling vocabulary, while leaving Mapping/Transformation semantics and PROV-O role machinery outside that core.
