    function renderScoreQuestion(question) {
      return `<div class="score-list">${(question.option || []).map((opt) => {
        const descMap = opt.attribute?.scoreDesc || {};
        const values = scoreValues(opt);
        return `<div class="score-item" data-score-option="${opt.id}" data-option-field="${opt.id}"><div class="field-label">${renderRich(opt.title)}</div>${renderMedia(opt.attribute?.media || [])}<div class="score-scale">${values.map((value) => {
          const display = formatScoreValue(value);
          return `<button class="score-pill" type="button" aria-pressed="false" aria-label="评分 ${display}" data-score-option-id="${opt.id}" data-score-value="${display}">${display}</button>`;
        }).join('')}</div><div class="score-desc" data-score-desc-for="${opt.id}"></div></div>`;
      }).join('')}</div><div class="error" role="alert" data-error>请完成当前评分题。</div>`;
    }


    function npsValues(option) {
      const scope = Array.isArray(option?.attribute?.scope) && option.attribute.scope.length === 2 ? option.attribute.scope : [0, 10];
      const min = Number(scope[0]);
      const max = Number(scope[1]);
      const values = [];
      for (let cur = min; cur <= max; cur += 1) values.push(cur);
      return values;
    }

    function renderNpsQuestion(question) {
      const opt = (question.option || [])[0] || { id: `${question.id}_nps`, attribute: { scope: [0, 10] } };
      const values = npsValues(opt);
      return `<div class="score-list nps-list"><div class="score-item nps-item" data-nps-option="${opt.id}" data-option-field="${opt.id}">${renderMedia(opt.attribute?.media || [])}<div class="score-scale nps-scale">${values.map((value) => {
        const display = formatScoreValue(value);
        return `<button class="score-pill nps-pill" type="button" aria-pressed="false" aria-label="NPS ${display} 分" data-score-option-id="${opt.id}" data-score-value="${display}">${display}</button>`;
      }).join('')}</div><div class="score-desc" data-score-desc-for="${opt.id}"></div></div></div><div class="error" role="alert" data-error>请选择一个 NPS 分值。</div>`;
    }


    function renderOption(question, option) {
      const children = option.child || [];
      const childHtml = children.length
        ? `<div class="child-list" data-child-wrap="${option.id}">${children.map((child) => `<div class="field"><div class="field-label">${renderRich(child.title)}</div>${createInputControl(child.attribute?.dataType || 'text', child.attribute || {}, `${question.id}__${option.id}__${child.id}`, '', child.id)}<div class="error" role="alert" data-child-error="${child.id}">请完善该补充内容。</div></div>`).join('')}</div>`
        : '';
      const exclusive = option.attribute?.exclusive === true;
      const mutual = option.attribute?.['mutual-exclusion'] === true;
      return `<div class="option" data-option-id="${option.id}" data-exclusive="${exclusive}" data-mutual-exclusion="${mutual}"><label class="option-label"><input type="${question.type === 'radio' ? 'radio' : 'checkbox'}" name="${question.id}" value="${option.id}" data-option-id="${option.id}" ${children.length ? 'data-has-child="true"' : ''} /><div class="option-title">${renderRich(option.title)}${renderMedia(option.attribute?.media || [])}</div></label>${childHtml}</div>`;
    }

    function renderQuestion(question) {
      const options = question.option ? shuffleIfNeeded(question.option, question.attribute?.random === true) : [];
      const content = question.type === 'input'
        ? `<div class="fields">${question.option.map((opt) => `<div class="field" data-option-field="${opt.id}"><div class="field-label">${renderRich(opt.title)}</div>${createInputControl(opt.attribute?.dataType || 'text', opt.attribute || {}, question.id, opt.id, '')}</div>`).join('')}<div class="error" role="alert" data-error>请按输入题规则完成填写。</div></div>`
        : question.type === 'score'
        ? renderScoreQuestion(question)
        : question.type === 'nps'
        ? renderNpsQuestion(question)
        : `<div class="options">${options.map((opt) => renderOption(question, opt)).join('')}</div><div class="error" role="alert" data-error>请完成当前题目。</div>`;
      const allowBack = surveySchema.survey.attribute?.allowBack === true;
      return screenShell(question.id, question.type, `<div class="question-head" style="grid-column:1 / -1;"><div><div class="question-index">第 ${String(questionNumber(question.id)).padStart(2, '0')} 题</div>${renderRich(question.title)}${renderRich(question.description)}</div>${question.attribute?.required ? '<div class="chip-row"><span class="chip warn">必填</span></div>' : ''}</div><div style="grid-column:1 / -1;">${renderMedia(question.attribute?.media || [])}${content}</div><div class="actions" style="grid-column:1 / -1;">${allowBack ? '<button class="btn secondary" type="button" data-prev>上一页</button>' : '<span></span>'}<div class="actions-right"><button class="btn" type="button" data-next>下一页</button></div></div>`);
    }


    function renderQuestionBlock(question) {
      const options = question.option ? shuffleIfNeeded(question.option, question.attribute?.random === true) : [];
      const content = question.type === 'input'
        ? `<div class="fields">${question.option.map((opt) => `<div class="field" data-option-field="${opt.id}"><div class="field-label">${renderRich(opt.title)}</div>${createInputControl(opt.attribute?.dataType || 'text', opt.attribute || {}, question.id, opt.id, '')}</div>`).join('')}<div class="error" role="alert" data-error>请按输入题规则完成填写。</div></div>`
        : question.type === 'score'
        ? renderScoreQuestion(question)
        : question.type === 'nps'
        ? renderNpsQuestion(question)
        : `<div class="options">${options.map((opt) => renderOption(question, opt)).join('')}</div><div class="error" role="alert" data-error>请完成当前题目。</div>`;
      return `<section class="field" data-screen-id="${question.id}" data-schema-type="${question.type}"><div class="question-head"><div><div class="question-index">第 ${String(questionNumber(question.id)).padStart(2, '0')} 题</div>${renderRich(question.title)}${renderRich(question.description)}</div>${question.attribute?.required ? '<div class="chip-row"><span class="chip warn">必填</span></div>' : ''}</div>${renderMedia(question.attribute?.media || [])}${content}</section>`;
    }
