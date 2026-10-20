# Project Spec — AI / Robotics 职位匹配看板（练习用）

## 产品目标
用户给你一个 CSV，你实现一个**本地、离线、能直接在浏览器打开**的 HTML 职位看板。
不用接真实招聘网站；`data/jobs.csv` 全都是**虚构示例数据**，并不代表实际招聘。
程序不能访问网络，也不需要安装任何 pip package。

## 输入 CSV
表头必须是：`company,title,sector,location,work_mode,salary_min_k,posted_date`。
- 读入时去掉每个字段首尾空格；支持 UTF-8 BOM（`utf-8-sig`）。
- 缺少任意必须列，抛 `ValueError`，说明缺哪一列。
- 空白行跳过。
- `salary_min_k` 是薪资下限，单位为千美元；允许留空（转换为 `None`），否则必须是非负整数。不合格抛 `ValueError`。
- `posted_date` 使用合法 `YYYY-MM-DD` ISO 日期，非法值抛 `ValueError`。
- 用 `(company,title,location)` 三列小写且去空格后作为去重键；重复时保留 `posted_date` 最新的记录，日期相同时保留先出现的记录。
- 输出每条职位为 dict，保留前述七个字段，`salary_min_k` 是 `int | None`。

## 匹配评分（必须严格遵循，方便自动验收）
使用大小写不敏感匹配，计算分值与可阅读的评分原因。
1. Title 包含 `technical program manager`、`engineering program manager`、独立单词 `TPM` 或 `EPM`：**+35**。否则，包含 `program manager` 或 `product manager`：**+15**。这两种不叠加。
2. Title 出现独立单词 `senior`、`staff`、`principal` 或 `lead`：**+20**，只加一次。
3. Sector（整格）为 `AI`、`Robotics`、`Autonomy`、`AI Infrastructure` 或 `Infrastructure`：**+25**。
4. Location 包含以下任一湾区地名：`San Francisco`、`San Jose`、`Sunnyvale`、`Palo Alto`、`Milpitas`、`Redwood City`、`Foster City`、`San Mateo`、`Mountain View`、`Menlo Park`、`Santa Clara`、`Cupertino`、`Bay Area`，或者 `work_mode=Remote`，或者 location 含 `Remote`：**+10**，只加一次。
5. `salary_min_k >= 250`：**+10**。
6. Title 有独立单词 `intern`、`junior`、`entry`、`associate`：**-50**，只扣一次。
7. `work_mode=Onsite` **且** Location 不在湾区（第 4 条的湾区名单）时：**-20**。
8. 最终分数不小于 0。

`score_job(job)` 返回 `{ "score": int, "verdict": str, "reasons": list[str] }`。
`reasons` 必须为人类可读的简短解释，至少解释每个生效的规则。无规则生效时给一条原因。

- `score >= 70`: verdict = `PRIORITY`
- `40 <= score < 70`: verdict = `CONSIDER`
- `score < 40`: verdict = `SKIP`

## 排名和汇总
- `rank_jobs(jobs)` 为每条记录合并 `score`, `verdict`, `reasons` 字段。
- 排序优先级：`score` 降序 → `posted_date` 降序 → `company` 字母序（大小写不敏感）。不修改传入 list 或 dict。
- `summarize_jobs(ranked)` 返回 `total`, `priority`, `consider`, `skip`, `avg_score`；平均分保留至少一位小数。空列表平均分是 0。

## HTML 看板
- `build_html(ranked)` 返回完整 HTML（以 `<!doctype html>` 开始，大小写随意）。简洁、现代、适合手机浏览。
- 展示：总数、PRIORITY / CONSIDER / SKIP 三个数量；每条职位的 Company, Title, Sector, Location, Work mode, Salary, Score, Verdict, Reasons, Date。
- 按照传入的排名顺序渲染。
- 页面顶端有可输入搜索框 `id="search"`，支持按公司或职位标题过滤。
- 页面有可切换的按钮：`data-filter="ALL"`、`data-filter="PRIORITY"`、`data-filter="CONSIDER"`、`data-filter="SKIP"`；通过浏览器内联 JS 在本地过滤，无需后端。
- **防止 HTML 注入/XSS**：CSV 所有动态文本必须正确 escape，包括 `<script>`、引号、`&` 等。
- 不依赖外部 CDN、外部 JS / CSS、网络请求、第三方资源，不输出虚构的招聘链接。可用内联 `<style>` 和 `<script>`（自己写的静态 JS）。
- 标注「虚构演示数据 / Demo only」。

## 验收命令
全部在项目文件夹根目录执行：

```bash
python3 -m unittest discover -s tests -v
python3 build.py
```

成功必须同时满足：
1. 所有自动化测试通过。
2. 生成 `output/report.html`，可双击在浏览器打开；搜索、筛选功能有效。
3. 生成 `output/morning_summary.md`。
4. Agent 额外创建 `output/AGENT_REPORT.md`，记录完成了哪些功能、实际执行的测试结果、自己发现并修复了什么、还存在哪些疑点；没有测试通过就不能谎报成功。
5. 不更改 `tests/` 内测试来让它变绿；不绕过失败、不隐藏错误。
