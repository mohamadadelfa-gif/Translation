#!/usr/bin/env python3
from pathlib import Path
import csv
import json
import hashlib
import sys

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / 'translation-references' / 'translation-craft' / 'corpus'
CSV = CORPUS / 'paired-sections.csv'


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def section_id(value):
    if isinstance(value, bool) or not isinstance(value, (str, int)):
        return None
    text = str(value).strip()
    return str(int(text)) if text.isdecimal() and int(text) > 0 else None


def validate(root=ROOT):
    errors = []
    mapping = {}
    duplicates = set()
    table = root / 'translation-references/translation-craft/corpus/paired-sections.csv'
    try:
        with table.open(encoding='utf-8-sig', newline='') as stream:
            rows = list(csv.DictReader(stream))
    except (OSError, UnicodeError, csv.Error) as exc:
        errors.append(f'Cannot read alignment table: {exc}')
        rows = []
    if len(rows) != 59:
        errors.append(f'Expected 59 aligned sections, found {len(rows)}.')
    for number, row in enumerate(rows, 2):
        section = section_id(row.get('section'))
        if section is None:
            errors.append(f'Alignment row {number}: missing or invalid section.')
            continue
        if section in mapping:
            duplicates.add(section)
            errors.append(f'Duplicate section mapping: {section}.')
        else:
            mapping[section] = row
        for language in ('english', 'persian'):
            name, expected = row.get(language + '_path'), row.get(language + '_sha256')
            if not name or not expected:
                errors.append(f'Section {section}: missing {language} path/checksum.')
                continue
            path = root / name
            if not path.is_file():
                errors.append(f'Missing {language} section {section}: {path}')
                continue
            try:
                if sha256(path) != expected:
                    errors.append(f'Checksum mismatch {language} section {section}: {path}')
            except OSError as exc:
                errors.append(f'Cannot read section {section}: {exc}')
    craft = root / 'translation-references/translation-craft/daryabandari/parallel-cases.jsonl'
    try:
        lines = craft.read_text(encoding='utf-8-sig').splitlines()
    except (OSError, UnicodeError) as exc:
        errors.append(f'Cannot read pilot cases: {exc}')
        lines = []
    for number, line in enumerate(lines, 1):
        if not line.strip():
            continue
        try:
            case = json.loads(line)
        except json.JSONDecodeError as exc:
            errors.append(f'Pilot line {number}: malformed JSON: {exc.msg}.')
            continue
        if not isinstance(case, dict):
            errors.append(f'Pilot line {number}: expected a JSON object.')
            continue
        section = section_id(case.get('section'))
        label = case.get('id', f'line {number}')
        if section is None:
            errors.append(f'Pilot {label}: missing or invalid section.')
        elif section in duplicates:
            errors.append(f'Pilot {label}: duplicate section mapping {section}.')
        elif section not in mapping:
            errors.append(f'Pilot {label}: unresolved section {section}.')
        else:
            for language in ('english', 'persian'):
                name = mapping[section].get(language + '_path')
                if not name or not (root / name).is_file():
                    errors.append(f'Pilot {label}: missing {language} file for section {section}.')
    return errors


if __name__ == '__main__':
    errors = validate()
    if errors:
        print('VALIDATION FAILED')
        for error in errors:
            print('-', error)
        sys.exit(1)
    print('VALIDATION OK')
    print('- 59 English/Persian section pairs present')
    print('- section checksums match')
    print('- pilot section IDs resolve through paired-sections.csv')
    print('- OCR/transcription and translation quality are not certified')
