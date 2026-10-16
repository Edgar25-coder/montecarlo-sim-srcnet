"""Explicit conversions; persistent storage volume is never time-scaled."""

SECONDS_PER_DAY = 86_400
BITS_PER_GIGABIT = 1_000_000_000
BYTES_PER_DECIMAL_PETABYTE = 1_000_000_000_000_000


def gbps_to_pb_per_day(gbps: float) -> float:
    """Convert a decimal-Gbps rate to decimal-PB transferable in one day."""
    if gbps < 0:
        raise ValueError("Gbps must be non-negative")
    return gbps * BITS_PER_GIGABIT * SECONDS_PER_DAY / (8 * BYTES_PER_DECIMAL_PETABYTE)


def quarterly_pb_to_pb_per_day(volume_pb: float, days: int = 90) -> float:
    """Convert a stated planning-window throughput allowance, not storage volume."""
    if volume_pb < 0 or days <= 0:
        raise ValueError("volume must be non-negative and days positive")
    return volume_pb / days
