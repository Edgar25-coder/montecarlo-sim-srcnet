from srcnet_mc.optimization.optimizer import (
    SRCNetOptimizer,
)


def test_capacity_constraint_respected(
    sample_world_state,
):
    """
    Verifica que el optimizador encuentra
    una solución factible cuando existe
    capacidad suficiente.
    """

    optimizer = SRCNetOptimizer()

    solution = optimizer.solve(
        sample_world_state
    )

    assert solution.is_feasible

    assert solution.is_optimal

    assert (
        len(solution.placements)
        ==
        len(sample_world_state.datasets)
    )