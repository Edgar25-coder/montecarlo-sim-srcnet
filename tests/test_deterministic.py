from dataclasses import replace

from srcnet_mc.domain import Arc, Node, Topology
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


def test_independent_validator_detects_inactive_arc_and_congestion_violation() -> None:
    fixture = synthetic_fixture()
    solution = solve(fixture)
    edge = ("sdp", "t0")
    invalid = replace(
        solution,
        active_arcs=frozenset(item for item in solution.active_arcs if item != edge),
        congestion={**solution.congestion, edge: 0.0},
    )
    violations = validate(fixture, invalid)
    assert "positive flow uses an inactive arc" in violations
    assert "congestion epigraph is violated" in violations


def test_independent_validator_detects_unavailable_arc_and_storage_overflow() -> None:
    fixture = synthetic_fixture()
    solution = solve(fixture)
    unavailable = tuple(
        Arc(arc.tail, arc.head, arc.capacity_pb_per_day, available=False, failure_exposure=arc.failure_exposure)
        if (arc.tail, arc.head) == ("sdp", "t0") else arc
        for arc in fixture.topology.arcs
    )
    undersized_nodes = tuple(
        Node(
            node.identifier, node.role, node.processing_capacity_pb_per_day,
            node.temporary_buffer_pb, persistent_capacity_pb=1.0,
            parent_se=node.parent_se, src=node.src,
        ) if node.identifier == "store-a" else node
        for node in fixture.topology.nodes
    )
    invalid_fixture = replace(fixture, topology=Topology(undersized_nodes, unavailable))
    violations = validate(invalid_fixture, solution)
    assert "positive flow uses an unavailable arc" in violations
    assert "replica exceeds persistent capacity" in violations


def test_independent_validator_detects_parent_and_src_diversity_violation() -> None:
    fixture = synthetic_fixture()
    solution = solve(fixture)
    invalid = replace(solution, replica_storage={"r1": "store-a", "r2": "store-a"})
    violations = validate(fixture, invalid)
    assert "replicas share a storage node" in violations
    assert "replicas share a non-T0 parent" in violations
    assert "replicas share an SRC" in violations
