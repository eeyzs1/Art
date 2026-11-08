import re, json, sys
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

ROOT = Path(r'F:\Art')
EN = ROOT / 'en'
errors = []

# --- 1. tree parity ---------------------------------------------------------
zh_pages = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob('*/**/*.html')) + \
           sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob('*.html')) + \
           sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob('reference/*.html'))
en_pages = sorted(p.relative_to(EN).as_posix() for p in EN.glob('**/*.html'))

zh_tree = [p for p in zh_pages if not p.startswith('en/')]
FOLDER_MAP = {
 '00-艺术通识':'00-art-fundamentals','01-绘画与版画':'01-painting-and-printmaking',
 '02-书法与篆刻':'02-calligraphy-and-seal-carving','03-雕塑与装置':'03-sculpture-and-installation',
 '04-建筑与景观':'04-architecture-and-landscape','05-工艺与设计':'05-craft-and-design',
 '06-摄影':'06-photography','07-文学与叙事':'07-literature-and-narrative',
 '08-音乐与声音艺术':'08-music-and-sound-art','09-舞蹈与身体艺术':'09-dance-and-body-based-art',
 '10-戏剧戏曲与现场表演':'10-theatre-chinese-opera-and-live-performance',
 '11-电影动画与视听':'11-film-animation-and-audiovisual-arts',
 '12-数字媒介与游戏艺术':'12-digital-media-and-game-art','13-民间艺术与跨媒介':'13-folk-art-and-intermedia'}
GROUP_MAP = {k: v.lower() for k, v in {
 '历史与理论':'History-and-Theory','人与制度':'People-and-Institutions','收藏与保护':'Collecting-and-Conservation',
 '材料与技法':'Materials-and-Techniques','版画与出版':'Printmaking-and-Publishing','画面问题':'Pictorial-Questions',
 '书体':'Script-Styles','研究与实践':'Research-and-Practice','形制与媒材':'Forms-and-Media','空间与事件':'Space-and-Events',
 '空间尺度':'Spatial-Scales','观察维度':'Dimensions-of-Observation','工艺材料':'Craft-Materials','设计领域':'Design-Fields',
 '类型与用途':'Genres-and-Uses','技术与呈现':'Technology-and-Presentation','文类':'Literary-Genres',
 '叙事与语言':'Narrative-and-Language','创作与实践':'Creation-and-Practice','学习维度':'Dimensions-of-Study',
 '传统与类型':'Traditions-and-Genres','实践与传统':'Practices-and-Traditions','创作与研究':'Creation-and-Research',
 '戏剧与综合舞台':'Theatre-and-the-Integrated-Stage','戏曲与曲艺':'Xiqu-and-Quyi',
 '现场及协作':'Live-Performance-and-Collaboration','视听形式':'Audiovisual-Forms','动画':'Animation',
 '制作与研究':'Production-and-Research','交互与计算':'Interaction-and-Computation','游戏与沉浸':'Games-and-Immersion',
 '生活中的艺术':'Art-in-Everyday-Life','跨媒介实践':'Intermedia-Practices'}.items()}
def map_path(p):
    for zh, en in FOLDER_MAP.items():
        p = p.replace(zh, en)
    for zh, en in GROUP_MAP.items():
        p = p.replace(zh + '.html', en + '.html')
    return p
mapped = sorted(map_path(p) for p in zh_tree)
missing = set(mapped) - set(en_pages)
extra = set(en_pages) - set(mapped)
print('zh pages:', len(zh_tree), '| en pages:', len(en_pages))
if missing: errors.append(f'en missing pages: {sorted(missing)[:10]}')
if extra: errors.append(f'en extra pages: {sorted(extra)[:10]}')

# --- 2. link integrity ------------------------------------------------------
class Links(HTMLParser):
    def handle_starttag(self, tag, attrs):
        for k, v in attrs:
            if k in ('href', 'src') and v and not urlsplit(v).scheme and not v.startswith('#'):
                target = (self.path.parent / unquote(v.split('#')[0]))
                if not target.exists():
                    errors.append(f'broken link {self.path.name}: {v}')
for p in EN.glob('**/*.html'):
    h = Links(); h.path = p; h.feed(p.read_text(encoding='utf-8'))
print('link check done over', len(en_pages), 'pages')

# --- 3. CJK leftovers -------------------------------------------------------
cjk_hits = []
for p in list(EN.glob('**/*.html')) + list(EN.glob('**/*.js')) + list(EN.glob('**/*.md')) + list(EN.glob('**/*.json')):
    t = p.read_text(encoding='utf-8')
    t = re.sub(r'<a href="[^"]+" hreflang="zh" lang="zh">中文</a>', '', t)  # deliberate language-switch links
    for m in re.finditer(r'[\u3000-\u9fff\uff01-\uff5d\uff5f-\uffef]', t):
        seg = t[max(0, m.start()-40):m.end()+40].replace('\n', ' ')
        cjk_hits.append((p.name, m.group(), seg))
        break  # one per file is enough to report
if cjk_hits: errors.append(f'CJK leftovers in {len(cjk_hits)} files: ' + '; '.join(f'{f}:{c}' for f, c, s in cjk_hits[:8]))
print('CJK scan:', 'CLEAN' if not cjk_hits else f'{len(cjk_hits)} files affected')

# --- 4. structural parity per lesson ----------------------------------------
zh_lessons = sorted(ROOT.glob('*/lessons/*.html'))
def lesson_sig(t):
    return (t.count('<section'), t.count('data-quiz'), t.count('data-note'), t.count('data-plan'), t.count('<h2'))
sig_bad = []
for zp in zh_lessons:
    rel = map_path(zp.relative_to(ROOT).as_posix())
    ep = EN / rel
    if not ep.exists():
        continue
    zs, es = lesson_sig(zp.read_text(encoding='utf-8')), lesson_sig(ep.read_text(encoding='utf-8'))
    if zs != es:
        sig_bad.append((rel, zs, es))
if sig_bad: errors.append(f'section-signature mismatches: {sig_bad[:5]}')
print('lesson signature parity:', 'OK' if not sig_bad else f'{len(sig_bad)} mismatches')

# --- 5. manifest parity -----------------------------------------------------
zm = json.loads((ROOT / 'course-manifest.json').read_text(encoding='utf-8'))
em = json.loads((EN / 'course-manifest.json').read_text(encoding='utf-8'))
for k in ('units', 'lessons', 'taxonomy_entries', 'group_microlessons', 'glossary_terms', 'timeline_anchors'):
    if zm[k] != em[k]:
        errors.append(f'manifest {k}: zh={zm[k]} en={em[k]}')
print('manifest:', {k: em[k] for k in ('units', 'lessons', 'taxonomy_entries', 'group_microlessons', 'glossary_terms', 'timeline_anchors')})

# --- 6. lang attribute + title ----------------------------------------------
bad_lang = [p.name for p in EN.glob('**/*.html') if 'lang="en"' not in p.read_text(encoding='utf-8')[:200]]
if bad_lang: errors.append(f'pages missing lang=en: {bad_lang[:5]}')
print('lang attributes:', 'OK' if not bad_lang else bad_lang[:5])

# --- 7. language-switch links ------------------------------------------------
import lang_switch
switch_bad = []
checked = 0
for tree, other_tag, label in ((ROOT, 'hreflang="en"', 'English'), (EN, 'hreflang="zh"', '中文')):
    for p in tree.glob('**/*.html'):
        rel_root = ROOT if tree is ROOT else EN
        try:
            rel = p.relative_to(rel_root).as_posix()
        except ValueError:
            continue
        if rel.startswith('en/') if tree is ROOT else False:
            continue
        t = p.read_text(encoding='utf-8')
        links = re.findall(rf'<a href="([^"]+)" {other_tag} [^>]*>{label}</a>', t)
        if len(links) != 1:
            switch_bad.append((p.name, f'{len(links)} switch links'))
            continue
        target = (p.parent / unquote(links[0])).resolve()
        if not target.exists():
            switch_bad.append((p.name, f'target missing: {links[0]}'))
            continue
        # round-trip: the target's own switch link must point back at this page
        back = re.findall(r'<a href="([^"]+)" (?:hreflang="zh"|hreflang="en") [^>]*>(?:中文|English)</a>', target.read_text(encoding='utf-8'))
        back_ok = any((target.parent / unquote(b)).resolve() == p.resolve() for b in back)
        if not back_ok:
            switch_bad.append((p.name, 'no switch link back from ' + links[0]))
        checked += 1
if switch_bad: errors.append(f'switch-link problems: {switch_bad[:8]}')
print('language switch:', f'OK ({checked} pages, one link each, round-trip verified)' if not switch_bad else switch_bad[:8])

print()
if errors:
    print('FAILURES:'); [print(' -', e) for e in errors]; sys.exit(1)
print('ALL VERIFICATIONS PASSED')
