from pyscipopt import Model

from srcnet_mc.optimization.variables import (
    VariableFactory,
)

from srcnet_mc.optimization.constraints import (
    ConstraintBuilder,
)

from srcnet_mc.optimization.scenario import (
    build_scenario,
)


def test_single_assignment_constraints(
    sample_world_state,
):

    scenario = build_scenario(
        sample_world_state
    )

    model = Model()

    variables = VariableFactory(
        model
    )

    x = (
        variables
        .create_placement_variables(
            scenario
        )
    )

    ConstraintBuilder(
        model
    ).add_single_placement_constraint(
        scenario,
        x,
    )

    assert (
        model.getNConss()
        ==
        len(
            scenario.datasets
        )
    )