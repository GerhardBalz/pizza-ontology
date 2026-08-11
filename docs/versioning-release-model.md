# Versioning and Release Model

## Status

Adopted preservation and repository-release model for `GerhardBalz/pizza-ontology`.

This repository distinguishes the semantic version of the historical Pizza ontology from versions of this preservation and engineering repository.

The central rule is:

> **A release of this repository is not a new semantic version of the historical Pizza ontology.**

## 1. Historical Semantic Baseline

The repository preserves **Pizza Ontology 2.0** as its historical semantic baseline.

```text
Ontology
Pizza Ontology

Ontology IRI
http://www.co-ode.org/ontologies/pizza

Version IRI
http://www.co-ode.org/ontologies/pizza/2.0.0

owl:versionInfo
2.0

Entity namespace
http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

Within the preservation line, this semantic baseline is treated as immutable unless a future correction is explicitly documented as a preservation correction rather than silently presented as a new historical Pizza version.

The historical ontology metadata also mentions earlier versions 1.4 and 1.5. Those are part of the upstream ontology history; they are not separate maintained release lines in this repository.

## 2. Repository Preservation Releases

The repository evolves independently around the historical semantic baseline. It contains engineering, documentation, access, validation, projection, publication, and integration artifacts that can change without changing Pizza Ontology 2.0.

Repository releases therefore use a separate release series:

```text
preservation-v0.1.0
preservation-v0.2.0
preservation-v0.3.0
...
```

A repository release can contain, for example:

```text
preservation-v0.2.0
    │
    ├── Pizza Ontology 2.0
    ├── ODK project configuration
    ├── semantic regression tests
    ├── provenance and governance documentation
    ├── OAK access examples
    ├── additional distributions
    ├── SHACL shapes and data examples
    └── ESKA integration metadata/examples
```

while the contained ontology still declares:

```text
owl:versionInfo 2.0
```

### Repository release semantics

The preservation release series follows semantic-versioning-style engineering semantics for the repository, not for the historical ontology:

- **MAJOR** — incompatible change to the repository's preservation/distribution/integration contract;
- **MINOR** — backward-compatible new engineering capability, distribution, example, or documented contract;
- **PATCH** — backward-compatible correction to repository infrastructure, documentation, tests, or packaging.

While the preservation repository is still establishing its contracts, the release line remains `0.x.y`.

## 3. Distribution Versions

A distribution is a representation or packaged artifact of semantic knowledge. Examples include:

```text
OWL Functional Syntax
RDF/XML
Turtle
classified ontology
non-classified ontology
SHACL shapes
```

Distribution type is not semantic version.

For example, the current ODK setting:

```text
primary_release: non-classified
```

describes an artifact type, not a version of Pizza.

Distributions should be associated with a repository preservation release and remain traceable to the Pizza 2.0 semantic baseline from which they are produced or derived.

Generated distributions containing historical Pizza semantic content retain the applicable upstream semantic-content license. Repository-authored tooling used to produce them may have a separate software license. See [../LICENSE.md](../LICENSE.md).

## 4. Toolchain Versions

Tool versions are another independent dimension. Examples include:

```text
ODK container version
ROBOT version
HermiT version
OAK version
```

A toolchain upgrade can result in a new repository preservation release without changing the semantic version of Pizza Ontology 2.0.

Tool versions should be pinned or recorded where reproducibility requires it.

## 5. Published and Planned Preservation Releases

### preservation-v0.1.0 — published baseline

The first repository preservation release is published as:

```text
preservation-v0.1.0
```

It established the conservative preservation baseline rather than claiming new Pizza semantics.

Its scope includes:

- Pizza Ontology 2.0 preserved as the semantic baseline;
- ODK-managed editor ontology;
- reproducible QC and semantic regression tests;
- ontology identity and publication model;
- Pizza provenance and authority analysis;
- this versioning and release model;
- clear attribution and licensing boundaries as defined in [LICENSE.md](../LICENSE.md) and [NOTICE.md](../NOTICE.md);
- release notes that explicitly distinguish repository release version from ontology version.

The release remains historically immutable. Engineering capabilities and distributions added after its source snapshot must not be retrofitted and presented as though they were part of `preservation-v0.1.0`.

### preservation-v0.2.0 — next preservation release

The next planned MINOR release is:

```text
preservation-v0.2.0
```

It is justified by backward-compatible engineering/reference additions since v0.1.0, including OAK access/query examples, executable semantic artifacts, implementation projections, application/UX references, and broader architecture/governance documentation while retaining Pizza Ontology 2.0 unchanged.

It is also the first release intended to publish the verified multi-format preservation distribution set as immutable release assets:

```text
pizza-2.0-preserved.ofn
pizza-2.0-preserved.ttl
SHA256SUMS
```

The generated artifacts must correspond to the exact tagged repository source revision and pass preservation identity, semantic-equivalence, and checksum verification before publication.

Later preservation releases may add further engineering capabilities, distributions, examples, or contracts without changing the historical ontology version.

## 6. Successor Ontology Lineage

Preservation does not prevent semantic modernization.

If a modernized Pizza ontology is created, it should be treated as a **successor ontology lineage**, not as an implicit continuation of the historical `co-ode.org` namespace.

```text
Historical Pizza Ontology 2.0
        │
        │ prov:wasDerivedFrom / explicit mappings
        ▼
Successor Pizza ontology
        │
        ├── new repository
        ├── explicit authority / stewardship
        ├── new ontology IRI
        ├── new governed entity namespace
        └── independent version series
```

Unless authority over the historical Pizza identifier space is established, the successor should not simply be called `Pizza 2.1`, `Pizza 3.0`, or use new version IRIs beneath `http://www.co-ode.org/ontologies/pizza`.

Mappings between historical and successor entities should be explicit and selected according to their actual semantic relationship.

## 7. Version Dimensions

The resulting model is:

```text
Semantic ontology version
    Pizza Ontology 2.0

Repository preservation release
    preservation-v0.x.y

Distribution / artifact type
    OWL / Turtle / classified / non-classified / SHACL / ...

Toolchain versions
    ODK / ROBOT / HermiT / OAK / ...

Possible successor ontology version
    separate lineage and version series
```

These dimensions must not be collapsed into one version number.

## 8. Release Naming Rule

Repository tags and GitHub Releases for the preservation line should use the explicit prefix:

```text
preservation-v<major>.<minor>.<patch>
```

This avoids a bare tag such as `v2.0.0`, which could be misread as an official release of the historical Pizza Ontology 2.0 by this repository.

## 9. Governance

The current repository role is:

> **Preservation, stewardship, engineering, and learning environment derived from Pizza Ontology 2.0.**

A future successor ontology may coexist with this preservation line. Creating such a successor is a separate architecture and governance decision and does not replace the responsibility to preserve the historical Pizza 2.0 artifact accurately.

Licensing follows the same separation of concerns as versioning: historical Pizza semantic content retains its upstream license, while newly authored repository software and documentation use separately declared licenses. See [LICENSE.md](../LICENSE.md).

The versioning strategy was established through GitHub issue #3. The first release was tracked through #7; preparation/publication of `preservation-v0.2.0` is tracked through #65.
