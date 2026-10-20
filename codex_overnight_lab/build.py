"""Command-line entry point. Agent should not need to change this file."""
import argparse
from pathlib import Path
from tracker import load_jobs, rank_jobs, build_html, summarize_jobs


def main():
    parser = argparse.ArgumentParser(description='Build a local AI & robotics job dashboard')
    parser.add_argument('--input', default='data/jobs.csv', help='CSV input')
    parser.add_argument('--output', default='output/report.html', help='HTML output path')
    args = parser.parse_args()

    ranked = rank_jobs(load_jobs(args.input))
    stats = summarize_jobs(ranked)
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_html(ranked), encoding='utf-8')

    summary = out_path.parent / 'morning_summary.md'
    summary.write_text(
        '# 早晨验收报告（程序自动生成）\n\n'
        f'- 总职位：{stats["total"]}\n'
        f'- 值得优先关注：{stats["priority"]}\n'
        f'- 值得考虑：{stats["consider"]}\n'
        f'- 暂不关注：{stats["skip"]}\n'
        f'- 平均匹配分：{stats["avg_score"]:.1f}\n'
        f'- HTML 报告：{out_path.name}\n',
        encoding='utf-8',
    )
    print(f'Created {out_path} ({stats["total"]} jobs).')
    print(f'Created {summary}.')


if __name__ == '__main__':
    main()
