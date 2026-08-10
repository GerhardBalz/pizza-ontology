# Licensing

This repository contains material from different sources and does not apply one blanket license to every artifact.

The applicable license depends on the origin and type of the material.

## Historical Pizza Ontology semantic content

The historical **Pizza Ontology 2.0** semantic baseline used by this repository declares:

> Creative Commons Attribution 3.0 (CC BY 3.0)

This includes the preserved ontology source in `src/ontology/pizza-edit.owl` and distributions that reproduce or transform the historical Pizza semantic content.

Canonical license information:

https://creativecommons.org/licenses/by/3.0/

The historical semantic content remains subject to its upstream attribution and provenance. See [NOTICE.md](NOTICE.md) and [docs/pizza-provenance.md](docs/pizza-provenance.md).

## New repository software and engineering material

Unless a file states otherwise, newly created software and engineering material in this repository is licensed under the **MIT License**.

This category includes repository-authored material such as:

- scripts and executable examples;
- CI/workflow code;
- tests and semantic regression infrastructure;
- build and packaging code;
- repository-specific configuration authored for this project.

The MIT license text is provided in [LICENSES/MIT.txt](LICENSES/MIT.txt).

## New repository documentation

Unless a document states otherwise, newly created original documentation in this repository is licensed under the **Creative Commons Attribution 4.0 International (CC BY 4.0)** license.

Canonical license information:

https://creativecommons.org/licenses/by/4.0/

This applies to repository-authored explanatory and architectural documentation, not to embedded or reproduced historical Pizza semantic content.

## Generated and mixed artifacts

A generated artifact does not automatically inherit the license of the tool that generated it.

For example:

```text
Pizza Ontology 2.0
        │
        │ transformed / serialized / packaged
        ▼
OWL / Turtle / classified / non-classified distribution
```

If the generated distribution contains the historical Pizza semantic content, that semantic content remains under **CC BY 3.0**.

Repository-authored scripts or build infrastructure used to generate the distribution may separately be under MIT.

If an artifact combines material under more than one license, the applicable notices must be retained and the licenses must not be represented as if one silently replaces the other.

## Third-party material

Third-party dependencies, tools, examples, or imported material retain their own licenses. Their inclusion or use by this repository does not relicense them under MIT, CC BY 4.0, or the Pizza Ontology's CC BY 3.0 terms.

## Summary

```text
Historical Pizza Ontology 2.0 semantic content
    → CC BY 3.0

New repository software / engineering material
    → MIT

New original repository documentation
    → CC BY 4.0

Third-party material
    → its own license
```

When a more specific license notice accompanies a file or artifact, that more specific notice takes precedence for that material.
