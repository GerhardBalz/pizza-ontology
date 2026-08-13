# Pizza preservation/reference resolution

## Purpose

The Pizza Ontology 2.0 preservation line must improve Web navigation without rewriting historical semantic identity or implying authority over the `co-ode.org` namespace.

The governing rule is:

> **Historical Pizza 2.0 IRIs are semantic identifiers. Resolvable preservation/reference URLs are separate publication resources governed by this project.**

This implements Pizza #72 on top of the existing identity/publication model rather than creating a second ontology identity model.

## Identity boundary

The preserved historical identifiers remain:

```text
Ontology IRI
http://www.co-ode.org/ontologies/pizza

Version IRI
http://www.co-ode.org/ontologies/pizza/2.0.0

Entity namespace
http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

They are not converted into repository URLs, W3ID aliases, or new ontology identifiers.

A failed HTTP dereference of one of those historical IRIs is therefore not, by itself, a repository broken-link failure.

The historical source location remains separately identified as:

```text
https://protege.stanford.edu/ontologies/pizza/pizza.owl
```

Because the repository presents that URL as a source/reference location, it is an actionable resolution promise and is checked accordingly.

## Machine policy

`metadata/reference-resolution-policy.json` records:

- the historical ontology/version/entity identifiers;
- the historical Stanford source location;
- the protected source-file Git blob identity;
- the planned preservation/reference namespace;
- candidate route targets;
- which reference roles are repository resolution promises.

`scripts/verify_pizza_references.py` scans every tracked UTF-8 text artifact and records every Pizza-specific HTTP(S) occurrence with file and line evidence.

The inventory distinguishes:

```text
historical-semantic-identifier
historical-source-reference
current-source-location
publication-landing-page
download-url
repository-reference
preservation-reference-url
url-template
url-construction-base
```

Any Pizza-specific URL that cannot be classified fails the verifier rather than being silently treated as either identity or location.

URL templates and bare construction bases are retained as engineering evidence but are not treated as finished actionable links.

## Baseline evidence

The first governed CI baseline on 13 August 2026 established:

```text
Pizza-specific HTTP(S) occurrences        231
unique Pizza-specific URLs                 41
historical semantic-identifier occurrences 151
network-checked actionable URLs            13
network failures                            0
unclassified occurrences                    0
UX files checked                            4
UX semantic-IRI display expressions        10
UX semantic-IRI anchor violations           0
```

The historical source Git blob also remained exactly:

```text
397492e484de5560f8a7e048ce8999b707d94388
```

This result is important: the current project-controlled source, publication, and download locations are resolving. The preservation problem is therefore not primarily a set of broken current repository links. It is the need to make the distinction between historical HTTP-shaped semantic identifiers and governed actionable locations explicit, stable, and machine-verifiable.

The two existing UX examples already display ontology/version/entity IRIs as text or traceability metadata rather than using those historical IRIs as `href` navigation targets. The regression now makes that behavior contractual.

## Resolution promises

Current source, publication, download, and historical-source locations are checked over the network in CI.

Historical `co-ode.org` identifiers are excluded from this network promise by design.

The checker therefore protects the distinction:

```text
valid IRI syntax
        ≠
semantic identity
        ≠
HTTP dereferenceability
        ≠
repository publication promise
```

## Protected historical source

The repository's preserved source remains:

```text
src/ontology/pizza-edit.owl
```

The policy pins its current Git blob SHA-1:

```text
397492e484de5560f8a7e048ce8999b707d94388
```

The reference-resolution verifier requires that exact Git object identity. Publication/navigation work must therefore not mutate the historical Pizza 2.0 source as a side effect.

## Planned preservation/reference namespace

The proposed namespace is:

```text
https://w3id.org/pizza-ontology/
```

This namespace is explicitly a **preservation/reference namespace** owned by `GerhardBalz/pizza-ontology`. It is not asserted to be the Pizza Ontology 2.0 ontology IRI or entity namespace.

The proposed route set is:

```text
https://w3id.org/pizza-ontology/
  → current preservation project landing page

https://w3id.org/pizza-ontology/preservation/2.0/
  → preservation-v0.2.0 release landing page

https://w3id.org/pizza-ontology/preservation/2.0/source
  → tagged preserved Pizza 2.0 source

https://w3id.org/pizza-ontology/preservation/2.0/turtle
  → immutable preservation-v0.2.0 Turtle release asset

https://w3id.org/pizza-ontology/preservation/2.0/functional
  → immutable preservation-v0.2.0 Functional Syntax release asset

https://w3id.org/pizza-ontology/preservation/2.0/checksums
  → immutable preservation-v0.2.0 checksum manifest

https://w3id.org/pizza-ontology/provenance
  → current provenance documentation

https://w3id.org/pizza-ontology/publication
  → current machine-readable publication metadata
```

The explicit `preservation/` segment avoids presenting the new namespace as a replacement semantic version IRI.

Immutable preservation routes point to the governed `preservation-v0.2.0` tag/release assets, not mutable `main`.

Current project documentation routes may point to `main` because they are navigation/reference resources, not immutable ontology-version identifiers.

## Activation boundary

The W3ID namespace remains `planned` until:

1. the inventory and route design are reviewed in the Pizza repository;
2. backend targets are verified;
3. the matching W3ID configuration is submitted upstream;
4. the upstream PR is merged;
5. the public `w3id.org` routes are externally verified;
6. the machine policy is changed from `planned` to `active` only after that evidence exists.

Until activation, the verifier does not treat planned W3ID URLs as live resolution promises.

## UX rule

User-facing interfaces should display historical IRIs as identifiers and use separately labelled resolvable links for navigation.

Preferred pattern:

```text
Entity IRI
http://www.co-ode.org/ontologies/pizza/pizza.owl#Pizza

Preserved definition
<resolvable preservation/reference URL>
```

Do not wrap a known non-resolving historical IRI in an anchor merely because it has HTTP syntax.

The CI regression checks UX JavaScript/HTML for semantic IRI fields assigned to `href` and for direct anchors to the historical `co-ode.org` Pizza namespace. Current UX code passes with zero violations.

## Success condition

The preservation/reference layer succeeds when:

```text
historical Pizza identity remains unchanged
        +
current project-promised Web locations resolve
        +
reference URLs are governed independently
        +
users are not misled into treating semantic identity as a storage location
```

Issue #4 remains the separate decision point for any future successor ontology with new governed semantic identity.
