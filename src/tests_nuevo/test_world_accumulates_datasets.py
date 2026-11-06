from srcnet_mc.domain.srcnet_world import (
    SRCNetWorld,
)


def test_world_accumulates_datasets(
    topology,
    simulation_parameters,
    rng,
    markov_chains,
):

    world = SRCNetWorld(
        topology=topology,
        parameters=simulation_parameters,
        rng=rng,
        chains=markov_chains,
    )

    for _ in range(50):

        state = world.step()

    assert len(state.datasets) > 0