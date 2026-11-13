"""Validate both editions; --static-only uses only the Python standard library."""
import argparse
from collections import Counter
from functools import partial
from html.parser import HTMLParser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import re
from threading import Thread
from urllib.parse import unquote, urlsplit

from lang_switch import zh_to_en, en_to_zh

ROOT = Path(__file__).resolve().parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.tags = Counter()
        self.attributes = Counter()
        self.ids = set()
        self.links = []
        self.switches = []
        self.lang = None
        self.visible_text = []
        self.ignored_depth = 0
        self.feed(path.read_text(encoding='utf-8'))
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags[tag] += 1
        self.attributes.update(attrs.keys())
        if tag == 'html':
            self.lang = attrs.get('lang')
        if 'id' in attrs:
            require(attrs['id'] not in self.ids, f'{self.path}: duplicate id {attrs["id"]}')
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])
        if tag == 'a' and attrs.get('hreflang'):
            self.switches.append((attrs['hreflang'], attrs.get('href', '')))
        if tag in ('script', 'style') or (tag == 'a' and attrs.get('hreflang') == 'zh'):
            self.ignored_depth += 1

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'a') and self.ignored_depth:
            self.ignored_depth -= 1

    def handle_data(self, data):
        if not self.ignored_depth:
            self.visible_text.append(data)


def local_target(page, href, root):
    """Resolve URL paths separately from queries/fragments, including #same-page."""
    url = urlsplit(href)
    if url.scheme or url.netloc:
        return None
    path = unquote(url.path)
    if not path:
        target = page
    elif path.startswith('/'):
        target = root / path.lstrip('/')
    else:
        target = page.parent / path
    target = target.resolve()
    if target.is_dir():
        target /= 'index.html'
    return target, unquote(url.fragment)


def check_static(root=ROOT):
    root = root.resolve()
    paths = sorted(root.rglob('*.html'))
    pages = {path: Page(path) for path in paths}
    require(bool(pages), 'No HTML pages found')
    for path, page in pages.items():
        require(page.tags['h1'] == 1, f'{path}: expected exactly one h1')
        require(page.tags['title'] == 1, f'{path}: expected one title')
        for href in page.links:
            result = local_target(path, href, root)
            if result is None:
                continue
            target, fragment = result
            require(target.is_relative_to(root), f'{path}: link leaves site: {href}')
            require(target.is_file(), f'{path}: broken link: {href}')
            if fragment and target in pages:
                require(fragment in pages[target].ids, f'{path}: missing anchor: {href}')

    zh = {path.relative_to(root).as_posix(): page for path, page in pages.items()
          if not path.is_relative_to(root / 'en')}
    en = {path.relative_to(root / 'en').as_posix(): page for path, page in pages.items()
          if path.is_relative_to(root / 'en')}
    mapped = {zh_to_en(path) for path in zh}
    require(None not in mapped, 'Unmapped Chinese page')
    require(mapped == set(en), f'Edition tree mismatch: missing {mapped - set(en)}, extra {set(en) - mapped}')
    for tree, language, other_language, base, other_base, mapper in (
        (zh, 'zh-CN', 'en', root, root / 'en', zh_to_en),
        (en, 'en', 'zh', root / 'en', root, en_to_zh),
    ):
        for relative, page in tree.items():
            require(page.lang == language, f'{page.path}: wrong document language')
            require(len(page.switches) == 1, f'{page.path}: expected one language switch')
            lang, href = page.switches[0]
            result = local_target(page.path, href, root)
            require(lang == other_language and result is not None and
                    result[0] == (other_base / mapper(relative)).resolve(),
                    f'{page.path}: wrong language counterpart')
            if language == 'en':
                # Shared JS deliberately contains both languages; inspect rendered text.
                require(not re.search(r'[\u3400-\u9fff]', ''.join(page.visible_text)),
                        f'{page.path}: untranslated Chinese text')
        manifest = json.loads((base / 'course-manifest.json').read_text(encoding='utf-8'))
        require(manifest['units'] == len(list(base.glob('[0-9][0-9]-*/index.html'))) == 14,
                f'{base}: unit count mismatch')
        require(manifest['lessons'] == len(list(base.glob('*/lessons/*.html'))) == 126, f'{base}: lesson count mismatch')
        require(manifest['group_microlessons'] == len(list(base.glob('*/micro/*.html'))) == 33, f'{base}: micro-lesson count mismatch')
        require(manifest['taxonomy_entries'] == len(manifest['coverage']), f'{base}: coverage count mismatch')
        require(tree['reference/coverage.html'].attributes['data-entry'] == manifest['taxonomy_entries'], f'{base}: coverage page count mismatch')
        require(tree['reference/glossary.html'].attributes['data-entry'] == manifest['glossary_terms'], f'{base}: glossary count mismatch')
        timeline = tree['reference/timeline.html']
        require(timeline.tags['tr'] - timeline.tags['table'] == manifest['timeline_anchors'], f'{base}: timeline count mismatch')
        added = manifest['added_lessons']
        require(len(added) == len({item['id'] for item in added}) == 84, f'{base}: extended lesson IDs mismatch')
        for item in added:
            require((base / item['path']).is_file(), f'{base}: missing lesson {item["id"]}')
        for item in manifest['coverage']:
            for key in ('shared_course', 'group_microlesson'):
                require((base / item[key]).is_file(), f'{base}: missing coverage target {item[key]}')
        for name in ('course.js', 'advanced.js', 'style.css'):
            require((base / 'assets' / name).read_text(encoding='utf-8') == (root / 'static' / name).read_text(encoding='utf-8'),
                    f'{base}: generated {name} differs from static source; rebuild the site')
    zm = json.loads((root / 'course-manifest.json').read_text(encoding='utf-8'))
    em = json.loads((root / 'en/course-manifest.json').read_text(encoding='utf-8'))
    for key in ('units', 'lessons', 'taxonomy_entries', 'group_microlessons', 'glossary_terms', 'timeline_anchors'):
        require(zm[key] == em[key], f'Bilingual manifest mismatch: {key}')
    for relative, page in zh.items():
        other = en[zh_to_en(relative)]
        require(page.tags == other.tags and page.attributes == other.attributes,
                f'{relative}: bilingual HTML structure mismatch')
    print(f'PASS static: {len(zh)} Chinese + {len(en)} English pages; links, anchors, manifests and bilingual parity.', flush=True)
    return paths


def check_layout(page, path):
    for width in (1280, 390, 320):
        page.set_viewport_size({'width': width, 'height': 900})
        require(page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'{path}: horizontal overflow at {width}px')


def check_interactions(page, english):
    for quiz in page.locator('[data-quiz]').all():
        quiz.locator('[data-correct="false"]').click()
        require(('Think again.' if english else '请再想') in quiz.locator('.feedback').inner_text(), 'Wrong-answer feedback')
        quiz.locator('[data-correct="true"]').click()
        require(('Correct.' if english else '回答正确') in quiz.locator('.feedback').inner_text(), 'Correct-answer feedback')
    for selector, output, value in (('#variable', '#lab-result', '80'), ('#contrast', '#contrast-result', '120')):
        if page.locator(selector).count():
            if selector == '#variable':
                before = page.locator('.stage').evaluate('''stage => ({
                    kind: stage.dataset.kind, gap: getComputedStyle(stage).gap,
                    widths: [...stage.children].map(shape => getComputedStyle(shape).width),
                    transforms: [...stage.children].map(shape => getComputedStyle(shape).transform)
                })''')
            page.locator(selector).fill(value)
            require(value in page.locator(output).inner_text(), f'{selector}: no update')
            if selector == '#variable':
                after = page.locator('.stage').evaluate('''stage => ({
                    gap: getComputedStyle(stage).gap,
                    widths: [...stage.children].map(shape => getComputedStyle(shape).width),
                    transforms: [...stage.children].map(shape => getComputedStyle(shape).transform)
                })''')
                require(before['widths'] == after['widths'], 'Spacing changed shape widths')
                if before['kind'] == 'visual':
                    require(before['transforms'] == after['transforms'], 'Spacing changed another variable')
                else:
                    require(before['gap'] == after['gap'], 'Shape experiment also changed spacing')
                if before['kind'] == 'motion':
                    require(page.locator('.shape').evaluate_all('''shapes => shapes.every(shape => {
                        const matrix = new DOMMatrix(getComputedStyle(shape).transform);
                        return matrix.a === 1 && matrix.b === 0 && matrix.c === 0 && matrix.d === 1;
                    })'''), 'Motion amplitude also changed rotation')
    if page.locator('#swap').count():
        page.locator('#swap').click()
        require('②' in page.locator('#shots').inner_text().splitlines()[0], 'Shot order did not change')
    if page.locator('#beat').count():
        page.locator('#beat').click()
        page.wait_for_function("/Beat 1|第 1 拍/.test(document.querySelector('#beat-result').textContent)")
        page.locator('#beat').click()
        require(page.locator('#beat').get_attribute('aria-pressed') == 'false', 'Metronome did not stop')
    if page.locator('#generate').count():
        first = page.locator('#generated').inner_html()
        page.locator('#generate').click()
        require(page.locator('#generated').inner_html() == first, 'Seed is not reproducible')
        page.locator('#seed').fill('43')
        page.locator('#generate').click()
        require(page.locator('#generated').inner_html() != first, 'Changing seed has no effect')
        page.locator('#seed').fill('1.5')
        page.locator('#generate').click()
        require(('integer' if english else '整数') in page.locator('#generate-result').inner_text(), 'Invalid seed accepted')
    if page.locator('#taxonomy-filter').count():
        first = page.locator('[data-entry]').first.text_content().strip()
        page.locator('#taxonomy-filter').fill(first)
        require(page.locator('[data-entry]:visible').count() > 0, 'Search has no match')
        page.locator('#taxonomy-filter').fill('no-match-不存在-987654321')
        require(page.locator('[data-entry]:visible').count() == 0, 'Search did not hide entries')
        require(('No matching' if english else '没有匹配') in page.locator('#filter-count').inner_text(), 'Missing empty-search feedback')
        page.locator('#taxonomy-filter').fill('')
        require(page.locator('[data-entry]:visible').count() == page.locator('[data-entry]').count(), 'Clearing search did not restore entries')


def check_saved_records(page, base_url, english):
    from lang_switch import FOLDER_ZH2EN, MICRO_ZH2EN
    folder = FOLDER_ZH2EN['07-文学与叙事'] if english else '07-文学与叙事'
    micro = MICRO_ZH2EN['文类'] if english else '文类'
    sample = '我的观察 <script>raw text</script>\nA second line.'
    for relative, selector in (
        (f'{folder}/lessons/01.html', '[data-note="practice"]'),
        (f'{folder}/lessons/04.html', '[data-note="project"]'),
        (f'{folder}/micro/{micro}.html', '[data-note="micro"]'),
    ):
        page.goto(base_url + relative)
        page.locator(selector).fill(sample)
        page.reload()
        require(page.locator(selector).input_value() == sample, f'{relative}: note lost on reload')
        if page.locator('[data-complete]').count():
            complete = page.locator('[data-complete]')
            if complete.get_attribute('aria-pressed') == 'true':
                complete.click()
            complete.click()
            page.reload()
            require(complete.get_attribute('aria-pressed') == 'true', 'Completed lesson not restored')
            complete.click()
            page.reload()
            require(complete.get_attribute('aria-pressed') == 'false', 'Completion could not be undone')
        if page.locator('[data-plan]').count():
            page.locator('[data-plan]').first.check()
            page.reload()
            require(page.locator('[data-plan]').first.is_checked(), 'Checkbox lost on reload')
        with page.expect_download() as download:
            page.locator('[data-export-notes]').click()
        require(sample in Path(download.value.path()).read_text(encoding='utf-8'), 'Export lost note content')
    page.goto(base_url + f'{folder}/lessons/04.html')
    require(bool(page.locator('#rewrite').input_value()), 'Initial rewrite example was erased')
    page.locator('#rewrite').fill(sample)
    page.reload()
    require(page.locator('#rewrite-result').inner_text() == sample, 'Restored rewrite preview is stale')
    page.locator('#rewrite').fill('')
    page.reload()
    require(page.locator('#rewrite').input_value() == '', 'Empty note was replaced by the example')
    page.goto(base_url + 'reference/checklist.html')
    box = page.locator('[data-plan]').first
    box.check()
    page.reload()
    require(box.is_checked() and '1 / 126' in page.locator('#checklist-progress').inner_text(), 'Checklist progress not restored')
    box.uncheck()


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def check_browser(paths, root=ROOT):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError as error:
        raise RuntimeError('Install requirements.txt and run python -m playwright install chromium, or use --static-only.') from error
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(accept_downloads=True)
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        for index, path in enumerate(paths, 1):
            page.goto(path.as_uri())
            check_layout(page, path)
            check_interactions(page, path.is_relative_to(root / 'en'))
            if index % 60 == 0:
                print(f'Browser: {index}/{len(paths)} pages checked.', flush=True)
        for base, english in ((root, False), (root / 'en', True)):
            check_saved_records(page, base.as_uri() + '/', english)
            dance = '09-dance-and-body-based-art' if english else '09-舞蹈与身体艺术'
            page.emulate_media(reduced_motion='reduce')
            page.goto((base / dance / 'lessons/04.html').as_uri())
            page.locator('#animate-time').click()
            require(('reduced motion' if english else '减少动态') in page.locator('#animation-result').inner_text(), 'Reduced motion ignored')
            require(page.locator('.runner').evaluate_all('(els) => els.every(el => el.getAnimations().length === 0)'), 'Animation ran with reduced motion')
            page.emulate_media(reduced_motion='no-preference')
        server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(root)))
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f'http://127.0.0.1:{server.server_port}/'
            for prefix, english in (('', False), ('en/', True)):
                check_saved_records(page, url + prefix, english)
        finally:
            server.shutdown()
            server.server_close()
            thread.join()
        for failure in ('blocked', 'quota'):
            failing = browser.new_context(accept_downloads=True)
            if failure == 'blocked':
                failing.add_init_script("Object.defineProperty(window, 'localStorage', { get() { throw new Error('Blocked'); } });")
            else:
                failing.add_init_script("Storage.prototype.setItem = () => { throw new DOMException('Full', 'QuotaExceededError'); };")
            failed_page = failing.new_page()
            failed_page.on('pageerror', lambda error: errors.append(str(error)))
            failed_page.goto((root / '00-艺术通识/lessons/01.html').as_uri())
            failed_page.locator('[data-note]').fill('Unsaved record')
            require(failed_page.locator('.storage-warning').is_visible(), 'Storage failure is silent')
            require('保存失败' in failed_page.locator('[data-note-status]').inner_text(), 'Incorrect save status')
            with failed_page.expect_download() as download:
                failed_page.locator('[data-export-notes]').click()
            require('Unsaved record' in Path(download.value.path()).read_text(encoding='utf-8'), 'Unsaved notes cannot be exported')
            failing.close()
        audio = browser.new_context()
        audio.add_init_script("window.AudioContext = class { resume() { return Promise.reject(new Error('Audio denied')); } };")
        audio_page = audio.new_page()
        audio_page.on('pageerror', lambda error: errors.append(str(error)))
        audio_page.goto((root / '08-音乐与声音艺术/lessons/01.html').as_uri())
        audio_page.locator('#beat').click()
        audio_page.wait_for_function("document.querySelector('#beat-result').textContent.includes('无法播放')")
        require(audio_page.locator('#beat').get_attribute('aria-pressed') == 'false', 'Failed audio remained active')
        audio.close()
        previews = root / '_research'
        previews.mkdir(exist_ok=True)
        for relative, width, name in (
            ('index.html', 1280, 'desktop-preview.png'),
            ('01-绘画与版画/lessons/01.html', 390, 'mobile-preview.png'),
            ('01-绘画与版画/lessons/04.html', 390, 'advanced-mobile-preview.png'),
        ):
            page.set_viewport_size({'width': width, 'height': 900})
            page.goto((root / relative).as_uri())
            page.screenshot(path=str(previews / name), full_page=True)
        require(not errors, f'Browser errors: {errors}')
        browser.close()
    print('PASS browser: all pages at 1280/390/320px; bilingual interactions, file/HTTP persistence, exports, storage/audio failures and reduced motion.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--static-only', action='store_true', help='Skip browser tests; no third-party dependencies required')
    args = parser.parse_args()
    paths = check_static()
    if not args.static_only:
        check_browser(paths)


if __name__ == '__main__':
    main()
