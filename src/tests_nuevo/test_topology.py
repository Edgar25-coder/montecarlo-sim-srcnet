from srcnet_mc.domain.model import (
    Node,
    Arc,
    Topology,
    NodeRole,
)


def test_valid_topology():

    topology = Topology(
        nodes=(
            Node(
                identifier="T0",
                role=NodeRole.T0,
            ),
        ),
        arcs=(),
    )

    topology.validate()