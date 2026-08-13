#!/usr/bin/env python3
"""Inventory Pizza-specific HTTP(S) references and verify resolution promises.

Historical Pizza 2.0 identifiers are semantic identifiers, not publication promises.
Current source/publication/download/reference URLs are checked when requested.
URL templates and construction bases are classified explicitly and are not treated as
finished actionable links. UX sources are additionally checked so historical semantic
IRIs cannot silently become clickable navigation targets.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = ROOT / "metadata" / "reference-resolution-policy.json"
URL_RE = re.compile(r"https?://[^\s<>\"'`]+")
TRAILING = ".,;:!?)]}"
USER_AGENT = "pizza-ontology-reference-verifier/1.0 (+https://github.com/GerhardBalz/pizza-ontology)"
SEMANTIC_IRI_TOKEN_RE = re.compile(r"(?:\.iri\b|ontologyIri\b|versionIri\b|sourceEntityIri\b)")
UX_HREF_FROM_SEMANTIC_IRI_RE = re.compile(
    r"(?:\.href\s*=|setAttribute\s*\(\s*[\"']href[\"']\s*,|href\s*=)[^\n;>]*(?:\.iri\b|ontologyIri\b|versionIri\b|sourceEntityIri\b)",
    re.IGNORECASE,
)
UX_DIRECT_HISTORICAL_ANCHOR_RE = re.compile(
    r"<a\b[^>]*href\s*=\s*[\"']http://www\.co-ode\.org/ontologies/pizza[^\"']*[\"']",
    re.IGNORECASE,
)


def load_policy() -> dict[str, Any]:
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))


def tracked_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "-z"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
    )
    return [ROOT / p.decode("utf-8") for p in result.stdout.split(b"\0") if p]


def is_pizza_specific(url: str, policy: dict[str, Any]) -> bool:
    return any(marker in url for marker in policy["classification"]["pizzaSpecificMarkers"])


def classify(url: str, policy: dict[str, Any]) -> tuple[str, bool]:
    historical = policy["historicalIdentity"]
    historical_prefixes = {
        historical["ontologyIri"],
        historical["versionIri"],
        historical["entityNamespace"].rstrip("#"),
    }
    if any(url.startswith(prefix) for prefix in historical_prefixes):
        return "historical-semantic-identifier", False

    # Repository docs and scripts legitimately contain URL templates such as
    # https://github.com/.../blob/{RELEASE_COMMIT}/.... They describe how a URL is
    # constructed; they are not themselves clickable publication promises.
    if "{" in url or "}" in url:
        return "url-template", False

    if url.startswith(policy["historicalSource"]["url"].rsplit("/", 1)[0] + "/"):
        return "historical-source-reference", True

    w3id_base = policy["preservationReferenceNamespace"]["base"]
    if url.startswith(w3id_base):
        active = policy["preservationReferenceNamespace"]["status"] == "active"
        return "preservation-reference-url", active

    repo = "https://github.com/GerhardBalz/pizza-ontology"
    construction_bases = {
        repo + "/releases/download/",
        repo + "/releases/tag/",
        repo + "/blob/",
        repo + "/tree/",
        "https://raw.githubusercontent.com/GerhardBalz/pizza-ontology/",
    }
    if url in construction_bases:
        return "url-construction-base", False

    if url.startswith(repo + "/releases/download/"):
        return "download-url", True
    if url.startswith(repo + "/releases/tag/"):
        return "publication-landing-page", True
    if url.startswith(repo + "/blob/") or url.startswith(repo + "/tree/"):
        return "current-source-location", True
    if url == repo or url == repo + "/":
        return "publication-landing-page", True
    if url.startswith(repo):
        return "repository-reference", False

    raw = "https://raw.githubusercontent.com/GerhardBalz/pizza-ontology/"
    if url.startswith(raw):
        return "current-source-location", True

    return "unclassified", False


def scan(policy: dict[str, Any]) -> list[dict[str, Any]]:
    occurrences: list[dict[str, Any]] = []
    for path in tracked_files():
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        rel = path.relative_to(ROOT).as_posix()
        for line_no, line in enumerate(text.splitlines(), start=1):
            for match in URL_RE.finditer(line):
                url = match.group(0).rstrip(TRAILING)
                if not is_pizza_specific(url, policy):
                    continue
                role, promised = classify(url, policy)
                occurrences.append(
                    {
                        "file": rel,
                        "line": line_no,
                        "url": url,
                        "role": role,
                        "resolutionPromised": promised,
                    }
                )
    return occurrences


def verify_protected_source(policy: dict[str, Any]) -> dict[str, Any]:
    protected = policy["protectedHistoricalSource"]
    path = protected["path"]
    expected = protected["gitBlobSha1"]
    actual = subprocess.check_output(["git", "hash-object", path], cwd=ROOT, text=True).strip()
    content = (ROOT / path).read_bytes()
    return {
        "path": path,
        "expectedGitBlobSha1": expected,
        "actualGitBlobSha1": actual,
        "sha256": hashlib.sha256(content).hexdigest(),
        "unchanged": actual == expected,
    }


def verify_ux_identifier_display() -> dict[str, Any]:
    """Ensure Pizza UX keeps historical semantic IRIs as display/traceability data.

    Relative application links are outside this historical-IRI rule. This regression
    specifically blocks code that assigns ontology/version/entity IRI fields to href.
    """

    files: list[dict[str, Any]] = []
    violations: list[dict[str, Any]] = []
    display_expressions: list[dict[str, Any]] = []

    ux_root = ROOT / "examples" / "ux"
    for path in tracked_files():
        if not path.is_file() or ux_root not in path.parents:
            continue
        if path.suffix.lower() not in {".js", ".html"}:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue

        rel = path.relative_to(ROOT).as_posix()
        files.append({"path": rel, "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest()})

        for pattern, rule in (
            (UX_HREF_FROM_SEMANTIC_IRI_RE, "semantic IRI field assigned to href"),
            (UX_DIRECT_HISTORICAL_ANCHOR_RE, "historical co-ode.org Pizza IRI embedded as anchor href"),
        ):
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                violations.append(
                    {
                        "file": rel,
                        "line": line,
                        "rule": rule,
                        "expression": match.group(0).strip(),
                    }
                )

        for line_no, line_text in enumerate(text.splitlines(), start=1):
            if ("textContent" in line_text or ".title" in line_text) and SEMANTIC_IRI_TOKEN_RE.search(line_text):
                display_expressions.append(
                    {"file": rel, "line": line_no, "expression": line_text.strip()}
                )

    return {
        "rule": "Historical Pizza ontology/version/entity IRIs may be displayed as text/traceability metadata but must not be generated as actionable href values by the UX examples.",
        "filesChecked": files,
        "semanticIriDisplayExpressions": display_expressions,
        "semanticIriAnchorViolations": violations,
        "passed": not violations,
    }


def resolve_once(url: str, method: str) -> tuple[int, str]:
    headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if method == "GET":
        headers["Range"] = "bytes=0-0"
    request = urllib.request.Request(url, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=20) as response:
        return int(response.status), response.geturl()


def resolve(url: str) -> dict[str, Any]:
    last_error = ""
    for attempt in range(1, 4):
        for method in ("HEAD", "GET"):
            try:
                status, effective = resolve_once(url, method)
                if 200 <= status < 400:
                    return {
                        "url": url,
                        "ok": True,
                        "status": status,
                        "effectiveUrl": effective,
                        "method": method,
                        "attempt": attempt,
                    }
            except urllib.error.HTTPError as exc:
                last_error = f"HTTP {exc.code}"
                if exc.code not in {403, 405, 429}:
                    break
            except Exception as exc:  # network evidence, keep exact failure text
                last_error = f"{type(exc).__name__}: {exc}"
        if attempt < 3:
            time.sleep(attempt)
    return {"url": url, "ok": False, "error": last_error}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-network", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    policy = load_policy()
    occurrences = scan(policy)
    protected = verify_protected_source(policy)
    ux = verify_ux_identifier_display()

    by_url: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in occurrences:
        by_url[item["url"]].append(item)

    unique: list[dict[str, Any]] = []
    for url in sorted(by_url):
        items = by_url[url]
        roles = sorted({item["role"] for item in items})
        promised = any(item["resolutionPromised"] for item in items)
        unique.append(
            {
                "url": url,
                "roles": roles,
                "resolutionPromised": promised,
                "occurrenceCount": len(items),
            }
        )

    network_results: list[dict[str, Any]] = []
    if args.check_network:
        for item in unique:
            if item["resolutionPromised"]:
                network_results.append(resolve(item["url"]))

    categories = Counter(item["role"] for item in occurrences)
    unclassified = [item for item in occurrences if item["role"] == "unclassified"]
    failed_network = [item for item in network_results if not item["ok"]]
    ux_violations = ux["semanticIriAnchorViolations"]

    evidence = {
        "policy": "metadata/reference-resolution-policy.json",
        "historicalIdentityRule": "Historical Pizza 2.0 IRIs are semantic identifiers and are not treated as HTTP resolution promises.",
        "constructionReferenceRule": "URL templates and bare construction bases are classified but are not treated as finished actionable links.",
        "preservationReferenceStatus": policy["preservationReferenceNamespace"]["status"],
        "protectedHistoricalSource": protected,
        "uxIdentifierDisplay": ux,
        "summary": {
            "pizzaSpecificOccurrences": len(occurrences),
            "uniquePizzaSpecificUrls": len(unique),
            "categories": dict(sorted(categories.items())),
            "unclassifiedOccurrences": len(unclassified),
            "networkChecks": len(network_results),
            "networkFailures": len(failed_network),
            "uxFilesChecked": len(ux["filesChecked"]),
            "uxSemanticIriDisplayExpressions": len(ux["semanticIriDisplayExpressions"]),
            "uxSemanticIriAnchorViolations": len(ux_violations),
        },
        "uniqueUrls": unique,
        "occurrences": occurrences,
        "network": network_results,
    }

    rendered = json.dumps(evidence, indent=2, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered + "\n", encoding="utf-8")

    print(json.dumps(evidence["summary"], indent=2, sort_keys=True))
    print(
        "protected historical source:",
        protected["actualGitBlobSha1"],
        "PASS" if protected["unchanged"] else "FAIL",
    )
    print(
        "UX semantic-IRI navigation regression:",
        "PASS" if ux["passed"] else "FAIL",
    )

    if unclassified:
        print("ERROR: unclassified Pizza-specific references:", file=sys.stderr)
        for item in unclassified[:20]:
            print(f"  {item['file']}:{item['line']} {item['url']}", file=sys.stderr)
    if failed_network:
        print("ERROR: promised actionable URLs did not resolve:", file=sys.stderr)
        for item in failed_network:
            print(f"  {item['url']} — {item.get('error', 'unknown')}", file=sys.stderr)
    if ux_violations:
        print("ERROR: UX turns historical semantic IRIs into actionable href values:", file=sys.stderr)
        for item in ux_violations:
            print(f"  {item['file']}:{item['line']} {item['expression']}", file=sys.stderr)
    if not protected["unchanged"]:
        print("ERROR: historical Pizza source bytes changed", file=sys.stderr)

    if unclassified or failed_network or ux_violations or not protected["unchanged"]:
        return 1

    print("PASS: Pizza identity/location inventory, UX semantics, and current resolution promises hold")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
