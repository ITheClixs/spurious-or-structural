UV ?= uv
DEMO_CONFIG ?= configs/demo.toml
G1_THREAD_ENV = BLIS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
override G2_RECOVERY_THREAD_ENV := BLIS_NUM_THREADS=1 MKL_NUM_THREADS=1 NUMEXPR_NUM_THREADS=1 OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1
override G2_RECOVERY_BOOTSTRAP_CACHE := data/g2_checkpoint_recovery/scratch/bootstrap-pycache

.PHONY: demo g1-benchmark g2-checkpoint-recovery lint format-check typecheck test verify-generated check all data features mc estimate falsify paper

demo:
	$(UV) run --locked python -m xid.demo --config $(DEMO_CONFIG) --root .

g1-benchmark:
	env $(G1_THREAD_ENV) $(UV) run --locked python -m xid.g1 benchmark --config configs/g1.toml --root .

mc:
	env $(G1_THREAD_ENV) caffeinate -i $(UV) run --locked python -m xid.g1 run --config configs/g1.toml --root .

g2-checkpoint-recovery:
	test ! -L data
	test ! -L data/g2_checkpoint_recovery
	test ! -L data/g2_checkpoint_recovery/scratch
	test ! -L data/g2_checkpoint_recovery/scratch/bootstrap-pycache
	mkdir -p $(G2_RECOVERY_BOOTSTRAP_CACHE)
	test -z "$$(find $(G2_RECOVERY_BOOTSTRAP_CACHE) -mindepth 1 -print -quit)"
	env $(G2_RECOVERY_THREAD_ENV) XID_G2_RECOVERY_MAKE_TARGET=g2-checkpoint-recovery-v1 PYTHONPYCACHEPREFIX=$(abspath $(G2_RECOVERY_BOOTSTRAP_CACHE)) PYTHONDONTWRITEBYTECODE=1 $(UV) run --locked python -B -m xid.g2_checkpoint_recovery _supervisor

lint:
	$(UV) run --locked --extra dev ruff check .

format-check:
	$(UV) run --locked --extra dev ruff format --check .

typecheck:
	$(UV) run --locked --extra dev mypy

test:
	$(UV) run --locked --extra dev pytest -q

verify-generated:
	git diff --exit-code -- results/demo results/g1

check: lint format-check typecheck test demo verify-generated

all: check

data features estimate falsify paper:
	@echo "$@ is gate-locked; read STATE.md before running future research phases."
	@exit 2

exhibits:
	uv run --locked python -m xid.exhibits --out docs/pre_results/generated
	git diff --exit-code -- docs/pre_results/generated
