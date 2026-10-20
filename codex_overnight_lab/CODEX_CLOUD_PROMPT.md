# Codex Cloud — 一次性的无人值守任务指令

你是负责独立交付的 coding agent。请从根目录起先读 `AGENTS.md`、`SPEC.md`、`tracker.py`、`build.py`、`tests/test_tracker.py` 与 `data/jobs.csv`。

目标：把刻意未完成的 AI / Robotics 职位匹配看板写成可以直接交付的离线工具：读取 CSV、清洗和去重、按给定规则评分排序、生成可搜索/筛选的独立 HTML 页面、生成汇总和 Agent 工作报告。

严格执行以下循环，而不是完成一小步就等待用户：

1. 先运行 `python3 -m unittest discover -s tests -v`，记录初始化失败（这些失败本来就是练习的一部分）。
2. 自主制定实现顺序，完成 `tracker.py` 中各函数。可以修改 `build.py` 的真正代码 Bug，但不得更改验收标准和现有测试。
3. 每次修改后，重新运行测试。如果失败，定位、修复、再跑。最多 12 轮测试/修复；若连续 3 轮没有进展，记录问题并停止。
4. 所有测试通过后执行 `python3 build.py`，确保 `output/report.html` 与 `output/morning_summary.md` 存在。
5. 再自行做一次独立 code review，尤其检查 HTML 文本 escape / XSS、字段校验、排序、不修改传入的数据、浏览器内联 JS 搜索/过滤。发现实际 Bug 就修并重新测试。
6. 写 `output/AGENT_REPORT.md`，告诉明天验收的人：实现了哪些功能、确切测试命令和结果、你主动修复的缺陷、仍未解决的问题、如何打开 HTML 验收。
7. 确保 `output/` 下三个成品文件随代码改动一起保留在任务中（不要 gitignore）。可以创建供用户审查的 PR，但不要自行 merge。

约束：只允许当前仓库、纯 Python 3 标准库、纯本地静态 HTML/CSS/JS；禁止访问互联网、安装依赖、部署、接触真实招聘/个人信息、修改 `tests/`、伪造通过结果。

当达到验收条件、到达修复轮数上限或确实被阻挡时再结束。在整个过程中你不需要等待用户逐步下命令。
