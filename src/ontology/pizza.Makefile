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
