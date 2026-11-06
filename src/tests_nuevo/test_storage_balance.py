import numpy as np

from srcnet_mc.domain.srcnet_world import (
    SRCNetWorld,
)


def test_storage_non_negative(
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

    for _ in range(200):

        state = world.step()

        for occupancy in (
            state.storage_occupancy_pb.values()
        ):

            assert occupancy >= 0.0