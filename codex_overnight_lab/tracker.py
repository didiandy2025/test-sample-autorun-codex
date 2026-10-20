"""AI / Robotics job dashboard exercise.

This file is deliberately unfinished. Your coding agent should complete it.
Only Python standard library is allowed.
"""


def load_jobs(path):
    """Read CSV, validate fields, normalize records, de-duplicate by newest date."""
    raise NotImplementedError('Agent task: implement load_jobs')


def score_job(job):
    """Return {score: int, verdict: str, reasons: list[str]} from SPEC.md."""
    raise NotImplementedError('Agent task: implement score_job')


def rank_jobs(jobs):
    """Return enriched jobs sorted by score, date, company, without mutation."""
    raise NotImplementedError('Agent task: implement rank_jobs')


def summarize_jobs(ranked):
    """Return dict with total, priority, consider, skip, avg_score."""
    raise NotImplementedError('Agent task: implement summarize_jobs')


def build_html(ranked):
    """Return complete standalone HTML for an offline searchable dashboard."""
    raise NotImplementedError('Agent task: implement build_html')
