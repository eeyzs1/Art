"""Shared language-switch helpers: map every generated page to its counterpart page in the other
language tree (zh at the repo root, en under en/), and inject a header-nav toggle link.

Both build_course.write (Chinese tree) and build_course_en.write (English tree) call inject() on
every generated HTML page, so every page carries exactly one switch link.
"""
import os
from pathlib import Path

# Category folders: zh folder name <-> en folder slug.
FOLDER_ZH2EN = {
    '00-艺术通识': '00-art-fundamentals',
    '01-绘画与版画': '01-painting-and-printmaking',
    '02-书法与篆刻': '02-calligraphy-and-seal-carving',
    '03-雕塑与装置': '03-sculpture-and-installation',
    '04-建筑与景观': '04-architecture-and-landscape',
    '05-工艺与设计': '05-craft-and-design',
    '06-摄影': '06-photography',
    '07-文学与叙事': '07-literature-and-narrative',
    '08-音乐与声音艺术': '08-music-and-sound-art',
    '09-舞蹈与身体艺术': '09-dance-and-body-based-art',
    '10-戏剧戏曲与现场表演': '10-theatre-chinese-opera-and-live-performance',
    '11-电影动画与视听': '11-film-animation-and-audiovisual-arts',
    '12-数字媒介与游戏艺术': '12-digital-media-and-game-art',
    '13-民间艺术与跨媒介': '13-folk-art-and-intermedia',
}
FOLDER_EN2ZH = {v: k for k, v in FOLDER_ZH2EN.items()}

# Micro-lesson filenames: the zh file is named by the zh group name, the en file by a slug of the
# English group name (group.replace(' ','-').lower(), as used in extend_course_en.py).
MICRO_ZH2EN = {
    '历史与理论': 'history-and-theory',
    '人与制度': 'people-and-institutions',
    '收藏与保护': 'collecting-and-conservation',
    '材料与技法': 'materials-and-techniques',
    '版画与出版': 'printmaking-and-publishing',
    '画面问题': 'pictorial-questions',
    '书体': 'script-styles',
    '研究与实践': 'research-and-practice',
    '形制与媒材': 'forms-and-media',
    '空间与事件': 'space-and-events',
    '空间尺度': 'spatial-scales',
    '观察维度': 'dimensions-of-observation',
    '工艺材料': 'craft-materials',
    '设计领域': 'design-fields',
    '类型与用途': 'genres-and-uses',
    '技术与呈现': 'technology-and-presentation',
    '文类': 'literary-genres',
    '叙事与语言': 'narrative-and-language',
    '创作与实践': 'creation-and-practice',
    '学习维度': 'dimensions-of-study',
    '传统与类型': 'traditions-and-genres',
    '实践与传统': 'practices-and-traditions',
    '创作与研究': 'creation-and-research',
    '戏剧与综合舞台': 'theatre-and-the-integrated-stage',
    '戏曲与曲艺': 'xiqu-and-quyi',
    '现场及协作': 'live-performance-and-collaboration',
    '视听形式': 'audiovisual-forms',
    '动画': 'animation',
    '制作与研究': 'production-and-research',
    '交互与计算': 'interaction-and-computation',
    '游戏与沉浸': 'games-and-immersion',
    '生活中的艺术': 'art-in-everyday-life',
    '跨媒介实践': 'intermedia-practices',
}
MICRO_EN2ZH = {v: k for k, v in MICRO_ZH2EN.items()}

# Pages whose names are identical in both trees.
_SHARED_PREFIX = 'reference/'


def zh_to_en(p):
    """zh-root-relative page path -> en-root-relative counterpart, or None if unmappable."""
    if p == 'index.html' or p.startswith(_SHARED_PREFIX):
        return p
    folder, _, rest = p.partition('/')
    en_folder = FOLDER_ZH2EN.get(folder)
    if en_folder is None:
        return None
    if rest.startswith('micro/'):
        stem = rest[len('micro/'):-len('.html')]
        slug = MICRO_ZH2EN.get(stem)
        return None if slug is None else f'{en_folder}/micro/{slug}.html'
    return f'{en_folder}/{rest}'


def en_to_zh(p):
    """en-root-relative page path -> zh-root-relative counterpart, or None if unmappable."""
    if p == 'index.html' or p.startswith(_SHARED_PREFIX):
        return p
    folder, _, rest = p.partition('/')
    zh_folder = FOLDER_EN2ZH.get(folder)
    if zh_folder is None:
        return None
    if rest.startswith('micro/'):
        stem = rest[len('micro/'):-len('.html')]
        zh = MICRO_EN2ZH.get(stem)
        return None if zh is None else f'{zh_folder}/micro/{zh}.html'
    return f'{zh_folder}/{rest}'


def switch_link(page_path, root):
    """<a> element for this page's counterpart in the other language tree ('' when unmappable)."""
    p = Path(page_path).resolve()
    root = Path(root).resolve()
    # Check the en tree first: en/ pages are also "relative to ROOT", so order matters.
    try:
        rel = p.relative_to(root / 'en').as_posix()
        side = 'en'
    except ValueError:
        try:
            rel = p.relative_to(root).as_posix()
            side = 'zh'
        except ValueError:
            return ''
    if not rel.endswith('.html'):
        return ''
    if side == 'zh':
        cp = zh_to_en(rel)
        if cp is None:
            return ''
        target = root / 'en' / cp
        label, hreflang, lang = 'English', 'en', 'en'
    else:
        cp = en_to_zh(rel)
        if cp is None:
            return ''
        target = root / cp
        label, hreflang, lang = '中文', 'zh', 'zh'
    href = os.path.relpath(target, p.parent).replace('\\', '/')
    return f'<a href="{href}" hreflang="{hreflang}" lang="{lang}">{label}</a>'


def inject(html_text, link):
    """Append the language link as the last item of the header nav (the first </nav> in the page)."""
    if not link or '</nav>' not in html_text:
        return html_text
    return html_text.replace('</nav>', link + '</nav>', 1)
