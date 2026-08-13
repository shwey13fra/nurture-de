# rescore results (auto-written by `eval/rescore.py` — do not hand-edit)

- generated: 2026-08-13 18:05Z
- run file: `last_run_phase8b.json`  (43 records)
- golden labels: `eval/golden.jsonl`
- reproduce: `py eval/rescore.py --run last_run_phase8b.json`

| metric | as measured | after label correction |
|---|---|---|
| behaviour match (all 43) | 28/43 = 65% | 33/43 = 77% |
| behaviour match (answerable 26) | 15/26 = 58% | 18/26 = 69% |
| recall@5 (answerable) | 0.90 | 0.90 (unchanged) |

_label corrections / pass flips this run: 5_
