#!/usr/bin/env python3
"""Unified entrypoint for the Q2BSTUDIO Auditor.

Pipeline (reproducible):
    scrape -> checkpoint -> analyze -> visualize -> (optional) archive

This wraps the existing modules:
    - q2b_studio_auditor.Q2BStudioAuditor
    - q2b_data_visualizer.Q2BDataVisualizer
    - wayback_archiver.WaybackArchiver

and exposes a simple CLI so journalists / researchers can run the whole
investigation with a single command.
"""

from __future__ import annotations

import argparse
import os
from datetime import datetime
from typing import Optional, Tuple

from q2b_data_visualizer import Q2BDataVisualizer
from q2b_studio_auditor import Q2BStudioAuditor
from wayback_archiver import WaybackArchiver


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------


def _select_or_create_output_dir(resume: bool) -> Tuple[Q2BStudioAuditor, int, int]:
    """Create an auditor and decide start/max page.

    - If resume is True, we try to auto-detect the latest checkpoint directory
      and resume from there.
    - If resume is False, we start a fresh run with a new timestamped directory.

    Returns:
        (auditor, start_page, max_page)
    """

    auditor = Q2BStudioAuditor(create_output_dir=not resume)

    if resume:
        # Find latest checkpoint directory matching q2b_audit_*
        candidates = [
            d
            for d in os.listdir(".")
            if os.path.isdir(d) and d.startswith("q2b_audit_")
        ]
        candidates.sort(reverse=True)

        if not candidates:
            print("[run.py] No checkpoint directories found, starting fresh instead.")
        else:
            latest = candidates[0]
            print(f"[run.py] Attempting to resume from checkpoint: {latest}")
            max_page_scraped = auditor.load_checkpoint(latest)
            if max_page_scraped:
                max_page = auditor.get_max_page_number()
                if not max_page:
                    raise SystemExit("Could not determine max page from site.")
                start_page = auditor.calculate_resume_page(max_page, articles_per_page=9)
                print(f"[run.py] Resuming from page {start_page} of {max_page}")
                return auditor, start_page, max_page
            else:
                print("[run.py] Failed to load checkpoint, falling back to fresh run.")

    # Fresh run path
    if auditor.output_dir is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        auditor.output_dir = f"q2b_audit_{timestamp}"
        os.makedirs(auditor.output_dir, exist_ok=True)
        print(f"[run.py] Created output directory: {auditor.output_dir}")

    max_page = auditor.get_max_page_number()
    if not max_page:
        raise SystemExit("Could not determine max page from site.")

    start_page = 1
    print(f"[run.py] Fresh run from page {start_page} to {max_page}")
    return auditor, start_page, max_page


# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------


def run_scrape(auditor: Q2BStudioAuditor, start_page: int, max_page: int, sample_every: int) -> None:
    """Run the scraping phase.

    Args:
        auditor: Initialized Q2BStudioAuditor instance.
        start_page: First page to scrape.
        max_page: Last page to scrape.
        sample_every: Scrape 1 of N pages (1 = all pages).
    """

    if start_page > max_page:
        print("[run.py] Nothing to scrape: start_page > max_page. Skipping scraping.")
        return

    pages_to_scrape = ((max_page - start_page) // sample_every) + 1
    print(
        f"[run.py] Scraping {pages_to_scrape} logical pages "
        f"({start_page} -> {max_page}, sample_every={sample_every})"
    )
    auditor.scrape_all_pages(max_page, start_page=start_page, sample_every=sample_every)



def run_analysis_and_visualization(auditor: Q2BStudioAuditor) -> None:
    """Generate report.json and graphs from the current auditor state."""

    report = auditor.generate_report()
    visualizer = Q2BDataVisualizer(input_dir=auditor.output_dir)
    visualizer.create_visualizations(report)
    print(f"[run.py] Analysis + visualizations complete in: {auditor.output_dir}")



def run_archiving(auditor: Q2BStudioAuditor, sample_size: int) -> None:
    """Archive a sample of articles to the Wayback Machine."""

    archiver = WaybackArchiver(auditor.output_dir)
    if not archiver.load_data():
        print("[run.py] Could not load CSV data, skipping archiving.")
        return

    print(f"[run.py] Archiving sample of {sample_size} articles to Wayback...")
    archiver.archive_sample(sample_size=sample_size)
    archiver.save_results()
    print("[run.py] Archiving complete.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Q2BSTUDIO Auditor – reproducible pipeline for scraping, "
            "analysis, visualization, and optional archiving."
        )
    )

    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from the latest q2b_audit_* checkpoint instead of starting fresh.",
    )

    parser.add_argument(
        "--visualize-only",
        action="store_true",
        help=(
            "Skip scraping and only regenerate report + graphs from the latest "
            "checkpoint (implies --resume)."
        ),
    )

    parser.add_argument(
        "--sample",
        type=int,
        default=1,
        metavar="N",
        help="Scrape every N-th page instead of all pages (default: 1 = all).",
    )

    parser.add_argument(
        "--archive",
        type=int,
        metavar="K",
        help=(
            "Archive a random sample of K articles to Wayback Machine after "
            "analysis is complete. If omitted, archiving is skipped."
        ),
    )

    return parser



def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    # Visualize-only implies resume
    resume_flag = args.resume or args.visualize_only

    auditor, start_page, max_page = _select_or_create_output_dir(resume=resume_flag)

    if args.visualize_only:
        print("[run.py] Visualization-only mode: no scraping will be performed.")
        run_analysis_and_visualization(auditor)
        if args.archive:
            run_archiving(auditor, sample_size=args.archive)
        return

    # Full pipeline: scrape -> analyze/visualize -> optional archive
    run_scrape(auditor, start_page=start_page, max_page=max_page, sample_every=args.sample)
    run_analysis_and_visualization(auditor)

    if args.archive:
        run_archiving(auditor, sample_size=args.archive)


if __name__ == "__main__":
    main()
