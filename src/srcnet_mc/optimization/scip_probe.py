"""A deliberately tiny MINLP compatibility probe for SCIP.

This is not an SRCNet optimiser.  It proves that the selected Python binding can
create binary and continuous variables together with the manuscript's exact
congestion shape on a positive-capacity operational link.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ScipProbeResult:
    """Serializable evidence produced by :func:`run_probe`."""

    status: str
    has_solution: bool
    flow: float | None
    activation: int | None
    congestion: float | None
    objective: float | None
    expected_congestion: float | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def run_probe() -> ScipProbeResult:
    """Solve a hand-checkable binary/continuous nonlinear model.

    The model requires a binary activated link and a positive flow of 2 over a
    capacity of 10.  Its exact optimum has congestion ``2 / (10 - 2) = 0.25``.
    A successful result is necessary, but not sufficient, evidence that SCIP is
    suitable for the full SRCNet MINLP.
    """
    from pyscipopt import Model, quicksum  # Imported lazily for clear CLI errors.

    capacity = 10.0
    required_flow = 2.0
    model = Model("srcnet_exact_congestion_probe")
    model.hideOutput()

    active = model.addVar("active", vtype="B")
    flow = model.addVar("flow", lb=0.0, ub=capacity - 1e-6, vtype="C")
    congestion = model.addVar("congestion", lb=0.0, vtype="C")

    model.addCons(flow == required_flow)
    model.addCons(flow <= capacity * active)
    # Equivalent to congestion >= flow / (capacity - flow), with a strictly
    # positive denominator. This intentionally keeps the nonlinear expression.
    model.addCons(congestion * (capacity - flow) >= flow)
    model.setObjective(congestion + 0.01 * quicksum([active]), "minimize")
    model.optimize()

    status = str(model.getStatus())
    if model.getNSols() == 0:
        return ScipProbeResult(status, False, None, None, None, None, None)

    solution = model.getBestSol()
    solved_flow = float(model.getSolVal(solution, flow))
    solved_active = int(round(model.getSolVal(solution, active)))
    solved_congestion = float(model.getSolVal(solution, congestion))
    objective = float(model.getSolObjVal(solution))
    expected = required_flow / (capacity - required_flow)
    return ScipProbeResult(
        status=status,
        has_solution=True,
        flow=solved_flow,
        activation=solved_active,
        congestion=solved_congestion,
        objective=objective,
        expected_congestion=expected,
    )

