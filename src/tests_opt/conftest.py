import numpy as np
import pytest

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

from srcnet_mc.domain.srcnet_world import (
    SRCNetWorld,
)


@pytest.fixture
def simulation_parameters():

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


@pytest.fixture
def topology():

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


@pytest.fixture
def rng():

    return np.random.default_rng(1234)


@pytest.fixture
def chains(
    rng,
    topology,
):

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


@pytest.fixture
def sample_world_state(
    topology,
    simulation_parameters,
    rng,
    chains,
):

    world = SRCNetWorld(
        topology=topology,
        parameters=simulation_parameters,
        rng=rng,
        chains=chains,
    )

    state = None

    #
    # Ejecutamos varios días para asegurar:
    # - datasets generados
    # - ocupación > 0
    # - estado realista para Fase B
    #

    for _ in range(5):

        state = world.step()

    return state