"""Acceptance tests intentionally shipped before implementation (red -> green)."""
import csv
import subprocess
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from tracker import load_jobs, score_job, rank_jobs, summarize_jobs, build_html

ROOT = Path(__file__).resolve().parents[1]
FIELDS = ['company', 'title', 'sector', 'location', 'work_mode', 'salary_min_k', 'posted_date']


def sample_job(**changes):
    job = {
        'company': 'Helix Labs',
        'title': 'Staff Technical Program Manager',
        'sector': 'Robotics',
        'location': 'San Mateo',
        'work_mode': 'Hybrid',
        'salary_min_k': 280,
        'posted_date': '2026-10-14',
    }
    job.update(changes)
    return job


def make_csv(folder, entries, fields=FIELDS, encoding='utf-8'):
    path = Path(folder) / 'jobs.csv'
    with path.open('w', newline='', encoding=encoding) as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        for item in entries:
            writer.writerow(item)
    return path


class TestLoadJobs(unittest.TestCase):
    def test_reads_csv_with_bom_and_trims_fields(self):
        with tempfile.TemporaryDirectory() as d:
            p = make_csv(d, [dict(company='  Alpha  ', title='Senior EPM', sector=' AI ',
                location='San Jose', work_mode='Hybrid', salary_min_k='250',
                posted_date='2026-10-16')], encoding='utf-8-sig')
            jobs = load_jobs(p)
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0]['company'], 'Alpha')
            self.assertEqual(jobs[0]['sector'], 'AI')
            self.assertEqual(jobs[0]['salary_min_k'], 250)

    def test_blanks_and_optional_salary(self):
        with tempfile.TemporaryDirectory() as d:
            p = make_csv(d, [dict(company='Beta', title='Program Manager', sector='Other',
                location='Seattle', work_mode='Remote', salary_min_k='',
                posted_date='2026-10-15')])
            jobs = load_jobs(p)
            self.assertIsNone(jobs[0]['salary_min_k'])

    def test_latest_duplicate_wins(self):
        with tempfile.TemporaryDirectory() as d:
            old = dict(company='Helix', title='Staff TPM', sector='AI', location='San Mateo',
                       work_mode='Hybrid', salary_min_k='230', posted_date='2026-10-14')
            new = dict(old, company=' helix ', title='STAFF TPM', location=' SAN MATEO ',
                       salary_min_k='295', posted_date='2026-10-17')
            p = make_csv(d, [old, new])
            jobs = load_jobs(p)
            self.assertEqual(len(jobs), 1)
            self.assertEqual(jobs[0]['salary_min_k'], 295)
            self.assertEqual(jobs[0]['posted_date'], '2026-10-17')

    def test_missing_header_raises_helpful_error(self):
        with tempfile.TemporaryDirectory() as d:
            fields = [name for name in FIELDS if name != 'posted_date']
            p = make_csv(d, [], fields=fields)
            with self.assertRaisesRegex(ValueError, 'posted_date'):
                load_jobs(p)

    def test_invalid_salary_raises(self):
        with tempfile.TemporaryDirectory() as d:
            job = sample_job(salary_min_k='a lot')
            p = make_csv(d, [job])
            with self.assertRaises(ValueError):
                load_jobs(p)

    def test_invalid_date_raises(self):
        with tempfile.TemporaryDirectory() as d:
            job = sample_job(posted_date='2026-02-30')
            p = make_csv(d, [job])
            with self.assertRaises(ValueError):
                load_jobs(p)

    def test_tie_duplicate_keeps_first(self):
        with tempfile.TemporaryDirectory() as d:
            one = sample_job(salary_min_k=200)
            two = sample_job(salary_min_k=300)
            p = make_csv(d, [one, two])
            result = load_jobs(p)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['salary_min_k'], 200)


class TestScore(unittest.TestCase):
    def test_high_fit_is_100(self):
        score = score_job(sample_job())
        self.assertEqual(score['score'], 100)
        self.assertEqual(score['verdict'], 'PRIORITY')
        self.assertGreaterEqual(len(score['reasons']), 4)

    def test_general_program_manager_has_15_not_35(self):
        score = score_job(sample_job(title='Program Manager', sector='Consumer',
                        location='Seattle', work_mode='Onsite', salary_min_k=None))
        self.assertEqual(score['score'], 0)  # 15 - 20 floored at zero
        self.assertEqual(score['verdict'], 'SKIP')

    def test_junior_penalty(self):
        score = score_job(sample_job(title='Junior Technical Program Manager', salary_min_k=160))
        self.assertEqual(score['score'], 20)  # 35 + 25 + 10 - 50
        self.assertEqual(score['verdict'], 'SKIP')

    def test_remote_outside_bay_area_has_location_points_without_onsite_penalty(self):
        score = score_job(sample_job(title='Staff TPM', location='Austin',
                        work_mode='Remote', sector='Robotics', salary_min_k=240))
        self.assertEqual(score['score'], 90)  # 35 + 20 + 25 + 10

    def test_onsite_outside_bay_area_penalty(self):
        score = score_job(sample_job(title='Senior Technical Program Manager',
                        location='Austin', work_mode='Onsite', salary_min_k=260))
        self.assertEqual(score['score'], 70)  # 35 + 20 + 25 + 10 - 20
        self.assertEqual(score['verdict'], 'PRIORITY')

    def test_keyword_boundaries_and_case_insensitive(self):
        score = score_job(sample_job(title='staff epm', sector='ROBOTICS',
                        location='san mateo', salary_min_k=249))
        self.assertEqual(score['score'], 90)

    def test_no_mutation_and_empty_reasons_fallback(self):
        job = sample_job(title='Analyst', sector='Consumer',
                         location='Remote - US', work_mode='Remote', salary_min_k=None)
        original = deepcopy(job)
        res = score_job(job)
        self.assertEqual(job, original)
        self.assertEqual(res['score'], 10)
        self.assertTrue(res['reasons'])


class TestRankAndSummary(unittest.TestCase):
    def test_sorted_by_score_then_newest_date(self):
        older = sample_job(company='Older', posted_date='2026-10-11')
        newer = sample_job(company='Newer', posted_date='2026-10-16')
        low = sample_job(company='Low', title='Analyst', sector='Consumer',
                         salary_min_k=None, work_mode='Onsite')
        result = rank_jobs([older, low, newer])
        self.assertEqual([x['company'] for x in result], ['Newer', 'Older', 'Low'])
        self.assertEqual(result[0]['score'], 100)
        self.assertIn('reasons', result[0])

    def test_alpha_tiebreaker_and_no_mutation(self):
        b = sample_job(company='Beta')
        a = sample_job(company='Alpha')
        originals = deepcopy([b, a])
        output = rank_jobs([b, a])
        self.assertEqual([j['company'] for j in output], ['Alpha', 'Beta'])
        self.assertEqual([b, a], originals)

    def test_summary_and_empty_summary(self):
        ranked = [{'score': 95, 'verdict':'PRIORITY'},
                  {'score': 55, 'verdict':'CONSIDER'},
                  {'score': 10, 'verdict':'SKIP'}]
        stats = summarize_jobs(ranked)
        self.assertEqual((stats['total'], stats['priority'], stats['consider'], stats['skip']),
                         (3, 1, 1, 1))
        self.assertAlmostEqual(stats['avg_score'], 160/3, places=1)
        self.assertEqual(summarize_jobs([])['avg_score'], 0)


class TestHTML(unittest.TestCase):
    def test_standalone_html_and_controls(self):
        ranked = rank_jobs([sample_job()])
        content = build_html(ranked)
        self.assertTrue(content.lstrip().lower().startswith('<!doctype html>'))
        self.assertIn('id="search"', content)
        for key in ('ALL', 'PRIORITY', 'CONSIDER', 'SKIP'):
            self.assertIn(f'data-filter="{key}"', content)
        self.assertIn('Helix Labs', content)
        self.assertIn('Demo', content)

    def test_escapes_dynamic_text_and_offline_only(self):
        hostile = sample_job(company='<script>alert(1)</script>',
                             title='Staff TPM & EPM "special"')
        content = build_html(rank_jobs([hostile]))
        self.assertNotIn('<script>alert(1)</script>', content)
        self.assertIn('&lt;script&gt;alert(1)&lt;/script&gt;', content)
        self.assertIn('&amp;', content)
        self.assertNotIn('https://', content)
        self.assertNotIn('http://', content)
        self.assertNotIn('<script src=', content)

    def test_build_cli_end_to_end(self):
        with tempfile.TemporaryDirectory() as d:
            dataset = make_csv(d, [dict(sample_job(), salary_min_k='280')])
            report = Path(d) / 'output' / 'report.html'
            proc = subprocess.run([sys.executable, str(ROOT / 'build.py'),
                '--input', str(dataset), '--output', str(report)],
                cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, msg=proc.stdout+'\n'+proc.stderr)
            self.assertTrue(report.exists())
            self.assertIn('Helix Labs', report.read_text(encoding='utf-8'))
            summary = report.parent / 'morning_summary.md'
            self.assertTrue(summary.exists())
            self.assertIn('总职位：1', summary.read_text(encoding='utf-8'))


if __name__ == '__main__':
    unittest.main()
