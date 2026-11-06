from types import SimpleNamespace

from pyscipopt import Model

from srcnet_mc.optimization.constraints import (
    ConstraintBuilder,
)


def _build_failure_budget_test_model(budget):

    model = Model()
    model.hideOutput()

    dataset_id = "dataset-1"
    nodes = ("node-a", "node-b")

    dataset = SimpleNamespace(
        dataset=SimpleNamespace(
            identifier=dataset_id,
            failure_exposure_budget=budget,
        )
    )

    scenario = SimpleNamespace(
        datasets=(dataset,),
        storage_nodes=nodes,
        failure_risk={
            "node-a": 0.50,
            "node-b": 0.25,
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
    ).add_failure_exposure_constraint(
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


def test_exposure_above_failure_budget_is_infeasible():

    model = _build_failure_budget_test_model(
        budget=0.74,
    )

    model.optimize()

    assert model.getStatus() == "infeasible"


def test_exposure_equal_to_failure_budget_is_allowed():

    model = _build_failure_budget_test_model(
        budget=0.75,
    )

    model.optimize()

    assert model.getStatus() == "optimal"
