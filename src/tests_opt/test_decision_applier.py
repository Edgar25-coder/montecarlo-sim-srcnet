from types import SimpleNamespace

from srcnet_mc.optimization.decision_applier import (
    DecisionApplier,
)
from srcnet_mc.optimization.solution import (
    OptimizationSolution,
    PlacementDecision,
    ReplicaDecision,
)


def _build_world():

    instance = SimpleNamespace(
        dataset=SimpleNamespace(
            volume_pb=2.0,
        ),
        stored_at={"T0"},
    )

    world = SimpleNamespace(
        datasets={"D1": instance},
        storage_occupancy={
            "T0": 2.0,
            "SRC1": 0.0,
            "SRC2": 0.0,
        },
    )

    return world, instance


def test_applies_placement_and_replica_updates_occupancy():

    world, instance = _build_world()

    solution = OptimizationSolution(
        objective_value=0.0,
        placements=[
            PlacementDecision(
                dataset_id="D1",
                destination_node="SRC1",
            ),
        ],
        replicas=[
            ReplicaDecision(
                dataset_id="D1",
                node="SRC2",
            ),
            ReplicaDecision(
                dataset_id="D1",
                node="SRC1",
            ),
            ReplicaDecision(
                dataset_id="unknown",
                node="SRC2",
            ),
        ],
        is_feasible=True,
        is_optimal=True,
    )

    DecisionApplier().apply(
        world,
        solution,
    )

    assert instance.stored_at == {"SRC1", "SRC2"}
    assert world.storage_occupancy == {
        "T0": 0.0,
        "SRC1": 2.0,
        "SRC2": 2.0,
    }


def test_infeasible_solution_does_not_change_world():

    world, instance = _build_world()

    solution = OptimizationSolution(
        objective_value=0.0,
        placements=[
            PlacementDecision(
                dataset_id="D1",
                destination_node="SRC1",
            ),
        ],
        replicas=[
            ReplicaDecision(
                dataset_id="D1",
                node="SRC2",
            ),
        ],
        is_feasible=False,
        is_optimal=False,
    )

    DecisionApplier().apply(
        world,
        solution,
    )

    assert instance.stored_at == {"T0"}
    assert world.storage_occupancy == {
        "T0": 2.0,
        "SRC1": 0.0,
        "SRC2": 0.0,
    }
