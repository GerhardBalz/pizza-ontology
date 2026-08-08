# Pizza Ontology Provenance

## Status

Draft provenance case study.

This document applies the concepts defined in `identity-publication-model.md` to the historical Pizza ontology and to this repository.

Its purpose is to establish provenance, authority, and lineage before deciding whether future work should preserve the historical Pizza 2.0 identity or establish a successor ontology with a new governed identifier space.

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

> **A preservation, migration, engineering, and learning environment based on the historical Pizza ontology.**

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
* and Executable Knowledge Architecture.

These uses do not change the provenance of the historical Pizza ontology.

## 8. Current Project Role

At this stage, `GerhardBalz/pizza-ontology` should not claim to be:

* the original Pizza ontology authority,
* the original source repository,
* the legal owner of Pizza,
* or an official continuation sanctioned by the historical contributors.

The project can currently be described as a:

> **Technical steward of a preservation and engineering repository derived from Pizza 2.0.**

This stewardship is distinct from semantic authority over the historical `co-ode.org` identifier space.

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
    future publication infrastructure
    future executable-knowledge demonstrations
```

Licensing of newly created repository infrastructure, examples, code, and documentation should be made deliberately rather than silently replacing the provenance or licensing of the upstream ontology.

## 10. Preservation vs Successor

The major architectural decision remains open.

### Preservation / Stewardship Path

```text
Pizza 2.0
   │
   └── preserved and republished
       with historical semantic IRIs
```

Under this path:

* historical ontology identity remains unchanged,
* historical entity IRIs remain unchanged,
* new engineering and publication infrastructure surrounds the existing ontology,
* provenance clearly identifies the project as a preservation and stewardship environment.

### Successor Ontology Path

```text
Pizza 2.0
   │
   │ prov:wasDerivedFrom
   ▼
Modernized Pizza Ontology
   │
   ├── new authority
   ├── new ontology identity
   ├── new governed identifier namespace
   └── explicit mappings to historical Pizza entities
```

Under this path, the project would establish a genuinely new ontology lineage rather than silently taking over the historical Pizza identifier space.

## 11. Open Questions

### Q1. Should this repository remain a preservation/stewardship project?

If yes, historical semantic identity should remain unchanged.

### Q2. Should a successor Pizza ontology be created?

If yes, its semantic authority and identifier namespace must be explicitly established.

### Q3. Who would be the authority for a successor ontology?

The answer must precede the choice of new IRIs.

### Q4. Should historical Pizza entity IRIs remain unchanged?

For preservation: yes.

For a successor: mappings between historical and successor entities should be explicit and evaluated individually.

### Q5. How should historical version 2.0 relate to future project releases?

A new engineering release of this repository should not pretend to be another official historical Pizza 2.0 release.

The model must distinguish:

```text
historical semantic version
```

from:

```text
new repository / preservation release
```

### Q6. How should ontology knowledge become executable?

Future work may explore semantic projections from the ontology into:

* query interfaces,
* APIs,
* schemas,
* knowledge graphs,
* validation,
* user experiences,
* rules and decisions,
* agents,
* and executable knowledge systems.

These derived artifacts should remain traceable to the underlying semantic model without assuming that all implementation knowledge belongs directly in OWL.

## 12. Current Conclusion

The current conservative interpretation is:

```text
Creator community:
    Manchester / Protégé OWL tutorial collaborators

Historical semantic artifact:
    Pizza ontology

Preservation baseline:
    Pizza 2.0

Current upstream host used by this project:
    Stanford Protégé

Current semantic authority over historical Pizza identifier space:
    Not established

Current legal rights holder:
    Not established from ontology metadata

Licence:
    CC BY 3.0

Current project role:
    Preservation / migration / engineering steward
```

The next architectural decision is therefore:

> **Does `pizza-ontology` remain a preservation and stewardship environment for Pizza 2.0, or does it eventually establish a new successor ontology?**

That decision should determine future ontology IRIs and entity identifier spaces—not the other way around.

## References

* Stanford Pizza ontology: https://protege.stanford.edu/ontologies/pizza/pizza.owl
* Protégé: https://protege.stanford.edu/
* Protégé GitHub organization: https://github.com/protegeproject
* OWLCS Pizza repository: https://github.com/owlcs/pizza-ontology
* Tawny Pizza: https://github.com/phillord/tawny-pizza
* Yasen/Xiaoqi Zhao Pizza project: https://github.com/yasenstar/protege_pizza
* Current preservation/engineering repository: https://github.com/GerhardBalz/pizza-ontology
