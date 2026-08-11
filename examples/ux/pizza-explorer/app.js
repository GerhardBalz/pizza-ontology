"use strict";

const PROJECTION_URL = "../../../projections/pizza-concepts/pizza-concepts.json";

const state = {
  projection: null,
  query: "",
  requiredTopping: "",
  showTraceability: false,
};

const elements = {
  search: document.querySelector("#search"),
  toppingFilter: document.querySelector("#topping-filter"),
  showTraceability: document.querySelector("#show-traceability"),
  resultStatus: document.querySelector("#result-status"),
  conceptGrid: document.querySelector("#concept-grid"),
  template: document.querySelector("#concept-template"),
  projectionId: document.querySelector("#projection-id"),
  ontologyIri: document.querySelector("#ontology-iri"),
  versionIri: document.querySelector("#version-iri"),
};

function humanizeIdentifier(identifier) {
  const localName = identifier.includes(":") ? identifier.split(":").at(-1) : identifier;
  return localName
    .replace(/Topping$/, " topping")
    .replace(/([a-z0-9])([A-Z])/g, "$1 $2")
    .replace(/\s+/g, " ")
    .trim();
}

function semanticReference(reference) {
  const item = document.createElement("li");
  const label = document.createElement("span");
  const id = document.createElement("code");

  label.className = "presentation-label";
  label.textContent = humanizeIdentifier(reference.id);
  label.title = "Presentation-only name derived from the CURIE local name";

  id.textContent = reference.id;
  id.title = reference.iri;

  item.append(label, id);
  return item;
}

function searchableText(concept) {
  return [
    concept.displayLabel,
    concept.id,
    concept.iri,
    ...concept.directSuperClasses.flatMap((item) => [item.id, item.iri]),
    ...concept.requiredToppings.flatMap((item) => [item.id, item.iri, humanizeIdentifier(item.id)]),
  ]
    .join(" ")
    .toLocaleLowerCase();
}

function visibleConcepts() {
  const concepts = state.projection?.concepts ?? [];
  const query = state.query.trim().toLocaleLowerCase();

  return concepts.filter((concept) => {
    const matchesQuery = !query || searchableText(concept).includes(query);
    const matchesTopping =
      !state.requiredTopping ||
      concept.requiredToppings.some((item) => item.id === state.requiredTopping);
    return matchesQuery && matchesTopping;
  });
}

function renderSourceFacts() {
  const { projection, sourceSemanticModel } = state.projection;
  elements.projectionId.textContent = projection.id;
  elements.ontologyIri.textContent = sourceSemanticModel.ontologyIri;
  elements.versionIri.textContent = sourceSemanticModel.versionIri;
}

function renderToppingFilter() {
  const toppings = new Map();
  for (const concept of state.projection.concepts) {
    for (const topping of concept.requiredToppings) {
      toppings.set(topping.id, topping);
    }
  }

  for (const topping of [...toppings.values()].sort((a, b) => a.id.localeCompare(b.id))) {
    const option = document.createElement("option");
    option.value = topping.id;
    option.textContent = `${humanizeIdentifier(topping.id)} · ${topping.id}`;
    elements.toppingFilter.append(option);
  }
}

function renderConcept(concept) {
  const fragment = elements.template.content.cloneNode(true);
  const card = fragment.querySelector(".concept-card");

  fragment.querySelector(".concept-label").textContent = concept.displayLabel;
  fragment.querySelector(".concept-id").textContent = concept.id;
  fragment.querySelector(".topping-count").textContent =
    `${concept.requiredToppings.length} required topping${concept.requiredToppings.length === 1 ? "" : "s"}`;

  const superclasses = fragment.querySelector(".superclasses");
  concept.directSuperClasses.forEach((item) => superclasses.append(semanticReference(item)));

  const toppings = fragment.querySelector(".toppings");
  concept.requiredToppings.forEach((item) => toppings.append(semanticReference(item)));

  fragment.querySelector(".entity-iri").textContent = concept.traceability.sourceEntityIri;
  fragment.querySelector(".superclass-semantics").textContent = concept.traceability.superclassSemantics;
  fragment.querySelector(".topping-semantics").textContent = concept.traceability.toppingSemantics;

  const traceability = fragment.querySelector(".traceability");
  traceability.open = state.showTraceability;

  card.dataset.conceptId = concept.id;
  return fragment;
}

function renderConcepts() {
  const concepts = visibleConcepts();
  elements.conceptGrid.replaceChildren(...concepts.map(renderConcept));
  elements.resultStatus.textContent =
    `${concepts.length} of ${state.projection.concepts.length} projected concept${state.projection.concepts.length === 1 ? "" : "s"} shown.`;
}

function bindControls() {
  elements.search.addEventListener("input", (event) => {
    state.query = event.target.value;
    renderConcepts();
  });

  elements.toppingFilter.addEventListener("change", (event) => {
    state.requiredTopping = event.target.value;
    renderConcepts();
  });

  elements.showTraceability.addEventListener("change", (event) => {
    state.showTraceability = event.target.checked;
    renderConcepts();
  });
}

async function loadProjection() {
  const response = await fetch(PROJECTION_URL, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`Projection request failed with HTTP ${response.status}`);
  }

  const projection = await response.json();
  if (!Array.isArray(projection.concepts) || !projection.projection || !projection.sourceSemanticModel) {
    throw new Error("Projection does not satisfy the UI's minimal consumer contract");
  }

  state.projection = projection;
  renderSourceFacts();
  renderToppingFilter();
  renderConcepts();
}

bindControls();
loadProjection().catch((error) => {
  console.error(error);
  elements.resultStatus.textContent = `Unable to load the semantic projection: ${error.message}`;
  elements.resultStatus.classList.add("error");
});
