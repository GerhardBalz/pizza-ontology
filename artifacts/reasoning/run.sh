#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/../.." && pwd)"
WORK="${HERE}/.work"
RESULTS="${HERE}/results"
VERIFY="${RESULTS}/verification"
SOURCE="${ROOT}/src/ontology/pizza-edit.owl"
EXPECTED_SOURCE_BLOB="397492e484de5560f8a7e048ce8999b707d94388"

ROBOT_VERSION="${ROBOT_VERSION:-1.9.10}"
ROBOT_JAR="${ROBOT_JAR:-${WORK}/robot.jar}"
ROBOT_URL="https://github.com/ontodev/robot/releases/download/v${ROBOT_VERSION}/robot.jar"

mkdir -p "${WORK}" "${RESULTS}" "${VERIFY}"
rm -f "${RESULTS}/reasoned.owl" "${RESULTS}/explanation.md"
rm -f "${VERIFY}"/* 2>/dev/null || true

if [[ ! -f "${SOURCE}" ]]; then
  echo "Pizza source not found: ${SOURCE}" >&2
  exit 1
fi

ACTUAL_SOURCE_BLOB="$(git -C "${ROOT}" hash-object "${SOURCE}")"
if [[ "${ACTUAL_SOURCE_BLOB}" != "${EXPECTED_SOURCE_BLOB}" ]]; then
  echo "Pizza source blob changed." >&2
  echo "Expected: ${EXPECTED_SOURCE_BLOB}" >&2
  echo "Actual:   ${ACTUAL_SOURCE_BLOB}" >&2
  echo "Review and re-establish reasoning-module provenance before updating the pinned source blob." >&2
  exit 1
fi

if [[ ! -f "${ROBOT_JAR}" ]]; then
  echo "Downloading ROBOT ${ROBOT_VERSION}..."
  curl --fail --location --silent --show-error "${ROBOT_URL}" --output "${ROBOT_JAR}"
fi

ROBOT=(java -jar "${ROBOT_JAR}")

printf '\n1/4 Verify the classification is not asserted...\n'
"${ROBOT[@]}" verify \
  --input "${HERE}/spicy-pizza.ofn" \
  --queries "${HERE}/verify-not-asserted.sparql" \
  --output-dir "${VERIFY}"

printf '\n2/4 Classify the coherent module with HermiT...\n'
"${ROBOT[@]}" reason \
  --input "${HERE}/spicy-pizza.ofn" \
  --reasoner hermit \
  --include-indirect true \
  --annotate-inferred-axioms true \
  --output "${RESULTS}/reasoned.owl"

printf '\n3/4 Verify the inferred classification...\n'
"${ROBOT[@]}" verify \
  --input "${RESULTS}/reasoned.owl" \
  --queries "${HERE}/verify-spicy.sparql" \
  --output-dir "${VERIFY}"

printf '\n4/4 Explain the inferred classification...\n'
"${ROBOT[@]}" explain \
  --input "${HERE}/spicy-pizza.ofn" \
  --reasoner hermit \
  --axiom "'American Hot' SubClassOf 'Spicy Pizza'" \
  --explanation "${RESULTS}/explanation.md"

printf '\nSUCCESS: canonical Pizza reasoning module is coherent and the expected classification is inferred.\n'
printf 'Asserted:   AmericanHot SubClassOf SpicyPizza  no\n'
printf 'Inferred:   AmericanHot SubClassOf SpicyPizza  yes\n'
printf 'Source:     git-blob:%s\n' "${EXPECTED_SOURCE_BLOB}"
printf 'Reasoned:   %s\n' "${RESULTS}/reasoned.owl"
printf 'Explanation:%s\n' "${RESULTS}/explanation.md"
