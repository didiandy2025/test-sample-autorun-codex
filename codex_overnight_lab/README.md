# Codex Cloud Overnight Lab（中文版操作指南）

## 目标

学习一次性交付任务给 **Codex Cloud**，然后关掉 Mac。第二天通过 GitHub / Codex 任务审查代码、自动化测试证据和生成的成品。

此项目使用 25 条虚构的 AI / Robotics 工作数据。`tracker.py` 故意没有写完；`tests/test_tracker.py` 包含 20 项测试。成功时会生成：

- `output/report.html`：本地可打开的搜索/筛选网页。
- `output/morning_summary.md`：匹配度统计总结。
- `output/AGENT_REPORT.md`：Agent 自己留下的任务、测试、问题和风险总结。

### 为什么用 Codex Cloud？

Codex Cloud 在 OpenAI 的云端环境工作；任务启动后，Mac 合盖/关闭仍可以继续。不要在 Mac 本地 Terminal 仅运行 `codex` 后就关机，那是另一种运行方式。

## 无需写 Git 命令的启动法

### 1. 用浏览器上传到 GitHub

1. 解压 ZIP，打开得到的 `codex_overnight_lab` 文件夹。
2. 打开 https://github.com/new ，创建一个全新的 **Private** 仓库，推荐名 `codex-overnight-lab`。可以先不初始化 README。
3. 在新仓库网页里选 **Add file → Upload files**（空仓库首页也有 upload an existing file）。
4. **把解压文件夹内的内容拖进去，而不是把 ZIP 压缩包拖进去。** 核查 GitHub 的文件列表结构：`AGENTS.md`、`SPEC.md`、`tracker.py`、`build.py`、`tests/test_tracker.py` 和 `data/jobs.csv` 都要存在。它们应位于仓库根目录或对应子目录。
5. 选择 **Commit changes** 保存。浏览器可能隐藏 `.gitignore` 之类的隐藏文件，不影响此实验。

Github 官方上传说明：https://docs.github.com/en/repositories/working-with-files/managing-files/adding-a-file-to-a-repository

### 2. 创建 Codex Cloud 环境

1. 打开 https://chatgpt.com/codex 并登录同一个 ChatGPT 账号。
2. 在新任务选择 **Work in → Cloud**，然后 **Select environment → Create environment**。
3. 如果提示连接 GitHub，授权刚刚创建的练习仓库（最好只授权这一仓库）。
4. 选择仓库，点击 **Get started**，让 Codex 为 Python 3 项目准备环境。此项目没有第三方依赖或 secrets，网络权限无须打开。
5. 环境配置阶段可能跑出红色测试：**这是预期的**，因为 `tracker.py` 尚未实现。只要 Python 3 可以执行且仓库文件齐全，环境就可准备好并 **Publish**。不要在环境初始化阶段把实现任务提前做完。

操作参照：https://learn.chatgpt.com/docs/environments/cloud-environments

### 3. 只发一次消息

选择刚发布的 Cloud 环境，在 **Code / Do anything** 类型任务中发送：

> 阅读仓库根目录 `AGENTS.md`、`SPEC.md` 和 `CODEX_CLOUD_PROMPT.md`。按照 `CODEX_CLOUD_PROMPT.md` 全部要求自主完成项目，不要每一步向我确认。实际运行测试，持续修复直到符合验收标准或者碰到明确阻碍。把 `output/` 下三个成品保存到任务代码改动中；完成后给我一个中文工作总结，若可用则提交一个待我审查、不要自动合并的 PR。

确认任务显示正在云端执行后，可关闭本地 Mac。

### 4. 第二天怎么验收

1. 回到 Codex 原任务查看状态，不要创建新任务寻找旧文件。
2. 查看修改差异 (diff)，尤其 `tracker.py` 是否真正补全。
3. 看 Codex 实际运行的 `python3 -m unittest discover -s tests -v` 和 `python3 build.py` 的输出，而不是只看它声称通过的总结。
4. 查看 `output/AGENT_REPORT.md`。从生成的改动 / PR 下载 `output/report.html` 在本地浏览器打开，手动尝试搜索和过滤。
5. 如果没完全通过，在同一云任务追问它继续修复；如果满意，再决定是否合并 PR。

## 文件介绍

- `AGENTS.md`：Codex 默认会读到的仓库级执行规则。
- `SPEC.md`：需求、详细评分规则与验收标准。
- `CODEX_CLOUD_PROMPT.md`：一次性交付的任务指令。
- `tracker.py`：Agent 需要实现的核心代码（故意未完成）。
- `build.py`：从 CSV 构建网页和汇总报告的入口。
- `data/jobs.csv`：虚构示例。
- `tests/test_tracker.py`：验收测试，**不要修改**。

## 注意

- 新云环境 **目前不支持直接在云端操作浏览器**，所以 UI 搜索/筛选的最后人工体验，建议下载 HTML 到 Mac 浏览器里操作；自动化测试可以在云环境直接运行。
- 这是学习实验，不需要上传公司代码、账户凭据或真实简历。Codex Cloud 可在机器关机后工作，但完成任务/碰到执行上限时会停止，不是必须运行八小时。
- 生成文件 `output/*.html` / `output/*.md` 必须保留在 Git 变更中，方便你在云端验收，**不要把它们加入 `.gitignore`**。
