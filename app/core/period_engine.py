from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta

from app.core.astro_engine import ChangePoint
from app.core.config import DEFAULT_SEGMENT_CONFIG, SegmentConfig


@dataclass
class PeriodWindow:
    id: str
    start_date: date
    end_date: date
    drivers: list[ChangePoint] = field(default_factory=list)

    @property
    def duration_days(self) -> int:
        return (self.end_date - self.start_date).days + 1


def build_periods(
    window_start: date,
    window_end: date,
    change_points: list[ChangePoint],
    config: SegmentConfig = DEFAULT_SEGMENT_CONFIG,
) -> list[PeriodWindow]:
    boundaries = [window_start]

    for point in sorted(change_points, key=lambda item: item.date):
        if point.date <= window_start or point.date > window_end:
            continue
        if (point.date - boundaries[-1]).days < config.merge_within_days:
            continue
        boundaries.append(point.date)

    boundaries.append(window_end + timedelta(days=1))

    periods: list[PeriodWindow] = []
    for index in range(len(boundaries) - 1):
        start = boundaries[index]
        end = boundaries[index + 1] - timedelta(days=1)
        drivers = [point for point in change_points if start <= point.date <= end]

        candidate = PeriodWindow(
            id=f"p{len(periods) + 1}",
            start_date=start,
            end_date=end,
            drivers=drivers,
        )

        if periods and candidate.duration_days < config.min_segment_days:
            periods[-1].end_date = candidate.end_date
            periods[-1].drivers.extend(candidate.drivers)
            continue

        periods.append(candidate)

    split_periods = _split_long_periods(periods, config.max_segment_days)
    return _compress_periods(split_periods, config.target_segment_count)


def _split_long_periods(periods: list[PeriodWindow], max_segment_days: int) -> list[PeriodWindow]:
    final_periods: list[PeriodWindow] = []

    for period in periods:
        if period.duration_days <= max_segment_days:
            final_periods.append(period)
            continue

        midpoint = period.start_date + timedelta(days=(period.duration_days // 2) - 1)
        final_periods.append(
            PeriodWindow(
                id=period.id,
                start_date=period.start_date,
                end_date=midpoint,
                drivers=period.drivers,
            )
        )
        final_periods.append(
            PeriodWindow(
                id=f"{period.id}b",
                start_date=midpoint + timedelta(days=1),
                end_date=period.end_date,
                drivers=period.drivers,
            )
        )

    for index, period in enumerate(final_periods, start=1):
        period.id = f"p{index}"

    return final_periods


def _compress_periods(periods: list[PeriodWindow], target_segment_count: int) -> list[PeriodWindow]:
    if len(periods) <= target_segment_count:
        return periods

    compressed = list(periods)
    while len(compressed) > target_segment_count:
        shortest_index = min(range(len(compressed)), key=lambda idx: compressed[idx].duration_days)

        if shortest_index == 0:
            merge_index = 0
        elif shortest_index == len(compressed) - 1:
            merge_index = shortest_index - 1
        else:
            left_days = compressed[shortest_index - 1].duration_days
            right_days = compressed[shortest_index + 1].duration_days
            merge_index = shortest_index - 1 if left_days <= right_days else shortest_index

        left = compressed[merge_index]
        right = compressed[merge_index + 1]
        merged = PeriodWindow(
            id=left.id,
            start_date=left.start_date,
            end_date=right.end_date,
            drivers=sorted(left.drivers + right.drivers, key=lambda item: (item.date, item.intensity)),
        )
        compressed = compressed[:merge_index] + [merged] + compressed[merge_index + 2 :]

    for index, period in enumerate(compressed, start=1):
        period.id = f"p{index}"

    return compressed
