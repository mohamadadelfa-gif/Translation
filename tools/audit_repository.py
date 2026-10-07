#!/usr/bin/env python3
"""Read-only structural audit for the Translation repository."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
BOOK_PDF_SHA256 = "0efedab3987f2dc797db4b5f10c290215e06556a39239097065f927fcef2f0be"

ACTIVE_DOCS = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "MENTOR_WORKFLOW.md",
    ROOT / "PROGRESS.md",
    ROOT / "translation-references" / "SOURCE-REGISTER.md",
    ROOT / "translation-references" / "SOURCE-PROVENANCE.md",
    ROOT / "translation-references" / "WORD-CHOICE-POLICY.md",
    ROOT / "translation-references" / "GLOSSARY.md",
    ROOT / "translation-references" / "GERMAN-CONCEPTS.md",
    ROOT / "drafts" / "README.md",
    ROOT / "approved-translations" / "README.md",
    ROOT / "translation-preparation" / "START-HERE.md",
    ROOT / "translation-preparation" / "CONTEXT-AND-STRUCTURE.md",
    ROOT / "tools" / "README.md",
]

REQUIRED = [
    ROOT / "README.md",
    ROOT / "AGENTS.md",
    ROOT / "MENTOR_WORKFLOW.md",
    ROOT / "PROGRESS.md",
    ROOT / "translation-references" / "SOURCE-REGISTER.md",
    ROOT / "translation-references" / "SOURCE-PROVENANCE.md",
    ROOT / "translation-references" / "GLOSSARY.md",
    ROOT / "translation-references" / "GERMAN-CONCEPTS.md",
    ROOT / "translation-references" / "najafi" / "tools" / "najafi_lookup.py",
    ROOT / "translation-references" / "translation-craft" / "corpus" / "paired-sections.csv",
    ROOT / "translation-preparation" / "C01.md",
    ROOT / "translation-preparation" / "PRACTICE-CHUNKS.json",
]

class Audit:
    def __init__(self):
        self.passes = []
        self.warnings = []
        self.failures = []

    def ok(self, msg):
        self.passes.append(msg)

    def warn(self, msg):
        self.warnings.append(msg)

    def fail(self, msg):
        self.failures.append(msg)

def rel(path):
    return path.relative_to(ROOT).as_posix()

def read(path):
    return path.read_text(encoding="utf-8-sig")

def files():
    return [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]

def resolve_link(source, target):
    target = target.strip().strip("<>")
    if not target or target.startswith("#"):
        return None
    if re.match(r"^[a-z]+://", target, re.I) or target.startswith("mailto:"):
        return None
    target = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not target:
        return None
    return (source.parent / target).resolve()

def check_required(a):
    missing = [rel(p) for p in REQUIRED if not p.exists()]
    if missing:
        for p in missing:
            a.fail("Required path missing: " + p)
    else:
        a.ok("All required control and retrieval paths exist.")

def check_authority(a):
    workflow = read(ROOT / "MENTOR_WORKFLOW.md")
    agents = read(ROOT / "AGENTS.md")
    register = read(ROOT / "translation-references" / "SOURCE-REGISTER.md")
    pointer = read(ROOT / "translation-references" / "WORD-CHOICE-POLICY.md")

    if "translation-references/TRANSLATION-PROFILE.md" in workflow:
        a.fail("Workflow still depends on nonexistent TRANSLATION-PROFILE.md.")
    else:
        a.ok("No ghost TRANSLATION-PROFILE.md dependency.")

    stale = re.search(r"(?<!translation-references/najafi/)tools/najafi_lookup\.py", workflow)
    if stale:
        a.fail("Workflow contains stale Najafi lookup-tool path.")
    elif "translation-references/najafi/tools/najafi_lookup.py" not in workflow:
        a.fail("Workflow does not name canonical Najafi lookup-tool path.")
    else:
        a.ok("Najafi lookup-tool wiring is canonical.")

    if "single authoritative workflow" not in agents.lower():
        a.fail("AGENTS.md does not declare the single workflow authority.")
    else:
        a.ok("Single workflow authority is explicit.")

    if "### Hezareh match semantics" in agents or "### Evidence-status discipline" in agents:
        a.fail("AGENTS.md still contains source-policy sections.")
    else:
        a.ok("AGENTS.md is operational rather than a parallel policy document.")

    old_sections = [
        "## 13. Evidence discipline",
        "## 14. Reference-use rule",
        "## 15. Core source-selection principle",
        "## 16. Practical lookup sequence",
        "## 18. Final rule",
    ]
    found = [h for h in old_sections if h in register]
    if found:
        for h in found:
            a.fail("SOURCE-REGISTER.md still contains duplicated workflow section: " + h)
    else:
        a.ok("SOURCE-REGISTER.md has no old parallel workflow tail.")

    if "not an independent workflow authority" not in pointer:
        a.fail("WORD-CHOICE-POLICY.md is not clearly subordinate.")
    else:
        a.ok("WORD-CHOICE-POLICY.md is a compatibility pointer.")

def check_links(a):
    pattern = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
    broken = []
    checked = 0
    for doc in ACTIVE_DOCS:
        if not doc.exists():
            continue
        for raw in pattern.findall(read(doc)):
            target = resolve_link(doc, raw)
            if target is None:
                continue
            checked += 1
            if not target.exists():
                broken.append(rel(doc) + " -> " + raw)
    if broken:
        for item in broken:
            a.fail("Broken internal Markdown link: " + item)
    else:
        a.ok("Internal Markdown links resolve (%d checked)." % checked)

def check_layers(a):
    tracked = files()

    old = [p for p in tracked if "translation-preparation/translation-craft-corpus" in p.as_posix()]
    if old:
        for p in old:
            a.fail("Old translation-craft path still tracked: " + rel(p))
    else:
        a.ok("No old translation-craft corpus paths remain.")

    root_drafts = [p for p in (ROOT / "drafts").glob("*") if p.is_file() and p.name != "README.md"]
    if root_drafts:
        for p in root_drafts:
            a.fail("Draft artifact is not chapter-scoped: " + rel(p))
    else:
        a.ok("All draft artifacts are chapter-scoped.")

    junk_re = re.compile(r"(^|/)(__pycache__|\.DS_Store|Thumbs\.db|desktop\.ini)(/|$)|\.tmp$|\.bak$|~$", re.I)
    junk = [rel(p) for p in tracked if junk_re.search(rel(p))]
    if junk:
        for p in junk:
            a.fail("Tracked temporary artifact: " + p)
    else:
        a.ok("No obvious temporary or cache artifacts are tracked.")

    leaked = []
    for p in (ROOT / "sources").rglob("*"):
        if p.is_file() and p.suffix.lower() in {".md", ".txt"}:
            try:
                text = read(p)
            except UnicodeError:
                continue
            if "<!-- practice-chunk:" in text:
                leaked.append(rel(p))
    if leaked:
        for p in leaked:
            a.fail("Practice-chunk marker leaked into frozen sources: " + p)
    else:
        a.ok("Practice-chunk markers are confined to working layers.")

def word_count(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    return len(re.findall(r"\S+", text))

def check_chunks(a):
    path = ROOT / "translation-preparation" / "C01.md"
    text = read(path)
    marker_re = re.compile(
        r"<!-- practice-chunk: (C\d\d-S\d\d-P\d\d) (START|END)(?:; source words: (\d+))? -->"
    )
    marks = list(marker_re.finditer(text))
    expected = {"C01-S01-P01": 338, "C01-S01-P02": 254}
    chunk_map_path = ROOT / "translation-preparation" / "PRACTICE-CHUNKS.json"
    chunk_map = json.loads(read(chunk_map_path))
    mapped = {item["id"]: item for item in chunk_map}

    for cid, expected_words in expected.items():
        item = mapped.get(cid)
        if item is None:
            a.fail("Practice Chunk missing from PRACTICE-CHUNKS.json: " + cid)
            continue
        if item.get("source_word_count") != expected_words:
            a.fail("%s map word count %r; expected %d." % (cid, item.get("source_word_count"), expected_words))

        start = next((m for m in marks if m.group(1) == cid and m.group(2) == "START"), None)
        end = next((m for m in marks if m.group(1) == cid and m.group(2) == "END"), None)
        if start is None or end is None:
            a.fail("Missing exact START or END marker for " + cid)
            continue
        declared = int(start.group(3)) if start.group(3) else None
        body = text[start.end():end.start()]
        actual = word_count(body)
        if declared != expected_words:
            a.fail("%s declared %r words; expected %d." % (cid, declared, expected_words))
        if actual != expected_words:
            a.fail("%s actual word count %d; expected %d." % (cid, actual, expected_words))
        if item.get("start_anchor") not in body:
            a.fail("%s start anchor is not inside its marked body." % cid)
        if item.get("end_anchor") not in body:
            a.fail("%s end anchor is not inside its marked body." % cid)
        if (
            declared == expected_words
            and actual == expected_words
            and item.get("source_word_count") == expected_words
            and item.get("start_anchor") in body
            and item.get("end_anchor") in body
        ):
            a.ok("%s map, anchors, boundary and word count verified (%d words)." % (cid, actual))

    progress = read(ROOT / "PROGRESS.md")
    if "**Current Practice Chunk:** `C01-S01-P02`" not in progress:
        a.fail("PROGRESS.md does not declare C01-S01-P02 as current Practice Chunk.")
    else:
        a.ok("PROGRESS.md current Practice Chunk is C01-S01-P02.")

    if "C01-S01-P02-draft-01.md" not in progress:
        a.fail("PROGRESS.md lacks canonical P02 next-save filename.")
    else:
        a.ok("PROGRESS.md records the canonical P02 next-save pattern.")

def check_names(a):
    chapter_re = re.compile(r"^C\d\d$")
    draft_re = re.compile(r"^C\d\d-S\d\d-P\d\d-(?:draft|reviewed|review-notes)-\d\d\.md$")
    legacy = []

    for chapter in (ROOT / "drafts").iterdir():
        if not chapter.is_dir():
            continue
        if not chapter_re.match(chapter.name):
            a.fail("Unexpected draft subdirectory: " + rel(chapter))
            continue
        for p in chapter.iterdir():
            if p.is_file() and not draft_re.match(p.name):
                legacy.append(rel(p))

    if legacy:
        a.warn("%d historical draft artifacts use legacy filenames; new saves must use Pxx names." % len(legacy))
    else:
        a.ok("All draft filenames use the current Pxx pattern.")

    approved = ROOT / "approved-translations"
    approved_re = re.compile(r"^C\d\d-S\d\d-P\d\d-approved\.md$")
    bad = []
    count = 0
    for p in approved.rglob("*"):
        if not p.is_file() or p.name == "README.md":
            continue
        count += 1
        r = p.relative_to(approved)
        if len(r.parts) != 2 or not chapter_re.match(r.parts[0]) or not approved_re.match(r.parts[1]):
            bad.append(rel(p))
    if bad:
        for p in bad:
            a.fail("Approved translation violates chapter/Pxx layout: " + p)
    else:
        a.ok("Approved translation layout valid (%d approved files)." % count)

def check_corpus(a):
    script = ROOT / "tools" / "validate_translation_craft_corpus.py"
    spec = importlib.util.spec_from_file_location("craft_validator", script)
    if spec is None or spec.loader is None:
        a.fail("Cannot load translation-craft validator.")
        return
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    errors = module.validate(ROOT)
    if errors:
        for error in errors:
            a.fail("Translation-craft corpus: " + error)
    else:
        a.ok("Translation-craft corpus validator passes.")

def check_provenance(a):
    prov = read(ROOT / "translation-references" / "SOURCE-PROVENANCE.md")
    if BOOK_PDF_SHA256 not in prov:
        a.fail("Recovered book-PDF checksum missing from SOURCE-PROVENANCE.md.")
    else:
        a.ok("Recovered book-PDF checksum is recorded.")

    matches = []
    for p in (ROOT / "sources").glob("*.pdf"):
        try:
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
        except OSError:
            continue
        if digest == BOOK_PDF_SHA256:
            matches.append(p)
    if matches:
        a.ok("Original book PDF is binary-tracked: " + rel(matches[0]))
    else:
        a.warn("Original book PDF is checksum-registered and recoverable but is not yet binary-tracked in GitHub.")

def check_tools(a):
    organize = read(ROOT / "tools" / "organize.ps1")
    dictionary = read(ROOT / "tools" / "test-dictionary.cjs")

    if "C:\\Users\\Adel\\Desktop" in organize:
        a.fail("organize.ps1 still has hard-coded Desktop input.")
    elif "sources\\revisiting-zero-hour-1945-structured.md" not in organize:
        a.fail("organize.ps1 lacks tracked default source.")
    elif "PRACTICE-CHUNKS.json" not in organize or "Practice-chunk start anchor not found" not in organize:
        a.fail("organize.ps1 does not fail closed while reapplying the Practice Chunk map.")
    else:
        a.ok("organize.ps1 has repository-default input and deterministic Practice Chunk reapplication.")

    if "C:/Users/Adel/Desktop" in dictionary:
        a.fail("test-dictionary.cjs still has hard-coded Desktop input.")
    elif "ARYANPOUR_LD2_PATH" not in dictionary or "--source" not in dictionary:
        a.fail("test-dictionary.cjs lacks explicit external-source configuration.")
    elif "d69ee28c3faa54648528e754aef85cb51f62f6330c0cadeed943ae2c5984d765" not in dictionary:
        a.fail("test-dictionary.cjs lacks known source checksum guard.")
    else:
        a.ok("Ariyanpour tool is parameterized and checksum-guarded.")

def main():
    a = Audit()
    check_required(a)
    check_authority(a)
    check_links(a)
    check_layers(a)
    check_chunks(a)
    check_names(a)
    check_corpus(a)
    check_provenance(a)
    check_tools(a)

    print("TRANSLATION REPOSITORY STRUCTURAL AUDIT")
    print("root:", ROOT)
    print()
    for msg in a.passes:
        print("PASS:", msg)
    for msg in a.warnings:
        print("WARN:", msg)
    for msg in a.failures:
        print("FAIL:", msg)
    print()
    print("summary: %d pass, %d warning, %d failure" % (len(a.passes), len(a.warnings), len(a.failures)))
    return 1 if a.failures else 0

if __name__ == "__main__":
    raise SystemExit(main())
