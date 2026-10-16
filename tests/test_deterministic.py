from srcnet_mc.optimization.deterministic import solve, synthetic_fixture
from srcnet_mc.optimization.validation import validate


def test_synthetic_exact_reference_is_feasible() -> None:
    fixture = synthetic_fixture()
    solution = solve(fixture)
    assert solution.status == "optimal"
    assert set(solution.replica_storage.values()) == {"store-a", "store-b"}
    assert validate(fixture, solution) == []
