"""Small exact deterministic SRCNet reference model and independent checker.

The fixture is synthetic and deliberately tiny.  It exercises the two flow
stages and the core placement/resource constraints before any stochastic layer
is introduced.  It is not a calibrated SRCNet instance.
"""

from __future__ import annotations

from dataclasses import dataclass

from srcnet_mc.domain import Arc, Dataset, Node, NodeRole, Topology


@dataclass(frozen=True)
class SyntheticFixture:
    topology: Topology
    dataset: Dataset
    replica_slots: tuple[str, ...]
    large_threshold_pb: float
    max_utilisation: float
    storage_distance: dict[tuple[str, str], float]


@dataclass(frozen=True)
class DeterministicSolution:
    status: str
    active_nodes: frozenset[str]
    active_arcs: frozenset[tuple[str, str]]
    receiver: str
    replica_storage: dict[str, str]
    stage0_flow: dict[tuple[str, str], float]
    stage1_flow: dict[tuple[str, tuple[str, str]], float]
    congestion: dict[tuple[str, str], float]
    processing_loads: dict[str, float]
    eta: float
    objective: float


def synthetic_fixture() -> SyntheticFixture:
    """Return a complete, hand-checkable synthetic topology.

    The volume is below the large threshold, requiring two replicas. Storage
    nodes are attached to distinct non-T0 parents in distinct SRCs.
    """
    topology = Topology(
        nodes=(
            Node("sdp", NodeRole.SDP),
            Node("t0", NodeRole.T0, processing_capacity_pb_per_day=8, temporary_buffer_pb=8),
            Node("se-a", NodeRole.NON_T0, processing_capacity_pb_per_day=8, temporary_buffer_pb=8, src="A"),
            Node("se-b", NodeRole.NON_T0, processing_capacity_pb_per_day=8, temporary_buffer_pb=8, src="B"),
            Node("store-a", NodeRole.STORAGE, processing_capacity_pb_per_day=8, persistent_capacity_pb=5, temporary_buffer_pb=5, parent_se="se-a", src="A"),
            Node("store-b", NodeRole.STORAGE, processing_capacity_pb_per_day=8, persistent_capacity_pb=5, temporary_buffer_pb=5, parent_se="se-b", src="B"),
        ),
        arcs=(
            Arc("sdp", "t0", 5), Arc("t0", "se-a", 5), Arc("se-a", "store-a", 5),
            Arc("t0", "se-b", 5), Arc("se-b", "store-b", 5),
        ),
    )
    topology.validate()
    return SyntheticFixture(
        topology=topology,
        dataset=Dataset("k1", "sdp", 2, frozenset({"t0"}), minimum_replica_distance=50, failure_exposure_budget=10),
        replica_slots=("r1", "r2"), large_threshold_pb=3, max_utilisation=0.8,
        storage_distance={("store-a", "store-b"): 100, ("store-b", "store-a"): 100},
    )


def solve(fixture: SyntheticFixture) -> DeterministicSolution:
    """Solve the exact deterministic fixture with SCIP.

    This reference includes all activation, placement, two-stage conservation,
    availability, capacity, stability, SRC/parent diversity, distance and
    failure-exposure constraints applicable to this fixture.
    """
    from pyscipopt import Model, quicksum

    dataset, topology = fixture.dataset, fixture.topology
    arcs = tuple((arc.tail, arc.head) for arc in topology.arcs)
    storage = tuple(node.identifier for node in topology.nodes if node.role is NodeRole.STORAGE)
    nodes = {node.identifier: node for node in topology.nodes}
    capacity = {edge: arc.capacity_pb_per_day for edge, arc in zip(arcs, topology.arcs)}
    exposure = {edge: arc.failure_exposure for edge, arc in zip(arcs, topology.arcs)}
    model = Model("srcnet_synthetic_deterministic")
    model.hideOutput()
    x = {node: model.addVar(f"x_{node}", vtype="B") for node in nodes if nodes[node].role is not NodeRole.SDP}
    alpha = {receiver: model.addVar(f"alpha_{receiver}", vtype="B") for receiver in dataset.compatible_receivers}
    z = {(slot, store): model.addVar(f"z_{slot}_{store}", vtype="B") for slot in fixture.replica_slots for store in storage}
    y = {edge: model.addVar(f"y_{edge[0]}_{edge[1]}", vtype="B") for edge in arcs}
    f0 = {edge: model.addVar(f"f0_{edge[0]}_{edge[1]}", lb=0) for edge in arcs}
    f1 = {(slot, edge): model.addVar(f"f1_{slot}_{edge[0]}_{edge[1]}", lb=0) for slot in fixture.replica_slots for edge in arcs}
    congestion = {edge: model.addVar(f"cong_{edge[0]}_{edge[1]}", lb=0) for edge in arcs}
    load = {node: model.addVar(f"load_{node}", lb=0) for node in nodes if node != dataset.source_sdp}
    eta = model.addVar("eta", lb=0, ub=fixture.max_utilisation)

    model.addCons(quicksum(x[node] for node in x if nodes[node].role is NodeRole.T0) >= 1)
    model.addCons(quicksum(alpha.values()) == 1)
    for receiver, value in alpha.items():
        model.addCons(value <= x[receiver])
    for slot in fixture.replica_slots:
        model.addCons(quicksum(z[slot, store] for store in storage) == 1)
    for store in storage:
        model.addCons(quicksum(z[slot, store] for slot in fixture.replica_slots) <= 1)
    for parent in ("se-a", "se-b"):
        model.addCons(quicksum(z[slot, store] for slot in fixture.replica_slots for store in storage if nodes[store].parent_se == parent) <= 1)
    for src in ("A", "B"):
        model.addCons(quicksum(z[slot, store] for slot in fixture.replica_slots for store in storage if nodes[store].src == src) <= 1)
    for left in fixture.replica_slots:
        for right in fixture.replica_slots:
            if left >= right:
                continue
            for a in storage:
                for b in storage:
                    if a != b and fixture.storage_distance[a, b] < dataset.minimum_replica_distance:
                        model.addCons(z[left, a] + z[right, b] <= 1)
    for store in storage:
        model.addCons(quicksum(dataset.volume_pb * z[slot, store] for slot in fixture.replica_slots) <= nodes[store].persistent_capacity_pb * x[store])
        model.addCons(x[store] <= x[nodes[store].parent_se])

    # In this fixture processing load is the aggregate inbound daily volume.
    # It is deliberately defined here, rather than inferred from quarterly
    # example values, to keep the synthetic unit convention explicit.
    for node, value in load.items():
        inbound = quicksum(f0[edge] for edge in arcs if edge[1] == node) + quicksum(f1[slot, edge] for slot in fixture.replica_slots for edge in arcs if edge[1] == node)
        model.addCons(value == inbound)
        model.addCons(value <= nodes[node].processing_capacity_pb_per_day * x[node])
        model.addCons(value <= nodes[node].temporary_buffer_pb * x[node])

    for node in nodes:
        out0 = quicksum(f0[edge] for edge in arcs if edge[0] == node)
        in0 = quicksum(f0[edge] for edge in arcs if edge[1] == node)
        rhs = dataset.volume_pb if node == dataset.source_sdp else -dataset.volume_pb * alpha.get(node, 0)
        model.addCons(out0 - in0 == rhs)
        for slot in fixture.replica_slots:
            out1 = quicksum(f1[slot, edge] for edge in arcs if edge[0] == node)
            in1 = quicksum(f1[slot, edge] for edge in arcs if edge[1] == node)
            rhs1 = dataset.volume_pb * alpha.get(node, 0) - dataset.volume_pb * z.get((slot, node), 0)
            model.addCons(out1 - in1 == rhs1)
    for edge in arcs:
        total = f0[edge] + quicksum(f1[slot, edge] for slot in fixture.replica_slots)
        model.addCons(total <= capacity[edge] * y[edge])
        model.addCons(total <= eta * capacity[edge])
        model.addCons(y[edge] <= x[edge[0]] if edge[0] in x else y[edge] <= 1)
        model.addCons(y[edge] <= x[edge[1]] if edge[1] in x else y[edge] <= 1)
        model.addCons(congestion[edge] * (capacity[edge] - total) >= total)
    model.addCons(quicksum(exposure[edge] * (f0[edge] + quicksum(f1[slot, edge] for slot in fixture.replica_slots)) for edge in arcs) <= dataset.failure_exposure_budget)
    model.setObjective(quicksum(x.values()) + quicksum(congestion.values()) + eta, "minimize")
    model.optimize()
    if model.getNSols() == 0:
        raise RuntimeError(f"synthetic fixture unexpectedly has no solution: {model.getStatus()}")
    sol = model.getBestSol()
    return DeterministicSolution(
        str(model.getStatus()), frozenset(node for node in x if model.getSolVal(sol, x[node]) > 0.5),
        frozenset(edge for edge in arcs if model.getSolVal(sol, y[edge]) > 0.5), "t0",
        {slot: next(store for store in storage if model.getSolVal(sol, z[slot, store]) > 0.5) for slot in fixture.replica_slots},
        {edge: model.getSolVal(sol, f0[edge]) for edge in arcs},
        {(slot, edge): model.getSolVal(sol, f1[slot, edge]) for slot in fixture.replica_slots for edge in arcs},
        {edge: model.getSolVal(sol, congestion[edge]) for edge in arcs},
        {node: model.getSolVal(sol, load[node]) for node in load}, model.getSolVal(sol, eta), model.getSolObjVal(sol),
    )
