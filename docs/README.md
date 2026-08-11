# Pizza Ontology Documentation

This directory contains the architectural, modeling, preservation, publication, provenance, and release documentation for the Pizza ontology reference project.

## Modeling

- [Pizza OWL Modeling Patterns and Teaching Cases](pizza-owl-modeling-patterns.md) — asserted versus defined classes, restrictions, disjointness, value partitions, individuals, open-world reasoning, and the two intentional unsatisfiable teaching classes.

## Architecture

- [Cross-Track Pizza Semantic Architecture](semantic-architecture.md) — boundaries and traceability across modeling, engineering, access, validation, publication, projections, UX, and executable semantic knowledge.
- [Ontology Identity and Publication Model](identity-publication-model.md) — conceptual distinctions among ontology identity, versions, releases, distributions, repositories, authority, stewardship, hosting, and provenance.

## Preservation and publication

- [Preservation-Safe Distributions](preservation-distributions.md) — verified Functional Syntax and Turtle distributions that retain historical Pizza 2.0 identity.
- [Publication and Distribution Policy](publication-distribution-policy.md) — canonical versus convenient locations, release assets, DCAT metadata, and authority boundaries.
- [Versioning and Release Model](versioning-release-model.md) — separation of the historical Pizza semantic version from repository preservation releases.

## Provenance

- [Pizza Ontology Provenance](pizza-provenance.md) — historical source, contributors, institutional context, current authority uncertainty, and the repository's preservation role.

## Releases

Release-specific notes live under [`releases/`](releases/).

## Executable traceability

Documentation is not treated as a second semantic source of truth. Where a document depends on representative source facts, the repository adds executable checks. In particular:

```text
src/ontology/pizza-edit.owl
        ↓
docs/pizza-owl-modeling-patterns.md
        ↓
docs/verify_modeling_reference.py
```

The modeling-reference verifier checks the preserved source for the representative axioms used by the guide.
