#!/usr/bin/env python3
"""Verify the staged Pizza preservation/reference W3ID config against policy."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POLICY = ROOT / "metadata" / "reference-resolution-policy.json"
HTACCESS = ROOT / "publication" / "w3id" / "pizza-ontology" / ".htaccess"
README = ROOT / "publication" / "w3id" / "pizza-ontology" / "README.md"


def route_pattern(path: str) -> str:
    if not path:
        return r"^$"
    escaped = re.escape(path.rstrip("/"))
    escaped = escaped.replace(r"\/", "/")
    return rf"^{escaped}/?$"


def main() -> int:
    policy = json.loads(POLICY.read_text(encoding="utf-8"))
    config = HTACCESS.read_text(encoding="utf-8")
    readme = README.read_text(encoding="utf-8")

    assert policy["preservationReferenceNamespace"]["status"] == "planned"
    assert policy["preservationReferenceNamespace"]["semanticIdentity"] is False
    assert "Point of contact: Gerhard Balz" in config
    assert "@GerhardBalz" in config
    assert "Options +FollowSymLinks -Indexes" in config
    assert "RewriteEngine On" in config
    assert "preservation/reference namespace" in config
    assert "does not replace" in readme.lower() or "does not replace" in config.lower()

    expected_lines: list[str] = []
    for route in policy["preservationReferenceNamespace"]["routes"]:
        pattern = route_pattern(route["path"])
        target = route["target"]
        expected = f"RewriteRule {pattern} {target} [R=303,NE,L]"
        expected_lines.append(expected)
        assert expected in config, f"missing policy route in .htaccess: {expected}"

        if route["path"].startswith("preservation/2.0"):
            assert "preservation-v0.2.0" in target, (
                f"immutable preservation route does not target preservation-v0.2.0: {route}"
            )
            assert "/main/" not in target and "/blob/main/" not in target, (
                f"immutable preservation route targets mutable main: {route}"
            )

    rewrite_lines = [
        line.strip()
        for line in config.splitlines()
        if line.strip().startswith("RewriteRule ")
    ]
    assert sorted(rewrite_lines) == sorted(expected_lines), (
        "staged .htaccess contains routes not governed by the machine policy "
        "or omits a governed route"
    )

    # Boundary documentation may explicitly mention terms such as owl:sameAs while
    # saying they are NOT asserted. What must be absent is any actual mapping/config
    # statement that uses them to relate the W3ID namespace to historical identity.
    for marker in ("owl:sameAs", "equivalentClass", "equivalentProperty"):
        assert marker not in config, (
            f"unexpected semantic-identity mapping term in .htaccess: {marker}"
        )

    positive_mapping_patterns = [
        r"https://w3id\.org/pizza-ontology/[^\s`]*\s+(?:is|=|maps?\s+to)\s+.*owl:sameAs",
        r"owl:sameAs\s+<http://www\.co-ode\.org/ontologies/pizza",
        r"equivalent(?:Class|Property)\s+<http://www\.co-ode\.org/ontologies/pizza",
    ]
    for pattern in positive_mapping_patterns:
        assert not re.search(pattern, readme, re.IGNORECASE), (
            f"unexpected positive semantic-identity claim in W3ID README: {pattern}"
        )

    historical = policy["historicalIdentity"]
    assert historical["authorityClaimedByPreservationProject"] is False
    assert historical["dereferenceabilityRequired"] is False

    print(f"verified {len(expected_lines)} planned W3ID routes")
    print("PASS: staged Pizza W3ID configuration matches the preservation/reference policy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
