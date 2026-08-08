# Editing the Pizza Ontology

These notes are for contributors working on the ontology and ODK engineering files in this repository.

## Editor source

The ontology editor source is:

```text
src/ontology/pizza-edit.owl
```

The current source preserves the historical Pizza 2.0 ontology, including its ontology IRI, version IRI, entity namespace, and intentionally unsatisfiable teaching examples.

## Editing with Protégé

Open `pizza-edit.owl` in Protégé when making ontology edits. Before saving, confirm that you are editing the repository's editor source rather than a generated release artifact.

The current preservation baseline should not silently change historical entity IRIs or semantics. Proposed breaking semantic or identifier changes should be discussed as a possible successor-ontology change.

## Validation

Run the complete repository test target from this directory:

```bash
odkrun make test
```

The custom `reason_test` expects exactly two intentionally unsatisfiable Pizza 2.0 classes:

- `CheeseyVegetableTopping`
- `IceCream`

The overall test target must finish successfully.

## Updating ODK-managed files

Project configuration lives in:

```text
pizza-odk.yaml
```

After changing it, regenerate ODK-managed files with ODK Runner:

```bash
odkrun odk.py update
```

Review the resulting Git diff before committing.

Do not put project-specific Make rules into the generated `Makefile`. Put overrides and custom targets in:

```text
pizza.Makefile
```

## Git workflow

Do not commit or push directly to `main`.

Use a focused branch, run the appropriate validation, commit the change, push the branch, and open a pull request. Merge only through the pull request after review and successful checks.

See the repository-level [`CONTRIBUTING.md`](../../CONTRIBUTING.md) for the full workflow.

## Identity and provenance

This repository is currently a preservation, migration, engineering, and learning environment derived from the historical Pizza 2.0 ontology. It does not claim authority over the historical `co-ode.org` identifier space.

See:

- [`docs/identity-publication-model.md`](../../docs/identity-publication-model.md)
- [`docs/pizza-provenance.md`](../../docs/pizza-provenance.md)
