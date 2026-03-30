"""
Ideas Dashboard — Unified CLI for viewing sync status

Combines BranchTracker, SyncDetector, and progress data
into a unified dashboard view.

Usage:
    python ideas_dashboard.py           # Show full dashboard
    python ideas_dashboard.py --branches   # Show branch status only
    python ideas_dashboard.py --ideas  # Show ideas status only
    python ideas_dashboard.py --sync IDEA-012  # Run sync detection for one idea
    python ideas_dashboard.py --full-scan  # Run full sync scan
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from branch_tracker import BranchTracker, BranchType, BranchStatus
from sync_detector import SyncDetector
from execution_tracker import ExecutionTracker


def print_header(title: str):
    """Print a formatted header"""
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_branches():
    """Show branch status dashboard"""
    print_header("BRANCH STATUS")
    
    tracker = BranchTracker()
    tracker.scan()
    
    active_features = tracker.get_feature_branches()
    active_hotfixes = tracker.get_hotfix_branches()
    merged = [b for b in tracker._branches.values() if b.status == BranchStatus.MERGED]
    stale = [b for b in tracker._branches.values() if b.status == BranchStatus.STALE]
    
    print(f"Last scanned: {tracker._last_scan.isoformat() if tracker._last_scan else 'Never'}")
    print()
    
    print(f"Active Feature Branches: {len(active_features)}")
    if active_features:
        for branch in sorted(active_features, key=lambda b: b.last_commit_date or ""):
            age = tracker._format_age(branch.last_commit_date) if branch.last_commit_date else "unknown"
            print(f"  - {branch.name} ({branch.idea_id or 'no IDEA'}) - {age}")
    else:
        print("  (none)")
    
    print()
    print(f"Active Hotfix Branches: {len(active_hotfixes)}")
    if active_hotfixes:
        for branch in sorted(active_hotfixes, key=lambda b: b.last_commit_date or ""):
            age = tracker._format_age(branch.last_commit_date) if branch.last_commit_date else "unknown"
            print(f"  - {branch.name} - {age}")
    else:
        print("  (none)")
    
    if merged:
        print()
        print(f"Merged Branches (pending deletion): {len(merged)}")
        for branch in merged[:5]:
            print(f"  - {branch.name}")
        if len(merged) > 5:
            print(f"  ... and {len(merged) - 5} more")
    
    if stale:
        print()
        print(f"Stale Branches (>30 days): {len(stale)}")
        for branch in stale[:5]:
            print(f"  - {branch.name}")
        if len(stale) > 5:
            print(f"  ... and {len(stale) - 5} more")


def print_ideas_status():
    """Show ideas/backlog status"""
    print_header("IDEAS STATUS")
    
    tracker = ExecutionTracker()
    ideas = tracker._parse_ideas_backlog()
    
    status_counts = {}
    for idea in ideas:
        status = idea.status
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print(f"Total IDEAS: {len(ideas)}")
    print()
    print("By Status:")
    for status, count in sorted(status_counts.items()):
        icon = {"IMPLEMENTED": "[x]", "IN_PROGRESS": "[-]", "ACCEPTED": "[ ]"}.get(status, "[ ]")
        print(f"  {icon} {status}: {count}")
    
    print()
    print("Recent IMPLEMENTED:")
    implemented = [i for i in ideas if i.status == "IMPLEMENTED"][-5:]
    for idea in implemented:
        print(f"  - {idea.idea_id}: {idea.title[:50]}...")
        if idea.implementation_commit:
            print(f"    Commit: {idea.implementation_commit}")


def print_sync_report(idea_id: str = None):
    """Show sync detection report"""
    if idea_id:
        print_header(f"SYNC REPORT: {idea_id}")
        detector = SyncDetector()
        report = detector.detect_sync(idea_id)
        print(report.to_markdown())
    else:
        print_header("FULL SYNC SCAN")
        detector = SyncDetector()
        results = detector.full_scan()
        
        if not results:
            print("No active ideas with overlaps detected.")
            return
        
        print(f"Scanned {len(results)} active ideas")
        print()
        
        for idea_id, report in results.items():
            print(f"## {idea_id}")
            print(report.to_markdown())
            print()


def print_progress():
    """Show progress.md status"""
    print_header("PROGRESS STATUS")
    
    tracker = ExecutionTracker()
    state = tracker._read_progress_file()
    
    if not state.get("exists"):
        print("progress.md not found")
        return
    
    checkboxes = state.get("checkboxes", {})
    
    todo = [k for k, v in checkboxes.items() if v == " "]
    done = [k for k, v in checkboxes.items() if v == "x"]
    in_progress = [k for k, v in checkboxes.items() if v == "-"]
    
    print(f"Completed: {len(done)}")
    print(f"In Progress: {len(in_progress)}")
    print(f"Pending: {len(todo)}")
    print()
    
    if done:
        print("Done:")
        for item in done[:10]:
            print(f"  [x] {item[:60]}")
    if in_progress:
        print("In Progress:")
        for item in in_progress[:10]:
            print(f"  [-] {item[:60]}")


def print_execution_draft():
    """Generate and show execution draft"""
    print_header("EXECUTION REPORT DRAFT")
    
    tracker = ExecutionTracker()
    draft = tracker.generate_draft()
    
    print(draft.to_markdown())
    
    print()
    print("=" * 60)
    print("To commit this draft to DOC-3:")
    print("  tracker.commit_to_doc3(draft, approved=True)")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Ideas Dashboard — Unified CLI")
    parser.add_argument("--branches", "-b", action="store_true", help="Show branch status")
    parser.add_argument("--ideas", "-i", action="store_true", help="Show ideas status")
    parser.add_argument("--sync", "-s", metavar="IDEA", help="Show sync report for IDEA")
    parser.add_argument("--full-scan", "-f", action="store_true", help="Run full sync scan")
    parser.add_argument("--progress", "-p", action="store_true", help="Show progress status")
    parser.add_argument("--execution", "-e", action="store_true", help="Generate execution draft")
    
    args = parser.parse_args()
    
    # If no args, show full dashboard
    if len(sys.argv) == 1:
        print_header(f"IDEAS DASHBOARD — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
        print()
        print_branches()
        print()
        print_ideas_status()
        print()
        print_progress()
        return
    
    # Show specific views
    if args.branches:
        print_branches()
    if args.ideas:
        print_ideas_status()
    if args.sync:
        print_sync_report(args.sync)
    if args.full_scan:
        print_sync_report()
    if args.progress:
        print_progress()
    if args.execution:
        print_execution_draft()


if __name__ == "__main__":
    main()
