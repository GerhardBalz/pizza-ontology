# Pizza OWL Modeling Patterns and Teaching Cases

## Status

Adopted modeling reference for the preserved Pizza Ontology 2.0 baseline.

This document explains representative OWL patterns in `src/ontology/pizza-edit.owl` in modeling terms that are visible in Protégé. It documents the historical ontology; it does **not** modernize, repair, or redefine Pizza Ontology 2.0.

The preserved semantic identity remains:

```text
Ontology IRI   http://www.co-ode.org/ontologies/pizza
Version IRI    http://www.co-ode.org/ontologies/pizza/2.0.0
Version info   2.0
Entity space   http://www.co-ode.org/ontologies/pizza/pizza.owl#
```

## 1. Reading the ontology in Protégé

The Functional Syntax source and common Protégé views correspond roughly as follows:

| OWL / Functional Syntax | Protégé-oriented reading |
| --- | --- |
| `SubClassOf(A B)` | class `A` has `B` under **SubClass Of** |
| `EquivalentClasses(A X)` | class `A` has `X` under **Equivalent To** |
| `DisjointClasses(...)` | participating classes are mutually disjoint |
| `ObjectSomeValuesFrom(p C)` | **p some C** existential restriction |
| `ObjectAllValuesFrom(p C)` | **p only C** universal restriction |
| `ObjectHasValue(p i)` | **p value i** restriction |
| object-property domain/range | **Domain** / **Range** of the property |
| functional / inverse-functional / transitive | property characteristics |
| `ClassAssertion(C i)` | individual `i` is an instance of `C` |

A crucial distinction throughout the ontology is between **asserted structure** and **defined classes**. Reasoners use both, but they play different modeling roles.

## 2. Asserted class: `pizza:AmericanHot`

`AmericanHot` is a named menu pizza described primarily with necessary conditions.

The preserved source asserts that it is a subclass of `NamedPizza` and requires several topping types, including jalapeño, mozzarella, tomato, pepperoni sausage, and hot green pepper.

Representative pattern:

```text
AmericanHot
  SubClassOf NamedPizza
  SubClassOf hasTopping some JalapenoPepperTopping
  SubClassOf hasTopping some MozzarellaTopping
  ...
```

These are **necessary conditions**. From an assertion `x rdf:type AmericanHot`, a reasoner may conclude that `x` satisfies those restrictions. The restrictions do not by themselves define every pizza satisfying the same conditions as `AmericanHot`.

### Existential and closure restrictions together

Named pizzas such as `AmericanHot` combine two different patterns:

```text
hasTopping some JalapenoPepperTopping
hasTopping some MozzarellaTopping
...
```

with a universal restriction equivalent to:

```text
hasTopping only
  (HotGreenPepperTopping
   or JalapenoPepperTopping
   or MozzarellaTopping
   or PeperoniSausageTopping
   or TomatoTopping)
```

The existential restrictions say that toppings of the listed types **must exist**. The universal restriction closes the topping *types* for that class: any topping an `AmericanHot` has must belong to the stated union.

This distinction matters because `only` does not assert existence. Conversely, a set of `some` restrictions does not prevent additional topping types under OWL's open-world semantics.

## 3. Defined class: `pizza:SpicyPizza`

`SpicyPizza` illustrates a defined class. Its preserved source gives an equivalence:

```text
SpicyPizza ≡ Pizza and (hasTopping some SpicyTopping)
```

This is both necessary and sufficient. A reasoner can therefore classify any individual or class satisfying the right-hand expression as a `SpicyPizza`, even when `SpicyPizza` was not asserted directly.

This is the essential difference from the `AmericanHot` pattern:

```text
AmericanHot
  asserted necessary conditions

SpicyPizza
  necessary + sufficient definition
```

The repository's reasoning example uses this distinction to demonstrate inferred classification rather than merely reading asserted superclass links.

## 4. Class hierarchy and disjointness

The ontology uses explicit taxonomies for pizzas, toppings, bases, and other domain concepts. For example:

```text
AmericanHot → NamedPizza → Pizza
MozzarellaTopping → CheeseTopping → PizzaTopping
TomatoTopping → VegetableTopping → PizzaTopping
```

Disjointness adds negative semantic commitments. The ontology declares the major topping categories mutually disjoint, including:

```text
CheeseTopping
FishTopping
FruitTopping
HerbSpiceTopping
MeatTopping
NutTopping
SauceTopping
VegetableTopping
```

Disjointness is stronger than a visual taxonomy split. It states that one individual cannot consistently be an instance of two disjoint classes.

The named pizza classes are also declared mutually disjoint in the historical tutorial model. This is a deliberate modeling choice of the example ontology, not a universal prescription for product modeling.

## 5. Object-property modeling

`hasTopping` demonstrates several OWL object-property mechanisms at once:

```text
hasTopping SubPropertyOf hasIngredient
hasTopping inverseOf isToppingOf
Domain(hasTopping) Pizza
Range(hasTopping) PizzaTopping
hasTopping is inverse-functional
```

The broader `hasIngredient` property is transitive and has `Food` as both domain and range.

### Domain and range are inference rules, not form validation

A particularly important teaching point is that an OWL domain does not mean:

> reject any triple whose subject has not already been declared a Pizza.

Instead, using `hasTopping` allows a reasoner to infer that the subject is a `Pizza`, because `Pizza` is the property's domain. Likewise, the object is inferred to be a `PizzaTopping` from the range.

This is one reason OWL domain/range semantics must not be confused with SHACL-style validation constraints.

## 6. Restrictions: `some`, `only`, and `value`

Pizza provides all three common object-property restriction styles.

### `some` — existential

```text
hasTopping some MozzarellaTopping
```

means at least one `hasTopping` value exists that is a `MozzarellaTopping`.

### `only` — universal

```text
hasTopping only (MozzarellaTopping or TomatoTopping)
```

means every `hasTopping` value, if any, belongs to the stated class expression. It does not itself assert that a topping exists.

### `value` — specific individual

Some named pizzas use country individuals through `hasCountryOfOrigin value ...`. For example, `American` and `AmericanHot` use the individual `pizza:America`.

The restriction points to an **individual**, not to the class `Country`.

## 7. Value partition: `pizza:Spiciness`

The historical ontology explicitly documents `Spiciness` as a value-partition example.

Its core pattern is:

```text
Spiciness ≡ Hot or Medium or Mild
Spiciness SubClassOf ValuePartition
Hot, Medium, Mild are pairwise disjoint
```

`hasSpiciness` has range `Spiciness` and is functional.

Together these axioms demonstrate a controlled semantic value space. A value reached through `hasSpiciness` must be in the `Spiciness` partition, and the partition is covered by the three disjoint subclasses. Functionality means one subject cannot have two distinct `hasSpiciness` values through that property.

This is a historical OWL modeling pattern. A future system might choose a different representation depending on the use case, but this preservation line documents rather than rewrites it.

## 8. Individuals: country values

Pizza 2.0 includes named individuals:

```text
pizza:America
pizza:England
pizza:France
pizza:Germany
pizza:Italy
```

Each is asserted as a `Country`, and the ontology declares the five individuals different from one another.

This supports class restrictions such as:

```text
hasCountryOfOrigin value pizza:America
```

and demonstrates the distinction between a class such as `Country` and particular members of that class.

## 9. Open-world reasoning: `pizza:UnclosedPizza`

`UnclosedPizza` is an explicit open-world teaching case.

It is asserted to be a `Pizza` and to have **some** mozzarella topping, but it has no universal topping closure restriction.

The ontology's own comment explains the consequence: a reasoner cannot classify it as either `VegetarianPizza` or `NonVegetarianPizza`, because additional, currently unknown toppings may exist.

```text
Known:
  hasTopping some MozzarellaTopping

Not known:
  that mozzarella is the only topping type
```

Under the open-world assumption, missing knowledge is not automatically false. The absence of a meat topping assertion therefore does not prove that no meat topping exists.

This is exactly why the first JSON semantic projection and UX example call their flattened relationships `requiredToppings` rather than presenting them as a complete recipe.

## 10. Intentional unsatisfiable class: `pizza:CheeseyVegetableTopping`

`CheeseyVegetableTopping` is deliberately modeled beneath two disjoint parents:

```text
CheeseyVegetableTopping SubClassOf CheeseTopping
CheeseyVegetableTopping SubClassOf VegetableTopping
```

while `CheeseTopping` and `VegetableTopping` occur in the same disjointness axiom.

Therefore no individual can consistently instantiate `CheeseyVegetableTopping`. A reasoner classifies the class as unsatisfiable (equivalent to `owl:Nothing`).

This is preserved as a teaching probe, not repaired as an ontology defect.

## 11. Intentional unsatisfiable class: `pizza:IceCream`

`IceCream` demonstrates a different modeling mistake:

```text
IceCream SubClassOf Food
IceCream SubClassOf hasTopping some FruitTopping
```

The property `hasTopping` has domain `Pizza`. Consequently, any `IceCream` instance satisfying that existential restriction is inferred to be a `Pizza`.

But `IceCream` and `Pizza` are declared disjoint. The class is therefore unsatisfiable.

This example is especially useful because it shows why domain axioms are inferential semantics rather than validation declarations.

### Unsatisfiable class versus inconsistent ontology

An unsatisfiable class cannot have an instance in any model of the ontology. Its presence does not by itself require the entire ontology to be inconsistent; inconsistency would arise if the axioms forced an actual individual into the contradiction.

The repository therefore describes Pizza 2.0 as intentionally containing two unsatisfiable teaching classes and regression-tests that historical behavior.

## 12. Asserted versus inferred knowledge

A useful way to read Pizza is to keep three layers separate:

```text
Asserted axioms
    what the ontology explicitly says

OWL semantics
    what those axioms mean under OWL

Reasoner inferences
    additional classifications entailed by those meanings
```

Protégé can display both asserted and inferred hierarchies when a reasoner is active. Those views should not be confused: an inferred superclass may disappear if supporting axioms change even though no explicit `SubClassOf` statement was edited.

The repository keeps canonical reasoning checks separate from the preserved source so that this distinction remains executable as well as documented.

## 13. Historical model versus successor modernization

These patterns belong to the **historical Pizza Ontology 2.0** preservation line.

They should not be silently rewritten because a modern ontology engineer might choose different patterns today. In particular:

- unusual property characteristics remain historical semantics;
- value-partition modeling remains historical semantics;
- the two unsatisfiable teaching classes remain historical behavior;
- historical IRIs remain unchanged;
- tutorial-oriented disjointness remains part of the preserved model.

If future work requires substantive semantic modernization, it belongs in the separately governed successor-ontology decision, with a new authority model and explicit mappings to the preserved lineage.

## 14. Traceability contract

The examples above are not free-floating tutorial prose. `docs/verify_modeling_reference.py` checks the preserved source for the representative axioms on which this document relies, including:

- ontology and version identity;
- asserted `AmericanHot` restrictions;
- defined `SpicyPizza` equivalence;
- `hasTopping` property semantics;
- `Spiciness` value-partition axioms;
- country individuals;
- `UnclosedPizza` open-world teaching structure;
- both intentional unsatisfiable-class mechanisms.

The contract deliberately verifies representative source axioms rather than trying to reimplement an OWL reasoner in documentation tooling.

## Architectural boundary

```text
Pizza Ontology 2.0
    owns historical OWL semantics
        ↓
this modeling guide
    explains selected patterns
        ↓
reasoning / projections / UX
    consume selected semantics through their own explicit contracts
```

Documentation explains the model; it does not become another semantic source of truth.
