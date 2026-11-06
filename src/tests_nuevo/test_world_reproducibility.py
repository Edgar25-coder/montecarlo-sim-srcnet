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
            mean=20,
            cv=0.10,
        ),
    )

    congested = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.70,
            variance=0.005,
        ),
        latency=LogNormalMoments(
            mean=50,
            cv=0.20,
        ),
    )

    degraded = LinkStateParameters(
        utilization=BetaMoments(
            mean=0.40,
            variance=0.005,
        ),
        latency=LogNormalMoments(
            mean=120,
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
            arrivals=PoissonRate(rate=5),
            size_distribution=LogNormalMoments(
                mean=1.0,
                cv=1.0,
            ),
            retention_distribution=WeibullMoments(
                mean_lifetime_days=365,
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

    P = np.array(
        [
            [0.90, 0.10, 0.00, 0.00],
            [0.10, 0.80, 0.10, 0.00],
            [0.00, 0.10, 0.80, 0.10],
            [0.20, 0.10, 0.00, 0.70],
        ]
    )

    return {
        ("T0", "SRC1"): MarkovChain(
            transition_matrix=P,
            initial_state=LinkState.NORMAL,
            rng=rng,
        )
    }
def test_world_reproducibility():

    rng1 = np.random.default_rng(1234)
    rng2 = np.random.default_rng(1234)

    world1 = SRCNetWorld(
        topology=build_topology(),
        parameters=build_parameters(),
        rng=rng1,
        chains=build_chains(rng1),
    )

    world2 = SRCNetWorld(
        topology=build_topology(),
        parameters=build_parameters(),
        rng=rng2,
        chains=build_chains(rng2),
    )

    state1 = world1.step()
    state2 = world2.step()

    arc1 = state1.arc_states[
        ("T0", "SRC1")
    ]

    arc2 = state2.arc_states[
        ("T0", "SRC1")
    ]

    assert state1.day == state2.day

    assert arc1.state == arc2.state

    assert (
        arc1.effective_capacity_pb_per_day
        ==
        arc2.effective_capacity_pb_per_day
    )

    assert (
        arc1.latency_ms
        ==
        arc2.latency_ms
    )