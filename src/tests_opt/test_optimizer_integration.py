from srcnet_mc.optimization.optimizer import (
    SRCNetOptimizer,
)


def test_world_state_to_optimizer(
    sample_world_state,
):

    optimizer = (
        SRCNetOptimizer()
    )

    solution = optimizer.solve(
        sample_world_state
    )

    dataset_ids = {
        p.dataset_id
        for p
        in solution.placements
    }

    assert (
        len(dataset_ids)
        ==
        len(
            sample_world_state.datasets
        )
    )