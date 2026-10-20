# Overnight Codex Cloud Lab — working agreements

## Purpose
This is a deliberately unfinished, self-contained **offline learning exercise**. All job listings are fictitious examples. Read `SPEC.md` and `CODEX_CLOUD_PROMPT.md` before making changes.

## Safety and scope
- Only inspect or edit this repository. Never access other GitHub repositories, connected apps, secrets, account settings, SSH keys, environment credentials, or personal files.
- Do not use the internet, scrape real job sites, download dependencies, install packages, deploy or run production services.
- Python 3 standard library only. No third-party dependencies, keys, credentials or external service connections needed.
- **Never modify, delete, skip, or weaken tests in `tests/`; never alter `data/jobs.csv` to pass tests.** All test failures must be fixed in implementation.
- Don't push/merge directly to `main`; keep work in the isolated task. You can propose a pull request if available, but leave it unmerged for review.
- Store generated deliverables in `output/` as tracked files, so they appear in the task diff / eventual PR. Do not add these artifacts to `.gitignore`.
- If an operation is blocked by environment permissions, don't bypass the restriction: document the blocker and stop.

## Work autonomously
1. Read the spec, initial implementation and tests; first run the exact baseline test command and record its failures.
2. Implement, rerun tests, analyze failures and keep fixing without waiting for a human response.
3. Once tests pass, run `python3 build.py`; review generated HTML for validity and basic offline search/filter JavaScript logic (Cloud may not offer a browser preview).
4. Independently review for edge cases, XSS escaping, consistent sorting, data mutation and error handling; if you find problems, repair and retest.
5. Produce `output/AGENT_REPORT.md` with a truthful test summary, work done, defects fixed, residual risks and exact morning checklist.
6. Maximum 12 test/fix iterations; stop after three consecutive iterations with no meaningful improvement, or after meeting all acceptance criteria. Never claim success without running tests.

## Commands
- Tests: `python3 -m unittest discover -s tests -v`
- Generate report: `python3 build.py`

## Communication
- Do not ask routine clarifying questions; choose reasonable defaults and record assumptions.
- Explain final status in clear Chinese with links to the files changed when possible.
