#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/../.." && pwd)"
WORK="${HERE}/.work"
RESULTS="${HERE}/results"
SOURCE="${ROOT}/src/ontology/pizza-edit.owl"
OAK_INPUT="${WORK}/pizza-edit.ofn"

mkdir -p "${WORK}" "${RESULTS}"
rm -f "${RESULTS}"/*

# The preserved ODK editor file is OWL Functional Syntax but retains the
# historical .owl editor filename. OAK selects local OWL parsers by descriptor
# / extension, so use a byte-identical temporary .ofn file as an explicit
# syntax hint without creating another semantic source artifact in the repo.
cp "${SOURCE}" "${OAK_INPUT}"
cmp "${SOURCE}" "${OAK_INPUT}"

printf '\n1/4 Python OAK access example...\n'
python "${HERE}/access_pizza.py" "${OAK_INPUT}" | tee "${RESULTS}/python-access.txt"

printf '\n2/4 OAK CLI entity lookup...\n'
runoak -i "${OAK_INPUT}" info "American Hot" | tee "${RESULTS}/info.txt"
grep -qi "American.*Hot" "${RESULTS}/info.txt"

printf '\n3/4 OAK CLI relationship projection...\n'
runoak -i "${OAK_INPUT}" relationships "American Hot" | tee "${RESULTS}/relationships.txt"
grep -q "JalapenoPepperTopping" "${RESULTS}/relationships.txt"

printf '\n4/4 OAK CLI is-a traversal...\n'
runoak -i "${OAK_INPUT}" ancestors -p i "American Hot" | tee "${RESULTS}/ancestors.txt"
grep -q "NamedPizza" "${RESULTS}/ancestors.txt"

printf '\nSUCCESS: OAK CLI and Python examples access the repository-owned Pizza semantic model.\n'
