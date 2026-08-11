# preservation-v0.2.0 publication record

`preservation-v0.2.0` is published at:

```text
https://github.com/GerhardBalz/pizza-ontology/releases/tag/preservation-v0.2.0
```

The release tag resolves to:

```text
3bd6e3817e2cdc44e77899a2e603878a85845e9d
```

This is a repository preservation release of the unchanged Pizza Ontology 2.0 semantic baseline. It is not a new Pizza ontology semantic version.

## Published distribution assets

The governed release asset set is:

```text
pizza-2.0-preserved.ofn
pizza-2.0-preserved.ttl
SHA256SUMS
```

Direct distribution locations are recorded in [`../../metadata/publication.ttl`](../../metadata/publication.ttl) as `dcat:Distribution` resources with real `dcat:downloadURL` values.

`preservation-v0.1.0` remains unchanged and intentionally has no retrofitted multi-format release distributions.

## External publication verification

[`../../metadata/verify_published_release.py`](../../metadata/verify_published_release.py) verifies the published release from an external-consumer path rather than from local build output. It checks:

- the public GitHub release record and exact three-asset set;
- release tag → commit binding;
- direct asset download URLs;
- the published `SHA256SUMS` manifest against downloaded `.ofn` and `.ttl` bytes;
- byte identity between the published Functional Syntax distribution and the tag-pinned editor ontology;
- historical ontology IRI, version IRI, and entity namespace anchors in the published Turtle bytes;
- GitHub-provided asset digests when available.

The pre-publication ROBOT build remains responsible for proving graph equivalence between the preserved Functional Syntax source and the Turtle serialization.

The publication verifier is run in normal CI so later repository work cannot silently move the release tag, alter its expected asset contract, or leave machine-readable publication metadata pointing at non-existent assets.
