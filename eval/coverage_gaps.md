# Coverage gaps — lived-experience questions the corpus can't answer

The reviewer's questions came from lived experience; the corpus came from official federal
portals. The gap between them is **product research, not a defect**: most of what a real
user types is either medical (refuse by design) or outside the administrative portals
entirely. Each gap below is a lived-experience question the current 24-source corpus cannot
answer, grouped by **what would close it**. This is the Phase-13+ acquisition/architecture
roadmap.

The three groups are not the same kind of gap — and the third is the important one.

---

## A. A source exists and could be added (retrieval gap → fetch it)

An official page answers this; it's just not in the corpus yet. Candidate sources named.

| Question (abridged) | Likely source to add |
|---|---|
| What happens at the first pregnancy appointment, docs to bring (1.6) | BZgA / Krankenkasse pregnancy page |
| When is the Mutterpass issued, what's recorded (1.7) | G-BA / BZgA (partly in `gesund_vorsorge`) |
| Which check-ups/scans/labs statutory insurance covers (2.1, coverage detail) | GKV / TK "Leistungen Schwangerschaft" |
| IGeL / optional self-pay services (2.2) | IGeL-Monitor / GKV |
| What to ask when a test isn't covered (2.3) | UPD (patient advice) / GKV |
| When insurance covers additional prenatal tests (2.7) | G-BA / GKV |
| Statutory vs private coverage differences (2.8) | GKV + private-insurer pages |
| Which midwife services are covered, extra charges (3.5) | GKV / TK Hebammen page |
| Compare maternity hospitals — neonatal, C-section, pain relief… (5.1) | Weisse Liste / hospital quality reports |
| When/how to register for delivery at a hospital (5.2) | Individual hospital pages |
| What to ask at a hospital info evening (5.3) | Hospital pages |
| Backup hospital / no delivery room at labour (5.4) | Land (Hessen) health portal |
| Ambulance coverage / when to use 112 — coverage part (5.8) | GKV / Land rescue-service info |
| Register the birth, birth-certificate documents (part of 6.2) | Standesamt Frankfurt/Hessen (deeper than `fam_anmeldung`) |
| U1/U2 logistics, newborn screening — non-clinical *when/where* (Q40 subs) | GKV / Kinderuntersuchungsheft info |
| Student maternity financial support — Studentinnen *ohne Nebenerwerb* (c06, PM-2) | BMFSFJ Familienportal (Leistungen) / BAföG + Stiftungen |
| Civil-servant per-Bundesland Mutterschutz detail — Schutzfristen/Leistungen/Verbote (c08, PM-2) | Land Mutterschutzverordnungen / Personalstelle guidance |

**PM-2 note (c06, c08):** these two are a *different* kind of A-gap. Recall was **1.0** — the
right federal page (`fam_mutterschutz`) *was* retrieved; it is a hub/overview stub that lacks the
per-situation depth (student finance, per-Bundesland civil-servant rules). So the fix is fetching
the *deeper* page, not finding a missing source. The system answered correctly with
`answer_partial` (report the rule that applies, name the authority — Personalstelle / Familienportal);
the golden `answer` label was optimistic about corpus depth and was corrected. Thin corpus, not a
bad value (PM-2).

**Note the constraint:** several of these are **Land/municipal** (Frankfurt/Hessen) or
insurer-specific — exactly the pages that were 403'd or SPA-blocked in Phase 1
(`frankfurt.de`, `verwaltung.bund.de`). Adding them may need the manual-capture escape hatch,
not the crawler.

## B. Genuinely out of scope — medical, stays out by design

These are **not** gaps to fill. The system must refuse them (Rule 2/6) and refer to a doctor
or midwife; adding a source would be a liability, not a feature.

- Pre-pregnancy health checks / blood tests / vaccinations (1.1)
- Folic acid — whether and how long to take it (1.2)
- Whether an optional test is *medically necessary* for me (2.4)
- Differences between first-trimester screening, NIPT, amniocentesis (2.6)
- Who decides vaginal delivery / induction / planned C-section (5.5)
- How an emergency C-section is handled and consent obtained (5.6)
- When is it an emergency — call hospital / on-call / ambulance (5.7, urgency judgement)
- What the U2 tests are; when first vaccinations happen (Q40 subs)
- Where to take a newborn for an urgent medical problem (Q40 sub — refer, don't answer)

## C. No document can answer this — it needs a REFERRAL layer, not retrieval

The most interesting group. These are live-lookup / directory questions — the answer is a
*current, local, personal match*, not a passage of text. `referrals.yaml` already holds the
seed of this layer (Ammely, GKV midwife search): the product needs **both a retrieval layer
(cite documents) and a referral layer (hand off to a live lookup)**, and that only became
visible by writing real user questions.

| Question | The live lookup it needs |
|---|---|
| Find a suitable / English-speaking gynaecologist (1.3) | KV-Arztsuche / doctor directory with language filter |
| What if gynaecologists aren't accepting new patients (1.5) | KV Terminservicestelle (116117) |
| Where to find midwives for prenatal + postpartum care (3.2) | Ammely / GKV Hebammensuche (already in `referrals.yaml`) |
| What if I can't find an available midwife (3.6) | Ammely / Terminservice |
| How Caritas / Pro Familia / counselling centres help (3.7) | Pregnancy-counselling-centre directory |
| Find a paediatrician before birth; practices not accepting (Q40 subs) | KV-Arztsuche (paediatrics) |
| Book a Geburtsvorbereitungskurs (birth-prep course) | Course finder / midwife directory |

**Product implication:** a document-retrieval system alone cannot serve group C. The
architecture needs a referral/hand-off layer with a small set of trusted live endpoints —
which is why `referrals.yaml` was kept separate from the citable corpus from Phase 1. Worth
stating in the Phase-13 design.

---

_Groups A and C are the acquisition roadmap; group B is the safety boundary. The eval golden
set draws its `out_of_corpus` and `refuse_medical` cases from A/C and B respectively, so the
gap is measured, not just asserted._
