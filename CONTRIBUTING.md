# Contributing to Pizza Ontology

Thank you for contributing to the Pizza Ontology reference project.

This repository preserves the historical Pizza 2.0 ontology while using it as a reference environment for ontology engineering, access, publication, semantic modeling, and executable knowledge experiments.

## Contribution workflow

All changes must go through a branch and pull request. Do not commit or push changes directly to `main`.

1. Start from an up-to-date `main` branch.
2. Create a focused branch for one logical change.
3. Make and validate the change.
4. Commit with a concise, descriptive message.
5. Push the branch.
6. Open a pull request against `main`.
7. Let the automated checks run and review the diff.
8. Merge through the pull request, preferably using squash merge for focused changes.

Keep branches and pull requests small enough to review comfortably.

## Documentation convention

Pizza adopts the shared [Semantic Knowledge Engineering Semantic Markdown convention](https://github.com/GerhardBalz/semantic-knowledge-engineering/blob/main/conventions/semantic-markdown.md):

- use ordered Markdown lists when order or procedure is part of the meaning;
- use unordered Markdown lists for non-sequential collections;
- reserve fenced blocks for code, commands, literal syntax, identifiers, diagrams, aligned specimens, or output where preformatted layout carries meaning.

Do not mechanically convert semantic architecture diagrams, ontology expressions, execution traces, formulas, identifier blocks, command examples, or other literal/preformatted specimens into lists merely because they contain multiple lines.

This convention was promoted to SKE after review feedback from @TallTed on `perma-id/w3id.org#6530` and is shared with ESKA and SMO.

## Validation

For ontology, ODK, build, or semantic-test changes, run from `src/ontology`:

```bash
odkrun make test
```

The Pizza 2.0 baseline intentionally contains two unsatisfiable tutorial classes. The repository's custom semantic regression test verifies that these remain exactly:

- `CheeseyVegetableTopping`
- `IceCream`

A reasoning error mentioning those two classes is therefore expected inside that regression test; the overall test target must still complete successfully.

For documentation-only changes, inspect rendered Markdown and verify links and paths.

## Ontology changes

`src/ontology/pizza-edit.owl` is the editor source.

The current repository is preservation-oriented: it keeps the historical Pizza 2.0 ontology IRI, version IRI, entity IRIs, and teaching semantics. Changes to the preserved ontology should therefore be deliberate and should state whether they are:

- a correction to the preservation/migration environment,
- a documentation or metadata improvement,
- a non-breaking publication improvement,
- or a proposed semantic change that may belong in a future successor ontology instead.

Do not silently replace historical identifiers or alter the meaning of historical Pizza entities.

For provenance and identity decisions, see:

- [`docs/identity-publication-model.md`](docs/identity-publication-model.md)
- [`docs/pizza-provenance.md`](docs/pizza-provenance.md)

## ODK-managed files

The repository is managed with the Ontology Development Kit (ODK).

Do not edit the generated `src/ontology/Makefile` for project-specific behavior. Put custom Make rules in `src/ontology/pizza.Makefile`.

When changing `src/ontology/pizza-odk.yaml`, regenerate ODK-managed files with:

```bash
cd src/ontology
odkrun odk.py update
```

Review the generated diff before committing it.

## Issues

Use the repository issue tracker for ontology problems, documentation issues, tooling problems, provenance questions, or ideas for new examples:

https://github.com/GerhardBalz/pizza-ontology/issues

This project is not currently an OBO Foundry ontology and does not use OLS or OBO term-request governance as its contribution model.
