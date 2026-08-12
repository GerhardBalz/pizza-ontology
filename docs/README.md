# Pizza Ontology Documentation

This directory contains the architectural, modeling, preservation, publication, provenance, and release documentation for the Pizza ontology reference project.

## Modeling

- [Pizza OWL Modeling Patterns and Teaching Cases](pizza-owl-modeling-patterns.md) — asserted versus defined classes, restrictions, disjointness, value partitions, individuals, open-world reasoning, and the two intentional unsatisfiable teaching classes.

## Architecture

- [Cross-Track Pizza Semantic Architecture](semantic-architecture.md) — boundaries and traceability across modeling, engineering, access, validation, publication, projections, UX, and executable semantic knowledge.
- [Semantic Modeling Concept Harvest](semantic-modeling-concept-harvest.md) — post-implementation reassessment of `SemanticModel`, `SemanticArtifact`, `Projection`, semantic-model roles, and the evidence threshold for a future reusable Semantic Modeling vocabulary.
- [Semantic Modeling Vocabulary Decision](semantic-modeling-vocabulary-decision.md) — adopts the evidence-backed conceptual pair `SemanticModel + ImplementationProjection` while deferring a separate namespace/repository until ESKA namespace governance stabilizes.
- [Ontology Identity and Publication Model](identity-publication-model.md) — conceptual distinctions among ontology identity, versions, releases, distributions, repositories, authority, stewardship, hosting, and provenance.

## Preservation and publication

- [Preservation-Safe Distributions](preservation-distributions.md) — verified Functional Syntax and Turtle distributions that retain historical Pizza 2.0 identity.
- [Publication and Distribution Policy](publication-distribution-policy.md) — canonical versus convenient locations, release assets, DCAT metadata, and authority boundaries.
- [Pizza URL/IRI Resolution Inventory](url-iri-resolution-inventory.md) — executable classification of historical semantic identifiers versus resolvable source, publication, distribution, documentation, and UX locations, plus the proposed W3ID preservation/reference routes.
- [Versioning and Release Model](versioning-release-model.md) — separation of the historical Pizza semantic version from repository preservation releases.

## Provenance

- [Pizza Ontology Provenance](pizza-provenance.md) — historical source, contributors, institutional context, current authority uncertainty, and the repository's preservation role.

## Releases

Release-specific notes live under [`releases/`](releases/).

- [`preservation-v0.1.0`](releases/preservation-v0.1.0.md) — first conservative preservation/source-snapshot release.
- [`preservation-v0.2.0`](releases/preservation-v0.2.0.md) — second preservation/reference-architecture release notes used for publication.
- [`preservation-v0.2.0` publication record](releases/preservation-v0.2.0-publication.md) — published tag/commit binding, governed release assets, and external-consumer verification contract.

## Executable traceability

Documentation is not treated as a second semantic source of truth. Where a document depends on representative source or publication facts, the repository adds executable checks.

Modeling-reference path:

```text
src/ontology/pizza-edit.owl
        ↓
docs/pizza-owl-modeling-patterns.md
        ↓
docs/verify_modeling_reference.py
```

Publication path:

```text
preservation-v0.2.0 GitHub Release
        ↓ public API/download URLs
metadata/publication.ttl
        ↓
metadata/verify_publication_metadata.py
metadata/verify_published_release.py

Pizza-specific URL/IRI surface
        ↓ role classification
metadata/url-iri-inventory.json
        ↓
metadata/verify_url_iri_inventory.py
```

The modeling-reference verifier checks the preserved source for the representative axioms used by the guide. The publication verifiers keep release/distribution metadata distinct from historical semantic identity and verify the published v0.2.0 asset contract from an external-consumer path. The URL/IRI verifier additionally protects the identifier-versus-location boundary and verifies canonical actionable references.
