# Pizza Catalog Reference Application

## Purpose

This is the first **application-mediated** Pizza reference path.

It sits between implementation projections and UX:

```text
Pizza Ontology 2.0
    authoritative semantic model
        ↓ OAK-verified source extraction during projection build
    ┌──────────────────────────────┐
    │                              │
    ▼                              ▼
JSON content projection       OpenAPI 3.1 projection
    concrete selected data        interface contract
    │                              │
    └──────────────┬───────────────┘
                   ▼
         Pizza Catalog Application
                   ▼
           API-backed Pizza UX
```

The application does **not** parse or reason over the Pizza OWL ontology at runtime.

## Why the application consumes two projections

The two projections have different roles.

### JSON content projection

`projections/pizza-concepts/pizza-concepts.json` contains the concrete selected application-facing concept content:

- semantic CURIE and full IRI;
- selected direct superclass references;
- selected existential `hasTopping some X` targets;
- projection-owned display labels;
- traceability statements.

### OpenAPI interface projection

`projections/pizza-openapi/pizza-concepts.openapi.json` defines how an application exposes that content:

```text
GET /concepts
GET /concepts/{conceptId}
```

plus:

- query parameters;
- response envelopes;
- status codes;
- response schemas;
- identifier domains.

The application implements this checked-in contract. It does not generate a second OpenAPI document from its source code.

## Application-owned behavior

Application behavior includes:

- case-insensitive text filtering through `q`;
- filtering by projected `requiredTopping` identifier;
- concept lookup by projected CURIE;
- collection envelope construction;
- HTTP `200` / `404` behavior;
- transport and static UX serving.

Those behaviors are not ontology facts.

The application only filters and transports projected semantic content. It does not infer new semantic relationships.

## Run

From the repository root:

```bash
python examples/application/pizza-catalog-api/app.py --port 8001
```

Then open:

```text
http://127.0.0.1:8001/
```

The same application exposes:

```text
http://127.0.0.1:8001/concepts
http://127.0.0.1:8001/openapi.json
```

The `openapi.json` endpoint is an inspection convenience serving the exact checked-in OpenAPI projection; it is not a separately generated semantic/API contract.

## Verification

Install dependencies and run:

```bash
python -m pip install -r examples/application/pizza-catalog-api/requirements.txt
node --check examples/ux/pizza-api-explorer/app.js
python examples/application/pizza-catalog-api/verify_application.py
```

The verifier starts the application on an ephemeral port and checks:

- the OpenAPI projection is structurally valid;
- runtime collection, concept and error responses validate against the OpenAPI 3.1 schemas;
- unfiltered content equals the checked-in JSON content projection;
- `q` filtering is application behavior over projected content;
- `requiredTopping` filtering is based on projected existential-target identifiers;
- concept lookup returns the projected concept unchanged;
- unknown identifiers return the documented `404` shape;
- the application serves the exact checked-in OpenAPI contract;
- neither application nor API-backed UX hard-codes selected Pizza concept/topping facts;
- the application does not import OAK or access OWL at runtime;
- the API-backed UX does not bypass the application to load the JSON projection directly.

## Comparison with the direct-projection UX

The existing explorer demonstrates:

```text
JSON ImplementationProjection → UX
```

This application demonstrates:

```text
JSON ImplementationProjection
        +
OpenAPI ImplementationProjection
        ↓
Application
        ↓
UX
```

Neither is declared universally better.

A direct projection consumer is small and useful when no independent application boundary is needed. An application-mediated consumer becomes useful when runtime operations, filtering, access policy, aggregation, deployment, multiple clients, or independent lifecycle concerns justify a service/application boundary.

## Deployment boundary

This reference server is deliberately local and deterministic.

GitHub Pages can host the existing static direct-projection explorer, but it cannot execute this Python HTTP application. Public deployment of the API-backed specimen is a separate operational/deployment concern and should not be mixed into the OpenAPI semantic/interface projection itself.
