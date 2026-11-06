from srcnet_mc.optimization.optimizer import (
    SRCNetOptimizer,
)


def test_optimizer_returns_solution(
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
        len(solution.placements)
        >
        0
    )