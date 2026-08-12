# Pizza concept projection/preservation profile

## Purpose

This profile is an executable proving ground for Pizza issue #70 and the SKE conformance-boundary decision in `GerhardBalz/semantic-knowledge-engineering#13`.

It does **not** introduce a generic conformance ontology. Instead, it gives the existing non-authoritative `pizza-concepts.json` projection an explicit target contract and keeps four concerns separate:

```text
Pizza OWL semantics
    ↓ selected preservation through OAK
Pizza concept JSON projection
    ↓ JSON Schema
implementation representation validity

projection + profile + provenance
    ↓ SHACL
profile-evidence graph validity

all executable checks
    ↓ ESKA Verification + PROV-O
verification evidence and lineage
```

## Standards status

This example deliberately distinguishes standards status:

- SHACL 2017 is the stable W3C Recommendation used for RDF validation here.
- PROF is used as the W3C Profiles Vocabulary, published as a **W3C Working Group Note** on 18 December 2019. It is useful for machine-readable profile/resource descriptions but is not presented as a W3C Recommendation.
- `dcterms:conformsTo` expresses the projection's explicit claim to this profile. It does not by itself prove the claim.
- PROV-O records lineage/evidence relationships.
- ESKA provides the existing architectural `Execution`, `Result`, and `Verification` roles without adding Pizza- or PROF-specific ESKA vocabulary.

## Why this is a root PROF profile

`prof:isProfileOf` targets `dcterms:Standard`. The preserved Pizza Ontology 2.0 semantic source is not reclassified as a standard merely to create a PROF hierarchy.

Therefore:

```text
urn:pizza-ontology:profile:pizza-concepts-preservation:v1
    a prof:Profile
```

is intentionally a root profile with no `prof:isProfileOf` relation.

## Profile resources

`profile.ttl` describes four resources:

1. this human-readable specification (`role:specification`);
2. `preservation-contract.json` (`role:constraints`);
3. the existing `projection.schema.json` (`role:schema` + `role:constraints`);
4. `shapes.ttl` (`role:validation` + `role:constraints`, conforming to SHACL).

## Preservation contract

`preservation-contract.json` makes the existing projection policy machine-readable.

### Must preserve

For the selected `pizza:AmericanHot` and `pizza:Margherita` classes:

- historical Pizza entity identity through `id` and `iri`;
- selected asserted named superclasses through `directSuperClasses`;
- selected `hasTopping some ...` targets through `requiredToppings` after the documented flattening transformation.

### May transform

- OWL identifiers may be exposed as CURIE plus full IRI;
- existential topping restrictions may be flattened to application references.

### May omit

- universal topping closure;
- country-of-origin restrictions;
- inferred classifications;
- disjointness;
- property characteristics and broader OWL axioms;
- unrelated ontology annotations.

### May introduce

- projection-owned `displayLabel` text;
- JSON object/array representation structure.

Nothing outside this scope is claimed to be preserved.

## Evidence graph

`evidence.ttl` is a checked-in candidate conformance/evidence sidecar. It identifies:

- Pizza Ontology 2.0 as the authoritative semantic source;
- the JSON projection as an ESKA `Result` and PROV `Entity`;
- its `dcterms:conformsTo` claim to this explicit profile;
- source/result provenance;
- the OAK-backed projection execution;
- the profile verification using existing ESKA and PROV-O terms.

The claim is guarded by executable CI. A failing preservation, representation, or SHACL check rejects the repository change that carries the claim.

## Executable verification

Run from the repository root:

```bash
python -m pip install -r projections/pizza-concepts/requirements.txt
python -m pip install -r projections/pizza-concepts/profile/requirements.txt
python projections/pizza-concepts/profile/verify_profile.py
```

The verifier performs distinct checks:

1. regenerates the projection from the authoritative OWL source through the existing OAK boundary;
2. validates the generated representation with the existing JSON Schema;
3. checks the checked-in projection for semantic drift;
4. verifies that the machine-readable preservation contract exactly covers the existing preserved/transformed/introduced/omitted policy;
5. SHACL-validates the combined profile/evidence RDF graph;
6. writes the positive `sh:ValidationReport` to `profile/build/shacl-report.ttl` and annotates it as ESKA/PROV verification evidence;
7. removes the `dcterms:conformsTo` claim in an in-memory negative control and requires SHACL to report non-conformance.

The final runtime summary is written to `profile/build/evidence.json`.

## What SHACL does not prove

A SHACL `sh:conforms true` result here means that the **RDF evidence graph satisfies the profile-specific evidence constraints**.

It does not mean:

- the JSON projection is semantically equivalent to the Pizza ontology;
- every OWL axiom has been preserved;
- every possible implementation satisfies this profile;
- SHACL replaced OWL reasoning.

The selected OWL-semantic preservation is established separately by regenerating and comparing the OAK-backed projection against the authoritative source.

## Architectural conclusion under test

If CI passes, the concrete claim is intentionally narrow:

```text
explicit profile/contract
        +
selected source-semantic preservation checks
        +
JSON representation validation
        +
SHACL evidence-graph validation
        +
ESKA/PROV verification evidence
        ↓
reviewable dcterms:conformsTo claim
```

If this remains sufficient in further projections, no new generic SMO/ESKA conformance vocabulary is justified.
