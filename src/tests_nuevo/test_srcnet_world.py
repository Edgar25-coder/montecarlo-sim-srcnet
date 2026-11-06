import numpy as np

from srcnet_mc.domain.model import (
    Arc,
    Node,
    NodeRole,
    Topology,
)

from srcnet_mc.domain.markov import (
    LinkState,
    MarkovChain,
)

from srcnet_mc.domain.srcnet_world import (
    SRCNetWorld,
)

from srcnet_mc.domain.parameters import (
    SimulationParameters,
    LinkParameters,
    LinkStateParameters,
    BetaMoments,
    LogNormalMoments,
    DatasetParameters,
    PoissonRate,
    WeibullMoments,
)


def build_parameters():

    normal = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.95,
            variance=0.001,
        ),
        latency=LogNormalMoments(
            mean=20.0,
            cv=0.10,
        ),
    )

    congested = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.70,
            variance=0.005,
        ),
        latency=LogNormalMoments(
            mean=50.0,
            cv=0.20,
        ),
    )

    degraded = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.40,
            variance=0.005,
        ),
        latency=LogNormalMoments(
            mean=120.0,
            cv=0.30,
        ),
    )

    return SimulationParameters(
        link_parameters=LinkParameters(
            normal=normal,
            congested=congested,
            degraded=degraded,
        ),
        dataset_parameters=DatasetParameters(
            arrivals=PoissonRate(
                rate=5.0,
            ),
            size_distribution=LogNormalMoments(
                mean=1.0,
                cv=1.0,
            ),
            retention_distribution=WeibullMoments(
                mean_lifetime_days=365.0,
                shape=1.5,
            ),
        ),
    )


def build_topology():

    topology = Topology(
        nodes=(
            Node(
                identifier="T0",
                role=NodeRole.T0,
            ),
            Node(
                identifier="SRC1",
                role=NodeRole.NON_T0,
            ),
        ),
        arcs=(
            Arc(
                tail="T0",
                head="SRC1",
                capacity_pb_per_day=10.0,
            ),
        ),
    )

    topology.validate()

    return topology


def build_chains(rng):

    transition_matrix = np.array(
        [
            [0.90, 0.10, 0.00, 0.00],
            [0.10, 0.80, 0.10, 0.00],
            [0.00, 0.10, 0.80, 0.10],
            [0.20, 0.10, 0.00, 0.70],
        ]
    )

    return {
        ("T0", "SRC1"): MarkovChain(
            transition_matrix=transition_matrix,
            initial_state=LinkState.NORMAL,
            rng=rng,
        )
    }


def test_world_runs_one_day():

    rng = np.random.default_rng(1234)

    world = SRCNetWorld(
        topology=build_topology(),
        parameters=build_parameters(),
        rng=rng,
        chains=build_chains(rng),
    )

    state = world.step()

    assert state.day == 1

    assert ("T0", "SRC1") in state.arc_states

    arc_state = state.arc_states[
        ("T0", "SRC1")
    ]

    assert arc_state.effective_capacity_pb_per_day >= 0.0

    assert arc_state.latency_ms >= 0.0


def test_world_runs_multiple_days():

    rng = np.random.default_rng(1234)

    world = SRCNetWorld(
        topology=build_topology(),
        parameters=build_parameters(),
        rng=rng,
        chains=build_chains(rng),
    )

    for _ in range(10):

        state = world.step()

    assert state.day == 10


def test_world_initial_storage():

    rng = np.random.default_rng(1234)

    world = SRCNetWorld(
        topology=build_topology(),
        parameters=build_parameters(),
        rng=rng,
        chains=build_chains(rng),
    )

    state = world.step()

    assert "T0" in state.storage_occupancy_pb

    assert "SRC1" in state.storage_occupancy_pb

    #
    # Layer 2 genera datasets automáticamente.
    # Por tanto T0 ya no tiene por qué permanecer vacío.
    #
    assert state.storage_occupancy_pb["T0"] >= 0.0

    assert state.storage_occupancy_pb["SRC1"] >= 0.0

    assert state.new_arrivals >= 0

    assert state.expired_datasets >= 0