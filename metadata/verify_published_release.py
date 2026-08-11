#!/usr/bin/env python3
"""Verify preservation-v0.2.0 as an external GitHub release consumer.

This check deliberately uses public GitHub release/tag/download URLs rather than
repository-local build output. It verifies that the published release is tied to
the intended source commit and that its immutable asset bundle remains complete,
fetchable, and checksum-consistent.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.request

REPOSITORY = "GerhardBalz/pizza-ontology"
TAG = "preservation-v0.2.0"
EXPECTED_COMMIT = "3bd6e3817e2cdc44e77899a2e603878a85845e9d"

RELEASE_PAGE = f"https://github.com/{REPOSITORY}/releases/tag/{TAG}"
RELEASE_API = f"https://api.github.com/repos/{REPOSITORY}/releases/tags/{TAG}"
TAG_API = f"https://api.github.com/repos/{REPOSITORY}/git/ref/tags/{TAG}"
TAG_SOURCE = (
    f"https://raw.githubusercontent.com/{REPOSITORY}/{TAG}/src/ontology/pizza-edit.owl"
)
DOWNLOAD_BASE = f"https://github.com/{REPOSITORY}/releases/download/{TAG}"

ASSET_URLS = {
    "pizza-2.0-preserved.ofn": f"{DOWNLOAD_BASE}/pizza-2.0-preserved.ofn",
    "pizza-2.0-preserved.ttl": f"{DOWNLOAD_BASE}/pizza-2.0-preserved.ttl",
    "SHA256SUMS": f"{DOWNLOAD_BASE}/SHA256SUMS",
}

HISTORICAL_ONTOLOGY_IRI = b"http://www.co-ode.org/ontologies/pizza"
HISTORICAL_VERSION_IRI = b"http://www.co-ode.org/ontologies/pizza/2.0.0"
HISTORICAL_ENTITY_NAMESPACE = b"http://www.co-ode.org/ontologies/pizza/pizza.owl#"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def request_bytes(url: str, *, accept: str | None = None) -> bytes:
    headers = {"User-Agent": "pizza-ontology-publication-verifier"}
    if accept:
        headers["Accept"] = accept

    # Use the workflow token only for GitHub API calls. Public raw/download
    # URLs are intentionally exercised the same way an unauthenticated external
    # consumer would reach them.
    token = os.environ.get("GITHUB_TOKEN")
    if token and url.startswith("https://api.github.com/"):
        headers["Authorization"] = f"Bearer {token}"

    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=60) as response:
        require(200 <= response.status < 300, f"unexpected HTTP status for {url}: {response.status}")
        return response.read()


def request_json(url: str) -> dict:
    return json.loads(request_bytes(url, accept="application/vnd.github+json"))


def resolve_tag_commit() -> str:
    ref = request_json(TAG_API)
    obj = ref["object"]

    # gh release create normally creates a lightweight tag, but follow an
    # annotated tag defensively if GitHub ever returns one here.
    for _ in range(4):
        obj_type = obj["type"]
        if obj_type == "commit":
            return obj["sha"]
        require(obj_type == "tag", f"unexpected Git ref object type: {obj_type}")
        tag_obj = request_json(obj["url"])
        obj = tag_obj["object"]

    raise AssertionError("tag indirection exceeded expected depth")


def parse_checksums(data: bytes) -> dict[str, str]:
    text = data.decode("utf-8").strip()
    entries: dict[str, str] = {}

    for line in text.splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})\s+(.+)", line.strip())
        require(match is not None, f"invalid SHA256SUMS line: {line!r}")
        digest, filename = match.groups()
        require(filename not in entries, f"duplicate checksum entry: {filename}")
        entries[filename] = digest

    require(
        set(entries) == {"pizza-2.0-preserved.ofn", "pizza-2.0-preserved.ttl"},
        f"unexpected SHA256SUMS entries: {sorted(entries)}",
    )
    return entries


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    release = request_json(RELEASE_API)
    require(release["tag_name"] == TAG, f"unexpected release tag: {release['tag_name']}")
    require(release["html_url"] == RELEASE_PAGE, f"unexpected release URL: {release['html_url']}")
    require(not release["draft"], "published preservation release must not be a draft")
    require(not release["prerelease"], "preservation-v0.2.0 must not be a prerelease")

    tag_commit = resolve_tag_commit()
    require(
        tag_commit == EXPECTED_COMMIT,
        f"release tag moved: expected {EXPECTED_COMMIT}, got {tag_commit}",
    )

    assets = {asset["name"]: asset for asset in release["assets"]}
    require(
        set(assets) == set(ASSET_URLS),
        f"published asset set drifted: expected={sorted(ASSET_URLS)}, actual={sorted(assets)}",
    )

    for name, expected_url in ASSET_URLS.items():
        asset = assets[name]
        require(asset["state"] == "uploaded", f"release asset is not uploaded: {name}")
        require(
            asset["browser_download_url"] == expected_url,
            f"unexpected download URL for {name}: {asset['browser_download_url']}",
        )

    checksum_bytes = request_bytes(ASSET_URLS["SHA256SUMS"])
    checksum_entries = parse_checksums(checksum_bytes)
    ofn_bytes = request_bytes(ASSET_URLS["pizza-2.0-preserved.ofn"])
    ttl_bytes = request_bytes(ASSET_URLS["pizza-2.0-preserved.ttl"])

    actual_digests = {
        "pizza-2.0-preserved.ofn": sha256(ofn_bytes),
        "pizza-2.0-preserved.ttl": sha256(ttl_bytes),
    }
    require(
        actual_digests == checksum_entries,
        f"published asset checksums do not match SHA256SUMS: {actual_digests!r}",
    )

    # The Functional Syntax release distribution is governed as an exact copy
    # of the tag-pinned editor source.
    source_bytes = request_bytes(TAG_SOURCE)
    require(
        ofn_bytes == source_bytes,
        "published Functional Syntax distribution differs from tag-pinned Pizza source",
    )

    # The Turtle graph-equivalence proof is performed by ROBOT before upload.
    # Here, as an external consumer, verify that the downloaded bytes still
    # retain the historical semantic identity anchors.
    for marker, description in (
        (HISTORICAL_ONTOLOGY_IRI, "ontology IRI"),
        (HISTORICAL_VERSION_IRI, "version IRI"),
        (HISTORICAL_ENTITY_NAMESPACE, "entity namespace"),
    ):
        require(marker in ttl_bytes, f"published Turtle is missing historical {description}")

    # When GitHub exposes an asset digest, require consistency with the governed
    # checksum manifest. Older/alternate API responses may omit it, so absence
    # alone is not a publication failure.
    for name in ("pizza-2.0-preserved.ofn", "pizza-2.0-preserved.ttl"):
        api_digest = assets[name].get("digest")
        if api_digest:
            require(
                api_digest == f"sha256:{actual_digests[name]}",
                f"GitHub asset digest differs for {name}: {api_digest}",
            )

    print(f"Published release verified: {RELEASE_PAGE}")
    print(f"Tag commit: {tag_commit}")
    for name in sorted(actual_digests):
        print(f"{actual_digests[name]}  {name}")
    print("SUCCESS: external release assets, checksums, source binding, and identity anchors verified.")


if __name__ == "__main__":
    main()
