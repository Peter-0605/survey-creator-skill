# survey-creator-skill

[English](./README.md) | 简体中文

**一个面向 AI 问卷生成场景的 schema 安全约束与合法性交付管线。**

`survey-creator-skill` 是一个开源的 skill + 工具链，用来把结构化问卷 schema 生成成可提交的 HTML 问卷页面，并在交付前完成整套合法性校验。

它不只是“生成 HTML”，还包括：

- 校验问卷 schema 的结构与字段合法性
- 修复安全范围内可自动修复的问题
- 渲染可提交的 HTML 问卷页面
- 通过浏览器运行时 / E2E 检查空白页与关键交互
- 校验可访问性
- 校验提交 payload 协议
- 校验 payload 与具体 schema 的一一对应关系

如果你希望 AI 生成问卷时，**不是只出一个能看但不一定能交付的页面**，而是得到一套可校验、可提交、可回收数据的结果，这个项目就是为此设计的。

---

## 为什么要做这个项目

很多“AI 表单 / AI 问卷生成器”只做到：

- 生成一份 JSON
- 渲染一份 HTML
- 假设提交数据大概率没问题

但真实业务场景里，这远远不够。

问卷系统至少要保证：

- schema 合法
- id 唯一且稳定
- 逻辑不会破坏必填校验
- 被隐藏 / 跳过的题目不会混进提交结果
- 页面不会打开白屏
- 交互可在浏览器里真实跑通
- 提交 payload 必须和当前问卷 schema 严格一致

`survey-creator-skill` 解决的就是这整条链路。

---

## 项目包含什么

### 1. Skill 层
- `SKILL.md`
- 基于自然语言理解生成问卷 schema
- schema-first 工作流
- legality-first 交付原则

### 2. Reference 层
- schema 说明
- 各题型字段说明
- 富文本规则
- 分页规则
- child 输入规则
- local cache 规则
- logic 规则与示例
- submission contract

### 3. Runtime 层
- 固定 HTML 模板
- 前端步进流转
- 显隐 / 跳题 / 跳页 / 结束逻辑
- 本地缓存处理
- payload 组装

### 4. Validation 层
- schema 校验
- schema 自动修复
- HTML runtime 校验
- HTML E2E 校验
- HTML 交互 E2E 校验
- accessibility 校验
- payload 校验
- payload-against-schema 校验
- reference consistency 校验

---

## 当前支持的题型 / 节点

- survey
- radio
- checkbox
- input
- score
- nps
- Pagination
- finish

---

## 当前支持的核心能力

- 欢迎页 / 结束页
- 单选 / 多选 / 输入题
- 评分题 / NPS 题
- child 输入
- 富文本 title / description
- media（image / video / audio）
- onePageOneQuestion
- allowBack
- localStorage 步进缓存
- 提交后清空缓存
- 必填校验
- 逻辑控制：
  - show_question
  - hide_question
  - show_option
  - hide_option
  - auto_select_option
  - jump_to_question
  - jump_to_page
  - end_survey
- 隐藏 / 跳过题目的 required 自动豁免
- 逻辑冲突按“后触发覆盖前触发”执行

---

## 适合哪些场景

- AI 生成问卷
- 满意度调查
- 报名问卷
- 用户研究
- 产品反馈收集
- 筛选 / 分流式问卷
- NPS / 评分 / 调研场景

---

## 仓库结构

```text
survey-creator-skill/
├── SKILL.md
├── README.md
├── README.zh-CN.md
├── references/
├── templates/
├── validators/
├── tests/
├── evals/
```

---

## 如何安装

### 方式 1：作为本地 skill 使用

把仓库放到你的 skill 目录，例如：

- `~/.codex/skills/survey-creator-skill`
- `~/.agents/skills/survey-creator-skill`

建议安装方式：

```bash
git clone <your-repo-url> ~/.codex/skills/survey-creator-skill
cd ~/.codex/skills/survey-creator-skill/validators
npm install
npx playwright install
```

当前 Python 校验脚本主要依赖标准库，不需要额外安装 Python 包。

### 方式 2：作为独立工具链使用

即使你的 Agent 系统不支持 skill 机制，也可以直接把它当成一个结构化问卷生成 / 校验管线来用。主入口命令：

```bash
python3 validators/run_survey_creator_pipeline.py \
  --schema /absolute/path/to/schema.json \
  --output-dir /absolute/path/to/out \
  --auto-repair \
  --fail-on-high-warning
```

这会输出：

- repaired schema
- HTML 页面
- sample payload
- pipeline report

### 依赖要求

- Python 3.10+
- Node.js 18+
- Playwright 浏览器

安装浏览器自动化依赖：

```bash
cd validators
npm install
npx playwright install
```

---

## 如何使用

在支持 skill 的 Agent 环境里，直接在 prompt 中调用：

> Use `survey-creator-skill` to generate a survey HTML page, validate the schema, render the HTML, and verify payload correctness before returning the result.

如果你想要中文描述，也可以直接说明业务目标、投放渠道、UI 风格、题型要求和逻辑需求。

---

## 文档入口

- 英文 README：[README.md](./README.md)
- GitHub 项目简介：[docs/GITHUB_OVERVIEW.md](./docs/GITHUB_OVERVIEW.md)
- 合法性保证：[LEGALITY_GUARANTEE.md](./LEGALITY_GUARANTEE.md)
- 合法性矩阵：[LEGALITY_MATRIX.md](./LEGALITY_MATRIX.md)

---

## License

MIT
