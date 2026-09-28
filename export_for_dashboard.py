"""Exports unresolved jobs from jobs.db, ranked the same way the automatic
feed is (location tier first, then disclosed pay), into two files ready to
paste into the dashboard's "Paste import" box.

Note: automatic phone-side syncing from GitHub doesn't work — published
Claude artifact pages are blocked from making network requests to outside
sites, by platform design, for security reasons. That's not fixable from
inside the page, so this manual export/paste is the reliable path, not a
downgrade from something that was working.

Usage:
  python export_for_dashboard.py

Produces:
  dashboard_shortlist.json  -> open the dashboard's Shortlist tab, tap
                               "Paste import", paste this file's contents.
  dashboard_backlog.json    -> switch to the Backlog tab, tap "Paste
                               import" again, paste this file's contents.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

from publish_dashboard_feed import build_lists, DB_PATH  # noqa: E402


def main():
    if not DB_PATH.exists():
        sys.exit("jobs.db not found — run scout.py at least once first.")
    shortlist, backlog = build_lists()
    (HERE / "dashboard_shortlist.json").write_text(
        json.dumps(shortlist, indent=2), encoding="utf-8")
    (HERE / "dashboard_backlog.json").write_text(
        json.dumps(backlog, indent=2), encoding="utf-8")
    print(f"Wrote {len(shortlist)} shortlist job(s) to "
          f"dashboard_shortlist.json")
    print(f"Wrote {len(backlog)} backlog job(s) to dashboard_backlog.json")
    print("Open each file, select all, copy, and paste into the matching "
          "tab's \"Paste import\" box on the dashboard.")


if __name__ == "__main__":
    main()
