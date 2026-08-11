#!/usr/bin/env python3
"""Verify that the Pizza OWL modeling guide remains anchored to the preserved source."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "src" / "ontology" / "pizza-edit.owl"
GUIDE = ROOT / "docs" / "pizza-owl-modeling-patterns.md"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    guide = GUIDE.read_text(encoding="utf-8")

    source_anchors = {
        "ontology IRI": "Ontology(<http://www.co-ode.org/ontologies/pizza>",
        "version IRI": "<http://www.co-ode.org/ontologies/pizza/2.0.0>",
        "version info": 'Annotation(owl:versionInfo "2.0")',
        "AmericanHot named-pizza assertion": "SubClassOf(pizza:AmericanHot pizza:NamedPizza)",
        "AmericanHot jalapeno existential": "SubClassOf(pizza:AmericanHot ObjectSomeValuesFrom(pizza:hasTopping pizza:JalapenoPepperTopping))",
        "AmericanHot topping closure": "SubClassOf(pizza:AmericanHot ObjectAllValuesFrom(pizza:hasTopping ObjectUnionOf(pizza:HotGreenPepperTopping pizza:JalapenoPepperTopping pizza:MozzarellaTopping pizza:PeperoniSausageTopping pizza:TomatoTopping)))",
        "SpicyPizza definition": "EquivalentClasses(pizza:SpicyPizza ObjectIntersectionOf(pizza:Pizza ObjectSomeValuesFrom(pizza:hasTopping pizza:SpicyTopping)))",
        "hasTopping subproperty": "SubObjectPropertyOf(pizza:hasTopping pizza:hasIngredient)",
        "hasTopping inverse": "InverseObjectProperties(pizza:hasTopping pizza:isToppingOf)",
        "hasTopping inverse-functional": "InverseFunctionalObjectProperty(pizza:hasTopping)",
        "hasTopping domain": "ObjectPropertyDomain(pizza:hasTopping pizza:Pizza)",
        "hasTopping range": "ObjectPropertyRange(pizza:hasTopping pizza:PizzaTopping)",
        "hasIngredient transitive": "TransitiveObjectProperty(pizza:hasIngredient)",
        "Spiciness covering axiom": "EquivalentClasses(pizza:Spiciness ObjectUnionOf(pizza:Hot pizza:Medium pizza:Mild))",
        "Spiciness partition parent": "SubClassOf(pizza:Spiciness pizza:ValuePartition)",
        "Spiciness values disjoint": "DisjointClasses(pizza:Hot pizza:Medium pizza:Mild)",
        "hasSpiciness functional": "FunctionalObjectProperty(pizza:hasSpiciness)",
        "hasSpiciness range": "ObjectPropertyRange(pizza:hasSpiciness pizza:Spiciness)",
        "Italy is a Country": "ClassAssertion(pizza:Country pizza:Italy)",
        "country individuals distinct": "DifferentIndividuals(pizza:America pizza:England pizza:France pizza:Germany pizza:Italy)",
        "UnclosedPizza is Pizza": "SubClassOf(pizza:UnclosedPizza pizza:Pizza)",
        "UnclosedPizza mozzarella existential": "SubClassOf(pizza:UnclosedPizza ObjectSomeValuesFrom(pizza:hasTopping pizza:MozzarellaTopping))",
        "CheeseyVegetable cheese parent": "SubClassOf(pizza:CheeseyVegetableTopping pizza:CheeseTopping)",
        "CheeseyVegetable vegetable parent": "SubClassOf(pizza:CheeseyVegetableTopping pizza:VegetableTopping)",
        "major topping categories disjoint": "DisjointClasses(pizza:CheeseTopping pizza:FishTopping pizza:FruitTopping pizza:HerbSpiceTopping pizza:MeatTopping pizza:NutTopping pizza:SauceTopping pizza:VegetableTopping)",
        "IceCream food parent": "SubClassOf(pizza:IceCream pizza:Food)",
        "IceCream topping existential": "SubClassOf(pizza:IceCream ObjectSomeValuesFrom(pizza:hasTopping pizza:FruitTopping))",
        "IceCream disjoint from Pizza": "DisjointClasses(pizza:IceCream pizza:Pizza pizza:PizzaBase pizza:PizzaTopping)",
    }

    missing = [label for label, anchor in source_anchors.items() if anchor not in source]
    require(not missing, "modeling guide source anchors missing: " + ", ".join(missing))

    guide_anchors = [
        "src/ontology/pizza-edit.owl",
        "Asserted class: `pizza:AmericanHot`",
        "Defined class: `pizza:SpicyPizza`",
        "Value partition: `pizza:Spiciness`",
        "Open-world reasoning: `pizza:UnclosedPizza`",
        "Intentional unsatisfiable class: `pizza:CheeseyVegetableTopping`",
        "Intentional unsatisfiable class: `pizza:IceCream`",
        "Unsatisfiable class versus inconsistent ontology",
        "Historical model versus successor modernization",
    ]
    missing_guide = [anchor for anchor in guide_anchors if anchor not in guide]
    require(not missing_guide, "modeling guide sections missing: " + ", ".join(missing_guide))

    require(
        "domain does not mean" in guide,
        "guide must preserve the OWL-domain-as-inference teaching point",
    )
    require(
        "missing knowledge is not automatically false" in guide,
        "guide must explain the open-world assumption explicitly",
    )

    print(
        "SUCCESS: Pizza OWL modeling guide remains traceable to representative "
        "axioms in the preserved Pizza Ontology 2.0 source."
    )


if __name__ == "__main__":
    main()
