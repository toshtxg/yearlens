from __future__ import annotations

import json
from pathlib import Path


class LocalReportRepository:
    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parents[2] / "artifacts" / "reports"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save_report(self, report: dict, target_year: int, profile_name: str | None = None) -> Path:
        slug = (profile_name or "yearlens-report").strip().lower().replace(" ", "-")
        destination = self.base_dir / f"{slug}-{target_year}.json"
        destination.write_text(json.dumps(report, indent=2), encoding="utf-8")
        return destination

    def load_report(self, filename: str) -> dict:
        target = self.base_dir / filename
        return json.loads(target.read_text(encoding="utf-8"))

    def list_reports(self) -> list[str]:
        return sorted(path.name for path in self.base_dir.glob("*.json"))

