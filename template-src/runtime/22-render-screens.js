    function renderSurvey() {
      const s = surveySchema.survey;
      return screenShell(s.id, 'survey', `<div>${renderRich(s.title)}${renderRich(s.description)}</div><div class="meta-grid"><div class="meta"><strong>填写说明</strong><span>请根据你的真实想法完成填写，提交前可返回上一页修改内容。</span></div>${renderMedia(s.attribute.media || [])}</div><div class="actions" style="grid-column:1 / -1;"><span></span><div class="actions-right"><button class="btn" type="button" data-next>开始问卷</button></div></div>`, true);
    }


    function renderManualPage(group, pageIndex) {
      const allowBack = surveySchema.survey.attribute?.allowBack === true;
      const blocks = group.map((question) => renderQuestionBlock(question)).join('');
      return screenShell(`page_${String(pageIndex + 1).padStart(2, '0')}`, 'page', `${blocks}<div class="actions" style="grid-column:1 / -1;">${allowBack ? '<button class="btn secondary" type="button" data-prev>上一页</button>' : '<span></span>'}<div class="actions-right"><button class="btn" type="button" data-next>下一页</button></div></div>`);
    }

    function renderFinish() {
      const f = surveySchema.finish;
      const allowBack = surveySchema.survey.attribute?.allowBack === true;
      return screenShell(f.id, 'finish', `<div>${renderRich(f.title)}${renderRich(f.description)}</div><div class="meta-grid">${renderMedia(f.media || [])}</div><div class="actions" style="grid-column:1 / -1;">${allowBack ? '<button class="btn secondary" type="button" data-prev>上一页</button>' : '<span></span>'}<div class="actions-right"><button class="btn" type="submit">提交问卷</button></div></div>`, true);
    }

    function screenShell(id, type, inner, dark = false) {
      return `<section class="screen" data-screen-id="${id}" data-schema-type="${type}"><article class="card ${dark ? 'dark' : ''}"><div class="card-body ${type === 'survey' ? 'hero-grid' : type === 'finish' ? 'finish-grid' : ''}">${inner}</div></article></section>`;
    }


    function render() {
      const onePageOneQuestion = surveySchema.survey.attribute?.onePageOneQuestion === true;
      if (hasManualPagination && !onePageOneQuestion) {
        form.innerHTML = [renderSurvey(), ...manualPages.map((group, index) => renderManualPage(group, index)), renderFinish()].join('');
      } else if (onePageOneQuestion) {
        form.innerHTML = [renderSurvey(), ...answerableQuestions.map(renderQuestion), renderFinish()].join('');
      } else {
        form.innerHTML = screenShell('all_in_one', 'survey-all', `<div style="grid-column:1 / -1;">${renderRich(surveySchema.survey.title)}${renderRich(surveySchema.survey.description)}</div>${answerableQuestions.map((q) => renderQuestionBlock(q)).join('')}<div style="grid-column:1 / -1;">${renderRich(surveySchema.finish.title)}${renderRich(surveySchema.finish.description)}</div><div class="actions" style="grid-column:1 / -1;"><span></span><div class="actions-right"><button class="btn" type="submit">提交问卷</button></div></div>`);
      }
      rebuildQuestionScreenMap();
      bindEvents();
      hydrateAll();
      applyLogicRuntime({ preserveActiveId: surveySchema.survey.id });
      if (!document.querySelector('.screen.is-active')) show(0);
    }
