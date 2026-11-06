from dataclasses import replace
from math import isfinite

from srcnet_mc.domain.markov import (
    LinkState,
)
from srcnet_mc.domain.world_state import (
    ArcState,
)
from srcnet_mc.optimization.scenario import (
    build_scenario,
)


def test_scenario_builds_correctly(
    sample_world_state,
):

    scenario = build_scenario(
        sample_world_state
    )

    assert (
        len(scenario.datasets)
        ==
        len(sample_world_state.datasets)
    )

    assert (
        len(
            scenario.storage_nodes
        )
        >
        0
    )


def test_failed_arc_keeps_scenario_latency_finite(
    sample_world_state,
):

    failed_arc = next(
        iter(sample_world_state.arc_states)
    )
    arc_states = sample_world_state.arc_states.copy()
    arc_states[failed_arc] = ArcState(
        state=LinkState.FAILED,
        effective_capacity_pb_per_day=0.0,
        latency_ms=float("inf"),
    )
    world_state = replace(
        sample_world_state,
        arc_states=arc_states,
    )

    scenario = build_scenario(
        world_state
    )

    assert failed_arc[1] in scenario.failed_nodes
    assert isfinite(
        scenario.latency_costs[failed_arc[1]]
    )
