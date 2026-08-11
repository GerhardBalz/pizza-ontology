# Semantic Modeling Vocabulary Decision

## Status

**Architecture decision — after two materially different implementation projections**

Related issue: #55.

This decision follows the first concept harvest in [`semantic-modeling-concept-harvest.md`](semantic-modeling-concept-harvest.md) and the implementation of two independent projection targets:

- `projections/pizza-concepts/` — content-first JSON concept catalog;
- `projections/pizza-openapi/` — schema/interface-first OpenAPI 3.1 contract.

The purpose is to decide whether the evidence now supports a small reusable Semantic Modeling vocabulary and, separately, whether such a vocabulary should be published under its own namespace now.

## Decision summary

The evidence supports the following conceptual core:

```text
SemanticModel
ImplementationProjection
```

with an important qualification:

> **The conceptual vocabulary is now justified, but a new repository/namespace is deliberately deferred until ESKA's permanent namespace activation and the post-W3ID ownership review of `SemanticModel` are complete.**

The decision is therefore asymmetric:

```text
conceptual extraction threshold      PASSED
new namespace/publication threshold  DEFERRED
```

## Decision 1 — `ImplementationProjection` has crossed the evidence threshold

The first projection alone was insufficient to distinguish a reusable projection concept from a Pizza-specific implementation artifact.

Two materially different targets now demonstrate the same architectural pattern.

### JSON content projection

```text
Pizza Ontology 2.0
    semantic source
        ↓ explicit source selection
selected semantic slice
        ↓ explicit projection policy
PizzaConceptCatalog JSON
        ↓
application / UX
```

This target is content-first. It publishes concrete selected concept records.

### OpenAPI interface projection

```text
Pizza Ontology 2.0
    semantic source
        ↓ explicit source selection
selected semantic slice
        ↓ explicit projection policy
OpenAPI 3.1 contract
        ↓
API implementation / clients
```

This target is interface-first. It introduces paths, operations, query parameters, response envelopes, status codes and schema structures that are application/API concerns rather than ontology facts.

### Shared invariants

Despite those differences, both implementations require the same cross-target invariants:

1. an explicit source semantic model;
2. explicit source selection;
3. a machine-verifiable source-access boundary;
4. an explicit policy identifying preserved semantics;
5. an explicit policy identifying transformed semantics;
6. an explicit policy identifying target-introduced concerns;
7. an explicit policy identifying omitted semantics;
8. preservation of semantic identity for selected entities;
9. traceability from projected structures back to source semantics;
10. regression verification against the source model;
11. explicit non-authority of the target representation.

These invariants are not JSON-specific, OpenAPI-specific, or Pizza-specific in their architecture role.

Therefore:

> **`ImplementationProjection` is now a sufficiently precise, evidence-backed reusable Semantic Modeling concept.**

## Definition — candidate reusable concept

The following definition is adopted architecturally, but no new ontology term is minted by this repository:

> **Implementation Projection** — a non-authoritative implementation-oriented representation or contract derived from selected semantics of one or more Semantic Models under an explicit policy that records semantic preservation, transformation, introduction and omission while retaining machine-verifiable traceability to the source semantics.

Important properties of the definition:

- it is not limited to one serialization;
- it is not limited to generated artifacts;
- it does not claim semantic equivalence with its source;
- it allows target-specific implementation concerns;
- it requires semantic loss/translation to be explicit rather than accidental;
- it remains downstream from semantic authority.

## Decision 2 — keep `ImplementationProjection` narrower than Mapping / Semantic Transformation

The word `Projection` remains too broad if it is used to cover every semantic transformation.

The implemented Mapping architecture is materially different:

```text
Semantic Transformation / Mapping
    source SemanticModel
        ↓
    mapping semantics
        ↓
    target SemanticModel
        ↓
    transformed target graph
```

By contrast:

```text
ImplementationProjection
    source SemanticModel
        ↓
    explicit projection policy
        ↓
    narrower application representation / contract
```

An implementation projection does not require its target to be a Semantic Model.

The OpenAPI target is the decisive counterexample: its target is an application interface contract containing HTTP concerns that do not belong to ontology/domain semantics.

Therefore:

- `ImplementationProjection` is adopted as the reusable concept;
- generic `Projection` remains unadopted;
- Mapping / Semantic Transformation remains outside this concept;
- no `targetSemanticModel` relation belongs in the generic implementation-projection contract.

## Decision 3 — `SemanticModel + ImplementationProjection` is enough for a small vocabulary

The first concept harvest concluded that a one-term vocabulary containing only `SemanticModel` would create disproportionate governance overhead.

That objection no longer holds conceptually.

The two concepts now form a coherent reusable boundary:

```text
SemanticModel
    owns / expresses machine-interpretable semantic commitments
        ↓ selected semantics
ImplementationProjection
    exposes selected semantics in a non-authoritative implementation form
        ↓
Application / API / UX / other consumer
```

This is enough to justify a deliberately small Semantic Modeling vocabulary **in principle**.

It does not justify a broad meta-ontology.

The vocabulary should begin small and compose with established standards rather than reproduce them.

## Decision 4 — no custom relation is required yet

A tempting design would introduce relations such as:

```text
sourceSemanticModel
projectsSemanticModel
projectionOf
```

The current evidence does not require a new relation to obtain machine-readable value.

The minimal standards-composing pattern can use:

```text
?projection a sm:ImplementationProjection ;
    dcterms:source ?model ;
    prov:wasDerivedFrom ?model .

?model a sm:SemanticModel .
```

where appropriate.

`dcterms:source` expresses the source relationship; `prov:wasDerivedFrom` expresses derivation when provenance semantics apply; the class types make the semantic role queryable.

This avoids introducing a vocabulary-specific property that merely duplicates an established relation.

Future evidence may justify a more specific semantic-model participation relation, especially where a projection uses multiple models with materially different roles. That evidence does not exist yet for implementation projections.

## Decision 5 — the projection policy is required architecturally, but not yet standardized as ontology terms

Both implemented projections explicitly classify their treatment of source semantics as:

```text
preserved
transformed
introduced
omitted
```

This policy is essential to the definition of `ImplementationProjection`.

However, the current evidence does not yet justify minting generic classes/properties for each policy category.

Why:

- both examples share the same source selection;
- both are from the same Pizza domain;
- the current policy structures are embedded in JSON/OpenAPI representations rather than independently modeled RDF resources;
- we have not tested how policy granularity changes across a different domain or a projection with materially different loss semantics.

Therefore the vocabulary concept requires an **explicit projection policy**, but the machine-readable vocabulary for that policy remains provisional.

A future implementation may justify concepts such as a projection specification/policy and qualified treatment of individual semantic elements. Do not create those terms by symmetry now.

## Decision 6 — standards ownership remains unchanged

The emerging Semantic Modeling vocabulary should remain compositional.

### OWL / RDF / SHACL / specialized semantic formalisms

They continue to own their own formal semantics.

`SemanticModel` is an architectural cross-formalism class; it does not replace or restate those formalisms.

### PROV-O

PROV-O continues to own:

- Entity / Activity / Agent lineage;
- derivation;
- generation and usage;
- qualified usage and roles.

No parallel Semantic Modeling provenance model should be introduced.

### DCAT

DCAT continues to own catalog/distribution concerns.

An `ImplementationProjection` may have one or more distributions, but the projection is not itself defined by a download location or media type.

### Dublin Core Terms

Dublin Core Terms remains appropriate for source, relation, conformance, identifiers and descriptive metadata.

## Decision 7 — publication of a new vocabulary is deferred

The conceptual vocabulary has matured, but publication now would create an avoidable governance collision.

The current ESKA core defines:

```text
eska:SemanticModel
```

under the provisional namespace:

```text
urn:eska:core:
```

ESKA is already executing a separate governed namespace transition toward:

```text
https://w3id.org/eska#
```

As of this decision, upstream W3ID PR `perma-id/w3id.org#6530` remains open and ESKA #53 still records the permanent namespace as not active.

Creating a new Semantic Modeling namespace now would force an ownership choice for `SemanticModel` before ESKA's own namespace migration has stabilized.

Therefore:

> **Do not create the Semantic Modeling repository/namespace yet.**

Sequence instead:

```text
W3ID #6530 merge
    ↓
external resolver verification
    ↓
ESKA #53 atomic namespace migration + first publication
    ↓
ESKA #57 SemanticModel ownership review
    ↓
create / align the Semantic Modeling vocabulary if the decision still holds
```

The conceptual shape should be retained so the later ownership decision is small and explicit rather than rediscovered.

## Candidate future vocabulary shape — non-normative until publication

If ESKA #57 confirms extraction, the smallest plausible vocabulary is:

```text
SemanticModel
ImplementationProjection
```

with standards composition:

```text
SemanticModel
    optionally prov:Entity

ImplementationProjection
    optionally prov:Entity
    dcterms:source → SemanticModel
    prov:wasDerivedFrom → SemanticModel
```

No custom property is required in the first version unless later evidence demonstrates one.

ESKA-specific concepts stay in ESKA:

```text
ExecutableSemanticKnowledgeArtifact
SemanticCapability
ApplicabilityCondition
Execution
Result
Verification
KnowledgeService
KnowledgeAgent
ServiceDeployment
```

Pizza-specific ontology entities and artifacts stay in `pizza-ontology`.

## Consequence for the OpenAPI → Application → UX path

The next executable test should move beyond projection generation and use the OpenAPI contract as an actual application boundary:

```text
Pizza Ontology 2.0
    ↓
ImplementationProjection
    OpenAPI 3.1
        ↓ contract implemented by
Application
        ↓ consumed by
UX
```

This path can test three additional boundaries:

1. **Projection vs application implementation** — OpenAPI defines the application interface, while application code owns runtime filtering, lookup, errors and transport behavior.
2. **Application vs semantic authority** — the application must not infer or recreate OWL semantics; it consumes source-verified projected data.
3. **Application vs UX** — the UX should consume the application contract rather than reading Pizza OWL or the checked-in semantic projection directly.

A useful first vertical slice is:

```text
OpenAPI projection
    /concepts
    /concepts/{conceptId}
        ↓
small deterministic reference application
        ↓
API-backed Pizza explorer
```

The existing GitHub Pages explorer should remain as the direct-projection UX specimen. The API-backed explorer should be a separate specimen so the architecture can compare:

```text
direct projection consumer
    projection → UX

application-mediated consumer
    projection contract → application → UX
```

Neither pattern should be declared universally superior; the value is making the boundary and trade-offs executable.

## Final architecture decision

The evidence after two implementation projections supports:

```text
REUSABLE NOW, CONCEPTUALLY
    SemanticModel
    ImplementationProjection

STANDARDS-OWNED
    provenance / roles        → PROV-O
    distribution/publication  → DCAT
    generic source/relation   → DCTERMS
    ontology/formal semantics → OWL / SHACL / other formalisms

LOCAL / NOT YET GENERALIZED
    projection-policy vocabulary
    source/target role refinements beyond standards
    semantic Mapping / Transformation abstraction
    authority / stewardship ontology terms

DEFERRED GOVERNANCE ACTION
    new Semantic Modeling repository + namespace
        until ESKA #53 and #57 complete
```

The important result is that implementation has now produced a second mature reusable concept without forcing unrelated concerns into a meta-model.
