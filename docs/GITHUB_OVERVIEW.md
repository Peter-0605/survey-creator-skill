# GitHub project overview

## English

### Short description

Schema-safe survey generator and legality pipeline for AI-driven questionnaire creation.

### One-paragraph intro

`survey-creator` is an open-source skill and toolchain for building production-safe survey experiences from structured schema. It does more than render HTML: it validates schema legality, repairs safe issues, renders submittable survey pages, verifies runtime behavior in browser E2E, checks interaction flow, validates accessibility, and guarantees that submitted payloads conform to the exact survey schema. It is especially useful for AI-assisted survey generation, AI Native form workflows, and teams that want stronger guardrails before shipping questionnaires to real users.

### Key features

- Schema validation for survey structure and field legality
- HTML rendering from validated schema
- Runtime/browser E2E verification
- Accessibility validation
- Payload contract validation
- Payload-against-schema validation
- Logic support for show/hide, jump, end, auto-select, and conflict resolution
- Required exemption for hidden/skipped questions
- Cache cleanup and payload cleanup guarantees
- Contract tests for high-risk logic scenarios

### Best for

- AI-generated surveys
- Feedback forms
- Registration questionnaires
- Screening/qualification flows
- NPS / score / satisfaction research
- Teams that need legality guardrails before shipping survey HTML

### Suggested GitHub tagline

**Schema-safe survey generator and validation pipeline for AI-driven questionnaire creation**

---

## 中文

### 短描述

一个面向 AI 问卷生成场景的 schema 安全约束与合法性交付管线。

### 一段话介绍

`survey-creator` 是一个开源的 skill + 工具链，用来把结构化问卷 schema 生成成可提交的 HTML 问卷页面，并在交付前完成整套合法性校验。它不只是“生成页面”，还包括：schema 校验、安全修复、HTML 渲染、浏览器运行时检查、交互 E2E、可访问性验证、payload 合法性校验，以及“提交数据必须与具体问卷 schema 完全一致”的最终兜底。它尤其适合 AI 辅助生成问卷、AI Native 表单流程，以及任何希望在真实投放前把风险拦在上线前的团队。

### 核心能力

- 问卷 schema 合法性校验
- 基于已校验 schema 渲染 HTML
- 浏览器运行时与 E2E 校验
- 可访问性校验
- payload 协议校验
- payload 与具体 schema 一致性校验
- 支持显隐、跳题、跳页、提前结束、自动勾选等逻辑能力
- 隐藏/跳过题 required 自动豁免
- 本地缓存与提交数据自动清理
- 高风险逻辑场景的 contract tests

### 适用场景

- AI 生成问卷
- 满意度调查
- 报名问卷
- 线索收集
- 筛选式问卷
- NPS / 评分 / 产品调研

### 建议的 GitHub 首页一句话

**一个面向 AI 问卷生成场景的 schema 安全约束与合法性交付管线**

