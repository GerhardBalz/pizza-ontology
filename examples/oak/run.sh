#!/usr/bin/env bash
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/../.." && pwd)"
WORK="${HERE}/.work"
RESULTS="${HERE}/results"
SOURCE="${ROOT}/src/ontology/pizza-edit.owl"
OAK_INPUT="${WORK}/pizza-edit.ofn"
PIZZA_NS="http://www.co-ode.org/ontologies/pizza/pizza.owl#"

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
runoak --prefix "pizza=${PIZZA_NS}" -l en -i "${OAK_INPUT}" info pizza:AmericanHot | tee "${RESULTS}/info.txt"
grep -qi "American.*Hot" "${RESULTS}/info.txt"

printf '\n3/4 OAK CLI relationship projection...\n'
runoak --prefix "pizza=${PIZZA_NS}" -l en -i "${OAK_INPUT}" relationships pizza:AmericanHot | tee "${RESULTS}/relationships.txt"
grep -q "pizza:JalapenoPepperTopping" "${RESULTS}/relationships.txt"

printf '\n4/4 OAK CLI is-a traversal...\n'
runoak --prefix "pizza=${PIZZA_NS}" -l en -i "${OAK_INPUT}" ancestors -p i pizza:AmericanHot | tee "${RESULTS}/ancestors.txt"
grep -q "pizza:NamedPizza" "${RESULTS}/ancestors.txt"

printf '\nSUCCESS: OAK CLI and Python examples access the repository-owned Pizza semantic model.\n'
