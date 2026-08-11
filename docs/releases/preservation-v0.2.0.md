# preservation-v0.2.0

## Second preservation and reference-architecture release

`preservation-v0.2.0` is the second repository preservation release of `GerhardBalz/pizza-ontology`.

It is a **repository preservation / engineering release**, not a new semantic version of the historical Pizza ontology.

## Semantic baseline

This release continues to preserve **Pizza Ontology 2.0** unchanged:

```text
Ontology IRI
http://www.co-ode.org/ontologies/pizza

Version IRI
http://www.co-ode.org/ontologies/pizza/2.0.0

owl:versionInfo
2.0

Entity namespace
http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

No Pizza 2.1, Pizza 3.0, replacement ontology identity, or new authority over the historical `co-ode.org` namespace is claimed.

## What changed since preservation-v0.1.0

`preservation-v0.1.0` established the conservative source-preservation baseline. This release adds the broader engineering and semantic-architecture reference layers built around that unchanged baseline.

### Preservation distributions

The release publishes the first complete preservation-safe multi-format ontology distribution set:

```text
pizza-2.0-preserved.ofn
pizza-2.0-preserved.ttl
SHA256SUMS
```

The release workflow verifies that:

- the Functional Syntax artifact is byte-identical to the preserved editor ontology;
- Turtle remains graph-equivalent to the preserved source according to ROBOT;
- historical ontology IRI, version IRI, `owl:versionInfo`, and entity namespace remain present;
- no unowned OBO-style Pizza release IRI is introduced;
- checksums cover both ontology distributions.

These are distribution representations of Pizza Ontology 2.0. They do not introduce a new semantic Pizza version.

### OAK access and query reference

Track 3 now includes both a minimal `pizza:AmericanHot` vertical slice and broader OAK exploration/query examples covering:

- CURIE / full-IRI identity and labels;
- direct named superclass relationships;
- transitive is-a ancestry;
- selected `hasTopping` relationship projection;
- descendant traversal;
- asserted direct-child inspection;
- explicit probing of backend-dependent lexical-search capability.

The examples keep OAK graph access distinct from OWL reasoning.

### Reasoning and validation

The repository includes independently executable reference artifacts for:

- OWL / HermiT reasoning;
- SHACL / pySHACL validation.

The two intentional Pizza tutorial unsatisfiable classes remain preserved and regression-tested.

### Seven source-owned executable semantic modes

The Pizza repository now publishes source-owned semantic artifacts for:

```text
Ontology    → reason
Constraint  → validate
Rule        → evaluate
Decision    → decide
Calculation → calculate
Mapping     → transform
Workflow    → execute
```

`artifacts/manifest.ttl` is the machine-readable consumer contract for the twenty-three semantic distributions used by the companion ESKA reference.

### Publication and governance

The repository now has an explicit preservation publication/distribution policy distinguishing:

```text
semantic identifier
repository release
source revision
distribution
publication/access/download location
```

GitHub Release pages are repository preservation publication records. Direct GitHub Release assets are distribution locations. Neither replaces the historical Pizza ontology or version IRI.

`preservation-v0.1.0` remains unchanged. The new `.ttl` distribution is published first in this release because it was engineered after the v0.1.0 source snapshot.

### Implementation Projections

Two source-verified application-facing projections are now implemented over a shared OAK source-extraction boundary.

#### JSON content Implementation Projection

`projections/pizza-concepts/` provides selected concrete Pizza concept content in JSON with a JSON Schema contract.

#### OpenAPI interface Implementation Projection

`projections/pizza-openapi/` provides an OpenAPI 3.1 interface contract for the same selected semantic slice while keeping HTTP paths, operations, parameters, response envelopes, and status semantics explicitly application-owned.

Both document semantics that are preserved, transformed, introduced, and omitted, and both remain regression-tested against the Pizza OWL source.

### Ontology-informed UX

Two comparable experience paths are now demonstrated.

Direct projection consumption:

```text
Pizza OWL
    ↓
JSON ImplementationProjection
    ↓
Pizza Semantic Explorer
```

The static explorer is published through GitHub Pages.

Application-mediated consumption:

```text
Pizza OWL
    ↓
JSON content + OpenAPI interface ImplementationProjections
    ↓
Pizza Catalog Application
    ↓ HTTP
API-backed Pizza Explorer
```

The deterministic application does not parse OWL, run OAK, or recreate Pizza semantics at runtime. It transports and filters already-projected semantic content according to the checked-in OpenAPI contract.

### Semantic Modeling architecture

The implemented tracks provide evidence for the reusable conceptual pair:

```text
SemanticModel
ImplementationProjection
```

`ImplementationProjection` is deliberately narrower than semantic Mapping / Transformation. Distribution and provenance concerns continue to reuse DCAT, Dublin Core Terms, and PROV-O rather than introducing parallel Pizza-specific vocabulary.

A separate Semantic Modeling namespace/repository remains deferred while ESKA permanent-namespace governance is unresolved.

### ESKA boundary

The ownership boundary remains explicit:

```text
pizza-ontology
    owns Pizza semantic source artifacts
        ↓ immutable source contract
ESKA
    owns executable capability / execution / result / verification
    and optional service / agent / deployment architecture
```

The release does not move Pizza-domain semantic ownership into ESKA.

## Release assets

The governed publication workflow builds and attaches exactly:

```text
pizza-2.0-preserved.ofn
pizza-2.0-preserved.ttl
SHA256SUMS
```

The artifacts are generated from the exact release target commit after preservation identity, ontology QC, semantic-equivalence, and checksum checks pass.

## Verification

The normal repository CI keeps thirteen independent concerns green, including ODK QC, OAK access/query, reasoning, validation, seven executable semantic artifact families, both Implementation Projections, and both UX paths.

The release publisher additionally rebuilds the preservation distribution set from the exact target commit and verifies the checksums immediately before publication.

## Licensing and attribution

The repository maintains explicit licensing boundaries:

- historical Pizza Ontology 2.0 semantic content and distributions containing it: **CC BY 3.0** with upstream attribution;
- newly created repository software and engineering material: **MIT** unless stated otherwise;
- newly created original repository documentation: **CC BY 4.0** unless stated otherwise;
- third-party material: its own license.

See `LICENSE.md` and `NOTICE.md`.

## Provenance and authority

The historical Pizza baseline is derived from the Pizza 2.0 ontology distributed by the Stanford Protégé site and the Manchester / Protégé tutorial tradition.

This repository acts as a preservation, stewardship, engineering, and learning environment. It does not claim to be the original ontology authority or rights holder of the historical Pizza ontology.

## What this release does not do

`preservation-v0.2.0` does **not**:

- alter Pizza Ontology 2.0 semantics;
- claim a new historical Pizza semantic version;
- change the historical Pizza ontology/version/entity IRIs;
- claim authority over `co-ode.org` or an OBO Pizza PURL;
- create a successor Pizza ontology;
- activate a separate Semantic Modeling namespace.

Any future semantic modernization remains a separate successor-lineage decision.
