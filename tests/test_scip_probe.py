"""Compatibility evidence for the selected exact optimisation route."""

from __future__ import annotations

import pytest

pyscipopt = pytest.importorskip("pyscipopt")

from srcnet_mc.optimization.scip_probe import run_probe


def test_exact_binary_nonlinear_congestion_probe() -> None:
    result = run_probe()

    assert result.status == "optimal"
    assert result.has_solution
    assert result.activation == 1
    assert result.flow == pytest.approx(2.0)
    assert result.congestion == pytest.approx(0.25, abs=1e-7)
    assert result.expected_congestion == pytest.approx(0.25)
    assert result.objective == pytest.approx(0.26, abs=1e-7)
