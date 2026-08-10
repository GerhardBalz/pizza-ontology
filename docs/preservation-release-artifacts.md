# Preservation Release Artifacts

## Status

Adopted artifact policy for the `pizza-ontology` preservation release line.

The central rule is:

> **A preservation repository release must not silently rewrite the historical semantic identity of Pizza Ontology 2.0.**

## Why a custom preservation path is needed

The repository was bootstrapped with ODK. Its generated Makefile contains standard OBO-oriented release machinery, including an OBO PURL base and date-based ontology version annotations.

Those defaults are useful for ontologies that intentionally publish through that infrastructure, but they are not the semantic authority model of this repository.

`GerhardBalz/pizza-ontology`:

- preserves the historical Pizza Ontology 2.0 identity;
- does not claim `purl.obolibrary.org/obo/pizza`;
- does not treat a repository preservation release as a new semantic Pizza ontology version.

Therefore the standard generated ODK `prepare_release` / `public_release` artifact path is not the preservation release path for this project.

## Preservation invariants

Any semantic preservation artifact must retain or explicitly trace to:

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

It must also retain the historical Pizza attribution and CC BY 3.0 licensing boundary documented in `NOTICE.md` and `LICENSE.md`.

## First release: preservation-v0.1.0

The first preservation release is deliberately conservative.

### Repository artifact

The Git tag / GitHub Release:

```text
preservation-v0.1.0
```

versions the **repository preservation and engineering state**.

GitHub's source archive for that tag contains:

- the preserved Pizza Ontology 2.0 editor baseline;
- ODK engineering configuration;
- semantic regression tests;
- provenance, identity, versioning, and licensing documentation;
- repository infrastructure.

### Semantic preservation artifact

A custom Make target produces:

```text
target/preservation-release/pizza-2.0-preserved.ofn
target/preservation-release/SHA256SUMS
```

Run from `src/ontology`:

```bash
odkrun make preservation_release_artifact
```

or within the ODK container:

```bash
make preservation_release_artifact
```

The artifact is an exact byte-for-byte copy of `pizza-edit.owl`, renamed with an `.ofn` suffix to make the OWL Functional Syntax serialization explicit.

The target fails if the source no longer contains the expected historical ontology IRI, version IRI, `owl:versionInfo`, or Pizza entity namespace, or if an OBO-style Pizza release IRI appears in the preservation source.

The target also verifies the copied artifact with `cmp` and produces a SHA-256 checksum.

## Not release assets in preservation-v0.1.0

The following generated ODK artifacts are deliberately **not** preservation release assets while the generated rules annotate them with OBO-style release identity:

```text
pizza.owl
pizza-non-classified.owl
```

Their omission is intentional, not a missing build step.

## Future distributions

Later preservation releases may add distributions such as:

```text
RDF/XML
Turtle
JSON-LD
classified semantic modules
SHACL shapes
```

Before such a distribution becomes a release asset, automated verification should establish at minimum:

1. semantic identity and provenance are preserved or explicitly represented;
2. the distribution does not claim an unowned ontology/release IRI;
3. the artifact is traceable to the tagged Pizza 2.0 baseline;
4. licensing and attribution remain clear;
5. serialization or reasoning does not introduce unintended semantic changes.

## ODK relationship

ODK remains the engineering and QC environment.

```text
ODK
  ├── build / QC / ROBOT / HermiT
  └── generated standard release machinery

pizza.Makefile
  └── preservation-specific invariants and artifact target
```

Preservation-specific behavior belongs in `pizza.Makefile`, which is included by the generated Makefile, rather than by hand-editing generated ODK internals.

## Release checklist relationship

The first preservation release is tracked in GitHub issue #7.

The preservation-safe artifact decision is tracked in issue #9.
