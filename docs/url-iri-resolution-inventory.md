# Pizza URL/IRI Resolution Inventory

## Status

Implementation inventory for Pizza issue #72.

This document operationalizes the existing [Publication and Distribution Policy](publication-distribution-policy.md). It does not introduce a second identity model.

The governing distinction is:

```text
semantic identifier
    ≠
current Web location
```

Historical Pizza 2.0 HTTP IRIs remain semantic identifiers even when their Web dereference behavior is poor. URLs that this preservation/reference project presents as current source, publication, download, documentation, or UX navigation are treated separately and are expected to resolve.

The machine-readable source for this inventory is [`metadata/url-iri-inventory.json`](../metadata/url-iri-inventory.json). [`metadata/verify_url_iri_inventory.py`](../metadata/verify_url_iri_inventory.py) checks the classification, historical identity anchors, projection traceability, UX boundary, route plan, and—when invoked with `--check-http`—canonical actionable URLs.

## 1. Historical semantic identifiers

These are preserved as identifiers, not advertised as repository-owned navigation URLs.

| Reference | Classification | Actionable link? | Project controls namespace? |
|---|---|---:|---:|
| `http://www.co-ode.org/ontologies/pizza` | ontology semantic identifier | No | No |
| `http://www.co-ode.org/ontologies/pizza/2.0.0` | version semantic identifier | No | No |
| `http://www.co-ode.org/ontologies/pizza/pizza.owl#…` | entity semantic identifier | No | No |
| `http://www.co-ode.org/ontologies/pizza#…` | preserved historical/default prefix | No | No |

The project therefore does not make a failed HTTP dereference of one of these IRIs equivalent to a broken repository publication URL.

The preserved ontology also contains the historical tutorial reference:

```text
http://owl.cs.manchester.ac.uk/publications/talks-and-tutorials/protg-owl-tutorial
```

That reference is preserved as historical source text. The preservation line does not promise its continued availability.

## 2. Current source and publication locations

The following references are locations rather than Pizza semantic identity.

| Reference | Role | Resolution contract |
|---|---|---|
| `https://protege.stanford.edu/ontologies/pizza/pizza.owl` | upstream/current preservation source location | HTTP-verified |
| `https://github.com/GerhardBalz/pizza-ontology` | preservation/reference project | GitHub API-verified |
| `…/releases/tag/preservation-v0.1.0` | immutable repository release landing page | GitHub API-verified |
| `…/releases/tag/preservation-v0.2.0` | immutable repository release landing page | GitHub API-verified |
| tag- and commit-pinned `src/ontology/pizza-edit.owl` URLs | immutable source locations | GitHub contents API-verified |
| v0.2.0 `.ofn`, `.ttl`, and `SHA256SUMS` release assets | immutable download URLs | existing published-release verifier |
| `metadata/publication.ttl` | current machine-readable publication catalog | GitHub contents API-verified |
| `docs/pizza-provenance.md` | current provenance documentation | GitHub contents API-verified |
| Pizza Semantic Explorer on GitHub Pages | application/UX link | HTTP-verified |

The exact canonical references and verification paths live in `metadata/url-iri-inventory.json`.

## 3. Repository-wide classification

The verifier scans text artifacts for Pizza-specific HTTP(S) references under these families:

```text
co-ode.org Pizza identifiers
Manchester Pizza tutorial reference
Stanford Pizza source
GerhardBalz/pizza-ontology GitHub project/release/source URLs
GerhardBalz/pizza-ontology raw GitHub URLs
GerhardBalz/pizza-ontology GitHub Pages URLs
```

Occurrences are classified as one of:

```text
semantic_identifier
historical_source_reference
current_source_location
publication_landing_page
access_url
download_url
documentation_reference_url
application_ux_link
```

The rule set is deliberately about **roles**, not HTTP syntax. An HTTP-looking IRI is not automatically an actionable Web link.

## 4. UX rule

The two Pizza explorers may display:

```text
pizza:Pizza
http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza
```

as semantic identity and traceability.

They must not silently turn those historical IRI values into navigation links.

A future UX may expose a separate action such as:

```text
Preserved definition
Source
Publication
```

but the target of that action must be a verified location/reference URL, not a historical Pizza IRI merely because the IRI uses the `http` scheme.

The CI verifier statically checks the current direct-projection and API-backed JavaScript for this boundary.

## 5. Proposed persistent preservation/reference namespace

The first route design is:

```text
https://w3id.org/pizza-ontology/
```

This is intentionally a **preservation/reference namespace**. It is not proposed as a replacement for:

```text
Ontology IRI
http://www.co-ode.org/ontologies/pizza

Version IRI
http://www.co-ode.org/ontologies/pizza/2.0.0

Entity namespace
http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

Candidate routes:

| W3ID path | Role | Target |
|---|---|---|
| `/pizza-ontology/` | project/publication landing page | preservation repository |
| `/pizza-ontology/2.0/source` | upstream source location | Stanford Pizza source |
| `/pizza-ontology/2.0/preservation` | repository preservation publication | `preservation-v0.2.0` release |
| `/pizza-ontology/2.0/preserved.ofn` | immutable distribution | v0.2.0 OFN asset |
| `/pizza-ontology/2.0/preserved.ttl` | immutable distribution | v0.2.0 Turtle asset |
| `/pizza-ontology/2.0/SHA256SUMS` | checksum manifest | v0.2.0 checksum asset |
| `/pizza-ontology/publication` | current publication catalog | `metadata/publication.ttl` |
| `/pizza-ontology/provenance` | provenance documentation | `docs/pizza-provenance.md` |

The route names use terms such as `source`, `preservation`, and `preserved.ttl` deliberately. They avoid making `/pizza-ontology/2.0/` appear to be the historical Pizza `owl:versionIRI`.

## 6. Entity reference routes are deferred

This increment does **not** introduce routes such as:

```text
https://w3id.org/pizza-ontology/entity/Pizza
```

Such a route may eventually be useful as a resolvable preservation/reference link, but it would need an explicit mapping and presentation contract so consumers do not mistake a repository reference alias for the historical semantic identity.

Until that contract exists:

```text
historical Pizza entity IRI
    remains semantic identity

resolvable entity reference
    not yet minted
```

## 7. Verification

Static contract:

```bash
python metadata/verify_url_iri_inventory.py
```

Static contract plus canonical actionable URL resolution:

```bash
python metadata/verify_url_iri_inventory.py --check-http
```

The existing publication verifier remains responsible for the deeper immutable v0.2.0 release-asset contract:

```bash
python metadata/verify_published_release.py
```

CI runs the URL/IRI verifier with live resolution enabled before the existing published-release verification.

## 8. Next step

After this inventory/contract PR is reviewed and merged:

1. prepare the `perma-id/w3id.org` configuration for the proposed preservation/reference routes;
2. submit the W3ID PR;
3. keep the route plan marked `proposed` until the upstream PR is merged;
4. switch the route plan to active and add W3ID resolution checks only after the routes actually resolve;
5. separately evaluate whether entity-level preservation/reference routes are useful and semantically safe.

Issue #4 remains the separate decision point for a future successor Pizza ontology whose *own* governed semantic identifiers could themselves be resolvable.
