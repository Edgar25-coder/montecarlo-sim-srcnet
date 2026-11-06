from srcnet_mc.optimization.optimizer import (
    SRCNetOptimizer,
)


def test_replication_exists(
    sample_world_state,
):

    solution = (
        SRCNetOptimizer()
        .solve(
            sample_world_state
        )
    )

    assert solution.is_feasible

    assert solution.is_optimal

    assert (
        len(solution.replicas)
        >
        0
    )

    dataset_ids = {
        d.identifier
        for d
        in (
            instance.dataset
            for instance
            in sample_world_state.datasets.values()
        )
    }

    replicated = {
        replica.dataset_id
        for replica
        in solution.replicas
    }

    assert replicated.issubset(
        dataset_ids
    )