"""Typed, immutable model inputs shared by solvers and validators."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class NodeRole(StrEnum):
    SDP = "sdp"
    T0 = "t0"
    NON_T0 = "non_t0"
    STORAGE = "storage"
    TRANSIT = "transit"


@dataclass(frozen=True)
class Node:
    identifier: str
    role: NodeRole
    processing_capacity_pb_per_day: float = 0.0
    temporary_buffer_pb: float = 0.0
    persistent_capacity_pb: float = 0.0
    parent_se: str | None = None
    src: str | None = None


@dataclass(frozen=True)
class Arc:
    tail: str
    head: str
    capacity_pb_per_day: float
    available: bool = True
    failure_exposure: float = 0.0


@dataclass(frozen=True)
class Dataset:
    identifier: str
    source_sdp: str
    volume_pb: float
    compatible_receivers: frozenset[str]
    minimum_replica_distance: float = 0.0
    failure_exposure_budget: float = float("inf")


@dataclass(frozen=True)
class Topology:
    nodes: tuple[Node, ...]
    arcs: tuple[Arc, ...]

    def node(self, identifier: str) -> Node:
        matches = [node for node in self.nodes if node.identifier == identifier]
        if len(matches) != 1:
            raise ValueError(f"expected exactly one node named {identifier!r}")
        return matches[0]

    def validate(self) -> None:
        identifiers = {node.identifier for node in self.nodes}
        if len(identifiers) != len(self.nodes):
            raise ValueError("node identifiers must be unique")
        for arc in self.arcs:
            if arc.tail not in identifiers or arc.head not in identifiers:
                raise ValueError("every arc endpoint must exist")
            if arc.capacity_pb_per_day < 0:
                raise ValueError("arc capacity must be non-negative")
        for node in self.nodes:
            if min(node.processing_capacity_pb_per_day, node.temporary_buffer_pb, node.persistent_capacity_pb) < 0:
                raise ValueError("node capacities must be non-negative")
            if node.role is NodeRole.STORAGE and node.parent_se not in identifiers:
                raise ValueError("storage nodes require an existing parent SE")
