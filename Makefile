UV ?= uv
DEMO_CONFIG ?= configs/demo.toml

.PHONY: demo lint format-check typecheck test verify-generated check all data features mc estimate falsify paper

demo:
	$(UV) run --locked python -m xid.demo --config $(DEMO_CONFIG) --root .

lint:
	$(UV) run --locked --extra dev ruff check .

format-check:
	$(UV) run --locked --extra dev ruff format --check .

typecheck:
	$(UV) run --locked --extra dev mypy

test:
	$(UV) run --locked --extra dev pytest -q

verify-generated:
	git diff --exit-code -- results/demo

check: lint format-check typecheck test demo verify-generated

all: check

data features mc estimate falsify paper:
	@echo "$@ is gate-locked; read STATE.md before running future research phases."
	@exit 2
