from srcnet_mc.domain.world_state import (
    ArcState,
    WorldState,
)

from srcnet_mc.domain.markov import (
    LinkState,
)


def test_world_state_creation():

    state = WorldState(
        day=1,
        arc_states={
            ("A", "B"): ArcState(
                state=LinkState.NORMAL,
                effective_capacity_pb_per_day=10.0,
                latency_ms=20.0,
            )
        },
        storage_occupancy_pb={
            "SE1": 5.0,
        },
        datasets={},
        new_arrivals=0,
        expired_datasets=0,
    )

    assert state.day == 1

    assert ("A", "B") in state.arc_states

    assert state.storage_occupancy_pb["SE1"] == 5.0

    assert state.new_arrivals == 0

    assert state.expired_datasets == 0


def test_world_state_empty_datasets():

    state = WorldState(
        day=5,
        arc_states={},
        storage_occupancy_pb={},
        datasets={},
        new_arrivals=0,
        expired_datasets=0,
    )

    assert len(state.datasets) == 0