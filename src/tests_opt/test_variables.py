from pyscipopt import Model

from srcnet_mc.optimization.variables import (
    VariableFactory,
)

from srcnet_mc.optimization.scenario import (
    build_scenario,
)


def test_variable_creation(
    sample_world_state,
):

    scenario = build_scenario(
        sample_world_state
    )

    model = Model()

    factory = VariableFactory(
        model
    )

    x = (
        factory
        .create_placement_variables(
            scenario
        )
    )

    expected = (
        len(scenario.datasets)
        *
        len(
            scenario.storage_nodes
        )
    )

    assert len(x) == expected