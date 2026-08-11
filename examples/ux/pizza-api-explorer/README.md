# Pizza API Explorer

This is the second ontology-informed UX specimen in the Pizza reference project and the first one with an explicit application boundary.

## Architecture

```text
Pizza Ontology 2.0
        ↓
Implementation Projections
    JSON content + OpenAPI interface
        ↓
Pizza Catalog Application
        ↓ HTTP
Pizza API Explorer
```

The browser does not load the Pizza OWL ontology and does not load `pizza-concepts.json` directly.

It uses:

```text
GET /concepts
GET /concepts/{conceptId}
GET /openapi.json     contract inspection/source facts only
```

The UX therefore depends on the **application contract**, not on the representation path of the underlying semantic projection.

## UX behavior

The explorer provides:

- search through the application's `q` query parameter;
- required-topping filtering through the application's `requiredTopping` parameter;
- list results from `GET /concepts`;
- explicit detail loading through `GET /concepts/{conceptId}`;
- semantic CURIE and IRI visibility;
- direct-superclass and existential required-topping details;
- source traceability;
- explicit explanation that `requiredToppings` is not a closed recipe.

## Application-owned versus UX-owned behavior

### Application-owned

- query matching;
- topping-filter matching;
- collection construction;
- concept lookup;
- `404` behavior;
- HTTP transport.

### UX-owned

- layout and visual design;
- when queries are issued;
- presentation-only humanization of CURIE local names;
- whether concept detail is opened;
- explanatory wording;
- interaction state.

### Semantics remain upstream

Neither application nor UX owns:

- Pizza entity identity;
- selected direct superclass semantics;
- selected existential `hasTopping` semantics.

Those facts arrive from the JSON implementation projection, which remains regression-tested to Pizza OWL through OAK.

## Comparison specimen

The existing [`../pizza-explorer/`](../pizza-explorer/) demonstrates direct projection consumption:

```text
JSON projection → UX
```

This specimen demonstrates:

```text
JSON projection + OpenAPI contract → Application → UX
```

Keeping both examples makes the architecture trade-off visible and testable rather than turning an application layer into a mandatory pattern.

## Run

Start the reference application from the repository root:

```bash
python examples/application/pizza-catalog-api/app.py --port 8001
```

Then open:

```text
http://127.0.0.1:8001/
```

## Public hosting note

The existing direct-projection explorer works on GitHub Pages because it is fully static.

This API-backed explorer requires a running HTTP application. GitHub Pages does not execute the reference Python server, so public deployment is intentionally a later deployment concern rather than part of this UX/contract slice.
