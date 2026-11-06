from srcnet_mc.optimization.optimizer import (
    SRCNetOptimizer,
)


def test_optimizer_reproducibility(
    sample_world_state,
):

    solution_1 = (
        SRCNetOptimizer()
        .solve(
            sample_world_state
        )
    )

    solution_2 = (
        SRCNetOptimizer()
        .solve(
            sample_world_state
        )
    )

    assert (
        solution_1.objective_value
        ==
        solution_2.objective_value
    )