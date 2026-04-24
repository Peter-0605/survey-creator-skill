# survey-creator-skill 上线前验收 checklist

用于确认一份由 `survey-creator-skill` 生成的问卷，是否适合真正交付给用户填写。

---

## A. Schema 层
- [ ] schema 已生成并冻结，不再在浏览器 runtime 动态生成核心 id
- [ ] 已查看 schema validator 的语义 lint warnings，并确认没有未处理的 high severity 误用
- [ ] medium severity warning 均已人工确认可接受
- [ ] 已运行 `validate_survey_schema.py`
- [ ] 如启用自动修复，已运行 `auto_repair_survey_schema.py`
- [ ] 已确认自动修复没有改坏业务语义
- [ ] schema 校验结果为 valid=true
- [ ] 无 duplicate id
- [ ] 无 unsupported field
- [ ] 所有 question type 都在支持范围内：radio / checkbox / input / score / nps
- [ ] 所有 child 都是 `type: input`
- [ ] 所有 child / input 的 `dataType` 都合法
- [ ] `finish` 结构合法

## B. 富文本与安全
- [ ] rich text 已经过白名单 sanitizer
- [ ] rich text 只允许展示类元素（div/p/span/strong/em/ul/ol/li/a 等）
- [ ] 不允许 script/style/iframe/form/input/button 等元素
- [ ] link 已限制危险协议（如 javascript:）

## C. HTML Runtime 层
- [ ] 已运行 `validate_survey_html_runtime.py`
- [ ] 已运行 `validate_survey_html_e2e.py`，并确认 desktop / mobile viewports 均通过
- [ ] 已运行 `validate_survey_html_accessibility.py`，并确认 desktop / mobile viewports 均通过
- [ ] runtime 校验结果为 valid=true
- [ ] E2E smoke 校验结果为 valid=true
- [ ] desktop viewport 不白屏且存在 active screen
- [ ] mobile viewport 不白屏且存在 active screen
- [ ] desktop interaction E2E 可完整填写并提交
- [ ] mobile interaction E2E 可完整填写并提交
- [ ] 所有 input / textarea / select 都有可访问名称
- [ ] 所有 button 都有可访问名称
- [ ] score / nps 按钮包含 aria-pressed 状态
- [ ] 校验错误文案包含 role="alert" 或 aria-live
- [ ] 图片包含 alt，音频/视频包含 controls
- [ ] 页面存在真实 `<form>`
- [ ] 存在 `assemblePayload()`
- [ ] 存在 `validateQuestion()`
- [ ] 存在 child 显隐逻辑
- [ ] 存在 exclusive 逻辑
- [ ] 存在 mutual-exclusion 逻辑
- [ ] 存在 localStorage set/remove
- [ ] submit 会拦截并组装 payload
- [ ] 页面打开后不会白屏
- [ ] 页面无 `pageerror`

## D. 手工交互验证
- [ ] welcome → question → finish 流程可完整走通
- [ ] allowBack=true 时可返回上一页且数据不丢
- [ ] onePageOneQuestion=true 时一次只显示一个 screen
- [ ] radio 正常单选
- [ ] checkbox 正常多选
- [ ] exclusive 选项会清空其他项
- [ ] mutual-exclusion 只会互斥同组项
- [ ] 选中带 child 的选项后，child 正常显示
- [ ] 取消选中后，child 隐藏符合预期
- [ ] input / child 的 datatype 渲染正确
- [ ] 必填项校验正确
- [ ] range 类型校验正确
- [ ] score 正常打分
- [ ] scoreDesc 会跟随当前分值正确变化
- [ ] score 题目媒体和打分项媒体渲染正确
- [ ] required 的 score 题必须所有评分行都完成
- [ ] nps 正常选择 0-10 分
- [ ] nps scoreDesc 范围文案会跟随分值正确变化
- [ ] nps 题目媒体和 scale 媒体渲染正确

## E. Payload 层
- [ ] 已运行 `validate_survey_payload.py`
- [ ] 已运行 `validate_payload_against_schema.py`，确认 payload 与具体 schema 完全匹配
- [ ] payload 校验结果为 valid=true
- [ ] 顶层包含 surveyId / submittedAt / answers
- [ ] 未作答题不会出现在 answers
- [ ] radio.value 为对象
- [ ] checkbox.value 为数组
- [ ] input.value 为数组
- [ ] score.value 为数组
- [ ] nps.value 为对象，包含 optionId / score
- [ ] child 为数组
- [ ] range value 为 `{start, end}`
- [ ] questionId 在 answers 中不重复
- [ ] payload.surveyId 与 schema.survey.id 一致
- [ ] 每个 answer.questionId 都存在于 schema.questions
- [ ] 每个 answer.questionType 都与 schema 中的问题类型一致
- [ ] 每个 optionId / childId 都存在于对应问题/选项下
- [ ] required question 均出现在 answers 中
- [ ] score / nps 分值均落在 schema.scope 和 step 约束内
- [ ] checkbox payload 不包含 exclusive 与其他选项共存的非法组合
- [ ] checkbox payload 不包含多个 mutual-exclusion 选项共存的非法组合

## F. 缓存与提交
- [ ] 刷新页面后缓存能正确回填
- [ ] 提交成功后 localStorage 已清空
- [ ] 重复提交不会产生明显异常
- [ ] console payload 与页面填写结果一致

## G. 交付判定
### 可交付给用户填写的最低标准
- [ ] pipeline report 中 `releaseDecision.shipReady === true`
- [ ] pipeline report 中 `htmlE2E.viewports.desktop.valid === true`
- [ ] pipeline report 中 `htmlE2E.viewports.mobile.valid === true`
- [ ] pipeline report 中 `htmlInteractionE2E.viewports.desktop.valid === true`
- [ ] pipeline report 中 `htmlInteractionE2E.viewports.mobile.valid === true`
- [ ] pipeline report 中 `htmlAccessibility.valid === true`
- [ ] pipeline report 中 `htmlAccessibility.viewports.desktop.valid === true`
- [ ] pipeline report 中 `htmlAccessibility.viewports.mobile.valid === true`
- [ ] A / C / D / E / F 全部通过
- [ ] 无 schema error
- [ ] 无 payload error
- [ ] 无 runtime error
- [ ] `manualReviewRequired` 已人工确认

### 不建议上线的情况
- [ ] 任意 validator 返回 non-zero
- [ ] rich text 未做 sanitizer
- [ ] schema id 仍在 runtime 动态生成
- [ ] 关键交互（exclusive / child / range / cache）未验证
- [ ] payload shape 与 contract 不一致

---

## 建议流程
1. 先跑 schema validator
2. 再生成 HTML
3. 再跑 runtime checker
4. 再做手工交互验证
5. 导出 payload 样例并跑 payload validator
6. 跑 payload-against-schema validator，确认回收数据不会引用不存在的 id 或越界分值
7. 通过后再给用户填写

也可以直接使用统一入口：

```bash
python3 <repo-root>/validators/run_survey_creator_pipeline.py \
  --schema /absolute/path/to/schema.json \
  --output-dir /absolute/path/to/output-dir \
  --auto-repair \
  --fail-on-high-warning
```

只有当 `releaseDecision.shipReady === true` 且 `payloadAgainstSchema.valid === true` 时，才允许交付 HTML。
