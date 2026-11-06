from pyscipopt import Model

from srcnet_mc.optimization.variables import (
    VariableFactory,
)

from srcnet_mc.optimization.objective import (
    ObjectiveBuilder,
)

from srcnet_mc.optimization.scenario import (
    build_scenario,
)


def test_objective_exists(
    sample_world_state,
):

    scenario = build_scenario(
        sample_world_state
    )

    model = Model()

    variables = VariableFactory(
        model
    )

    x = variables.create_placement_variables(
        scenario
    )

    y = variables.create_replica_variables(
        scenario
    )

    ObjectiveBuilder(
        model
    ).set_objective(
        scenario,
        x,
        y,
    )

    assert (
        model.getObjective()
        is not None
    )