# Pizza Semantic Explorer

This is the first **ontology-informed UX** example in the Pizza reference project.

It demonstrates how an application can benefit from semantic knowledge without moving application-specific concerns into the ontology and without parsing OWL throughout the UI.

## Architecture

```text
Pizza Ontology 2.0
    src/ontology/pizza-edit.owl
            │
            │ OAK verifies selected source semantics
            ▼
Pizza concept projection
    projections/pizza-concepts/pizza-concepts.json
            │
            │ stable application-facing JSON contract
            ▼
Pizza Semantic Explorer
    examples/ux/pizza-explorer/
```

The UI consumes only the checked-in projection. The projection remains regression-tested against the OWL source by Track 6.

The browser therefore does **not**:

- parse the Pizza OWL ontology;
- run a reasoner;
- interpret OWL restrictions independently;
- copy selected Pizza concept definitions into JavaScript;
- treat display labels as semantic identity.

## What the UX demonstrates

The explorer provides:

- search over projected concept labels, identifiers, and topping references;
- filtering by existentially required topping;
- semantic identifiers alongside human-friendly presentation names;
- direct-superclass and required-topping views;
- optional traceability details explaining where each relationship came from;
- an explicit explanation of the difference between an existential requirement and a closed recipe.

The current projection contains only a small selected slice. The UI is intentionally generic over that slice; adding another projected concept should not require changing `app.js`.

## Semantic versus UX responsibility

### Ontology-derived / projection-provided

The UI receives these facts from `pizza-concepts.json`:

- Pizza entity CURIE and full IRI;
- selected direct named superclass relationships;
- selected `hasTopping` existential targets;
- traceability statements describing those projected relationships;
- the explicit projection-layer `displayLabel` choice.

### UX-specific

These concerns remain local to the application:

- page layout and visual design;
- search interaction;
- topping filter interaction;
- whether traceability details are expanded;
- explanatory copy;
- presentation-only humanization of CURIE local names for related entities.

Humanizing a CURIE local name is a rendering convenience, not a semantic label claim. The CURIE and IRI remain visible as the semantic identity.

## Important interpretation

`requiredToppings` is a projection of OWL existential restrictions of the form:

```text
hasTopping some X
```

For the UX, this means:

> at least one topping of type `X` is required.

It does **not** mean:

> the listed toppings are the complete set of toppings allowed on the Pizza.

Universal closure restrictions and other OWL semantics are deliberately outside this first projection.

## Run locally

From the repository root:

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/examples/ux/pizza-explorer/
```

The server must start at the repository root because the UX intentionally fetches the shared projection from `projections/pizza-concepts/` rather than maintaining a copied JSON file beside the application.

## Verify

Run:

```bash
node --check examples/ux/pizza-explorer/app.js
python examples/ux/pizza-explorer/verify_ux.py
```

The verifier checks that:

- the browser's `PROJECTION_URL` resolves to the Track 6 projection;
- projected Pizza concepts and topping identities are not hard-coded in HTML or JavaScript;
- the UI consumes the `requiredToppings`, `directSuperClasses`, and traceability contract;
- the existential topping semantics are explained explicitly;
- all static assets and the shared projection resolve through a local HTTP smoke test.

## Boundary to future work

This example is deliberately small. Future UX work can extend search, navigation, forms, explanation, or validation, but should preserve the same architecture rule:

> **Application experience may be informed by semantic knowledge without becoming a second semantic source of truth.**
