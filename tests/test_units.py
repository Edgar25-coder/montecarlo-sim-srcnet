"""Analytical unit checks from the manuscript review."""

from __future__ import annotations

import pytest

from srcnet_mc.domain.units import gbps_to_pb_per_day, quarterly_pb_to_pb_per_day


def test_gbps_to_daily_decimal_pb() -> None:
    assert gbps_to_pb_per_day(25) == pytest.approx(0.27)
    assert gbps_to_pb_per_day(400) == pytest.approx(4.32)


def test_quarterly_throughput_conversion_does_not_apply_to_storage() -> None:
    assert quarterly_pb_to_pb_per_day(120) == pytest.approx(120 / 90)


@pytest.mark.parametrize("value", [-1.0])
def test_negative_rate_is_invalid(value: float) -> None:
    with pytest.raises(ValueError, match="non-negative"):
        gbps_to_pb_per_day(value)
