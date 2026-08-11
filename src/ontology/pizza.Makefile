## Customize Makefile settings for pizza

# Pizza 2.0 intentionally contains two unsatisfiable classes used
# as examples in the Protégé OWL tutorial:
#   - CheeseyVegetableTopping
#   - IceCream
#
# Preserve these in the migration baseline, but fail if reasoning
# produces any different result.

.RECIPEPREFIX := >

.PHONY: reason_test
reason_test: $(EDIT_PREPROCESSED)
>@set -eu; \
  log=$$(mktemp); \
  if $(ROBOT) reason --input $< --reasoner $(REASONER) \
      --equivalent-classes-allowed asserted-only \
      --exclude-tautologies structural \
      --output test.owl >"$$log" 2>&1; then \
    cat "$$log"; \
    rm -f "$$log" test.owl; \
    echo "ERROR: Expected the two intentional Pizza 2.0 unsatisfiable classes."; \
    exit 1; \
  fi; \
  count=$$(grep -c 'unsatisfiable:' "$$log" || true); \
  if [ "$$count" -ne 2 ] || \
     ! grep -q 'pizza.owl#CheeseyVegetableTopping' "$$log" || \
     ! grep -q 'pizza.owl#IceCream' "$$log"; then \
    cat "$$log"; \
    rm -f "$$log" test.owl; \
    echo "ERROR: Unexpected unsatisfiable classes."; \
    exit 1; \
  fi; \
  cat "$$log"; \
  rm -f "$$log" test.owl; \
  echo "Expected Pizza 2.0 unsatisfiable classes confirmed."

# Preservation releases are repository releases, not new semantic Pizza
# ontology versions. The default generated ODK release targets rewrite
# ontology identity using OBO-style URIBASE/ONTBASE and date versions, so
# they are deliberately not used for the preservation artifacts below.

PRESERVATION_RELEASE_DIR ?= ../../target/preservation-release
PRESERVATION_ONTOLOGY := $(PRESERVATION_RELEASE_DIR)/pizza-2.0-preserved.ofn
PRESERVATION_TURTLE := $(PRESERVATION_RELEASE_DIR)/pizza-2.0-preserved.ttl
PRESERVATION_DIFF := $(PRESERVATION_RELEASE_DIR)/pizza-2.0-preserved.diff

.PHONY: preservation_identity_test
preservation_identity_test: $(SRC)
>@set -eu; \
  grep -Fq 'Ontology(<http://www.co-ode.org/ontologies/pizza>' $< || { \
    echo 'ERROR: historical Pizza ontology IRI is not preserved.'; exit 1; }; \
  grep -Fq '<http://www.co-ode.org/ontologies/pizza/2.0.0>' $< || { \
    echo 'ERROR: historical Pizza 2.0 version IRI is not preserved.'; exit 1; }; \
  grep -Fq 'Annotation(owl:versionInfo "2.0")' $< || { \
    echo 'ERROR: historical Pizza owl:versionInfo 2.0 is not preserved.'; exit 1; }; \
  grep -Fq 'http://www.co-ode.org/ontologies/pizza/pizza.owl#' $< || { \
    echo 'ERROR: historical Pizza entity namespace is not present.'; exit 1; }; \
  if grep -Fq 'http://purl.obolibrary.org/obo/pizza' $<; then \
    echo 'ERROR: unowned OBO Pizza release IRI found in preservation source.'; exit 1; \
  fi; \
  echo 'Historical Pizza 2.0 semantic identity confirmed.'

# Add the preservation identity invariant to the normal ODK QC suite.
test: preservation_identity_test

.PHONY: preservation_distribution_test
preservation_distribution_test: preservation_identity_test
>@set -eu; \
  mkdir -p $(PRESERVATION_RELEASE_DIR); \
  $(ROBOT) convert --input $(SRC) --format ttl --output $(PRESERVATION_TURTLE); \
  $(ROBOT) diff --left $(SRC) --right $(PRESERVATION_TURTLE) --output $(PRESERVATION_DIFF); \
  if [ -s $(PRESERVATION_DIFF) ]; then \
    cat $(PRESERVATION_DIFF); \
    echo 'ERROR: Turtle distribution is not semantically equivalent to the preserved source ontology.'; \
    exit 1; \
  fi; \
  grep -Fq 'http://www.co-ode.org/ontologies/pizza' $(PRESERVATION_TURTLE) || { \
    echo 'ERROR: historical Pizza ontology identity is missing from Turtle distribution.'; exit 1; }; \
  grep -Fq 'http://www.co-ode.org/ontologies/pizza/2.0.0' $(PRESERVATION_TURTLE) || { \
    echo 'ERROR: historical Pizza 2.0 version IRI is missing from Turtle distribution.'; exit 1; }; \
  grep -Fq 'http://www.co-ode.org/ontologies/pizza/pizza.owl#' $(PRESERVATION_TURTLE) || { \
    echo 'ERROR: historical Pizza entity namespace is missing from Turtle distribution.'; exit 1; }; \
  if grep -Fq 'http://purl.obolibrary.org/obo/pizza' $(PRESERVATION_TURTLE); then \
    echo 'ERROR: unowned OBO Pizza release IRI found in Turtle distribution.'; exit 1; \
  fi; \
  rm -f $(PRESERVATION_DIFF); \
  echo 'Preservation-safe Turtle distribution is graph-equivalent to the source ontology.'

.PHONY: preservation_release_artifact
preservation_release_artifact: preservation_distribution_test
>@set -eu; \
  mkdir -p $(PRESERVATION_RELEASE_DIR); \
  cp $(SRC) $(PRESERVATION_ONTOLOGY); \
  cmp -s $(SRC) $(PRESERVATION_ONTOLOGY) || { \
    echo 'ERROR: preservation release artifact differs from editor baseline.'; exit 1; }; \
  cd $(PRESERVATION_RELEASE_DIR) && \
    sha256sum $$(basename $(PRESERVATION_ONTOLOGY)) $$(basename $(PRESERVATION_TURTLE)) > SHA256SUMS; \
  echo 'Created preservation-safe semantic artifacts:'; \
  echo '  $(PRESERVATION_ONTOLOGY)'; \
  echo '  $(PRESERVATION_TURTLE)'; \
  echo '  $(PRESERVATION_RELEASE_DIR)/SHA256SUMS'
