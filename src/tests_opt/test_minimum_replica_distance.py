from types import SimpleNamespace

from pyscipopt import Model

from srcnet_mc.optimization.constraints import (
    ConstraintBuilder,
)


def _build_distance_test_model(distance):

    model = Model()
    model.hideOutput()

    dataset_id = "dataset-1"
    nodes = ("node-a", "node-b")

    dataset = SimpleNamespace(
        dataset=SimpleNamespace(
            identifier=dataset_id,
            minimum_replica_distance=10.0,
        )
    )

    scenario = SimpleNamespace(
        datasets=(dataset,),
        storage_nodes=nodes,
        distances={
            ("node-a", "node-b"): distance,
        },
    )

    x = {
        (dataset_id, node): model.addVar(
            vtype="B",
            name=f"x_{node}",
        )
        for node in nodes
    }

    y = {
        (dataset_id, node): model.addVar(
            vtype="B",
            name=f"y_{node}",
        )
        for node in nodes
    }

    ConstraintBuilder(
        model
    ).add_minimum_replica_distance_constraint(
        scenario,
        x,
        y,
    )

    model.addCons(
        x[dataset_id, "node-a"] == 1
    )
    model.addCons(
        y[dataset_id, "node-b"] == 1
    )

    return model


def test_replicas_closer_than_minimum_distance_are_forbidden():

    model = _build_distance_test_model(
        distance=9.0,
    )

    model.optimize()

    assert model.getStatus() == "infeasible"


def test_replicas_at_minimum_distance_are_allowed():

    model = _build_distance_test_model(
        distance=10.0,
    )

    model.optimize()

    assert model.getStatus() == "optimal"
