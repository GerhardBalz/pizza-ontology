# Publication and Distribution Policy

## Status

Adopted publication policy for the Pizza Ontology preservation line.

This document defines **where repository preservation releases and preservation-safe distributions are published, how those locations relate to semantic identifiers, and which locations consumers may treat as stable**.

It applies the architecture in:

- `docs/identity-publication-model.md`;
- `docs/pizza-provenance.md`;
- `docs/versioning-release-model.md`;
- `docs/preservation-distributions.md`;
- `docs/semantic-architecture.md`.

The governing principle is:

> **Semantic identity, repository release, distribution, source revision, and publication location are different things.**

## 1. Publication roles

The preservation line distinguishes five kinds of references.

```text
Historical semantic identifier
    identifies Pizza ontology meaning

Repository release
    identifies an immutable publication decision for this repository

Distribution
    identifies a concrete serialization or packaged artifact

Source revision
    identifies the exact Git state from which an artifact is reproduced

Publication location
    tells a consumer where a release or distribution can be accessed
```

No one reference should silently serve all five roles.

## 2. Historical Pizza identifiers remain semantic identifiers

The preserved Pizza 2.0 baseline continues to use its historical identifiers:

```text
Ontology IRI
http://www.co-ode.org/ontologies/pizza

Version IRI
http://www.co-ode.org/ontologies/pizza/2.0.0

Entity namespace
http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

This repository does **not** control the historical `co-ode.org` identifier space and therefore does not redefine those IRIs as repository publication URLs.

If a historical IRI does not resolve reliably, that is treated as a **resolution/publication problem**, not as permission to change the preserved semantic identity.

The preservation line may provide working access locations for the same preserved content while retaining the historical identifiers inside the ontology.

## 3. Upstream preservation source

The upstream Pizza 2.0 distribution used by this repository is:

```text
https://protege.stanford.edu/ontologies/pizza/pizza.owl
```

This is recorded as an upstream source location, for example with `dcterms:source` or PROV-O derivation relationships.

The Stanford URL is a host/location reference. It does not by itself establish present-day semantic authority over the historical Pizza namespace.

## 4. Repository publication locations

The repository home is:

```text
https://github.com/GerhardBalz/pizza-ontology
```

Its role is the engineering and stewardship environment for this preservation line.

The canonical publication record for a repository preservation release is its GitHub Release page:

```text
https://github.com/GerhardBalz/pizza-ontology/releases/tag/<PRESERVATION-TAG>
```

For example:

```text
https://github.com/GerhardBalz/pizza-ontology/releases/tag/preservation-v0.1.0
```

A GitHub Release page identifies a **repository preservation release**. It is not the Pizza ontology IRI or Pizza ontology version IRI.

## 5. Preservation distribution location policy

Beginning with the first preservation release that actually contains the generated multi-format distribution set, preservation-safe ontology distributions should be attached to the corresponding GitHub Release as immutable release assets.

The expected asset set is:

```text
pizza-2.0-preserved.ofn
pizza-2.0-preserved.ttl
SHA256SUMS
```

Additional verified serializations may be added in later repository releases without changing the historical Pizza 2.0 semantic version.

The release asset pattern is:

```text
https://github.com/GerhardBalz/pizza-ontology/releases/download/<PRESERVATION-TAG>/<ASSET>
```

A direct release-asset URL is a **distribution location**. It must not be embedded into the ontology as a replacement ontology IRI or version IRI.

## 6. Do not retrofit `preservation-v0.1.0`

`preservation-v0.1.0` established the conservative source-snapshot baseline before the preservation-safe Turtle distribution was added to the engineering workflow.

The release should therefore remain historically accurate and immutable.

The repository must **not** attach a newly generated Turtle artifact from a later source revision to `preservation-v0.1.0` and present it as though it formed part of that release.

Instead, a subsequent preservation release should publish the verified Functional Syntax and Turtle distributions together with their checksums.

This preserves the invariant:

```text
release contents
    correspond to
release source revision
```

## 7. Canonical versus convenient locations

The project uses the following stability model.

| Reference | Role | Stability expectation | Canonical for |
|---|---|---|---|
| Historical ontology IRI | semantic identifier | historical / externally governed | ontology identity |
| Historical version IRI | semantic identifier | historical / externally governed | Pizza 2.0 semantic version |
| Historical entity IRI | semantic identifier | historical / externally governed | Pizza entities |
| Stanford Pizza URL | upstream location | externally hosted | upstream preservation source |
| GitHub repository URL | repository location | stable project entry point | stewardship/engineering project |
| GitHub Release page | release publication record | immutable by policy | repository preservation release |
| GitHub release asset URL | direct distribution location | immutable by policy | released distribution bytes |
| Git tag | source/release revision reference | immutable by policy | released repository state |
| Commit-pinned GitHub URL | immutable source location | immutable | exact source bytes / provenance |
| `main` branch URL | development convenience | mutable | latest project state only |
| `raw.githubusercontent.com/.../main/...` | development convenience | mutable | latest raw file only |

Consumers that require reproducibility should prefer a release tag, release asset, or commit-pinned source URL rather than `main`.

## 8. Machine-readable metadata rules

The project prefers established vocabularies rather than defining Pizza-specific publication vocabulary.

Recommended terms include:

```text
dcat:Catalog       publication catalog
dcat:Dataset       release-level or dataset-level publication record
dcat:Distribution  concrete published representation
dcat:landingPage   human-facing project/release page
dcat:accessURL     access page when direct download is not the intended relation
dcat:downloadURL   direct downloadable distribution location

dcterms:identifier local or release identifier
dcterms:source     upstream or source reference
dcterms:relation   related semantic resource
dcterms:format     media/serialization format
dcterms:license    applicable license

prov:wasDerivedFrom provenance/derivation relation
prov:wasRevisionOf revision relation where applicable
```

### `dcat:downloadURL`

Use `dcat:downloadURL` only when the referenced file **actually exists as a published immutable release asset**.

Do not mint speculative download URLs for planned releases or distributions.

### `dcat:accessURL` and `dcat:landingPage`

Use these for repository or release pages where the consumer first accesses or understands the publication.

They are locations, not semantic identifiers.

### `dcterms:source`

Use this for upstream source locations or exact repository source references where appropriate.

It must not be used to imply that the repository owns the historical Pizza namespace.

## 9. Current machine-readable publication catalog

`metadata/publication.ttl` records the current repository publication facts that actually exist:

- the preservation repository/catalog;
- the historical Pizza ontology relation;
- the Stanford upstream source;
- the published `preservation-v0.1.0` release landing page;
- the tag-pinned release source location.

It intentionally does **not** claim `dcat:downloadURL` values for ontology release assets that were not part of `preservation-v0.1.0`.

When a subsequent repository preservation release publishes the verified `.ofn`, `.ttl`, and checksum assets, that release's metadata can add corresponding `dcat:Distribution` resources and real `dcat:downloadURL` values.

## 10. Publication flow for future preservation releases

A future multi-format preservation release should follow this sequence:

```text
source revision selected
        ↓
ODK/ROBOT QC green
        ↓
preservation distributions generated
        ↓
identity + semantic-equivalence checks green
        ↓
SHA256SUMS generated
        ↓
repository tag created
        ↓
GitHub Release created
        ↓
verified assets attached
        ↓
machine-readable publication metadata records actual asset URLs
```

The release tag and released files must all correspond to the same source state.

## 11. Consumer resolution guidance

A consumer should choose a reference according to intent.

### I need the semantic identifier

Use the historical ontology, version, or entity IRI.

### I need the upstream historical file

Use the Stanford Protégé source location recorded by the repository.

### I need an immutable repository publication

Use the relevant `preservation-vX.Y.Z` GitHub Release page.

### I need immutable distribution bytes

Use a release-asset `dcat:downloadURL` when that asset is published, and verify it against `SHA256SUMS` where supplied.

### I need the exact engineering source

Use the release tag or a commit-pinned GitHub source URL.

### I need the latest development state

Use `main`, understanding that it is mutable and not an immutable publication reference.

## 12. Authority and hosting invariant

The preservation line makes no inference from hosting to semantic authority.

```text
GitHub hosts this repository
    ≠ GitHub is Pizza ontology authority

GerhardBalz owns this repository
    ≠ repository owner owns the historical Pizza namespace

Stanford hosts an upstream Pizza file
    ≠ hosting alone establishes sole current semantic authority

working URL
    ≠ semantic identifier
```

This is especially important when historical semantic identifiers are not resolvable.

## 13. Relationship to a possible successor ontology

A future successor Pizza ontology would need its own publication and identifier policy because it would establish a new governed semantic lineage.

That successor could legitimately choose resolvable ontology/entity IRIs under a controlled namespace.

It must not solve the historical preservation-line location problem by silently changing the identifiers of Pizza Ontology 2.0.

## Architectural invariant

> **The preservation line publishes repository releases and concrete distributions at locations it controls, while preserving historical Pizza semantic identifiers and making no unsupported claim of authority over their namespace.**
