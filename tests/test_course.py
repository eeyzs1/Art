"""Regression tests for generation, authored data and the static validator."""
from copy import deepcopy
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

import build_course
import check_course
import extend_course
from course_validation import validate_data

ROOT = Path(__file__).resolve().parents[1]


def authored_data():
    return deepcopy((build_course.DATA, extend_course.TAXONOMY, extend_course.CONTENT,
                     extend_course.MICRO, extend_course.GLOSSARY,
                     extend_course.TIMELINE, extend_course.MASTER_STARTS))


class SourceDataTests(unittest.TestCase):
    def test_both_editions_are_valid(self):
        import extend_course_en
        extend_course.validate_data()
        extend_course_en.validate_data()

    def test_missing_micro_lesson_is_rejected(self):
        data = authored_data()
        data[3].pop(next(iter(data[3])))
        with self.assertRaisesRegex(ValueError, 'Micro-lessons'):
            validate_data(*data)

    def test_incomplete_extended_lesson_is_rejected(self):
        data = authored_data()
        data[2]['00'] = data[2]['00'].replace('｜', '', 1)
        with self.assertRaisesRegex(ValueError, '6 extended lessons'):
            validate_data(*data)

    def test_duplicate_glossary_term_is_rejected(self):
        data = authored_data()
        data[4]['00'].append(data[4]['00'][0])
        with self.assertRaisesRegex(ValueError, 'duplicate glossary'):
            validate_data(*data)


class LinkTests(unittest.TestCase):
    def test_encoded_paths_queries_and_fragments(self):
        root = ROOT.resolve()
        path = root / 'reference/index.html'
        target, fragment = check_course.local_target(path, '../a%20b.html?mode=read#part%201', root)
        self.assertEqual(target, root / 'a b.html')
        self.assertEqual(fragment, 'part 1')
        self.assertEqual(check_course.local_target(path, '#main', root), (path, 'main'))

    def test_external_and_protocol_relative_urls_are_skipped(self):
        for url in ('https://example.com/a', '//example.com/a', 'mailto:example@example.com'):
            self.assertIsNone(check_course.local_target(ROOT / 'index.html', url, ROOT))

    def test_duplicate_ids_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix='art-links-') as temp:
            page = Path(temp) / 'index.html'
            page.write_text('<h1 id="x">Title</h1><p id="x">Duplicate</p>', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'duplicate id'):
                check_course.Page(page)

    def test_missing_anchor_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='art-links-') as temp:
            root = Path(temp)
            (root / 'index.html').write_text('<title>Test</title><h1>Title</h1><a href="#missing">Link</a>', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'missing anchor'):
                check_course.check_static(root)


class BuildTests(unittest.TestCase):
    def test_imports_are_silent_and_do_not_overwrite_files(self):
        code = """
from unittest.mock import patch
with patch('pathlib.Path.write_text', side_effect=RuntimeError('Unexpected write')):
    import build_course, build_course_en, extend_course, extend_course_en
"""
        result = subprocess.run([sys.executable, '-B', '-c', code], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')

    def test_validation_survives_optimized_python(self):
        code = """
import extend_course
from unittest.mock import patch
extend_course.CONTENT = dict(extend_course.CONTENT, **{'00': 'invalid'})
with patch('pathlib.Path.write_text', side_effect=RuntimeError('Wrote invalid course')):
    try:
        extend_course.build_site()
    except ValueError:
        pass
    else:
        raise RuntimeError('Invalid data was accepted')
"""
        result = subprocess.run([sys.executable, '-O', '-B', '-c', code], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_english_data_does_not_overwrite_chinese_pages(self):
        code = """
import extend_course, extend_course_en
from unittest.mock import patch
extend_course_en.CONTENT = dict(extend_course_en.CONTENT, **{'00': 'invalid'})
with patch('pathlib.Path.write_text', side_effect=RuntimeError('Partial bilingual build')):
    try:
        extend_course.build_site()
    except ValueError:
        pass
    else:
        raise RuntimeError('Invalid English data was accepted')
"""
        result = subprocess.run([sys.executable, '-B', '-c', code], cwd=ROOT,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_repeated_build_and_standalone_english_build(self):
        with tempfile.TemporaryDirectory(prefix='art-build-') as temp:
            target = Path(temp) / 'site'
            shutil.copytree(ROOT, target, ignore=shutil.ignore_patterns('.git', '__pycache__', '*.png'))
            code = """
import hashlib
from pathlib import Path
import extend_course, extend_course_en
from check_course import check_static
root = Path.cwd()
def hashes():
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
extend_course.build_site()
first = hashes()
extend_course.build_site()
if hashes() != first:
    raise RuntimeError('Repeated build changed files')
extend_course_en.build_site()
if hashes() != first:
    raise RuntimeError('Standalone English build changed shared or Chinese files')
check_static(root)
"""
            result = subprocess.run([sys.executable, '-B', '-c', code], cwd=target,
                                    capture_output=True, text=True, encoding='utf-8')
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
