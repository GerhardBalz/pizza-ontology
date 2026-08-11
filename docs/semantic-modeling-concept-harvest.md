# Semantic Modeling Concept Harvest

## Status

**Architecture decision — evidence review after Tracks 1–9 implementation**

Related issue: #51.

This document revisits the provisional concept-harvesting matrix in [`semantic-architecture.md`](semantic-architecture.md) after the Pizza reference project implemented the first semantic projection, ontology-informed UX, preservation-safe distributions, publication metadata, and explicit OWL modeling guide.

The purpose is not to create a generic ontology by symmetry. The purpose is to decide which abstractions have now earned a reusable semantic identity and which still need more evidence.

## Evidence baseline

### Pizza reference

The repository now demonstrates the following boundaries in executable or machine-verifiable form:

```text
Pizza Ontology 2.0
    authoritative OWL semantic model
        ↓
source-owned semantic artifacts
    reasoning / validation / rule / decision / calculation / mapping / workflow
        ↓
publication and distributions
    DCTERMS / DCAT / PROV-O metadata
        ↓
semantic projection
    selected OWL semantics → JSON / JSON Schema
        ↓
ontology-informed UX
    projection consumer, not a semantic source
```

The first implementation projection is documented in [`../projections/pizza-concepts/README.md`](../projections/pizza-concepts/README.md). It explicitly records preserved, transformed, introduced, and omitted semantics.

### ESKA reference

The companion ESKA repository currently defines `eska:SemanticModel` in its provisional core and has used that concept across seven materially different executable-semantic modes.

Evidence reviewed for this decision is pinned to:

```text
GerhardBalz/executable-semantic-knowledge-architecture
@dac2b12a434aafd5217a6785a013e3a76f8a2552
```

Relevant ESKA evidence includes:

- `model/eska-core.ttl` — `SemanticModel`, `ExecutableSemanticKnowledgeArtifact`, `SemanticCapability`, `Execution`, `Result`, `Verification`;
- Mapping evidence — local `sourceSemanticModel`, `mappingSemanticModel`, and `targetSemanticModel` refinements below `eska:usesSemanticModel`;
- runtime semantic-model participation qualified through PROV-O `prov:Usage` and `prov:hadRole`;
- seven execution modes using one unchanged provisional ESKA core.

The ESKA-specific executable architecture remains outside the scope of a generic Semantic Modeling layer.

## Standards-first ownership

A new vocabulary should not duplicate semantics already owned by established standards.

### OWL

OWL owns ontology semantics: ontologies, axioms, classes, properties, individuals, imports, and ontology identity/version constructs.

An OWL ontology can be treated architecturally as a `SemanticModel`, but a generic Semantic Modeling vocabulary should not redefine `owl:Ontology` or reproduce OWL axiom semantics.

Reference: <https://www.w3.org/TR/owl2-syntax/>

### PROV-O

PROV-O already supplies the generic provenance layer needed here:

- `prov:Entity` for physical, digital, conceptual, or other entities;
- `prov:Activity` for processes that use/generate entities;
- `prov:used`, `prov:wasGeneratedBy`, and `prov:wasDerivedFrom` for lineage;
- qualified `prov:Usage` plus `prov:hadRole` when an entity's role in an activity must be explicit.

A Semantic Modeling vocabulary should therefore not create parallel generic `Source`, `Target`, `TransformationActivity`, or provenance-role machinery when PROV-O qualification is sufficient.

Reference: <https://www.w3.org/TR/prov-o/>

### DCAT

DCAT owns catalog/publication resource and distribution concerns.

The important architectural distinction is:

```text
semantic resource
    ≠
its accessible representation / distribution
```

`dcat:Distribution` already represents a specific accessible representation of a dataset, while `dcat:Resource` is an extension point for cataloged resource types. Pizza publication metadata should continue using DCAT instead of introducing Semantic-Model-specific download/distribution terms.

Reference: <https://www.w3.org/TR/vocab-dcat-3/>

### Dublin Core Terms

Dublin Core Terms already covers generic descriptive relations such as source, relation, conformance, title, identifier, creator/publisher, and related metadata.

A future Semantic Modeling vocabulary should use those terms where their semantics fit rather than introduce prefixed equivalents.

Reference: <https://www.dublincore.org/specifications/dublin-core/dcmi-terms/>

## Reassessed concept matrix

| Candidate | Evidence after implementation | Standards overlap | Decision now |
|---|---|---|---|
| `SemanticModel` | Pizza OWL source + ESKA seven-mode use + projection/UX boundary | No established cross-formalism class with this exact architectural role | **Mature reusable concept; ownership extraction justified in principle, but defer namespace move** |
| `SemanticArtifact` | Pizza has many source-owned machine-interpretable artifacts across seven semantic roles | Generic resourcehood already covered by `prov:Entity` / catalog concerns by DCAT | **Useful architecture concept, but not yet precise enough to mint** |
| `Projection` | JSON implementation projection + Mapping vocabulary uses “projection” operationally | PROV-O covers transformation activity/derivation, but not the semantic policy itself | **Do not mint yet; current evidence exposes overloaded meanings** |
| source / mapping / target semantic-model roles | Mapping has three explicit model roles; JSON projection has a semantic source but an implementation target representation | PROV-O qualified usage can express runtime roles | **Keep local/static refinements; use PROV-O roles at runtime** |
| representation / distribution | Multiple preservation representations and publication locations implemented | DCAT directly addresses distributions and access/download URLs | **Standards-owned** |
| authority / stewardship | Strong governance need across inherited Pizza identity and repository stewardship | DCTERMS/PROV-O can describe responsible/source agents but do not by themselves define semantic authority | **Keep architectural/governance concept for now; no generic ontology term** |

## Decision 1 — `SemanticModel` has crossed the evidence threshold

`SemanticModel` is the strongest reusable concept.

It is no longer justified only by one executable architecture:

```text
Pizza Ontology 2.0
    is treated as an authoritative semantic model

ESKA
    uses SemanticModel across seven execution modes

Pizza semantic projection
    has an explicit source semantic model

Pizza UX
    consumes a projection while semantic meaning remains upstream
```

The concept describes a role that cuts across representation technologies. Examples include OWL ontology axioms, SHACL shapes, DMN decision semantics, an OpenMath formula plus semantic vocabulary, and mapping source/target vocabularies.

That breadth is exactly why `SemanticModel` is potentially broader than ESKA.

### But do not move it now

ESKA is in the middle of the governed `urn:eska:core:` → `https://w3id.org/eska#` activation sequence. Extracting `SemanticModel` into another namespace before that work is complete would combine two independent governance changes:

1. activating ESKA's permanent namespace;
2. changing ownership of a generic concept.

Therefore:

> **Treat `SemanticModel` as extraction-ready conceptually, but keep the current ESKA term unchanged until ESKA #53 is complete.**

The post-W3ID ownership decision is tracked by ESKA issue #57.

## Decision 2 — do not mint `SemanticArtifact` yet

The phrase **Semantic Artifact** remains useful in architecture prose because Pizza owns many machine-interpretable artifacts:

```text
OWL model
SHACL constraint profile
SPARQL rule
DMN decision table
OpenMath calculation
semantic Mapping
BPMN workflow semantic artifact
JSON semantic projection
```

However, the proposed generic class currently risks becoming a broad synonym for “resource that has semantics”. That would add little machine-readable value beyond existing resource/provenance classes.

Before introducing a term, we need a sharper contract. Candidate questions include:

- Is every `SemanticModel` a `SemanticArtifact`?
- Is a semantic input data graph an artifact or merely data used by one?
- Is an executable mapping specification both a semantic model and an artifact?
- Is a projection output an artifact even when it intentionally omits most source semantics?
- What query or validation becomes possible only after introducing this class?

Until those questions produce a stable boundary, use concrete types plus `prov:Entity`, DCAT publication metadata where applicable, and existing domain/execution vocabularies.

## Decision 3 — `Projection` is currently overloaded

The implemented evidence shows that the word **projection** is being used for at least two distinct architectures.

### Implementation projection

Track 6 performs:

```text
source semantic model
    Pizza Ontology 2.0
        ↓ explicit selection/transformation policy
implementation representation
    PizzaConceptCatalog JSON
```

The target is not asserted to be a new semantic model. It is a narrower application contract with deliberate omissions and projection-owned display labels.

### Semantic transformation / mapping

The Mapping execution performs:

```text
source semantic model
    Pizza vocabulary
        ↓
mapping semantic model
    SPARQL mapping semantics
        ↓
target semantic model
    Menu vocabulary
        ↓
target RDF graph
```

This is a transformation between two semantic-model spaces.

Those are related but not identical. A single generic class named `Projection` would currently hide an important distinction:

```text
implementation projection
    semantic model → narrower representation

semantic transformation
    source semantic model → target semantic model
```

Therefore:

> **Do not mint `Projection` until at least these two meanings have been named and their common contract is clear.**

A future vocabulary may eventually contain concepts such as `ImplementationProjection`, `SemanticTransformation`, or a more abstract relationship above them, but the current project should not choose names before more examples falsify the distinction.

## Decision 4 — source/target model roles remain contextual

Mapping needs explicit source, mapping, and target semantic-model roles. ESKA currently models these as mode-local refinements below `eska:usesSemanticModel` and uses qualified PROV-O roles at runtime.

The JSON projection demonstrates why those roles should not yet become universal generic properties:

- it has a clear **source semantic model**;
- its target is an **implementation representation**, not necessarily a `SemanticModel`.

So a universal `targetSemanticModel` relation would be wrong for at least one implemented projection pattern.

The current extension pattern is therefore retained:

```text
generic participation relation
    ↓ refine only where semantics require it
mode/local source/target/mapping roles

runtime role precision
    → prov:qualifiedUsage / prov:hadRole
```

## Decision 5 — keep distribution and provenance out of a future core

The Pizza publication work provides concrete evidence that semantic identity and distribution identity are separate:

```text
semantic model / artifact identity
    ≠
distribution
    ≠
download URL
    ≠
repository release
```

DCAT and Dublin Core Terms already serve the publication layer. PROV-O already serves lineage and role-qualified participation.

A future Semantic Modeling vocabulary should therefore remain small and compositional. It should reference these standards rather than duplicate them.

## Decision 6 — no separate Semantic Modeling ontology yet

The implementation phase has improved the evidence, but the threshold for a separate ontology/repository is **not yet met**.

Why:

1. `SemanticModel` is clearly mature, but a one-term ontology would create disproportionate namespace/governance overhead.
2. `SemanticArtifact` is still semantically broad and risks duplicating generic resource classes.
3. `Projection` has become more ambiguous, not less, after implementation.
4. source/target semantic-model roles are contextual rather than universal.
5. distribution and provenance are already owned by standards.

Therefore the current decision is:

> **Do not create `semantic-modeling-ontology` yet. Preserve the candidate layer as an architecture boundary and gather one more round of evidence.**

This is not a rejection of the idea. It is a stronger definition of the evidence needed before creating it.

## Evidence gates for reconsideration

A separate Semantic Modeling vocabulary should be reconsidered when at least one of the following produces a second mature reusable term alongside `SemanticModel`.

### Gate A — a second materially different implementation projection

Add another projection whose target and semantic-loss policy differ materially from `PizzaConceptCatalog`, for example an API contract, search/index model, or another application representation.

The goal is to determine whether a stable generic projection contract emerges or whether multiple named projection subtypes are needed.

### Gate B — cross-domain use of `SemanticModel`

Apply the same architecture outside Pizza. Cross-domain evidence would test whether the current ESKA definition of `SemanticModel` remains appropriately broad without being Pizza-shaped or execution-shaped.

### Gate C — executable value for `SemanticArtifact`

Identify a real cross-repository query, validation, publication rule, or agent-discovery need that becomes simpler or safer if a generic `SemanticArtifact` class exists.

The term should be introduced only when it creates a verifiable contract, not merely a nicer diagram.

### Gate D — ESKA permanent namespace activation

Complete ESKA #53 before changing ownership of `SemanticModel`.

After that migration stabilizes, ESKA #57 can decide whether to retain the term, align it to a future external concept, or migrate it with explicit compatibility semantics.

## Candidate future shape — non-normative

If later evidence justifies a Semantic Modeling ontology, the likely shape should remain deliberately small.

A possible direction — **not adopted by this decision** — is:

```text
SemanticModel
    a reusable cross-formalism semantic representation
    potentially aligned with prov:Entity

[second evidence-backed concept]
    e.g. a precisely defined projection/transformation or artifact concept

external standards
    OWL      ontology semantics
    PROV-O   provenance / activity / roles
    DCAT     distributions / catalog publication
    DCTERMS  source / relation / conformance / descriptive metadata
```

ESKA-specific concepts would remain in ESKA:

```text
ExecutableSemanticKnowledgeArtifact
SemanticCapability
ApplicabilityCondition
Execution
Result
Verification
KnowledgeService
KnowledgeAgent
Deployment
```

Pizza-specific concepts and semantic artifacts would remain in `pizza-ontology`.

## Ownership result

The architecture after this review is:

```text
pizza-ontology
    domain semantics
    concrete semantic artifacts
    projection evidence
    UX evidence
    preservation/publication evidence

ESKA
    executable semantic architecture
    current provisional SemanticModel term
    SemanticCapability / Execution / Result / Verification
    Service / Agent / Deployment extensions

external standards
    OWL / RDF / RDFS / SHACL
    PROV-O
    DCAT
    Dublin Core Terms
    BPMN / DMN / OpenMath

future Semantic Modeling layer
    SemanticModel: conceptually mature
    additional terms: not yet mature
```

## Architectural rule retained

Before minting a generic Semantic Modeling term:

1. require evidence from more than one implementation or repository boundary;
2. prefer established standards where they already express the semantics;
3. require concrete machine-readable value;
4. reject names that collapse materially different roles;
5. preserve domain, execution, publication, and governance ownership boundaries.

The result of this harvest is therefore deliberately asymmetric: **one concept has matured, but the ontology has not.**
