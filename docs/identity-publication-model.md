# Ontology Identity and Publication Model

## Status

Draft architecture model.

This document defines the concepts used to reason about ontology identity, versioning, publication, provenance, and governance.

It is intentionally independent of any particular ontology. The Pizza ontology is used separately as a case study in `pizza-provenance.md`.

The model is informed by the OBO Foundry principles and related semantic-web standards, but does not imply that an ontology using this model is itself an OBO Foundry ontology.

## 1. Core Concepts

### Ontology

An **Ontology** is a semantic artifact: an explicit specification of concepts, relationships, constraints, and other semantic commitments within a defined scope.

An ontology is not identical to:

* an OWL file,
* a Git repository,
* a URL where a file happens to be hosted,
* a serialization format,
* or a particular release.

Those are manifestations, locations, or engineering artifacts associated with the ontology.

### Ontology IRI

An **Ontology IRI** is the persistent semantic identifier of an ontology.

It answers:

> Which ontology is this?

The Ontology IRI should be stable and governed by an authority capable of maintaining the corresponding identifier space.

Identity and location are distinct concerns.

A persistent identifier may resolve to a representation, but moving that representation should not in itself require changing the ontology identity.

### Semantic Entity

A **Semantic Entity** is an identifiable semantic element defined or used by an ontology.

Examples include:

* Class
* Object Property
* Data Property
* Annotation Property
* Named Individual

### Entity IRI

An **Entity IRI** is the persistent identifier of a semantic entity.

It answers:

> Which concept, property, or individual is this?

Changing labels, documentation, serialization, or physical storage location should not by itself change an Entity IRI.

If the meaning changes substantially enough that the entity denotes different referents, a new identity should normally be introduced rather than silently changing the meaning of an existing identifier.

### Ontology Version

An **Ontology Version** is a particular semantic state of an ontology.

```text
Ontology
    │
    └── hasVersion ──► Ontology Version
```

A version represents substantive ontology content.

A different serialization of the same semantic content is not a different ontology version.

### Version IRI

A **Version IRI** uniquely identifies a particular ontology version.

It answers:

> Which exact semantic version of this ontology is this?

In OWL, `owl:versionIRI` provides the standard mechanism for identifying a particular ontology version.

### Release

A **Release** is the official publication of an ontology version.

A release:

* selects a particular ontology version for publication,
* has an issuance date,
* is immutable once officially published,
* may have multiple distributions,
* and should be traceable to an identified source revision.

```text
Ontology Version
       │
       └── publishedAs ──► Release
```

A more detailed provenance model may distinguish the release activity from the released artifact.

### Distribution

A **Distribution** is a concrete representation through which a release is made available.

Examples include:

* RDF/XML
* Turtle
* OWL Functional Syntax
* Manchester Syntax
* OBO format
* JSON-LD

Multiple distributions may represent the same released semantic content.

```text
Release
   │
   ├── Distribution: RDF/XML
   ├── Distribution: Turtle
   └── Distribution: Functional Syntax
```

Serialization therefore does not define ontology identity.

### Source Repository

A **Source Repository** is the engineering environment in which an ontology is developed and maintained.

It may contain:

* editor ontology source,
* imports,
* build configuration,
* tests,
* documentation,
* release automation,
* issue and contribution workflows.

The repository is not itself the ontology.

```text
Ontology
    │
    └── maintainedIn ──► Source Repository
```

### Source Revision

A **Source Revision** identifies an exact engineering state from which a version or release can be reproduced.

Typical implementations include:

* Git commit,
* Git tag,
* signed release tag.

```text
Source Repository
       │
       └── hasRevision ──► Source Revision
                                 │
                                 └── produces ──► Release
```

### Creator

A **Creator** is an agent responsible for originating the semantic artifact.

Creation is a provenance and attribution concept.

Creator does not automatically imply:

* current authority,
* current stewardship,
* hosting responsibility,
* or legal ownership.

### Authority

An **Authority** is the person, organization, or governed project entitled to determine meaning and manage identifiers within an ontology's identifier space.

Authority answers:

> Who has the mandate to say what this ontology and its identifiers mean?

Authority therefore precedes identifier design.

The ability to technically create a URL does not establish semantic authority over that namespace.

### Steward

A **Steward** is an agent responsible for ongoing maintenance of an ontology or ontology lineage.

Stewardship and authority may coincide, but they are conceptually distinct.

A steward may maintain a preservation copy or derivative without having authority over the original ontology's identifier namespace.

### Host

A **Host** provides infrastructure through which a repository, documentation site, or distribution is served.

Examples include:

* an institutional web server,
* GitHub,
* an artifact repository,
* a persistent-identifier service.

Hosting does not by itself establish semantic authority.

### Rights Holder

A **Rights Holder** is the person or organization owning or managing legal rights over a resource.

Rights Holder and Authority are different concepts.

An organization may hold legal rights without determining semantic meaning, while an ontology authority may operate under rights owned by another organization.

### Provenance

**Provenance** describes the origin and evolution of an ontology or related artifact.

It may include:

* creators,
* contributors,
* upstream sources,
* derivations,
* revisions,
* migration activities,
* tools,
* build processes,
* source revisions,
* responsible agents.

## 2. Relationship Model

```text
                              Creator
                                 │
                          creates/contributes
                                 ▼
Authority ── governs ───────► Ontology ◄──── maintained by ─── Steward
                                 │
                                 │ identified by
                                 ▼
                            Ontology IRI
                                 │
                                 │ has version
                                 ▼
                         Ontology Version
                                 │
                                 ├── Version IRI
                                 │
                                 │ officially published as
                                 ▼
                              Release
                                 │
                    ┌────────────┼─────────────┐
                    ▼            ▼             ▼
                 RDF/XML       Turtle          OFN
               Distribution  Distribution  Distribution
                    │            │             │
                    └────── download/access ───┘

Ontology ───────── maintained in ─────────► Source Repository
                                               │
                                               ▼
                                         Source Revision
                                               │
                                               │ produces
                                               ▼
                                            Release

Ontology Version ── derived from ─────────► Upstream Version

Host ───────── serves ────────────────────► Repository / Distribution

Rights Holder ───── holds/manages rights ─► Ontology / Distribution
```

## 3. Architectural Principles

### 3.1 Identity is not location

A persistent ontology or entity IRI represents semantic identity.

A repository URL or download URL represents location.

Moving an artifact should not automatically create a new semantic identity.

### 3.2 Authority precedes identifier design

An ontology should use an identifier space controlled by an authority capable of maintaining it.

The identifier should follow the governance model, not determine it.

### 3.3 Version is not serialization

RDF/XML, Turtle, and Functional Syntax representations of the same semantic state are distributions of one ontology version, not separate versions.

### 3.4 Version is not release

A semantic version describes a state of the ontology.

A release is the decision and act of publishing such a version.

The distinction may be small in simple projects but becomes important for provenance and reproducibility.

### 3.5 Release is not repository state

Every Git commit is not an ontology release.

A release is an explicit publication decision.

### 3.6 Official releases are immutable

Once officially released, a version and its published semantic content should not be silently changed.

Corrections should produce a subsequent version or release.

### 3.7 Entity meaning is stable

An existing Entity IRI should continue to denote substantially the same referents.

If the semantic meaning changes materially, a new identity should be considered and the relationship between old and new entities documented explicitly.

### 3.8 Attribution, authority, stewardship, hosting, and rights differ

These roles must not be inferred from each other.

```text
Host ≠ Steward
Steward ≠ Creator
Creator ≠ Rights Holder
Rights Holder ≠ Authority
Repository Owner ≠ Ontology Authority
```

### 3.9 Preservation and succession are different activities

A **preservation or stewardship project** keeps historical semantic identities and documents provenance.

A **successor ontology** establishes a new governed identity and identifier space and explicitly records derivation from its predecessor.

This decision should be made before new identifiers are minted.

## 4. Relationship to OBO Foundry Principles

The OBO Foundry principles provide useful architectural guidance beyond OBO-specific biomedical ontologies.

Particularly relevant principles include:

* **P1 Open** — openness, reuse, attribution, and preservation of identifiers.
* **P3 URI/Identifier Space** — persistent and governed identifiers.
* **P4 Versioning** — identifiable and immutable official releases.
* **P8 Documentation** — documented use and development.
* **P11 Locus of Authority** — explicit responsibility for ontology governance.
* **P13 Notification of Changes** — communication of important semantic changes.
* **P16 Maintenance** — explicit long-term stewardship.
* **P19 Stability of Term Meaning** — stable meaning associated with persistent entity identifiers.

The architecture should adopt the underlying principles without assuming OBO-specific registration or identifier conventions.

In particular, an ontology outside OBO should not simply use the OBO PURL namespace unless it participates in the corresponding governance process.

## 5. Candidate RDF Vocabulary Mapping

The conceptual model is vocabulary-independent.

Existing vocabularies can implement parts of it.

| Concept              | Candidate RDF/OWL term                      |
| -------------------- | ------------------------------------------- |
| Ontology             | `owl:Ontology`                              |
| Ontology IRI         | OWL ontology identifier                     |
| Version IRI          | `owl:versionIRI`                            |
| Version label        | `owl:versionInfo`                           |
| Title                | `dcterms:title`                             |
| Description          | `dcterms:description`                       |
| Creator              | `dcterms:creator`                           |
| Contributor          | `dcterms:contributor`                       |
| License              | `dcterms:license`                           |
| Rights Holder        | `dcterms:rightsHolder`                      |
| Version relation     | `dcterms:hasVersion`, `dcterms:isVersionOf` |
| Upstream source      | `dcterms:source`                            |
| Provenance statement | `dcterms:provenance`                        |
| Release date         | `dcterms:issued`                            |
| Derivation           | `prov:wasDerivedFrom`                       |
| Revision             | `prov:wasRevisionOf`                        |
| Attribution          | `prov:wasAttributedTo`                      |
| Distribution         | `dcat:Distribution`                         |
| Download location    | `dcat:downloadURL`                          |
| Access location      | `dcat:accessURL`                            |

These mappings implement the conceptual model; they do not define it.

## 6. Decision Rule for Identifier Changes

Before changing an existing ontology or entity IRI, ask:

1. Has the semantic identity changed?
2. Has the authority responsible for the identifier space changed?
3. Are we preserving an existing ontology or creating a successor?
4. Is the problem merely that the current identifier does not resolve?
5. Can resolution or publication infrastructure be repaired without changing semantic identity?
6. Will existing users reasonably expect the old and new identifier to denote the same thing?

A location problem should preferably be solved as a publication or resolution problem.

A semantic-identity or authority change may justify a new identifier.

## 7. Architectural Invariant

The central invariant of this model is:

> **Ontology identity, semantic version, official release, concrete distribution, and source repository are distinct concepts connected by explicit relationships.**

This distinction allows ontology engineering, publication, provenance, and governance to evolve independently without silently changing semantic identity.

## References

* OBO Foundry Principles: https://obofoundry.org/principles/fp-000-summary.html
* OBO Foundry URI/Identifier Space: https://obofoundry.org/principles/fp-003-uris.html
* OBO Foundry Versioning: https://obofoundry.org/principles/fp-004-versioning.html
* OBO Foundry Locus of Authority: https://obofoundry.org/principles/fp-011-locus-of-authority.html
* OBO Foundry Stability of Term Meaning: https://obofoundry.org/principles/fp-019-term-stability.html
* Dublin Core Terms: https://www.dublincore.org/specifications/dublin-core/dcmi-terms/
* PROV-O: https://www.w3.org/TR/prov-o/
* DCAT: https://www.w3.org/TR/vocab-dcat-3/
