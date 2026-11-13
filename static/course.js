(() => {
  'use strict';

  const english = document.documentElement.lang.startsWith('en');
  const text = (zh, en) => english ? en : zh;
  const notes = [...document.querySelectorAll('textarea[data-note]')];
  const completions = [...document.querySelectorAll('[data-complete]')];
  const plans = [...document.querySelectorAll('[data-plan]')];
  let storageWarning;

  function warnStorage() {
    if (!storageWarning) {
      storageWarning = document.createElement('p');
      storageWarning.className = 'storage-warning';
      storageWarning.setAttribute('role', 'status');
      document.querySelector('main').prepend(storageWarning);
    }
    storageWarning.textContent = text(
      '浏览器无法保存或读取学习记录。离开前请导出本页记录。',
      'The browser cannot save or read study records. Export this page before leaving.'
    );
  }

  const storage = {
    load(key) {
      try {
        return localStorage.getItem(key);
      } catch {
        warnStorage();
        return null;
      }
    },
    save(key, value) {
      try {
        localStorage.setItem(key, value);
        return true;
      } catch {
        warnStorage();
        return false;
      }
    }
  };
  // Keep the original keys so existing notes and progress remain readable.
  window.ArtCourse = { text, storage };

  document.querySelectorAll('[data-quiz]').forEach(quiz => {
    quiz.querySelectorAll('button').forEach(button => {
      button.addEventListener('click', () => {
        quiz.querySelector('.feedback').textContent = (
          button.dataset.correct === 'true'
            ? text('回答正确。', 'Correct. ')
            : text('请再想一想。', 'Think again. ')
        ) + quiz.dataset.feedback;
      });
    });
  });

  notes.forEach((note, index) => {
    const saved = storage.load(location.pathname + note.dataset.note);
    // A missing record must preserve the lesson's example text; an empty saved
    // string, on the other hand, is an intentional edit.
    if (saved !== null) note.value = saved;
    const status = document.createElement('span');
    status.className = 'note-status';
    status.id = `note-status-${index}`;
    status.setAttribute('role', 'status');
    status.setAttribute('data-note-status', '');
    note.setAttribute('aria-describedby', [
      note.getAttribute('aria-describedby'), status.id
    ].filter(Boolean).join(' '));
    note.after(status);
    note.addEventListener('input', () => {
      status.textContent = storage.save(location.pathname + note.dataset.note, note.value)
        ? text('已保存到此浏览器。', 'Saved in this browser.')
        : text('保存失败，请导出记录。', 'Save failed. Export your records.');
    });
  });

  completions.forEach(button => {
    const initialLabel = button.textContent;
    let done = storage.load(location.pathname + 'done') === '1';
    function render() {
      button.setAttribute('aria-pressed', String(done));
      button.textContent = done
        ? text('已完成本课（点击可取消）', 'Lesson completed (click to undo)')
        : initialLabel;
    }
    button.addEventListener('click', () => {
      done = !done;
      storage.save(location.pathname + 'done', done ? '1' : '0');
      render();
    });
    render();
  });

  plans.forEach(box => {
    box.checked = storage.load('art-plan:' + box.dataset.plan) === '1';
    box.addEventListener('change', () => {
      storage.save('art-plan:' + box.dataset.plan, box.checked ? '1' : '0');
    });
  });

  if (notes.length || completions.length || plans.length) {
    const tools = document.createElement('section');
    tools.className = 'study-tools';
    const heading = document.createElement('h2');
    heading.textContent = text('保存学习记录', 'Keep your study records');
    const hint = document.createElement('p');
    hint.textContent = text(
      '笔记和勾选尽力保存在此浏览器。导出本页记录可留作备份；清理浏览器数据可能使记录丢失。',
      'Notes and checkmarks are saved in this browser when possible. Export this page as a backup; clearing browser data can erase records.'
    );
    const button = document.createElement('button');
    button.type = 'button';
    button.setAttribute('data-export-notes', '');
    button.textContent = text('导出本页学习记录', 'Export this page’s study records');
    tools.append(heading, hint, button);
    document.querySelector('main').append(tools);

    button.addEventListener('click', () => {
      const title = document.querySelector('h1').textContent;
      const lines = [
        '# ' + title, '',
        text('页面：', 'Page: ') + location.href,
        text('导出时间：', 'Exported: ') + new Date().toISOString(), ''
      ];
      notes.forEach(note => {
        const label = note.closest('label')?.cloneNode(true);
        label?.querySelectorAll('textarea, [data-note-status]').forEach(el => el.remove());
        lines.push('## ' + (label?.textContent.trim() || note.dataset.note), '', note.value, '');
      });
      if (completions.length || plans.length) {
        lines.push('## ' + text('本页勾选状态', 'Page checkmarks'), '');
        completions.forEach(item => lines.push(
          `- [${item.getAttribute('aria-pressed') === 'true' ? 'x' : ' '}] ` + title
        ));
        plans.forEach(item => lines.push(
          `- [${item.checked ? 'x' : ' '}] ` + (item.closest('label')?.textContent.trim() || item.dataset.plan)
        ));
      }
      const url = URL.createObjectURL(new Blob([lines.join('\n')], { type: 'text/markdown;charset=utf-8' }));
      const link = document.createElement('a');
      link.href = url;
      // Avoid reserved Windows filename characters in translated lesson titles.
      link.download = title.replace(/[<>:"/\\|?*\x00-\x1f]/g, '_').slice(0, 80) + '.md';
      document.body.append(link);
      link.click();
      link.remove();
      setTimeout(() => URL.revokeObjectURL(url), 1000);
    });
  }

  const variable = document.querySelector('#variable');
  if (variable) {
    const stage = document.querySelector('.stage');
    const out = document.querySelector('#lab-result');
    function update() {
      const value = Number(variable.value);
      const kind = stage.dataset.kind;
      if (kind === 'visual') stage.style.gap = (value * 0.15) + '%';
      stage.querySelectorAll('.shape').forEach((shape, index) => {
        shape.style.transform = kind === 'motion'
          ? `translateY(${(index - 1) * value / 3}px)`
          : kind === 'line' ? `scaleX(${0.3 + value / 60})`
            : kind === 'space' ? `perspective(400px) rotateY(${value}deg)` : 'translateY(0)';
      });
      out.textContent = text(
        `当前变量：${value}。请比较疏密、重心或轮廓；意义解释需要你另外提出证据。`,
        `Current value: ${value}. Compare spacing, balance, or contour; interpreting meaning requires additional evidence from you.`
      );
    }
    variable.addEventListener('input', update);
    update();
  }

  const swap = document.querySelector('#swap');
  swap?.addEventListener('click', () => {
    const shots = document.querySelector('#shots');
    shots.append(shots.firstElementChild);
    document.querySelector('#shot-result').textContent = text(
      '顺序已改变。写下你推断的故事，并区分画面事实与联想。',
      'Order changed. Write down the story you infer, and separate what the images show from your associations.'
    );
  });

  const play = document.querySelector('#beat');
  if (play) {
    const initialLabel = play.textContent;
    const tempo = document.querySelector('#tempo');
    const result = document.querySelector('#beat-result');
    let timer = null;
    let context = null;
    let generation = 0;
    let playing = false;
    function stop() {
      generation++;
      clearInterval(timer);
      timer = null;
      playing = false;
      play.textContent = initialLabel;
      play.setAttribute('aria-pressed', 'false');
    }
    play.setAttribute('aria-pressed', 'false');
    play.addEventListener('click', async () => {
      if (playing) {
        stop();
        return;
      }
      playing = true;
      const request = ++generation;
      play.textContent = text('停止声音', 'Stop sound');
      play.setAttribute('aria-pressed', 'true');
      try {
        context ||= new (window.AudioContext || window.webkitAudioContext)();
        await context.resume();
        if (request !== generation) return;
        if (document.hidden || context.state !== 'running') {
          stop();
          return;
        }
        let count = 0;
        function tick() {
          const oscillator = context.createOscillator();
          const gain = context.createGain();
          oscillator.connect(gain);
          gain.connect(context.destination);
          oscillator.frequency.value = count % 4 === 0 ? 660 : 440;
          gain.gain.setValueAtTime(0.08, context.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, context.currentTime + 0.08);
          oscillator.onended = () => {
            oscillator.disconnect();
            gain.disconnect();
          };
          oscillator.start();
          oscillator.stop(context.currentTime + 0.09);
          result.textContent = text(`第 ${count % 4 + 1} 拍`, `Beat ${count % 4 + 1}`);
          count++;
        }
        tick();
        timer = setInterval(tick, 60000 / Number(tempo.value));
      } catch {
        if (request !== generation) return;
        stop();
        result.textContent = text(
          '浏览器无法播放声音，请自行匀速数四拍。',
          'The browser cannot play sound; count four even beats on your own.'
        );
      }
    });
    tempo.addEventListener('input', stop);
    document.addEventListener('visibilitychange', () => { if (document.hidden) stop(); });
    window.addEventListener('pagehide', stop);
  }
})();
