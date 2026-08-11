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

printf '\n1/6 Minimal Python OAK access slice...\n'
python "${HERE}/access_pizza.py" "${OAK_INPUT}" | tee "${RESULTS}/python-access.txt"

printf '\n2/6 Broader Python OAK exploration/query example...\n'
python "${HERE}/query_pizza.py" "${OAK_INPUT}" | tee "${RESULTS}/python-query.txt"
grep -q "broader OAK exploration verified" "${RESULTS}/python-query.txt"

printf '\n3/6 OAK CLI entity lookup...\n'
runoak --prefix "pizza=${PIZZA_NS}" -i "${OAK_INPUT}" info pizza:AmericanHot | tee "${RESULTS}/info.txt"
grep -q "pizza:AmericanHot" "${RESULTS}/info.txt"

printf '\n4/6 OAK CLI relationship projection...\n'
runoak --prefix "pizza=${PIZZA_NS}" -i "${OAK_INPUT}" relationships pizza:AmericanHot | tee "${RESULTS}/relationships.txt"
grep -q "pizza:JalapenoPepperTopping" "${RESULTS}/relationships.txt"

printf '\n5/6 OAK CLI is-a ancestor traversal...\n'
runoak --prefix "pizza=${PIZZA_NS}" -i "${OAK_INPUT}" ancestors -p i pizza:AmericanHot | tee "${RESULTS}/ancestors.txt"
grep -q "pizza:NamedPizza" "${RESULTS}/ancestors.txt"

printf '\n6/6 OAK CLI is-a descendant traversal...\n'
runoak --prefix "pizza=${PIZZA_NS}" -i "${OAK_INPUT}" descendants -p i pizza:NamedPizza | tee "${RESULTS}/descendants.txt"
grep -q "pizza:AmericanHot" "${RESULTS}/descendants.txt"
grep -q "pizza:Margherita" "${RESULTS}/descendants.txt"

printf '\nSUCCESS: OAK Python and CLI examples access labels, relationships, ancestor/descendant graph traversal, and explicit adapter capability boundaries over the repository-owned Pizza semantic model.\n'
