# `w3id.org/pizza-ontology` preservation/reference namespace

Maintainer: **Gerhard Balz** — GitHub [`@GerhardBalz`](https://github.com/GerhardBalz)

Canonical project: `https://github.com/GerhardBalz/pizza-ontology`

## Scope

This directory is the repository-owned source for the planned W3ID configuration at:

```text
https://w3id.org/pizza-ontology/
```

The namespace is a **preservation/reference namespace** for the `GerhardBalz/pizza-ontology` project.

It does not replace or claim authority over the historical Pizza Ontology 2.0 identifiers:

```text
http://www.co-ode.org/ontologies/pizza
http://www.co-ode.org/ontologies/pizza/2.0.0
http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

Those remain the preserved semantic identities.

## Route policy

- The namespace root and current documentation/reference routes may follow the current project because they are navigation resources.
- `preservation/2.0/*` routes point only to the governed immutable `preservation-v0.2.0` tag/release.
- No entity aliases are minted.
- No `owl:sameAs` or ontology-identity equivalence is asserted between W3ID routes and the historical Pizza namespace.

## Activation lifecycle

1. Review the route design and identity/location policy in `GerhardBalz/pizza-ontology`.
2. Verify all backend targets.
3. Copy this directory into `perma-id/w3id.org` as `pizza-ontology/` and submit the upstream PR.
4. Wait for upstream review and merge.
5. Externally verify the public W3ID routes.
6. Only then change the Pizza machine policy from `planned` to `active` and expose persistent-reference URLs as current publication/navigation promises.

Until step 5 succeeds, the W3ID namespace is planned rather than active.
