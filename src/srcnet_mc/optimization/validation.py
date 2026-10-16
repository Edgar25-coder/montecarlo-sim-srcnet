"""Independent arithmetic checks for deterministic solutions."""

from __future__ import annotations

from srcnet_mc.optimization.deterministic import DeterministicSolution, SyntheticFixture


def validate(fixture: SyntheticFixture, solution: DeterministicSolution, tolerance: float = 1e-7) -> list[str]:
    """Return violations without querying the SCIP model or variables."""
    errors: list[str] = []
    stores = set(solution.replica_storage.values())
    if solution.receiver not in fixture.dataset.compatible_receivers:
        errors.append("receiver is incompatible")
    if len(stores) != len(fixture.replica_slots):
        errors.append("replicas share a storage node")
    parents = [fixture.topology.node(store).parent_se for store in stores]
    if len(set(parents)) != len(parents):
        errors.append("replicas share a non-T0 parent")
    srcs = [fixture.topology.node(store).src for store in stores]
    if len(set(srcs)) != len(srcs):
        errors.append("replicas share an SRC")
    arcs = {(arc.tail, arc.head): arc for arc in fixture.topology.arcs}
    for node in (item.identifier for item in fixture.topology.nodes):
        stage0_balance = sum(amount for edge, amount in solution.stage0_flow.items() if edge[0] == node) - sum(amount for edge, amount in solution.stage0_flow.items() if edge[1] == node)
        expected0 = fixture.dataset.volume_pb if node == fixture.dataset.source_sdp else -fixture.dataset.volume_pb if node == solution.receiver else 0.0
        if abs(stage0_balance - expected0) > tolerance:
            errors.append(f"stage-0 flow conservation fails at {node}")
        for slot, store in solution.replica_storage.items():
            stage1_balance = sum(amount for (replica, edge), amount in solution.stage1_flow.items() if replica == slot and edge[0] == node) - sum(amount for (replica, edge), amount in solution.stage1_flow.items() if replica == slot and edge[1] == node)
            expected1 = fixture.dataset.volume_pb if node == solution.receiver else -fixture.dataset.volume_pb if node == store else 0.0
            if abs(stage1_balance - expected1) > tolerance:
                errors.append(f"stage-1 flow conservation fails for {slot} at {node}")
    for edge, arc in arcs.items():
        total = solution.stage0_flow[edge] + sum(solution.stage1_flow[slot, edge] for slot in fixture.replica_slots)
        if total < -tolerance:
            errors.append("negative flow")
        if total > arc.capacity_pb_per_day * fixture.max_utilisation + tolerance:
            errors.append("flow exceeds stability capacity")
        if total > tolerance and edge not in solution.active_arcs:
            errors.append("positive flow uses an inactive arc")
        if arc.available is False and total > tolerance:
            errors.append("positive flow uses an unavailable arc")
        if solution.congestion[edge] + tolerance < total / (arc.capacity_pb_per_day - total):
            errors.append("congestion epigraph is violated")
    exposure = sum(arcs[edge].failure_exposure * (solution.stage0_flow[edge] + sum(solution.stage1_flow[slot, edge] for slot in fixture.replica_slots)) for edge in arcs)
    if exposure > fixture.dataset.failure_exposure_budget + tolerance:
        errors.append("failure exposure budget is violated")
    for store in stores:
        if fixture.dataset.volume_pb > fixture.topology.node(store).persistent_capacity_pb + tolerance:
            errors.append("replica exceeds persistent capacity")
    return errors
