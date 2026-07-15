from __future__ import annotations

import hashlib
import platform
import sys
from dataclasses import replace
from pathlib import Path
from typing import cast

import numpy as np
import pytest
from numpy.typing import NDArray

from xid.sim.g2 import (
    G2Component,
    G2Stream,
    RNGAddress,
    TestRngNamespace,
    load_g2_contract,
)

_TEST_SEED = 1729
_BOOTSTRAP_TEST_SEED = 9191


def _sha256_bytes(values: NDArray[np.generic], dtype: str) -> str:
    return hashlib.sha256(values.astype(dtype, copy=False).tobytes(order="C")).hexdigest()


def _root() -> Path:
    return Path(__file__).parents[1]


def test_rng_address_has_exact_thirteen_field_entropy_order() -> None:
    namespace = TestRngNamespace.from_contract(load_g2_contract(_root()), _TEST_SEED)
    address = namespace.dgp_address(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=7,
        date_index=11,
        component=G2Component.FACTOR,
    )

    assert address.entropy() == (
        1729,
        3,
        2,
        20,
        0,
        0,
        0,
        252,
        7,
        0,
        11,
        1,
        0,
    )
    with pytest.raises(TypeError, match="Python integer"):
        replace(address, master_seed=True)
    with pytest.raises(ValueError, match="nonnegative"):
        replace(address, panel_index=-1)


def test_uint32_field_bound_prevents_seedsequence_word_spill_collisions() -> None:
    contract = load_g2_contract(_root())

    def pack32(words: list[int]) -> int:
        return sum(word << (32 * index) for index, word in enumerate(words))

    colliding_large_master = pack32([1729, 3, 2, 10, 0, 0, 0, 252])
    colliding_large_panel = pack32([3, 2, 10, 1, 0, 0, 252, 7])
    with pytest.raises(ValueError, match=r"smaller than 2\*\*32"):
        RNGAddress(
            colliding_large_master,
            3,
            2,
            10,
            1,
            0,
            0,
            252,
            7,
            0,
            0,
            1,
            0,
        )
    namespace = TestRngNamespace.from_contract(contract, _TEST_SEED)
    with pytest.raises(ValueError, match="uint32-range"):
        namespace.dgp_address(
            stream=G2Stream.RESOURCE_SMOOTH,
            n_dates=252,
            panel_index=colliding_large_panel,
            date_index=0,
            component=G2Component.FACTOR,
        )


@pytest.mark.parametrize(
    ("stream", "n_dates", "expected"),
    [
        (G2Stream.RESOURCE_SMOOTH, 252, (10, 0)),
        (G2Stream.RESOURCE_PAPER, 252, (10, 1)),
        (G2Stream.VALIDATION_SIZE, 252, (20, 0)),
        (G2Stream.VALIDATION_POWER, 252, (21, 0)),
        (G2Stream.VALIDATION_DATE_FRONTIER, 48, (22, 2)),
        (G2Stream.VALIDATION_RECOVERY, 252, (23, 0)),
        (G2Stream.VALIDATION_IID, 252, (24, 0)),
        (G2Stream.VALIDATION_PAPER_RECOVERY, 252, (25, 4)),
        (G2Stream.RESEARCH, 252, (30, 0)),
    ],
)
def test_only_licensed_phase_scenario_assignments_can_draw(
    stream: G2Stream,
    n_dates: int,
    expected: tuple[int, int],
) -> None:
    namespace = TestRngNamespace.from_contract(load_g2_contract(_root()), _TEST_SEED)
    address = namespace.dgp_address(
        stream=stream,
        n_dates=n_dates,
        panel_index=0,
        date_index=0,
        component=G2Component.FACTOR,
    )

    assert (address.phase_id, address.scenario_id) == expected


def test_metadata_only_reliability_frontier_cannot_construct_an_address() -> None:
    namespace = TestRngNamespace.from_contract(load_g2_contract(_root()), _TEST_SEED)

    with pytest.raises(ValueError, match="metadata-only"):
        namespace.dgp_address(
            stream=G2Stream.VALIDATION_RELIABILITY_FRONTIER_METADATA_ONLY,
            n_dates=252,
            panel_index=0,
            date_index=0,
            component=G2Component.FACTOR,
        )


@pytest.mark.parametrize(
    ("stream", "n_dates", "panel_index"),
    [
        (G2Stream.VALIDATION_SIZE, 48, 0),
        (G2Stream.VALIDATION_POWER, 96, 0),
        (G2Stream.VALIDATION_DATE_FRONTIER, 252, 0),
        (G2Stream.VALIDATION_RECOVERY, 252, 100),
        (G2Stream.VALIDATION_IID, 252, 100),
        (G2Stream.VALIDATION_PAPER_RECOVERY, 252, 1),
        (G2Stream.RESEARCH, 252, 1),
    ],
)
def test_stream_specific_date_and_panel_schedule_is_mandatory(
    stream: G2Stream,
    n_dates: int,
    panel_index: int,
) -> None:
    namespace = TestRngNamespace.from_contract(load_g2_contract(_root()), _TEST_SEED)

    with pytest.raises(ValueError, match="n_dates|panel_index"):
        namespace.dgp_address(
            stream=stream,
            n_dates=n_dates,
            panel_index=panel_index,
            date_index=0,
            component=G2Component.FACTOR,
        )


def test_bootstrap_address_binds_parent_pair_and_date_count() -> None:
    namespace = TestRngNamespace.from_contract(
        load_g2_contract(_root()),
        _BOOTSTRAP_TEST_SEED,
    )
    address = namespace.bootstrap_address(
        parent_stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=7,
        replicate_index=17,
    )

    assert address.entropy() == (
        9191,
        3,
        2,
        40,
        0,
        21,
        0,
        252,
        7,
        0,
        0,
        6,
        17,
    )
    namespace.validate_bootstrap_address(address)
    namespace.bootstrap_address(
        parent_stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=7,
        replicate_index=498,
    )
    with pytest.raises(ValueError, match="0 through 498"):
        namespace.bootstrap_address(
            parent_stream=G2Stream.VALIDATION_POWER,
            n_dates=252,
            panel_index=7,
            replicate_index=499,
        )
    with pytest.raises(ValueError, match="bootstrap address"):
        namespace.validate_bootstrap_address(replace(address, date_index=1))


def test_test_fixture_seeds_are_disjoint_from_registered_seeds() -> None:
    contract = load_g2_contract(_root())

    assert {_TEST_SEED, _BOOTSTRAP_TEST_SEED}.isdisjoint(contract.registered_seeds)
    for registered_seed in contract.registered_seeds:
        with pytest.raises(ValueError, match="registered G2 seed"):
            TestRngNamespace.from_contract(contract, registered_seed)
        with pytest.raises(ValueError, match="registered G2 seed"):
            TestRngNamespace(contract=contract, master_seed=registered_seed)


def test_every_draw_rechecks_test_seed_disjointness_before_rng(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, _TEST_SEED)
    address = namespace.dgp_address(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=0,
        component=G2Component.FACTOR,
    )
    object.__setattr__(namespace, "master_seed", contract.registered_seeds[1])

    def forbidden_seed_sequence(*args: object, **kwargs: object) -> None:
        raise AssertionError("RNG was reached after test authority corruption")

    monkeypatch.setattr(np.random, "SeedSequence", forbidden_seed_sequence)
    with pytest.raises(ValueError, match="registered G2 seed"):
        namespace.draw_standard_normal(address)


def test_rng_subclass_dispatch_cannot_replace_validated_entropy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, _TEST_SEED)
    nominal = namespace.dgp_address(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=0,
        component=G2Component.FACTOR,
    )

    class ForgedAddress(RNGAddress):
        def entropy(self) -> tuple[int, ...]:
            values = list(super().entropy())
            values[0] = contract.registered_seeds[1]
            return tuple(values)

    forged = object.__new__(ForgedAddress)
    for field in (
        "master_seed",
        "config_schema_version",
        "rng_key_schema_version",
        "phase_id",
        "scenario_id",
        "parent_phase_id",
        "parent_scenario_id",
        "n_dates",
        "panel_index",
        "cell_key",
        "date_index",
        "component_id",
        "replicate_index",
    ):
        object.__setattr__(forged, field, getattr(nominal, field))

    def forbidden_seed_sequence(*args: object, **kwargs: object) -> None:
        raise AssertionError("subclass-dispatched registered entropy reached SeedSequence")

    monkeypatch.setattr(np.random, "SeedSequence", forbidden_seed_sequence)
    with pytest.raises(TypeError, match="exact RNGAddress"):
        namespace.draw_standard_normal(forged)


def test_namespace_subclass_cannot_override_registered_seed_guard(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = load_g2_contract(_root())

    class ForgedNamespace(TestRngNamespace):
        def _validate_authority(self) -> None:
            return None

    forged = object.__new__(ForgedNamespace)
    object.__setattr__(forged, "contract", contract)
    object.__setattr__(forged, "master_seed", contract.registered_seeds[0])

    def forbidden_seed_sequence(*args: object, **kwargs: object) -> None:
        raise AssertionError("subclassed namespace reached SeedSequence")

    monkeypatch.setattr(np.random, "SeedSequence", forbidden_seed_sequence)
    with pytest.raises(TypeError, match="exact TestRngNamespace"):
        forged.draw_standard_normal(
            RNGAddress(
                contract.registered_seeds[0],
                3,
                2,
                20,
                0,
                0,
                0,
                252,
                0,
                0,
                0,
                1,
                0,
            )
        )


def test_bootstrap_consumes_one_prevalidation_entropy_snapshot(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    contract = load_g2_contract(_root())
    namespace = TestRngNamespace.from_contract(contract, _BOOTSTRAP_TEST_SEED)
    address = namespace.bootstrap_address(
        parent_stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=0,
        replicate_index=0,
    )
    real_full = np.full
    captured: list[tuple[int, ...]] = []

    class SeedProbeReached(RuntimeError):
        pass

    def mutating_full(
        shape: int,
        fill_value: float,
        *,
        dtype: type[np.float64],
    ) -> NDArray[np.float64]:
        object.__setattr__(address, "master_seed", contract.registered_seeds[1])
        return real_full(shape, fill_value, dtype=dtype)

    def capture_seed_sequence(entropy: tuple[int, ...]) -> None:
        captured.append(entropy)
        raise SeedProbeReached

    monkeypatch.setattr(np, "full", mutating_full)
    monkeypatch.setattr(np.random, "SeedSequence", capture_seed_sequence)

    with pytest.raises(SeedProbeReached):
        namespace.draw_bootstrap_weights(address)

    assert captured == [
        (
            _BOOTSTRAP_TEST_SEED,
            *address.entropy()[1:],
        )
    ]


@pytest.mark.parametrize(
    "parent_stream",
    [G2Stream.VALIDATION_RECOVERY, G2Stream.VALIDATION_IID],
)
def test_bootstrap_rejects_streams_without_date_bootstrap(
    parent_stream: G2Stream,
) -> None:
    namespace = TestRngNamespace.from_contract(
        load_g2_contract(_root()),
        _BOOTSTRAP_TEST_SEED,
    )

    with pytest.raises(ValueError, match="date bootstrap"):
        namespace.bootstrap_address(
            parent_stream=parent_stream,
            n_dates=252,
            panel_index=0,
            replicate_index=0,
        )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("config_schema_version", 2),
        ("rng_key_schema_version", 1),
        ("phase_id", 99),
        ("scenario_id", 99),
        ("parent_phase_id", 1),
        ("parent_scenario_id", 1),
        ("n_dates", 48),
        ("panel_index", 100),
        ("date_index", 252),
        ("cell_key", 1),
        ("component_id", 0),
        ("component_id", 6),
        ("replicate_index", 1),
    ],
)
def test_mutated_dgp_address_fails_before_seedsequence(
    field: str,
    value: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    namespace = TestRngNamespace.from_contract(load_g2_contract(_root()), _TEST_SEED)
    address = namespace.dgp_address(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=7,
        date_index=11,
        component=G2Component.FACTOR,
    )
    object.__setattr__(address, field, value)

    def forbidden_seed_sequence(*args: object, **kwargs: object) -> None:
        raise AssertionError("RNG was reached with a mutated DGP address")

    monkeypatch.setattr(np.random, "SeedSequence", forbidden_seed_sequence)
    with pytest.raises((TypeError, ValueError)):
        namespace.draw_standard_normal(address)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("config_schema_version", 2),
        ("rng_key_schema_version", 1),
        ("phase_id", 41),
        ("scenario_id", 1),
        ("parent_phase_id", 99),
        ("parent_scenario_id", 99),
        ("n_dates", 96),
        ("panel_index", 100),
        ("cell_key", 1),
        ("date_index", 1),
        ("component_id", 5),
        ("replicate_index", 499),
    ],
)
def test_mutated_bootstrap_address_fails_before_seedsequence(
    field: str,
    value: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    namespace = TestRngNamespace.from_contract(
        load_g2_contract(_root()),
        _BOOTSTRAP_TEST_SEED,
    )
    address = namespace.bootstrap_address(
        parent_stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=7,
        replicate_index=17,
    )
    object.__setattr__(address, field, value)

    def forbidden_seed_sequence(*args: object, **kwargs: object) -> None:
        raise AssertionError("RNG was reached with a mutated bootstrap address")

    monkeypatch.setattr(np.random, "SeedSequence", forbidden_seed_sequence)
    with pytest.raises((TypeError, ValueError)):
        namespace.draw_bootstrap_weights(address)


@pytest.mark.parametrize(
    ("component", "expected_hash"),
    [
        (G2Component.FACTOR, "30a773aa28fb77cc545ad16862447c641f018e5293d2a3bac6c4d2407c641747"),
        (
            G2Component.FLOW_INNOVATION,
            "30f87c3b6ccf31deed2c0bb52bd60199fd4cc2427f3f3ab9771064b3091abde9",
        ),
        (
            G2Component.RETURN_INNOVATION,
            "e709ae59d68183c82c83699a340f2b60646af1492306668e27087538a293520b",
        ),
        (
            G2Component.LEVEL_NOISE,
            "593fe9b8e8f102bce0e58303a49b26cd713121c38e2219c9005ebaaf1c074091",
        ),
        (
            G2Component.PROXY_NOISE,
            "28d3f3b5b9e3fe24734d84456e3bbc1304394012fde1dca707c1f6ecbaac8243",
        ),
    ],
)
def test_standard_normal_component_known_answers(
    component: G2Component,
    expected_hash: str,
) -> None:
    namespace = TestRngNamespace.from_contract(load_g2_contract(_root()), _TEST_SEED)
    address = namespace.dgp_address(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=7,
        date_index=11,
        component=component,
    )

    values = namespace.draw_standard_normal(address)

    assert values.shape == namespace.contract.draw_shape(component)
    assert values.dtype == np.float64
    assert values.flags.c_contiguous
    actual_hash = _sha256_bytes(values, "<f8")
    if actual_hash != expected_hash:
        flat = values.reshape(-1)
        chunks = tuple(
            _sha256_bytes(flat[start : start + 1_000], "<f8")
            for start in range(0, flat.size, 1_000)
        )
        raw = np.random.PCG64DXSM(np.random.SeedSequence(address.entropy())).random_raw(150_000)
        pytest.fail(
            "standard_normal known-answer mismatch; "
            f"python={sys.version.split()[0]!r}, numpy={np.__version__!r}, "
            f"platform={platform.platform()!r}, component={component.name!r}, "
            f"expected={expected_hash!r}, actual={actual_hash!r}, "
            f"raw150k={_sha256_bytes(raw, '<u8')!r}, "
            f"first8_hex={tuple(float(value).hex() for value in flat[:8])!r}, "
            f"chunk1000={chunks!r}, "
            "indices60000_60999_hex="
            f"{tuple(float(value).hex() for value in flat[60_000:61_000])!r}"
        )
    if component is G2Component.FACTOR:
        np.testing.assert_array_equal(
            values[:6],
            np.asarray(
                [
                    -0.7880912772725455,
                    1.0062457415428372,
                    0.5680305156227258,
                    -0.1474744116452011,
                    -0.05575006536799127,
                    -0.6856120070028286,
                ],
                dtype=np.float64,
            ),
        )


def test_pcg64dxsm_level_noise_raw_known_answer() -> None:
    namespace = TestRngNamespace.from_contract(load_g2_contract(_root()), _TEST_SEED)
    address = namespace.dgp_address(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=7,
        date_index=11,
        component=G2Component.LEVEL_NOISE,
    )
    raw = np.random.PCG64DXSM(np.random.SeedSequence(address.entropy())).random_raw(150_000)

    assert _sha256_bytes(raw, "<u8") == (
        "4b513e5dee9968d985cca87af4640a9e466238afedcf6bece87784ab56ccfdf4"
    )


def test_multinomial_bootstrap_known_answer() -> None:
    namespace = TestRngNamespace.from_contract(
        load_g2_contract(_root()),
        _BOOTSTRAP_TEST_SEED,
    )
    address = namespace.bootstrap_address(
        parent_stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=7,
        replicate_index=17,
    )

    weights = namespace.draw_bootstrap_weights(address)

    assert weights.dtype == np.float64
    assert weights.flags.c_contiguous
    assert float(np.sum(weights)) == 252.0
    assert int(np.count_nonzero(weights)) == 150
    np.testing.assert_array_equal(
        weights[:30],
        np.asarray(
            [
                0,
                2,
                4,
                1,
                1,
                1,
                0,
                1,
                0,
                4,
                4,
                1,
                1,
                0,
                2,
                0,
                1,
                2,
                1,
                2,
                0,
                0,
                1,
                1,
                0,
                0,
                1,
                0,
                3,
                0,
            ],
            dtype=np.float64,
        ),
    )
    assert hashlib.sha256(weights.astype("<f8", copy=False).tobytes(order="C")).hexdigest() == (
        "e669caa93d109760389e39b44aa5d20363fa5248cfa37b18651f1b2271e8ff1a"
    )


def test_representative_active_namespace_states_are_unique() -> None:
    namespace = TestRngNamespace.from_contract(load_g2_contract(_root()), _TEST_SEED)
    streams_and_dates = (
        (G2Stream.RESOURCE_SMOOTH, 252),
        (G2Stream.RESOURCE_PAPER, 252),
        (G2Stream.VALIDATION_SIZE, 252),
        (G2Stream.VALIDATION_POWER, 252),
        (G2Stream.VALIDATION_DATE_FRONTIER, 48),
        (G2Stream.VALIDATION_DATE_FRONTIER, 96),
        (G2Stream.VALIDATION_RECOVERY, 252),
        (G2Stream.VALIDATION_IID, 252),
        (G2Stream.VALIDATION_PAPER_RECOVERY, 252),
        (G2Stream.RESEARCH, 252),
    )
    addresses = [
        namespace.dgp_address(
            stream=stream,
            n_dates=n_dates,
            panel_index=0,
            date_index=0,
            component=component,
        )
        for stream, n_dates in streams_and_dates
        for component in tuple(G2Component)[:-1]
    ]
    addresses.extend(
        namespace.bootstrap_address(
            parent_stream=stream,
            n_dates=n_dates,
            panel_index=0,
            replicate_index=0,
        )
        for stream, n_dates in streams_and_dates
        if stream not in (G2Stream.VALIDATION_RECOVERY, G2Stream.VALIDATION_IID)
    )
    entropy = [address.entropy() for address in addresses]
    states = [
        np.random.SeedSequence(address).generate_state(4).astype("<u4").tobytes(order="C")
        for address in entropy
    ]

    assert len(entropy) == len(set(entropy))
    assert len(states) == len(set(states))


def test_standard_normal_uses_the_exact_one_call_contract(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    namespace = TestRngNamespace.from_contract(load_g2_contract(_root()), _TEST_SEED)
    address = namespace.dgp_address(
        stream=G2Stream.VALIDATION_SIZE,
        n_dates=252,
        panel_index=0,
        date_index=0,
        component=G2Component.FACTOR,
    )
    events: list[tuple[str, object]] = []
    seed_token = object()
    bit_generator_token = object()

    def fake_seed_sequence(entropy: object) -> object:
        events.append(("SeedSequence", entropy))
        return seed_token

    def fake_pcg64dxsm(seed_sequence: object) -> object:
        events.append(("PCG64DXSM", seed_sequence))
        return bit_generator_token

    class FakeGenerator:
        def standard_normal(
            self,
            *,
            size: tuple[int, ...],
            dtype: type[np.float64],
        ) -> NDArray[np.float64]:
            events.append(("standard_normal", (size, dtype)))
            return np.zeros(size, dtype=dtype)

        def normal(self, *args: object, **kwargs: object) -> None:
            raise AssertionError("forbidden Generator.normal call")

    def fake_generator(bit_generator: object) -> FakeGenerator:
        events.append(("Generator", bit_generator))
        return FakeGenerator()

    monkeypatch.setattr(np.random, "SeedSequence", fake_seed_sequence)
    monkeypatch.setattr(np.random, "PCG64DXSM", fake_pcg64dxsm)
    monkeypatch.setattr(np.random, "Generator", fake_generator)

    values = namespace.draw_standard_normal(address)

    assert values.shape == (330,)
    assert events == [
        ("SeedSequence", address.entropy()),
        ("PCG64DXSM", seed_token),
        ("Generator", bit_generator_token),
        ("standard_normal", ((330,), np.float64)),
    ]


def test_bootstrap_uses_exact_full_and_one_multinomial_call(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    namespace = TestRngNamespace.from_contract(
        load_g2_contract(_root()),
        _BOOTSTRAP_TEST_SEED,
    )
    address = namespace.bootstrap_address(
        parent_stream=G2Stream.VALIDATION_POWER,
        n_dates=252,
        panel_index=0,
        replicate_index=0,
    )
    events: list[tuple[str, object]] = []
    seed_token = object()
    bit_generator_token = object()
    real_full = np.full

    def fake_full(
        shape: int,
        fill_value: float,
        *,
        dtype: type[np.float64],
    ) -> NDArray[np.float64]:
        events.append(("full", (shape, fill_value, dtype)))
        return real_full(shape, fill_value, dtype=dtype)

    def fake_seed_sequence(entropy: object) -> object:
        events.append(("SeedSequence", entropy))
        return seed_token

    def fake_pcg64dxsm(seed_sequence: object) -> object:
        events.append(("PCG64DXSM", seed_sequence))
        return bit_generator_token

    class FakeGenerator:
        def multinomial(
            self,
            *,
            n: int,
            pvals: NDArray[np.float64],
            size: None,
        ) -> NDArray[np.int64]:
            events.append(("multinomial", (n, pvals.copy(), size)))
            return np.ones(n, dtype=np.int64)

    def fake_generator(bit_generator: object) -> FakeGenerator:
        events.append(("Generator", bit_generator))
        return FakeGenerator()

    monkeypatch.setattr(np, "full", fake_full)
    monkeypatch.setattr(np.random, "SeedSequence", fake_seed_sequence)
    monkeypatch.setattr(np.random, "PCG64DXSM", fake_pcg64dxsm)
    monkeypatch.setattr(np.random, "Generator", fake_generator)

    weights = namespace.draw_bootstrap_weights(address)

    assert np.array_equal(weights, np.ones(252, dtype=np.float64))
    assert events[:4] == [
        ("full", (252, 1.0 / 252.0, np.float64)),
        ("SeedSequence", address.entropy()),
        ("PCG64DXSM", seed_token),
        ("Generator", bit_generator_token),
    ]
    name, payload = events[4]
    assert name == "multinomial"
    n, pvals, size = cast(tuple[int, NDArray[np.float64], None], payload)
    assert n == 252
    assert size is None
    np.testing.assert_array_equal(
        pvals,
        real_full(252, 1.0 / 252.0, dtype=np.float64),
    )
    assert len(events) == 5
