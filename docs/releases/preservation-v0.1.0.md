# preservation-v0.1.0

## First preservation and engineering release

`preservation-v0.1.0` is the first repository release of `GerhardBalz/pizza-ontology`.

It is a **repository preservation release**, not a new semantic version of the historical Pizza ontology.

## Semantic baseline

This release preserves **Pizza Ontology 2.0**:

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

No new official historical Pizza ontology version is claimed by this release.

## What this release establishes

- preservation/stewardship role for the repository;
- ODK-managed Pizza 2.0 editor baseline;
- reproducible ontology QC;
- semantic regression checks for the two intentional unsatisfiable tutorial classes;
- ontology identity and publication model;
- Pizza provenance and authority analysis;
- independent repository preservation versioning;
- explicit licensing and attribution boundaries;
- preservation-safe semantic identity checks;
- a preservation-safe OWL Functional Syntax release artifact target.

## Preservation semantic artifact

From `src/ontology`:

```bash
odkrun make preservation_release_artifact
```

produces:

```text
target/preservation-release/pizza-2.0-preserved.ofn
target/preservation-release/SHA256SUMS
```

`pizza-2.0-preserved.ofn` is an exact copy of the preserved editor ontology. The target verifies the expected historical semantic identity and fails if an OBO-style Pizza release IRI appears in the preservation source.

## ODK release artifacts intentionally excluded

The generated ODK Makefile currently contains standard OBO-oriented release rules that annotate `pizza.owl` and `pizza-non-classified.owl` with OBO PURL/date-based release identity.

Those files are **not** preservation release assets in `preservation-v0.1.0`.

This repository does not claim `purl.obolibrary.org/obo/pizza`, and repository release `preservation-v0.1.0` must not be confused with a new semantic Pizza ontology release.

## Licensing and attribution

The release uses an explicit licensing boundary:

- historical Pizza Ontology 2.0 semantic content: **CC BY 3.0**;
- new repository software and engineering material: **MIT** unless stated otherwise;
- new original repository documentation: **CC BY 4.0** unless stated otherwise;
- third-party material: its own license.

See `LICENSE.md` and `NOTICE.md`.

## Provenance

The preservation baseline is derived from the Pizza 2.0 ontology distributed by the Stanford Protégé site and the wider Manchester / Protégé OWL tutorial tradition.

The repository does not claim to be the original semantic authority, source repository, or legal rights holder of the historical Pizza ontology.

See `docs/pizza-provenance.md`.

## Successor ontology

A future modernized Pizza ontology may be created as a separate successor lineage with a new authority model, ontology identity, governed namespace, repository, mappings, and version series.

That possible successor does not replace this preservation line and is not part of `preservation-v0.1.0`.

## Next directions

After the preservation baseline release, the project can evolve through the existing tracks, including:

- OAK access and query examples;
- additional verified distributions such as Turtle;
- SHACL and semantic validation assets;
- semantic projections into schemas and APIs;
- ontology-informed UX;
- integration with Executable Semantic Knowledge Architecture (ESKA).
