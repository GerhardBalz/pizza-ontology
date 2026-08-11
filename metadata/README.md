# Publication Metadata

`publication.ttl` is the machine-readable publication catalog for the Pizza Ontology preservation line.

It keeps repository preservation releases and their concrete distributions separate from the historical Pizza semantic identifiers.

## Current published releases

```text
preservation-v0.1.0
    repository source-snapshot release
    no retrofitted multi-format download assets

preservation-v0.2.0
    repository preservation/reference release
    ├── pizza-2.0-preserved.ofn
    ├── pizza-2.0-preserved.ttl
    └── SHA256SUMS
```

The v0.2.0 release distributions have concrete `dcat:downloadURL` values because those immutable GitHub Release assets now exist. The historical ontology IRI, version IRI, and entity IRIs remain semantic identifiers and are not given repository-owned download/landing semantics.

## Verification

Local RDF publication contract:

```bash
python metadata/verify_publication_metadata.py
```

External published-release contract:

```bash
python metadata/verify_published_release.py
```

The external verifier reads the public GitHub release/tag APIs and direct download URLs, validates the exact published asset set and checksums, compares the released Functional Syntax bytes with the tag-pinned source, and confirms the historical semantic identity anchors in the published Turtle distribution.
