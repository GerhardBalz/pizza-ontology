#!/usr/bin/env bash
set -euo pipefail

RELEASE_DIR="${1:-target/preservation-release}"

expected=(
  "pizza-2.0-preserved.ofn"
  "pizza-2.0-preserved.ttl"
  "SHA256SUMS"
)

for asset in "${expected[@]}"; do
  test -s "${RELEASE_DIR}/${asset}" || {
    echo "ERROR: required release asset missing or empty: ${asset}"
    exit 1
  }
done

mapfile -t actual < <(find "${RELEASE_DIR}" -maxdepth 1 -type f -printf '%f\n' | sort)
mapfile -t wanted < <(printf '%s\n' "${expected[@]}" | sort)

if [[ "${#actual[@]}" -ne "${#wanted[@]}" ]] || \
   [[ "$(printf '%s\n' "${actual[@]}")" != "$(printf '%s\n' "${wanted[@]}")" ]]; then
  echo "ERROR: release bundle must contain exactly the governed asset set."
  echo "Expected:"
  printf '  %s\n' "${wanted[@]}"
  echo "Actual:"
  printf '  %s\n' "${actual[@]}"
  exit 1
fi

test "$(wc -l < "${RELEASE_DIR}/SHA256SUMS")" -eq 2 || {
  echo "ERROR: SHA256SUMS must contain exactly two ontology-distribution entries."
  exit 1
}

(
  cd "${RELEASE_DIR}"
  sha256sum -c SHA256SUMS
)

for distribution in pizza-2.0-preserved.ofn pizza-2.0-preserved.ttl; do
  grep -Fq " ${distribution}" "${RELEASE_DIR}/SHA256SUMS" || {
    echo "ERROR: SHA256SUMS does not cover ${distribution}."
    exit 1
  }
done

echo "Governed preservation release bundle verified:"
ls -l "${RELEASE_DIR}"
cat "${RELEASE_DIR}/SHA256SUMS"
