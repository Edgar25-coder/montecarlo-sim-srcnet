from dataclasses import replace

from srcnet_mc.optimization.deterministic import solve, synthetic_fixture
from srcnet_mc.optimization.validation import validate


def test_synthetic_exact_reference_is_feasible() -> None:
    fixture = synthetic_fixture()
    solution = solve(fixture)
    assert solution.status == "optimal"
    assert set(solution.replica_storage.values()) == {"store-a", "store-b"}
    assert validate(fixture, solution) == []


def test_independent_validator_detects_processing_violation() -> None:
    fixture = synthetic_fixture()
    solution = solve(fixture)
    invalid = solution.__class__(**{**solution.__dict__, "processing_loads": {**solution.processing_loads, "t0": 99.0}})
    assert "processing load is inconsistent at t0" in validate(fixture, invalid)
    assert "processing capacity is exceeded at t0" in validate(fixture, invalid)


def test_independent_validator_detects_flow_conservation_violation() -> None:
    fixture = synthetic_fixture()
    solution = solve(fixture)
    broken_flows = {**solution.stage0_flow, ("sdp", "t0"): 1.0}
    invalid = replace(solution, stage0_flow=broken_flows)
    assert "stage-0 flow conservation fails at sdp" in validate(fixture, invalid)
