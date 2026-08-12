# Pizza Concept Semantic Projection

## Purpose

This is the first implementation-oriented projection from the preserved Pizza Ontology 2.0 semantic model.

It provides a deliberately small JSON representation for application and UX consumption while preserving a strict boundary:

```text
Pizza Ontology 2.0
    authoritative semantic model
        ↓ selected graph projection through OAK
Pizza concept JSON projection
    implementation representation
        ↓
applications / UX
```

The JSON is **not** the ontology, not a new ontology version, and not a competing semantic source of truth.

## Scope

The first projection contains two named Pizza classes:

- `pizza:AmericanHot`
- `pizza:Margherita`

They are intentionally small but useful enough to exercise hierarchy and topping relationships for a later ontology-informed UX example.

## Files

```text
projections/pizza-concepts/
├── profile/
├── projection-config.json
├── projection.schema.json
├── pizza-concepts.json
├── project.py
├── requirements.txt
└── README.md
```

`projection-config.json` selects the source entities and application-facing display labels.

`projection.schema.json` defines the implementation contract.

`pizza-concepts.json` is the checked-in projection.

`project.py` regenerates the projection from the repository-owned Pizza source through OAK and verifies the checked-in JSON against current source semantics.

`profile/` defines and executes the explicit projection/preservation profile for this non-authoritative implementation projection.

## Projection rules

The projection records its semantic treatment explicitly.

| Pizza semantic source | JSON projection | Treatment |
|---|---|---|
| historical entity IRI | `id` + `iri` | identity preserved; CURIE added as implementation convenience |
| asserted named `SubClassOf` | `directSuperClasses` | selected relation preserved in graph form |
| `hasTopping some Topping` | `requiredToppings` | OWL existential restriction flattened through OAK graph projection |
| application display text | `displayLabel` | introduced by projection configuration |
| universal topping closure | not represented | omitted |
| country-of-origin restrictions | not represented | omitted |
| inferred classifications | not represented | omitted |
| disjointness | not represented | omitted |
| property characteristics | not represented | omitted |
| unrelated annotations/axioms | not represented | omitted |

The name `requiredToppings` is intentional. It represents existential restrictions such as:

```text
hasTopping some JalapenoPepperTopping
```

It must not be interpreted as a complete closed list of every allowed topping. Pizza 2.0 also contains universal restrictions that this first projection deliberately does not carry across.

## Display labels

`displayLabel` is explicitly owned by the projection layer.

This avoids turning a backend-specific choice among multilingual `rdfs:label` values into an accidental application contract. The source ontology remains free to contain its historical labels and SKOS annotations; the projection chooses application-facing display text independently and records that choice as `displayLabelSource: projection-config`.

## Traceability and regression

The source is always:

```text
src/ontology/pizza-edit.owl
```

The generator uses the established OAK Functional-Syntax access boundary. Because the historical editor file keeps a `.owl` filename while containing OWL Functional Syntax, the script creates a temporary byte-identical `.ofn` copy as a syntax hint. That temporary file is not a repository semantic artifact.

Run:

```bash
python -m pip install -r projections/pizza-concepts/requirements.txt
python projections/pizza-concepts/project.py --check
```

The check:

1. reads the current Pizza source ontology;
2. projects selected superclass and `hasTopping` relationships through OAK;
3. validates the generated JSON against `projection.schema.json`;
4. compares the generated representation with the checked-in `pizza-concepts.json`;
5. fails if the projection assumptions drift from the current source semantics.

To intentionally regenerate the projection after reviewing a source or projection-policy change:

```bash
python projections/pizza-concepts/project.py --write
```

A changed generated JSON file is therefore an explicit projection change requiring review; it is not silently treated as an ontology change.

## Projection/preservation profile

The optional machine-readable preservation evidence for this projection lives in `profile/`.

It makes the existing projection policy executable without changing `pizza-concepts.json`. The profile explicitly separates:

- selected OWL semantics that must be preserved;
- transformations that are permitted;
- source semantics that may be omitted;
- implementation information that may be introduced;
- JSON representation validation;
- RDF evidence-graph validation and provenance.

Run the full profile proving ground with:

```bash
python -m pip install -r projections/pizza-concepts/profile/requirements.txt
python projections/pizza-concepts/profile/verify_profile.py
```

See `profile/README.md` for the PROF, DCTERMS, SHACL, ESKA, and PROV-O responsibility boundaries and the required negative control.

## Architectural evidence

This implementation provides concrete evidence for the provisional cross-cutting concept **Projection**:

```text
source semantic model
    Pizza Ontology 2.0
        ↓ explicit projection policy
implementation representation
    PizzaConceptCatalog JSON
```

It also demonstrates why source and target semantic roles should remain explicit. The source is an OWL semantic model; the target is an implementation representation with a narrower contract and deliberately omitted semantics.

No generic Semantic Modeling ontology is introduced here. The implementation is evidence to harvest later if the same abstraction proves reusable across additional projections.

## Relationship to UX

Track 7 / issue #17 should consume `pizza-concepts.json` (or regenerate the same contract) rather than parse Pizza OWL independently inside UI code.

That keeps the boundary explicit:

```text
OWL / OAK
    ↓
semantic projection
    ↓
UX
```

The UX can add interaction, presentation, search behavior, and application state without pushing those concerns back into Pizza Ontology 2.0.
