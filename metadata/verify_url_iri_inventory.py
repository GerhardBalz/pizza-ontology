from __future__ import annotations

import argparse
import json
import os
import re
import urllib.request
from collections import Counter
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "metadata" / "url-iri-inventory.json"

HISTORICAL_ONTOLOGY = "http://www.co-ode.org/ontologies/pizza"
HISTORICAL_VERSION = "http://www.co-ode.org/ontologies/pizza/2.0.0"
HISTORICAL_ENTITY_NAMESPACE = "http://www.co-ode.org/ontologies/pizza/pizza.owl#"
HISTORICAL_DEFAULT_PREFIX = "http://www.co-ode.org/ontologies/pizza#"

ALLOWED_ROLES = {
    "semantic_identifier",
    "historical_source_reference",
    "current_source_location",
    "publication_landing_page",
    "access_url",
    "download_url",
    "documentation_reference_url",
    "application_ux_link",
}

TEXT_SUFFIXES = {
    ".md", ".ttl", ".owl", ".ofn", ".rq", ".sparql", ".json", ".yaml",
    ".yml", ".xml", ".py", ".js", ".html", ".css", ".sh", ".bat", ".txt",
}

SCAN_EXCLUSIONS = {
    Path("metadata/url-iri-inventory.json"),
    Path("metadata/verify_url_iri_inventory.py"),
    Path("docs/url-iri-resolution-inventory.md"),
}

URL_RE = re.compile(r"https?://[^\s<>'\"`)\]}]+")
FORBIDDEN_UX_LINK_PATTERNS = (
    re.compile(r"\.href\s*=\s*[^;\n]*(?:\.iri|sourceEntityIri|ontologyIri|versionIri)", re.IGNORECASE),
    re.compile(r"setAttribute\(\s*['\"]href['\"]\s*,\s*[^)]*(?:\.iri|sourceEntityIri|ontologyIri|versionIri)", re.IGNORECASE),
)


def load_inventory() -> dict:
    with INVENTORY_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def match_rule(url: str, rules: list[dict]) -> dict | None:
    for rule in rules:
        if rule["match"] == "exact" and url == rule["value"]:
            return rule
        if rule["match"] == "prefix" and url.startswith(rule["value"]):
            return rule
    return None


def verify_inventory_structure(inventory: dict) -> tuple[dict[str, dict], dict[str, dict]]:
    if inventory.get("inventoryVersion") != 1:
        raise AssertionError("Expected url/iri inventoryVersion 1")

    rules = inventory.get("classificationRules")
    references = inventory.get("canonicalReferences")
    if not isinstance(rules, list) or not rules:
        raise AssertionError("classificationRules must be a non-empty list")
    if not isinstance(references, list) or not references:
        raise AssertionError("canonicalReferences must be a non-empty list")

    rules_by_id: dict[str, dict] = {}
    for rule in rules:
        rule_id = rule.get("id")
        if not rule_id or rule_id in rules_by_id:
            raise AssertionError(f"Duplicate or missing classification rule id: {rule_id!r}")
        if rule.get("match") not in {"exact", "prefix"}:
            raise AssertionError(f"Unsupported match mode for {rule_id}: {rule.get('match')!r}")
        if rule.get("role") not in ALLOWED_ROLES:
            raise AssertionError(f"Unsupported role for {rule_id}: {rule.get('role')!r}")
        if not isinstance(rule.get("actionable"), bool):
            raise AssertionError(f"actionable must be boolean for {rule_id}")
        if not isinstance(rule.get("controlledByProject"), bool):
            raise AssertionError(f"controlledByProject must be boolean for {rule_id}")
        rules_by_id[rule_id] = rule

    refs_by_id: dict[str, dict] = {}
    qc_text = (ROOT / ".github" / "workflows" / "qc.yml").read_text(encoding="utf-8")
    for ref in references:
        ref_id = ref.get("id")
        if not ref_id or ref_id in refs_by_id:
            raise AssertionError(f"Duplicate or missing canonical reference id: {ref_id!r}")
        rule_id = ref.get("classificationRule")
        if rule_id not in rules_by_id:
            raise AssertionError(f"Unknown classification rule {rule_id!r} for {ref_id}")
        rule = rules_by_id[rule_id]
        if match_rule(ref["value"], [rule]) is None:
            raise AssertionError(f"Canonical reference {ref_id} does not match its declared rule {rule_id}")

        verification = ref.get("verification", {})
        mode = verification.get("mode")
        if mode not in {"none", "http", "existing_verifier"}:
            raise AssertionError(f"Unsupported verification mode {mode!r} for {ref_id}")
        if rule["actionable"] and mode == "none":
            raise AssertionError(f"Actionable reference {ref_id} has no resolution verification")
        if not rule["actionable"] and mode != "none":
            raise AssertionError(f"Non-actionable semantic/historical reference {ref_id} must not imply resolution")
        if mode == "http" and not verification.get("url"):
            raise AssertionError(f"HTTP verification URL missing for {ref_id}")
        if mode == "existing_verifier":
            verifier_path_value = verification.get("path", "")
            verifier_path = ROOT / verifier_path_value
            if not verifier_path.is_file():
                raise AssertionError(f"Existing verifier for {ref_id} does not exist: {verifier_path}")
            expected_command = f"python {verifier_path_value}"
            if expected_command not in qc_text:
                raise AssertionError(f"Existing verifier for {ref_id} is not wired into main CI: {expected_command}")
        refs_by_id[ref_id] = ref

    return rules_by_id, refs_by_id


def verify_historical_identity(rules_by_id: dict[str, dict], refs_by_id: dict[str, dict]) -> None:
    required = {
        "pizza-2.0-ontology-iri": HISTORICAL_ONTOLOGY,
        "pizza-2.0-version-iri": HISTORICAL_VERSION,
        "pizza-2.0-entity-namespace": HISTORICAL_ENTITY_NAMESPACE,
        "pizza-2.0-default-prefix": HISTORICAL_DEFAULT_PREFIX,
    }
    for ref_id, expected in required.items():
        ref = refs_by_id.get(ref_id)
        if ref is None or ref.get("value") != expected:
            raise AssertionError(f"Historical identity inventory mismatch for {ref_id}")
        rule = rules_by_id[ref["classificationRule"]]
        if rule["role"] != "semantic_identifier":
            raise AssertionError(f"{ref_id} must remain classified as semantic_identifier")
        if rule["actionable"] or rule["controlledByProject"]:
            raise AssertionError(f"{ref_id} must not become a project-controlled actionable URL")

    ontology_text = (ROOT / "src" / "ontology" / "pizza-edit.owl").read_text(encoding="utf-8")
    anchors = (
        f"Prefix(:=<{HISTORICAL_DEFAULT_PREFIX}>)",
        f"Prefix(pizza:=<{HISTORICAL_ENTITY_NAMESPACE}>)",
        f"Ontology(<{HISTORICAL_ONTOLOGY}>",
        f"<{HISTORICAL_VERSION}>",
    )
    for anchor in anchors:
        if anchor not in ontology_text:
            raise AssertionError(f"Historical Pizza identity anchor missing from source: {anchor}")

    projection = json.loads((ROOT / "projections" / "pizza-concepts" / "pizza-concepts.json").read_text(encoding="utf-8"))
    source = projection["sourceSemanticModel"]
    if source["ontologyIri"] != HISTORICAL_ONTOLOGY:
        raise AssertionError("JSON projection changed historical ontology IRI")
    if source["versionIri"] != HISTORICAL_VERSION:
        raise AssertionError("JSON projection changed historical version IRI")
    for concept in projection["concepts"]:
        if not concept["iri"].startswith(HISTORICAL_ENTITY_NAMESPACE):
            raise AssertionError(f"Projection entity IRI escaped historical namespace: {concept['iri']}")
        trace = concept["traceability"]["sourceEntityIri"]
        if trace != concept["iri"]:
            raise AssertionError(f"Projection traceability no longer preserves entity IRI: {concept['id']}")

    openapi = json.loads((ROOT / "projections" / "pizza-openapi" / "pizza-concepts.openapi.json").read_text(encoding="utf-8"))
    openapi_source = openapi["x-pizza-projection"]["sourceSemanticModel"]
    if openapi_source["ontologyIri"] != HISTORICAL_ONTOLOGY:
        raise AssertionError("OpenAPI projection changed historical ontology IRI")
    if openapi_source["versionIri"] != HISTORICAL_VERSION:
        raise AssertionError("OpenAPI projection changed historical version IRI")


def verify_repository_surface(inventory: dict, rules_by_id: dict[str, dict]) -> Counter:
    prefixes = tuple(inventory["pizzaSpecificPrefixes"])
    rules = list(rules_by_id.values())
    counts: Counter = Counter()
    unclassified: list[tuple[Path, str]] = []

    for path in ROOT.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        relative = path.relative_to(ROOT)
        if relative in SCAN_EXCLUSIONS:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        for raw in URL_RE.findall(text):
            url = raw.rstrip(".,;:")
            if not url.startswith(prefixes):
                continue
            rule = match_rule(url, rules)
            if rule is None:
                unclassified.append((relative, url))
            else:
                counts[rule["role"]] += 1

    if unclassified:
        sample = "\n".join(f"  {path}: {url}" for path, url in unclassified[:20])
        raise AssertionError(f"Unclassified Pizza-specific URL/IRI occurrences:\n{sample}")

    if counts["semantic_identifier"] == 0:
        raise AssertionError("Repository scan found no historical semantic identifier occurrences")
    if counts["current_source_location"] == 0:
        raise AssertionError("Repository scan found no current Pizza source-location occurrences")
    if counts["publication_landing_page"] == 0:
        raise AssertionError("Repository scan found no Pizza publication landing-page occurrences")

    return counts


def verify_ux_does_not_link_historical_iris() -> None:
    ux_files = (
        ROOT / "examples" / "ux" / "pizza-explorer" / "app.js",
        ROOT / "examples" / "ux" / "pizza-api-explorer" / "app.js",
    )
    for path in ux_files:
        text = path.read_text(encoding="utf-8")
        if 'href="http://www.co-ode.org/ontologies/pizza' in text or "href='http://www.co-ode.org/ontologies/pizza" in text:
            raise AssertionError(f"Historical Pizza IRI rendered as literal hyperlink in {path}")
        for pattern in FORBIDDEN_UX_LINK_PATTERNS:
            if pattern.search(text):
                raise AssertionError(f"UX appears to turn semantic IRI data into navigation href in {path}")


def verify_persistent_reference_plan(inventory: dict) -> None:
    plan = inventory.get("persistentReferencePlan", {})
    if plan.get("namespace") != "https://w3id.org/pizza-ontology/":
        raise AssertionError("Unexpected proposed persistent-reference namespace")
    if plan.get("status") != "proposed":
        raise AssertionError("W3ID routes must remain proposed until the upstream registration is merged")
    if not plan.get("routes"):
        raise AssertionError("Persistent-reference route plan is empty")
    if plan.get("entityRoutes", {}).get("status") != "deferred":
        raise AssertionError("Entity aliases must remain deferred until an explicit mapping/authority contract exists")

    historical = {HISTORICAL_ONTOLOGY, HISTORICAL_VERSION, HISTORICAL_ENTITY_NAMESPACE, HISTORICAL_DEFAULT_PREFIX}
    for route in plan["routes"]:
        target = route["target"]
        if target in historical:
            raise AssertionError(f"Persistent-reference route {route['path']!r} must target a location, not pretend a historical identifier is a repository-owned location")


def check_http_reference(ref: dict) -> None:
    verification = ref["verification"]
    url = verification["url"]
    parsed = urlsplit(url)
    headers = {
        "User-Agent": "pizza-ontology-url-iri-verifier/1.0",
        "Accept": "*/*",
        "Range": "bytes=0-0",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if parsed.netloc == "api.github.com":
        headers["Accept"] = "application/vnd.github+json"
        headers["X-GitHub-Api-Version"] = "2022-11-28"
        if token:
            headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(request, timeout=30) as response:
        status = getattr(response, "status", 200)
        if status < 200 or status >= 400:
            raise AssertionError(f"Actionable reference {ref['id']} did not resolve: HTTP {status} {url}")
        response.read(1)


def verify_http_references(refs_by_id: dict[str, dict]) -> None:
    checked = 0
    delegated = 0
    for ref in refs_by_id.values():
        mode = ref["verification"]["mode"]
        if mode == "http":
            check_http_reference(ref)
            checked += 1
        elif mode == "existing_verifier":
            delegated += 1
    print(f"Resolution verification completed: {checked} HTTP references checked, {delegated} release-asset references delegated to the existing published-release verifier.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Pizza semantic identifier vs resolvable-location policy.")
    parser.add_argument("--check-http", action="store_true", help="Dereference canonical actionable URLs in addition to static contract checks.")
    args = parser.parse_args()

    inventory = load_inventory()
    rules_by_id, refs_by_id = verify_inventory_structure(inventory)
    verify_historical_identity(rules_by_id, refs_by_id)
    counts = verify_repository_surface(inventory, rules_by_id)
    verify_ux_does_not_link_historical_iris()
    verify_persistent_reference_plan(inventory)

    if args.check_http:
        verify_http_references(refs_by_id)

    summary = ", ".join(f"{role}={count}" for role, count in sorted(counts.items()))
    print(f"Pizza URL/IRI classification verified: {summary}")


if __name__ == "__main__":
    main()
