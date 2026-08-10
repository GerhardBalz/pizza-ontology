# Pizza Ontology Provenance

## Status

Provenance case study with an adopted preservation-line decision.

This document applies the concepts defined in `identity-publication-model.md` to the historical Pizza ontology and to this repository.

Its purpose is to establish provenance, authority, and lineage and to document the current architectural decision:

> **`GerhardBalz/pizza-ontology` is the preservation, stewardship, engineering, and learning line for the historical Pizza Ontology 2.0 baseline.**

A future successor ontology remains possible, but if created it should be a separate ontology lineage with its own authority, identity, governed namespace, repository, and version series.

The corresponding repository release model is documented in [`versioning-release-model.md`](versioning-release-model.md).

## 1. Preservation Baseline

The preservation baseline used by this project is the Pizza ontology distributed by the Stanford Protégé site:

https://protege.stanford.edu/ontologies/pizza/pizza.owl

The artifact declares:

```text
Ontology IRI
http://www.co-ode.org/ontologies/pizza

Version IRI
http://www.co-ode.org/ontologies/pizza/2.0.0

Version Info
2.0

Entity Namespace
http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

The ontology describes itself as an ontology about pizzas and their toppings and as an example ontology containing the constructs required for the Pizza Tutorial run by Manchester University.

It explicitly names the following contributors:

* Alan Rector
* Chris Wroe
* Matthew Horridge
* Nick Drummond
* Robert Stevens

The ontology declares:

```text
Creative Commons Attribution 3.0 (CC BY 3.0)
```

as its licence.

This artifact is therefore treated as the **upstream preservation source for this project**.

That does not imply that Stanford is established as the sole creator, semantic authority, steward, or legal rights holder of the Pizza ontology.

## 2. Historical Context

The Pizza ontology belongs to the wider Manchester OWL tutorial and Protégé collaboration.

Protégé originated at Stanford University.

The development of OWL support and teaching material involved collaboration between the Stanford Protégé project and Alan Rector's group at the University of Manchester.

The historical Pizza teaching publication *OWL Pizzas: Common errors & common patterns from practical experience of teaching OWL-DL* includes contributors from this wider collaboration.

The available evidence therefore supports describing Pizza as a product of the:

> **Manchester OWL tutorial / Protégé collaboration**

rather than assigning sole authorship or authority to the current Stanford host or to any particular GitHub organization.

## 3. Provenance Roles

The following roles are deliberately kept separate.

### Creators and Historical Contributors

Known historical contributors include the individuals explicitly named in the Pizza 2.0 ontology and the wider group associated with the historical Pizza tutorial and teaching publications.

The Pizza 2.0 artifact explicitly identifies:

* Alan Rector
* Chris Wroe
* Matthew Horridge
* Nick Drummond
* Robert Stevens

### Historical Institutional Context

The broad institutional lineage can be represented as:

```text
University of Manchester OWL group
            │
            │ collaboration
            ▼
Stanford Protégé project
            │
            ▼
Pizza OWL tutorial tradition
```

This expresses historical collaboration and provenance.

It is not a statement of legal ownership.

### Current Host of the Pizza 2.0 Distribution

The upstream Pizza 2.0 file used by this project is currently hosted by the Stanford Protégé site.

```text
Host:
Stanford Protégé
```

Hosting alone does not establish:

```text
Creator
Authority
Steward
Rights Holder
```

### Current Authority

**Not established from the available evidence.**

The Pizza 2.0 ontology does not identify an explicit present-day locus of authority responsible for governing the historical Pizza identifier space.

No evidence currently establishes Stanford, Manchester, `protegeproject`, `owlcs`, or another current organization as the sole authority entitled to evolve:

```text
http://www.co-ode.org/ontologies/pizza
```

This uncertainty should be represented explicitly rather than resolved by inference.

### Current Steward

**No single steward of the historical Pizza 2.0 lineage has been established.**

Several projects maintain copies, tutorials, test fixtures, implementations, or derivatives.

Repository activity alone does not establish stewardship of the historical ontology identity.

This repository therefore uses the more limited role **technical steward of its own preservation and engineering environment** rather than claiming stewardship authority over the historical identifier space itself.

### Rights Holder

**Not established from the ontology metadata.**

The Pizza 2.0 artifact provides a licence but does not explicitly identify a rights holder.

Licence and rights-holder identity are different concepts.

## 4. Known Pizza Repositories and Lineages

The Pizza ontology has become a widely reused educational artifact.

The existence or popularity of a GitHub repository does not establish semantic authority over the historical Pizza ontology.

### Stanford Pizza 2.0

```text
Role:
Upstream preservation source

Version:
2.0

Status:
Historical distribution

Host:
Stanford Protégé
```

This is the source used for the current ODK migration.

### `protegeproject/protege`

The official Protégé Desktop repository contains Pizza ontology files as software test resources.

```text
Role:
Software test fixture

Authority over Protégé software:
Protégé project

Authority over historical Pizza 2.0 ontology:
Not established
```

The presence of `pizza.owl` in the Protégé codebase does not make that repository the canonical source repository for Pizza 2.0.

### `owlcs/pizza-ontology`

A dedicated Pizza repository exists under the OWLCS GitHub organization.

It represents an older Pizza lineage rather than the Pizza 2.0 artifact used by this project.

```text
Role:
Historical / technical Pizza repository

Lineage:
Older than Pizza 2.0

Authority over Pizza 2.0:
Not established
```

### `phillord/tawny-pizza`

This project implements a version of the Pizza ontology as a demonstration of Tawny-OWL.

```text
Role:
Derivative implementation / demonstrator

Authority over historical Pizza identity:
Not established
```

### `yasenstar/protege_pizza`

This is an active educational and ontology-engineering project based on the Pizza tutorial tradition.

It extends the tutorial toward additional ontology-engineering, knowledge-graph, governance, and executable-knowledge practices.

```text
Role:
Modern educational derivative / successor tutorial project

Authority over historical Pizza identity:
Not established
```

It is useful as evidence of the continued evolution of the Pizza tradition, but it is not used as the upstream source of Pizza 2.0 in this repository.

## 5. Provenance Graph

The current provenance model can be represented as:

```text
Manchester / Protégé OWL tutorial collaboration
                     │
                     │ created and evolved
                     ▼
             Pizza ontology tradition
                     │
                     ▼
                 Pizza 2.0
                     │
       Ontology IRI:
       http://www.co-ode.org/ontologies/pizza
                     │
       Version IRI:
       http://www.co-ode.org/ontologies/pizza/2.0.0
                     │
                     │ distributed by
                     ▼
              Stanford Protégé
                     │
                     │ upstream source for
                     ▼
             ODK migration
                     │
                     ▼
      GerhardBalz/pizza-ontology
                     │
                     │ preservation / engineering releases
                     ▼
          preservation-v0.x.y
```

The current repository is therefore derived from the upstream Pizza 2.0 artifact.

Candidate semantic relationships include:

```text
dcterms:source
prov:wasDerivedFrom
```

depending on whether a lightweight metadata relationship or a more explicit provenance model is required.

## 6. ODK Migration Baseline

The Stanford Pizza 2.0 source was converted to OWL Functional Syntax using ROBOT.

The resulting ontology was copied unchanged into the ODK editor ontology.

The migration verified that the ODK editor source was byte-for-byte identical to the converted upstream ontology.

The migration baseline is represented by Git commit:

```text
2344eab Migrate Pizza 2.0 ontology to ODK
```

At that checkpoint:

* the historical ontology IRI is preserved,
* the historical version IRI is preserved,
* the historical entity IRIs are preserved,
* the ontology semantics are preserved,
* the two intentionally unsatisfiable tutorial classes are explicitly regression-tested,
* the configured ODK tests pass,
* the ontology validates against the OWL 2 DL profile.

The two intentionally unsatisfiable classes are:

```text
CheeseyVegetableTopping
IceCream
```

They are treated as expected semantic characteristics of the historical teaching ontology rather than migration defects.

## 7. Current Repository

Source repository:

```text
https://github.com/GerhardBalz/pizza-ontology
```

Current role:

> **A preservation, stewardship, migration, engineering, and learning environment based on the historical Pizza ontology.**

The repository is intended to support multiple uses of the same semantic artifact, including examples for:

* Protégé ontology authoring and reasoning,
* Ontology Development Kit (ODK) migration and lifecycle management,
* Ontology Access Kit (OAK) access and querying,
* ROBOT transformations and validation,
* ontology publication and governance,
* semantic modeling,
* API and schema derivation,
* ontology-informed user experiences,
* knowledge graphs,
* executable knowledge,
* and Executable Semantic Knowledge Architecture.

These uses do not change the provenance or semantic version of the historical Pizza ontology.

## 8. Current Project Role

`GerhardBalz/pizza-ontology` should not claim to be:

* the original Pizza ontology authority,
* the original source repository,
* the legal owner of Pizza,
* or an official continuation sanctioned by the historical contributors.

The project is described as a:

> **Technical steward of a preservation and engineering repository derived from Pizza 2.0.**

This stewardship is distinct from semantic authority over the historical `co-ode.org` identifier space.

The repository may create versioned preservation and engineering releases without claiming that those releases are new semantic versions of the historical Pizza ontology.

## 9. Licence and Attribution

The Pizza 2.0 ontology declares CC BY 3.0.

The repository should therefore preserve clear attribution to the historical source and contributors.

The project should distinguish:

```text
Original semantic work
    Pizza ontology / Pizza tutorial tradition

Derived engineering work
    ODK migration
    build configuration
    semantic regression tests
    documentation
    examples
    publication infrastructure
    executable-knowledge integrations
```

Licensing of newly created repository infrastructure, examples, code, and documentation should be made deliberately rather than silently replacing the provenance or licensing of the upstream ontology.

## 10. Preservation Line and Possible Successor

The current repository role is now resolved:

### Adopted Preservation / Stewardship Line

```text
Pizza Ontology 2.0
   │
   └── preserved and engineered in
       GerhardBalz/pizza-ontology
             │
             └── repository releases
                 preservation-v0.x.y
```

Under this line:

* historical ontology identity remains unchanged,
* historical entity IRIs remain unchanged,
* Pizza Ontology 2.0 remains the semantic baseline,
* new engineering and publication infrastructure surrounds the existing ontology,
* repository releases are versioned independently from the ontology,
* provenance clearly identifies the project as a preservation and stewardship environment.

The detailed release model is defined in [`versioning-release-model.md`](versioning-release-model.md).

### Possible Successor Ontology Lineage

Semantic modernization remains possible as a separate lineage:

```text
Pizza Ontology 2.0
   │
   │ prov:wasDerivedFrom / explicit mappings
   ▼
Successor Pizza Ontology
   │
   ├── separate repository
   ├── explicit authority / stewardship
   ├── new ontology identity
   ├── new governed identifier namespace
   └── independent version series
```

A successor would not replace the preservation line. Both may coexist.

Unless authority over the historical Pizza identifier space is established, a successor should not silently adopt new version IRIs beneath:

```text
http://www.co-ode.org/ontologies/pizza
```

or assume the names `Pizza 2.1` or `Pizza 3.0` imply official continuity.

## 11. Open Questions and Decisions

### Q1. Should this repository remain a preservation/stewardship project?

**Decided: yes.**

Historical semantic identity remains unchanged. Repository engineering evolves through a separate `preservation-v0.x.y` release line.

### Q2. Should a successor Pizza ontology be created?

**Open.**

A successor should be created only when there is a concrete need for semantic modernization that should not be represented as part of the immutable Pizza 2.0 preservation baseline.

### Q3. Who would be the authority for a successor ontology?

**Open.**

The answer must precede the choice of successor ontology and entity IRIs.

### Q4. Should historical Pizza entity IRIs remain unchanged?

For the preservation repository: **yes**.

For a successor: mappings between historical and successor entities should be explicit and evaluated individually.

### Q5. How should historical version 2.0 relate to future project releases?

**Decided.**

The repository uses an independent preservation release series:

```text
Historical semantic version
    Pizza Ontology 2.0

Repository release
    preservation-v0.x.y
```

A repository release must not pretend to be a new official semantic release of historical Pizza 2.0.

### Q6. How should ontology knowledge become executable?

This remains an incremental engineering question.

The repository can provide stable semantic artifacts and projections for:

* query interfaces,
* APIs,
* schemas,
* knowledge graphs,
* validation,
* user experiences,
* rules and decisions,
* agents,
* and executable knowledge systems.

The companion ESKA project can operationalize those artifacts as semantic capabilities, services, agents, verification, and provenance.

Derived artifacts should remain traceable to the underlying semantic model without assuming that all implementation knowledge belongs directly in OWL.

## 12. Current Conclusion

The current interpretation is:

```text
Creator community:
    Manchester / Protégé OWL tutorial collaborators

Historical semantic artifact:
    Pizza ontology

Preservation baseline:
    Pizza Ontology 2.0

Current upstream host used by this project:
    Stanford Protégé

Current semantic authority over historical Pizza identifier space:
    Not established

Current legal rights holder:
    Not established from ontology metadata

Licence:
    CC BY 3.0

Current project role:
    Preservation / stewardship / migration / engineering line

Repository release series:
    preservation-v0.x.y
```

The preservation-versus-successor question is therefore no longer a binary decision for this repository:

> **`pizza-ontology` preserves Pizza Ontology 2.0. A separate successor ontology may be created later if semantic modernization requires a new lineage.**

The remaining architectural decision is whether and when such a successor should be created. That future decision should determine its authority, ontology IRI, entity namespace, mappings, and version series—not the other way around.

## References

* Stanford Pizza ontology: https://protege.stanford.edu/ontologies/pizza/pizza.owl
* Protégé: https://protege.stanford.edu/
* Protégé GitHub organization: https://github.com/protegeproject
* OWLCS Pizza repository: https://github.com/owlcs/pizza-ontology
* Tawny Pizza: https://github.com/phillord/tawny-pizza
* Yasen/Xiaoqi Zhao Pizza project: https://github.com/yasenstar/protege_pizza
* Current preservation/engineering repository: https://github.com/GerhardBalz/pizza-ontology
* Versioning and Release Model: `docs/versioning-release-model.md`
