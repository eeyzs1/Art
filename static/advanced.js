(() => {
  'use strict';
  const { text } = window.ArtCourse;
  const filter = document.querySelector('#taxonomy-filter');
  if (filter) {
    const entries = [...document.querySelectorAll('[data-entry]')].map(element => ({
      element, content: element.textContent.toLocaleLowerCase()
    }));
    const groups = [...document.querySelectorAll('section')].map(section => ({
      section, entries: entries.filter(item => section.contains(item.element))
    })).filter(group => group.entries.length);
    const result = document.querySelector('#filter-count');
    function update() {
      const query = filter.value.trim().toLocaleLowerCase();
      let count = 0;
      entries.forEach(({ element, content }) => {
        element.hidden = !content.includes(query);
        if (!element.hidden) count++;
      });
      groups.forEach(group => {
        group.section.hidden = !group.entries.some(item => !item.element.hidden);
      });
      result.textContent = count
        ? text(`符合条件：${count}个条目`, `Matching entries: ${count}`)
        : text('没有匹配条目，请换一个关键词。', 'No matching entries. Try another keyword.');
    }
    filter.addEventListener('input', update);
    update();
  }

  const contrast = document.querySelector('#contrast');
  if (contrast) {
    contrast.addEventListener('input', () => {
      const value = Number(contrast.value);
      document.querySelectorAll('.color-sample')[1].style.background = `rgb(${value},${value},${value})`;
      document.querySelector('#contrast-result').textContent = text(
        `右侧背景灰阶为 ${value}；两块中心灰始终相同。请描述感知差异，而非修改事实。`,
        `The right background gray level is ${value}; the two center grays are always identical. Describe the perceptual difference rather than changing the facts.`
      );
    });
  }

  const edit = document.querySelector('#rewrite');
  if (edit) {
    function update() {
      document.querySelector('#rewrite-result').textContent = edit.value || text(
        '请写一句话，并用换行制造停顿。', 'Write one sentence and use line breaks to create pauses.'
      );
    }
    edit.addEventListener('input', update);
    // course.js restores saved notes before this script runs.
    update();
  }

  const animate = document.querySelector('#animate-time');
  if (animate) {
    animate.addEventListener('click', () => {
      const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
      document.querySelectorAll('.runner').forEach((runner, index) => {
        runner.getAnimations().forEach(animation => animation.cancel());
        if (reduced) return;
        const width = Math.max(0, runner.parentElement.clientWidth - 70);
        runner.animate([
          { transform: 'translateX(0)' }, { transform: `translateX(${width}px)` }
        ], { duration: 1800, easing: index ? 'ease-in-out' : 'linear' });
      });
      document.querySelector('#animation-result').textContent = reduced ? text(
        '你已选择减少动态效果：匀速在等时距内移动等距离；缓入缓出会先慢后快再慢。',
        'You have reduced motion enabled: at constant speed, equal distances move in equal times; ease-in-out goes slow, then fast, then slow again.'
      ) : text('上方匀速，下方缓入缓出；请比较中途的位置。', 'The upper dot moves at constant speed; the lower dot eases in and out. Compare their positions midway.');
    });
  }

  const generate = document.querySelector('#generate');
  if (generate) {
    const input = document.querySelector('#seed');
    const result = document.querySelector('#generate-result');
    function draw() {
      if (input.value === '' || !input.checkValidity()) {
        result.textContent = text('请输入0到999999之间的整数种子。', 'Enter an integer seed from 0 to 999999.');
        return;
      }
      let seed = Number(input.value) >>> 0;
      const root = document.querySelector('#generated');
      const fragment = document.createDocumentFragment();
      for (let index = 0; index < 12; index++) {
        seed = (1664525 * seed + 1013904223) >>> 0;
        const x = 20 + seed % 540;
        seed = (1664525 * seed + 1013904223) >>> 0;
        const y = 20 + seed % 130;
        seed = (1664525 * seed + 1013904223) >>> 0;
        const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
        Object.entries({ x1: x, y1: y, x2: x + seed % 61 - 30, y2: y + 25,
          stroke: index % 2 ? '#b05e3f' : '#25564c', 'stroke-width': 4
        }).forEach(([key, value]) => line.setAttribute(key, value));
        fragment.append(line);
      }
      root.replaceChildren(fragment);
      result.textContent = text(
        '固定种子与规则可重现本示例。伪随机只是组织结果的一种工具。',
        'A fixed seed and fixed rules reproduce this demo. Pseudorandomity is just one tool for organizing outcomes.'
      );
    }
    generate.addEventListener('click', draw);
    draw();
  }

  const progress = document.querySelector('#checklist-progress');
  if (progress) {
    const boxes = [...document.querySelectorAll('input[data-plan^="chk-"]')];
    function update() {
      const count = boxes.filter(box => box.checked).length;
      progress.textContent = text(`已能复述并举例：${count} / ${boxes.length} 课`, `Recited with examples: ${count} / ${boxes.length} lessons`);
    }
    boxes.forEach(box => box.addEventListener('change', update));
    update();
  }
})();
