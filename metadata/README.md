# Publication Metadata

`publication.ttl` is the machine-readable publication catalog for the Pizza Ontology preservation line.

It keeps repository preservation releases and their concrete distributions separate from the historical Pizza semantic identifiers.

`url-iri-inventory.json` is the machine-readable classification and resolution contract for Pizza-specific HTTP(S) identifiers and locations. It distinguishes semantic identifiers from source, publication, download, documentation, and UX URLs and contains the proposed W3ID preservation/reference route plan.

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

## URL/IRI resolution contract

The operational rule is:

```text
historical semantic identifier
    ≠
current Web location
```

Canonical actionable URLs are recorded with an explicit verification path. Historical Pizza IRIs are recorded as non-actionable semantic identifiers rather than being treated as failed publication URLs.

See [Pizza URL/IRI Resolution Inventory](../docs/url-iri-resolution-inventory.md).

## Verification

Local RDF publication contract:

```bash
python metadata/verify_publication_metadata.py
```

URL/IRI classification and historical-identity contract:

```bash
python metadata/verify_url_iri_inventory.py
```

URL/IRI contract plus live checks for canonical actionable URLs:

```bash
python metadata/verify_url_iri_inventory.py --check-http
```

External published-release contract:

```bash
python metadata/verify_published_release.py
```

The external verifier reads the public GitHub release/tag APIs and direct download URLs, validates the exact published asset set and checksums, compares the released Functional Syntax bytes with the tag-pinned source, and confirms the historical semantic identity anchors in the published Turtle distribution.
