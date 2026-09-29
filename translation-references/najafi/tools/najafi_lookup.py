#!/usr/bin/env python3
"""Najafi navigation lookup. Returned rows are navigation, not source evidence."""
from __future__ import annotations
import argparse,csv,difflib,re,unicodedata
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
VERIFIED=ROOT/"index"/"headwords-master.csv"
SOURCE=ROOT/"index"/"source-index-master.csv"
def norm(s):
    trans=str.maketrans({"ي":"ی","ك":"ک","ى":"ی","ۀ":"ه","ة":"ه","ؤ":"و","إ":"ا","أ":"ا","ٱ":"ا"})
    s=s.translate(trans)
    s="".join(ch for ch in unicodedata.normalize("NFKD",s) if unicodedata.category(ch)!="Mn")
    s=re.sub(r"[^\u0600-\u06FFA-Za-z0-9]+"," ",s)
    return re.sub(r"\s+"," ",s).strip().lower()
def load(p):
    with open(p,encoding="utf-8-sig") as f:return list(csv.DictReader(f))
def show(label,rows):
    print(label)
    for r in rows:
        keys=["headword","candidate_headword","pdf_page","printed_page","printed_page_refs_candidate","printed_pages_parsed","derived_pdf_pages_candidate","source_index_pdf_page","source_index_column","navigation_confidence","verification_status","status"]
        print({k:r.get(k,"") for k in keys if k in r})
def main():
    ap=argparse.ArgumentParser();ap.add_argument("query");ap.add_argument("--fuzzy",type=int,default=8);a=ap.parse_args();q=norm(a.query)
    verified=load(VERIFIED);source=load(SOURCE)
    exact=[r for r in verified if norm(r.get("headword",""))==q or norm(r.get("normalized_headword",""))==q]
    if exact:show("VERIFIED BODY-HEADING NAVIGATION — inspect scanned entry before evidence use",exact);return
    exact=[r for r in source if norm(r.get("candidate_headword",""))==q or norm(r.get("normalized_headword",""))==q]
    if exact:show("PRINTED SOURCE-INDEX CANDIDATE — visually verify body page before attribution",exact);return
    first={}
    for r in source:
        k=norm(r.get("candidate_headword",""))
        if k and k not in first:first[k]=r
    m=difflib.get_close_matches(q,list(first),n=a.fuzzy,cutoff=.48)
    if not m:print("No machine-index candidate. Inspect the relevant alphabetical range in the printed source index/canonical PDF.");return
    show("FUZZY PRINTED SOURCE-INDEX CANDIDATES — navigation only; verify visually",[first[x] for x in m])
if __name__=="__main__":main()
