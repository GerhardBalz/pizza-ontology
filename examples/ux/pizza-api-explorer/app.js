"use strict";

const COLLECTION_URL = "/concepts";
const CONTRACT_URL = "/openapi.json";

const state = {
  query: "",
  requiredTopping: "",
  initialConcepts: [],
};

const elements = {
  search: document.querySelector("#search"),
  toppingFilter: document.querySelector("#topping-filter"),
  resultStatus: document.querySelector("#result-status"),
  conceptGrid: document.querySelector("#concept-grid"),
  projectionId: document.querySelector("#projection-id"),
  contractVersion: document.querySelector("#contract-version"),
  ontologyIri: document.querySelector("#ontology-iri"),
  versionIri: document.querySelector("#version-iri"),
  detail: document.querySelector("#concept-detail"),
  detailLabel: document.querySelector("#detail-label"),
  detailId: document.querySelector("#detail-id"),
  detailSuperclasses: document.querySelector("#detail-superclasses"),
  detailToppings: document.querySelector("#detail-toppings"),
  detailSourceIri: document.querySelector("#detail-source-iri"),
  detailSuperclassSemantics: document.querySelector("#detail-superclass-semantics"),
  detailToppingSemantics: document.querySelector("#detail-topping-semantics"),
  closeDetail: document.querySelector("#close-detail"),
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

async function fetchJson(url) {
  const response = await fetch(url, { cache: "no-store" });
  const payload = await response.json();
  if (!response.ok) {
    throw new Error(payload.message || `Application request failed with HTTP ${response.status}`);
  }
  return payload;
}

async function loadContractFacts() {
  const contract = await fetchJson(CONTRACT_URL);
  const projection = contract["x-pizza-projection"];
  if (!projection?.projection || !projection?.sourceSemanticModel) {
    throw new Error("OpenAPI contract does not expose the expected projection metadata");
  }

  elements.projectionId.textContent = projection.projection.id;
  elements.contractVersion.textContent = contract.info.version;
  elements.ontologyIri.textContent = projection.sourceSemanticModel.ontologyIri;
  elements.versionIri.textContent = projection.sourceSemanticModel.versionIri;
}

function populateToppingFilter(concepts) {
  const toppings = new Map();
  for (const concept of concepts) {
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

function conceptSummaryCard(concept) {
  const card = document.createElement("article");
  card.className = "concept-card concept-summary";

  const heading = document.createElement("div");
  heading.className = "card-heading";

  const identity = document.createElement("div");
  const kind = document.createElement("p");
  kind.className = "concept-kind";
  kind.textContent = "API result";

  const label = document.createElement("h3");
  label.textContent = concept.displayLabel;

  const id = document.createElement("code");
  id.className = "concept-id";
  id.textContent = concept.id;
  id.title = concept.iri;

  identity.append(kind, label, id);

  const count = document.createElement("span");
  count.className = "topping-count";
  count.textContent = `${concept.requiredToppings.length} required topping${concept.requiredToppings.length === 1 ? "" : "s"}`;

  heading.append(identity, count);

  const summary = document.createElement("p");
  summary.className = "api-summary-text";
  summary.textContent = `${concept.directSuperClasses.length} direct superclass relation${concept.directSuperClasses.length === 1 ? "" : "s"} projected.`;

  const button = document.createElement("button");
  button.className = "detail-button";
  button.type = "button";
  button.textContent = "Load detail through item API";
  button.addEventListener("click", () => openDetail(concept.id));

  card.append(heading, summary, button);
  return card;
}

function renderCollection(collection) {
  elements.conceptGrid.replaceChildren(...collection.items.map(conceptSummaryCard));
  elements.resultStatus.textContent =
    `${collection.count} projected concept${collection.count === 1 ? "" : "s"} returned by the application.`;
}

function collectionUrl() {
  const parameters = new URLSearchParams();
  if (state.query.trim()) {
    parameters.set("q", state.query.trim());
  }
  if (state.requiredTopping) {
    parameters.set("requiredTopping", state.requiredTopping);
  }
  const query = parameters.toString();
  return query ? `${COLLECTION_URL}?${query}` : COLLECTION_URL;
}

async function refreshCollection() {
  try {
    elements.resultStatus.classList.remove("error");
    elements.resultStatus.textContent = "Querying application…";
    const collection = await fetchJson(collectionUrl());
    renderCollection(collection);
  } catch (error) {
    elements.resultStatus.textContent = `Unable to query the application: ${error.message}`;
    elements.resultStatus.classList.add("error");
  }
}

async function openDetail(conceptId) {
  try {
    const concept = await fetchJson(`${COLLECTION_URL}/${encodeURIComponent(conceptId)}`);
    elements.detailLabel.textContent = concept.displayLabel;
    elements.detailId.textContent = concept.id;
    elements.detailId.title = concept.iri;
    elements.detailSuperclasses.replaceChildren(
      ...concept.directSuperClasses.map(semanticReference),
    );
    elements.detailToppings.replaceChildren(...concept.requiredToppings.map(semanticReference));
    elements.detailSourceIri.textContent = concept.traceability.sourceEntityIri;
    elements.detailSuperclassSemantics.textContent = concept.traceability.superclassSemantics;
    elements.detailToppingSemantics.textContent = concept.traceability.toppingSemantics;
    elements.detail.hidden = false;
    elements.detail.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (error) {
    elements.resultStatus.textContent = `Unable to load concept detail: ${error.message}`;
    elements.resultStatus.classList.add("error");
  }
}

function bindControls() {
  elements.search.addEventListener("input", (event) => {
    state.query = event.target.value;
    refreshCollection();
  });

  elements.toppingFilter.addEventListener("change", (event) => {
    state.requiredTopping = event.target.value;
    refreshCollection();
  });

  elements.closeDetail.addEventListener("click", () => {
    elements.detail.hidden = true;
  });
}

async function initialize() {
  bindControls();
  await loadContractFacts();
  const initial = await fetchJson(COLLECTION_URL);
  state.initialConcepts = initial.items;
  populateToppingFilter(initial.items);
  renderCollection(initial);
}

initialize().catch((error) => {
  console.error(error);
  elements.resultStatus.textContent = `Unable to initialize the API-backed explorer: ${error.message}`;
  elements.resultStatus.classList.add("error");
});
