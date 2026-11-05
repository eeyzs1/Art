from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote,urlsplit
from playwright.sync_api import sync_playwright
import json

if not __debug__:
    raise SystemExit('check_course.py 依赖 assert 做校验；请勿使用 python -O 运行。')

root=Path(__file__).resolve().parent
class Links(HTMLParser):
    def handle_starttag(self,tag,attrs):
        for k,v in attrs:
            if k in ('href','src') and v and not urlsplit(v).scheme and not v.startswith('#'):
                assert (self.path.parent/unquote(v.split('#')[0])).exists(),(self.path,v)
files=list(root.rglob('*.html'))
manifest=json.loads((root/'course-manifest.json').read_text(encoding='utf-8'))
lesson_files=list(root.glob('*/lessons/*.html'))
assert len(lesson_files)==manifest['lessons']==126
assert len(manifest['coverage'])==manifest['taxonomy_entries']
for path in files:
    p=Links();p.path=path;p.feed(path.read_text(encoding='utf-8'))
with sync_playwright() as p:
    browser=p.chromium.launch()
    page=browser.new_page(viewport={'width':1280,'height':900})
    errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
    for path in files:
        page.goto(path.as_uri())
        assert page.locator('h1').count()==1,path
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),path
        quiz=page.locator('[data-quiz]')
        if quiz.count():
            quiz.locator('[data-correct="false"]').click()
            assert '请再想' in quiz.locator('.feedback').inner_text()
            quiz.locator('[data-correct="true"]').click()
            assert '回答正确' in quiz.locator('.feedback').inner_text()
        if page.locator('#variable').count():
            page.locator('#variable').fill('80')
            assert '80' in page.locator('#lab-result').inner_text()
        if page.locator('#swap').count():
            page.locator('#swap').click()
            assert '②' in page.locator('#shots').first.inner_text().splitlines()[0]
        if page.locator('#beat').count():
            page.locator('#beat').click();page.wait_for_timeout(100)
            assert '第' in page.locator('#beat-result').inner_text()
            page.locator('#beat').click()
        if page.locator('#contrast').count():
            page.locator('#contrast').fill('120')
            assert '120' in page.locator('#contrast-result').inner_text()
        if page.locator('#rewrite').count():
            page.locator('#rewrite').fill('一个词\n一次停顿')
            assert page.locator('#rewrite-result').inner_text()=='一个词\n一次停顿'
        if page.locator('#animate-time').count():
            page.locator('#animate-time').click()
        if page.locator('#generate').count():
            first=page.locator('#generated').inner_html()
            page.locator('#generate').click()
            assert page.locator('#generated').inner_html()==first
            page.locator('#seed').fill('43');page.locator('#generate').click()
            assert page.locator('#generated').inner_html()!=first
        if page.locator('#taxonomy-filter').count():
            page.locator('#taxonomy-filter').fill('陶瓷')
            assert page.locator('[data-entry]:visible').count()>0
            assert page.locator('[data-entry]:visible').count()<manifest['taxonomy_entries']
            page.locator('#taxonomy-filter').fill('一个不可能匹配的条目')
            assert page.locator('[data-entry]:visible').count()==0
        if page.locator('[data-plan]').count():
            check=page.locator('[data-plan]').first
            check.check();page.reload()
            assert page.locator('[data-plan]').first.is_checked()
    page.goto((root/'index.html').as_uri());page.screenshot(path=str(root/'_research/desktop-preview.png'),full_page=True)
    page.set_viewport_size({'width':390,'height':844})
    for path in files:
        page.goto(path.as_uri())
        assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),('mobile',path)
    page.goto((root/'01-绘画与版画/lessons/01.html').as_uri())
    page.screenshot(path=str(root/'_research/mobile-preview.png'),full_page=True)
    page.goto((root/'01-绘画与版画/lessons/04.html').as_uri())
    page.screenshot(path=str(root/'_research/advanced-mobile-preview.png'),full_page=True)
    page.emulate_media(reduced_motion='reduce')
    page.goto((root/'09-舞蹈与身体艺术/lessons/04.html').as_uri())
    page.locator('#animate-time').click()
    assert '减少动态' in page.locator('#animation-result').inner_text()
    assert not errors,errors
    browser.close()
print(f'PASS: {len(files)} HTML files / 126 lessons; links, desktop/mobile layout, quizzes, sliders, audio, sequence, generation, filter, saved checkboxes and reduced motion; no browser errors.')
