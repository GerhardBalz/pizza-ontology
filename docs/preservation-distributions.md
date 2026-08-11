# Preservation-Safe Distributions

## Purpose

The Pizza repository preserves the historical Pizza Ontology 2.0 semantic identity while allowing the same ontology graph to be distributed in multiple serializations.

A distribution is a representation of the ontology. It is not a new ontology identity, ontology version, or successor lineage.

```text
Pizza Ontology 2.0
    ontology identity + semantics
        │
        ├── OWL Functional Syntax distribution
        └── Turtle distribution
```

## Source of truth

The preservation editor ontology remains:

```text
src/ontology/pizza-edit.owl
```

It declares:

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

Generated distributions must preserve those identities and semantics.

## Preservation distributions

From `src/ontology` run:

```bash
odkrun make preservation_release_artifact
```

The target produces:

```text
target/preservation-release/
├── pizza-2.0-preserved.ofn
├── pizza-2.0-preserved.ttl
└── SHA256SUMS
```

### Functional Syntax

`pizza-2.0-preserved.ofn` is an exact byte-for-byte copy of the preservation source ontology.

This remains the most conservative preservation artifact.

### Turtle

`pizza-2.0-preserved.ttl` is generated from the same source ontology with ROBOT `convert`.

The Turtle file is a serialization distribution only. It does not receive a new ontology IRI, version IRI, or repository-defined semantic version.

## Verification

The build verifies the Turtle distribution before it is accepted.

The checks include:

1. the preserved source ontology passes the historical identity invariant;
2. ROBOT converts the source ontology to Turtle;
3. ROBOT `diff` compares the source ontology with the Turtle distribution at the ontology/axiom level;
4. the diff must be empty;
5. the historical ontology IRI, Pizza 2.0 version IRI, and entity namespace must remain present;
6. the unowned OBO Pizza namespace must not appear;
7. SHA-256 checksums are generated for both preservation distributions.

This distinguishes serialization change from semantic change.

## Why standard ODK release targets are still excluded

The generated ODK project includes standard OBO-oriented release behavior. Those rules are useful for ontologies governed within the OBO publication model, but they are not appropriate for this preservation line because this repository does not own an OBO Pizza identifier space.

The repository therefore does not use generated `pizza.owl` or `pizza-non-classified.owl` release assets when those workflows would annotate the ontology with OBO PURL/date-based release identity.

The custom preservation targets live in `src/ontology/pizza.Makefile` rather than modifying generated ODK Makefile internals.

## Toolchain reproducibility

CI currently runs ontology engineering in the pinned container:

```text
obolibrary/odkfull:v1.6.1
```

This provides the ODK/ROBOT/reasoner toolchain used for preservation conversion and verification. The repository intentionally pins the ODK container version rather than relying on an unversioned `latest` image.

A future toolchain upgrade should be treated as an explicit engineering change and must keep the preservation identity and semantic-equivalence tests green.

## Relationship to publication

This document defines **what** a preservation-safe distribution is and how it is verified.

Issue #15 separately defines **where** distributions should be published and how locations, download URLs, repository releases, ontology identifiers, and authority should be represented.

The distinction is intentional:

```text
semantic identity
    ≠ serialization
    ≠ distribution
    ≠ publication location
    ≠ repository release
```
