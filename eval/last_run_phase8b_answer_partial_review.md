# answer_partial diagnostic review

Every run the judge labelled `answer_partial`. Read a handful to decide the layer:
CORRECT BUT HEDGED (caveats, 'confirm with…', flags what's missing) → generator is
over-applying prompt rules 3/5, a **prompt** fix. GENUINELY INCOMPLETE → **context
assembly**. Retrieval is NOT the suspect here (recall is high on these).


---

## L06 / hybrid_rerank  (expected: answer_partial)

**Question:** What happens during the first pregnancy appointment, and which documents should I bring?

**Judge reason:** The answer provides grounded details about the first appointment itself but explicitly acknowledges it does not cover what documents to bring to that specific visit, only what to bring to the hospital for birth.

**Cited chunks:** ['tk_maternity_benefits__pregnancy-benefits__52dff011', 'tk_maternity_benefits__on-call-midwifery-service__adac2a20', 'gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__811d40c3', 'gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f']
**Retrieved top-5:** [('tk_maternity_benefits__pregnancy-benefits__52dff011', 0.0323), ('tk_maternity_benefits__on-call-midwifery-service__adac2a20', 0.0325), ('gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__811d40c3', 0.0287), ('gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f', 0.0293), ('gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__a5e2344d', 0.0299)]
**Citation validity:** 8/8

**Answer:**

**At the first appointment**, the doctor takes a full history and does a thorough examination: a physical and pelvic examination, blood pressure, weight, and lab work for blood values, blood group and Rhesus factor. You'll be told about HIV risks and offered an HIV test, and given advice on the flu vaccination, oral hygiene, and healthy eating in pregnancy. [1]

This is also usually when the **Mutterpass** (personal maternity notes) is issued — the booklet in which all findings from every later check-up are recorded. [2] Keep it with you at all times, so a doctor who doesn't know you can react properly in an unexpected situation. [1]

After that, check-ups are normally every four weeks, and every 14 days from around week 32. [2]

**On the documents:** I don't have information about what to bring to the *first* prenatal appointment. Your doctor's practice (Frauenarzt/Frauenärztin) or your health insurer can tell you — for statutory insurance this is usually handled through the practice when you book.

What the sources do cover is what to bring **to the hospital for the birth**, in case that's useful later:

- Mutterpass [3]
- personal identification (identity card or passport) [3]
- health insurance card [4]
- marriage certificate if you are married, or family register; birth certificate for single mothers [3][4]

Sources
[1] Techniker Krankenkasse — Pregnancy benefits — verified 2026-08-03
    tk_maternity_benefits__pregnancy-benefits__52dff011
[2] Bundesministerium für Gesundheit — Prenatal care: check-ups and counseling — verified 2026-08-03
    gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__811d40c3
[3] Techniker Krankenkasse — Childbirth / Important documents — verified 2026-08-03
    tk_maternity_benefits__on-call-midwifery-service__adac2a20
[4] Bundesministerium für Gesundheit — What needs to be packed in the hospital bag? — verified 2026-08-03
    gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f

---

## L10 / hybrid_rerank  (expected: answer_partial)

**Question:** Which examinations are considered optional self-pay services, or IGeL-Leistungen?

**Judge reason:** The answer provides specific examples of IGeL services (toxoplasmosis test, prenatal diagnostics, amniocentesis, chorionic villus sampling) and key conditions (insurance coverage in high-risk cases, informed consent requirement), but explicitly acknowledges that the sources do not provide a complete list of IGeL services and directs the user to the Mutterschafts-Richtlinien for the full scope.

**Cited chunks:** ['gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 'gesund_vorsorge_en__where-are-all-the-important-rules-and-regulations-to-be-foun__e5e1b986', 'gesund_vorsorge_de__wann-finden-die-vorsorgeuntersuchungen-statt__4ef8d67d']
**Retrieved top-5:** [('gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 0.0333), ('gesund_vorsorge_en__where-are-all-the-important-rules-and-regulations-to-be-foun__e5e1b986', 0.0292), ('tk_maternity_benefits__pregnancy-benefits__52dff011', 0.0258), ('gesund_vorsorge_de__wann-finden-die-vorsorgeuntersuchungen-statt__4ef8d67d', 0.0198), ('tk_maternity_benefits__pregnancy-benefits__e0864ce6', 0.0286)]
**Citation validity:** 7/7

**Answer:**

Tests that are **not** part of the standard prenatal care package are classed as individual health services — **IGeL** (individuelle Gesundheitsleistungen) — and you pay for them yourself. [1]

The examples named in the sources:

- **The toxoplasmosis test** (Toxoplasmose-Test) [1]
- **Certain prenatal diagnostic tests** (Pränataldiagnostik), for example tests that can detect chromosomal abnormalities such as trisomy 21 [1] — including procedures such as amniotic fluid sampling (**Fruchtwasserpunktion**) and placental tissue sampling (**Chorionzottenbiopsie**) [2]

Two important conditions:

- **Statutory health insurance does cover these** if there is a well-founded suspicion of a disease, in the case of a high-risk pregnancy, or if abnormalities need to be clarified. Only otherwise are they self-pay. [1][2]
- IGeL services may only be carried out **with your consent**, after you have been informed of the benefits and risks. All prenatal examinations are voluntary. [1][2]

One thing that is *not* available even as a self-pay service: additional ultrasound scans that are not medically necessary ("baby TV") have been prohibited since the start of 2021. [1]

The sources don't give a complete list of IGeL services in pregnancy. The full list of what statutory insurance *does* cover is in the maternity regulations — **Mutterschafts-Richtlinien** — issued by the Joint Federal Committee (Gemeinsamer Bundesausschuss, G-BA), available on the G-BA website. [3] Your gynaecological practice or your Krankenkasse can tell you what a specific test would cost.

Source [2] is from Familienportal/BMG in German only; I've translated the relevant passage.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_de__wann-finden-die-vorsorgeuntersuchungen-statt__4ef8d67d
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__where-are-all-the-important-rules-and-regulations-to-be-foun__e5e1b986

---

## L13 / hybrid_rerank  (expected: answer_partial)

**Question:** Can I take time to decide about an additional prenatal test, or must I agree during the appointment?

**Judge reason:** The answer confirms that prenatal tests are voluntary and no deadline is set by law, but explicitly acknowledges that the sources do not specify whether a reflection period exists or is required, directing the user to ask their doctor directly.

**Cited chunks:** ['gesund_vorsorge_de__wann-finden-die-vorsorgeuntersuchungen-statt__4ef8d67d', 'gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38']
**Retrieved top-5:** [('gesund_vorsorge_de__wann-finden-die-vorsorgeuntersuchungen-statt__4ef8d67d', 0.012), ('gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 0.0311), ('tk_maternity_benefits__pregnancy-benefits__52dff011', 0.0303), ('gesund_vorsorge_en__what-do-prenatal-check-ups-involve__b2799a30', 0.0307), ('gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f', 0.0277)]
**Citation validity:** 2/2

**Answer:**

The sources don't set a deadline for deciding — but they are clear that these tests are voluntary.

All prenatal examinations — **vorgeburtliche Untersuchungen** — are in principle voluntary. [1] Additional tests that aren't part of standard prenatal care (for example a toxoplasmosis test or tests for chromosomal abnormalities) are classed as individual health services — **IGeL**, short for *individuelle Gesundheitsleistungen*. These may only be performed if you have given your consent and have been informed about the possible benefits and risks. [2] Unless there is a well-founded suspicion of a disease, a high-risk pregnancy, or abnormalities to be clarified, you pay for them yourself. [2]

What the documents do **not** say is whether there is a time limit on your decision, or a required reflection period. That would depend on the specific test and on your doctor's practice — the gynaecological practice (**frauenärztliche Praxis**) is the place to ask how long you have. You can also ask to be given the information and decide at a later appointment.

For more background on prenatal diagnostics (**Pränataldiagnostik**), the Bundesministerium für Gesundheit points to the portal familienplanung.de run by the Bundesinstitut für Öffentliche Gesundheit (BIÖG). [1]

Note: source [1] is available in German only; I've translated the relevant passage.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_de__wann-finden-die-vorsorgeuntersuchungen-statt__4ef8d67d
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38

---

## L16 / hybrid_rerank  (expected: answer_partial)

**Question:** Which services may be covered differently by statutory insurance and private insurance?

**Judge reason:** The answer details what statutory insurance covers and notes that private coverage varies by individual contract, but explicitly acknowledges the sources do not provide a list of specific services private insurers cover or when private coverage systematically differs from statutory coverage.

**Cited chunks:** ['gesund_vorsorge_en__healthy-living-prenatal-care-check-ups-and-counseling__3b768553', 'gesund_vorsorge_en__what-is-prenatal-care__57d9d120', 'gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 'gesund_vorsorge_en__what-do-prenatal-check-ups-involve__b2799a30']
**Retrieved top-5:** [('gesund_vorsorge_en__healthy-living-prenatal-care-check-ups-and-counseling__3b768553', 0.0306), ('gesund_vorsorge_en__what-is-prenatal-care__57d9d120', 0.0281), ('gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 0.0325), ('gesund_vorsorge_en__what-do-prenatal-check-ups-involve__b2799a30', 0.0271), ('tk_maternity_benefits__postnatal-care__c0ec5b29', 0.0325)]
**Citation validity:** 4/4

**Answer:**

The documents draw only one distinction between statutory and private insurance, and it is a general one.

**Prenatal care overall:** the costs of prenatal care (check-ups and counseling) are covered by statutory health insurance funds and "usually also" by private health insurance providers. [1] A second passage says the same thing as "in most cases, also by private health insurance providers." [2] So the sources treat statutory coverage as certain and private coverage as typical but not guaranteed.

**What statutory insurance covers explicitly.** For those with statutory insurance (gesetzliche Krankenversicherung), prenatal services include counseling, testing such as blood pressure monitoring and blood tests for gestational diabetes, monitoring of high-risk pregnancies, ultrasound diagnostics, screening for HIV, hepatitis B, syphilis and chlamydia, and determining the rhesus factor. [3] Statutory insurance also covers check-ups and counseling for new mothers shortly after delivery, in the postpartum period (Wochenbett). [4]

**Where coverage varies within statutory insurance.** Some tests — the toxoplasmosis test and certain prenatal diagnostic tests, for example those detecting chromosomal abnormalities such as trisomy 21 — are not part of the standard statutory package. Health insurance providers will cover them if there is a well-founded suspicion of a disease, in a high-risk pregnancy, or if abnormalities need clarification. Otherwise they count as individual health services — **individuelle Gesundheitsleistungen (IGeL)** — which patients pay for themselves. [4]

What I don't have: the documents give no list of which specific services private insurers do or don't cover, and no explanation of when private coverage differs. That depends on your individual contract, so your private insurer (private Krankenversicherung) is the place to confirm it.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-is-prenatal-care__57d9d120
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__healthy-living-prenatal-care-check-ups-and-counseling__3b768553
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__b2799a30
[4] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38

---

## L20 / hybrid_rerank  (expected: answer)

**Question:** What services can a midwife provide before birth, during birth and after returning home?

**Judge reason:** The answer provides comprehensive, grounded coverage of midwife services across all three stages with proper source citations, but explicitly names a discrepancy between two federal sources on the exact number of postnatal visits and advises the user to confirm with their insurer—a deliberate acknowledgment of what is not fully settled in the corpus.

**Cited chunks:** ['gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286', 'gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f', 'gesund_geburtsvorbereitung_en__how-important-is-the-recovery-period-after-childbirth__1a701426', 'tk_maternity_benefits__postnatal-care__c0ec5b29']
**Retrieved top-5:** [('gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286', 0.0331), ('gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f', 0.0302), ('gesund_geburtsvorbereitung_en__how-important-is-the-recovery-period-after-childbirth__1a701426', 0.0318), ('tk_maternity_benefits__postnatal-care__c0ec5b29', 0.028), ('tk_maternity_benefits__on-call-midwifery-service__b41bd111', 0.031)]
**Citation validity:** 13/14

**Answer:**

A midwife (**Hebamme**) can support you across all three stages. Every pregnant woman is entitled to midwife assistance, and the costs are covered by statutory health insurance. [4]

**Before the birth**
- Antenatal (prenatal) care. [4]
- Support with health issues or problems during pregnancy. [4]
- Birthing classes and activity programmes — for example pregnancy swimming, yoga, meditation, baby massage and postnatal exercises. [4]

Midwives are often fully booked, so it helps to start looking early in the pregnancy. [4]

**During the birth**
- Assisting with the birth in a hospital, a birthing centre, or at home. [4]
- If you give birth in hospital, the hospital provides a midwife for the birth. [4]

**After you come home**
- Midwifery-led postnatal care during the first twelve weeks after childbirth; your doctor can prescribe additional postnatal care if necessary. [1]
- Home visits, where the midwife examines and weighs the baby regularly, and asks about any physical complaints you are having. [3]
- Advice on healthy eating, breastfeeding, postnatal exercise, skin care, and the daily care of the newborn — and she is your contact for any concerns or problems. [1]
- Support can continue by phone or with home visits until the child is 12 weeks old, and if necessary until the end of the breastfeeding period or when the child is 9 months old. [2] Another federal page describes this ongoing support as lasting up to 9 months after the birth. [4]

**On how many visits you get, the two federal sources differ:**
- One states up to 20 visits in the first 10 days after the birth. [2]
- The other states you may consult a midwife at least once a day for up to 10 days after the birth, and up to 16 visits in the first 12 weeks. [3]

Both were last verified on the same date, so I can't tell which is more current. Your health insurer or the midwife herself can confirm the exact number you're entitled to. Where there are problems — for example with breastfeeding — additional midwife visits are covered by health insurance. [3]

One exception: support from a lactation consultant (breastfeeding consultant) is not covered by statutory health insurance benefits, according to Techniker Krankenkasse. [1]

**Finding a midwife** — suggested places to look: your regional midwifery association (www.hebammenverband.de), the search engine www.ammely.de, the list from the National Association of Statutory Health Insurance Funds (**Spitzenverband der gesetzlichen Kranken- und Pflegekassen, GKV**, www.gkv-spitzenverband.de), midwifery and ob-gyn practices, your health insurer, the public health authority, family education centres, and hospitals or birthing centres. [4]

Sources
[1] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__postnatal-care__c0ec5b29
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-important-is-the-recovery-period-after-childbirth__1a701426
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f
[4] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286

---

## L26 / hybrid_rerank  (expected: answer)

**Question:** What is the difference between Mutterschutz and Elternzeit regarding duration, payment, job protection and eligibility?

**Judge reason:** The answer provides a complete grounded explanation of Mutterschutz across all four dimensions (duration, payment, job protection, eligibility) but explicitly acknowledges that Elternzeit coverage is incomplete—naming specific gaps (duration/splitting, dismissal protection, eligibility, application process) and directing the user to the appropriate federal authority for those details.

**Cited chunks:** ['tk_maternity_pay__what-is-the-mutterschutzfrist-maternity-protection-period__e6e51237', 'fam_mutterschutz__was-ist-der-unterschied-zwischen-mutterschutz-und-mutterschu__4eaeab66', 'tk_maternity_pay__what-is-mutterschaftsgeld-maternity-pay__c0c74de6', 'fam_staatliche_leistungen__mutterschutz-und-mutterschaftsleistungen__a9bb8567']
**Retrieved top-5:** [('tk_maternity_pay__what-is-the-mutterschutzfrist-maternity-protection-period__e6e51237', 0.0331), ('fam_mutterschutz__was-ist-der-unterschied-zwischen-mutterschutz-und-mutterschu__4eaeab66', 0.0238), ('tk_maternity_pay__what-is-mutterschaftsgeld-maternity-pay__c0c74de6', 0.0331), ('fam_staatliche_leistungen__mutterschutz-und-mutterschaftsleistungen__a9bb8567', 0.0222), ('fam_mutterschutz__welche-frauen-werden-geschuetzt__9d20eeda', 0.0223)]
**Citation validity:** 9/9

**Answer:**

**Short version:** Mutterschutz is a protection period around the birth with income replacement; Elternzeit is unpaid time off after that to care for your child. My documents cover Mutterschutz in detail but say very little about Elternzeit — I'll be clear about where the gap is.

---

## Mutterschutz

**What it is.** Mutterschutz is a special protection for employees (Arbeitnehmerinnen) who are pregnant or breastfeeding. It includes health protection at the workplace, special protection against dismissal (**Kündigungsschutz**), the employment ban (**Beschäftigungsverbot**), and income protection during that ban. It applies before and after the birth, and — with some particularities — also to pupils and students. [1]

**Duration.** The protection period — **Mutterschutzfrist** — is the time in which you are not allowed to work before and after the birth. It normally begins 6 weeks before the expected due date and ends 8 weeks after the birth, so usually 14 weeks in total. [1] It is extended to 12 weeks after delivery in the case of an early or multiple birth, or if a disability is diagnosed within 8 weeks after birth. If the child is born before the expected due date, the period is extended by the time lost before birth; if the birth is later than expected, the period is extended correspondingly. [2]

One special feature applies to the period *before* the birth: if you expressly wish it, you may continue working during those weeks. [1]

**Payment.** Income during this time comes from **Mutterschaftsleistungen** (maternity benefits). Which ones you can get depends, for example, on your work situation — the sources distinguish between employed, self-employed, marginally employed (geringfügig beschäftigt) and not employed. [3] Techniker Krankenkasse describes its own case: if you are a TK member and were working before, you usually receive maternity pay from the health insurance fund — 13 EUR per calendar day — and your employer tops up the difference to your previous net income. [4]

**Job protection.** Special protection against dismissal (Kündigungsschutz) is part of Mutterschutz. [1]

## Elternzeit

My documents contain only one statement about it: Elternzeit is **unpaid** time off from working life for parents who care for and raise their child themselves. [3]

Separately, **Elterngeld** is described as a benefit for parents of infants and small children, intended to make it possible for them to raise and care for their child. [3] Elterngeld and Elternzeit are two different things — one is money, one is leave from work.

## What I don't have

For Elternzeit, these documents do not cover:

- how long it lasts, or how it can be split
- whether and how dismissal protection applies during it
- who is eligible
- how and by when to apply

Those details would come from Familienportal des Bundes (the federal family portal), and for Elterngeld from your local **Elterngeldstelle**. For your own Mutterschaftsgeld amount and forms, your health insurer (Krankenkasse) and your employer are the ones who decide and pay.

Two of the sources below (Familienportal des Bundes) are available in German only; I've translated the relevant passages for you.

Sources
[1] Familienportal des Bundes (German only) — verified 2026-08-03
    fam_mutterschutz__was-ist-der-unterschied-zwischen-mutterschutz-und-mutterschu__4eaeab66
[2] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_pay__what-is-the-mutterschutzfrist-maternity-protection-period__e6e51237
[3] Familienportal des Bundes (German only) — verified 2026-08-03
    fam_staatliche_leistungen__mutterschutz-und-mutterschaftsleistungen__a9bb8567
[4] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_pay__what-is-mutterschaftsgeld-maternity-pay__c0c74de6

---

## L27 / hybrid_rerank  (expected: ask_for_attributes)

**Question:** How are Mutterschaftsgeld, the employer supplement, Elterngeld and salary calculated?

**Judge reason:** The answer fully explains the employer supplement and how Mutterschaftsleistungen offset against Elterngeld, but explicitly declares three gaps: the Mutterschaftsgeld amount itself, the Elterngeld formula from prior income, and ordinary salary during the protection period are not covered in the corpus.

**Cited chunks:** ['fam_mutterschaftsleistungen__wie-kann-ich-den-arbeitgeberzuschuss-zum-mutterschaftsgeld-b__6767b2c2', 'fam_mutterschaftsleistungen__wie-hoch-ist-der-arbeitgeberzuschuss-zum-mutterschaftsgeld__79c5220d', 'fam_elterngeld_faq__kann-ich-elterngeld-und-mutterschaftsleistungen-bekommen__7b2a66e9', 'fam_elterngeld_faq__kann-ich-elterngeld-und-mutterschaftsleistungen-bekommen__93d50023']
**Retrieved top-5:** [('fam_mutterschaftsleistungen__wie-kann-ich-den-arbeitgeberzuschuss-zum-mutterschaftsgeld-b__6767b2c2', 0.0141), ('fam_mutterschaftsleistungen__wie-hoch-ist-der-arbeitgeberzuschuss-zum-mutterschaftsgeld__79c5220d', 0.0198), ('fam_elterngeld_faq__kann-ich-elterngeld-und-mutterschaftsleistungen-bekommen__7b2a66e9', 0.0187), ('fam_elterngeld_faq__kann-ich-elterngeld-und-mutterschaftsleistungen-bekommen__93d50023', 0.0178), ('tk_maternity_pay__what-is-mutterschaftsgeld-maternity-pay__c0c74de6', 0.0331)]
**Citation validity:** 0/0

**Answer:**

Here is what the documents cover — and what they don't.

## Employer supplement (**Arbeitgeberzuschuss zum Mutterschaftsgeld**)

This is calculated individually. The basis is your average daily wage (**durchschnittliches kalendertägliches Arbeitsentgelt**) over the last 3 settled calendar months before the start of the protection period (**Mutterschutzfrist**) before the birth, which begins 6 weeks before the expected date of birth. [1]

The health insurer (**Krankenkasse**) pays 13 euros per day; the employer pays the difference. [1] The employer is obliged to pay the supplement if the average daily net wage before the protection period is higher than 13 euros — so from a monthly net wage of 390 euros. [1]

The worked example in the source: with a monthly net of 1,800 euros and a 30-day month, that is 60 euros per day. 13 euros come from the Krankenkasse, the remaining 47 euros from the employer. There are no further deductions. [1]

Not included in the calculation: [1]
- holiday or Christmas pay (**Urlaubs- oder Weihnachtsgeld**)
- one-off payments such as bonuses
- days without wages due to short-time work (**Kurzarbeit**) or work stoppages

The supplement counts as wage or wage replacement, and the employer must pay it on the same dates as your previous salary. [1]

**Special case — during Elternzeit:** if you work part-time during parental leave, the Mutterschaftsgeld and the supplement are calculated from that part-time income. [2] If you do not work part-time, there is no employer supplement. [2] If Elternzeit ends before the Mutterschutzfrist, the employment relationship revives automatically and the supplement is paid without an application, calculated from the income you had before Elternzeit and would have had again. [2] If you ended a part-time Elternzeit early, it must be checked which basis is more favourable for you — income during or before the Elternzeit. [2] Legal basis: § 22 MuSchG. [2]

## Elterngeld and Mutterschaftsleistungen

The documents do not explain how the Elterngeld amount itself is calculated. They explain how Mutterschaftsleistungen are offset against it.

Mutterschaftsleistungen include the Mutterschaftsgeld from statutory health insurers, the employer supplement, and the salary of civil servants (**Dienstbezüge für Beamtinnen**) during Mutterschutz — but not the one-off 210 euros from the Bundesamt für Soziale Sicherung for people who are not in statutory health insurance. [3]

Payments for the same child are offset in full against Elterngeld, because they serve the same purpose. [3] The result: if the Mutterschaftsleistungen are higher than the Elterngeld, only the Mutterschaftsleistungen are paid; if the Elterngeld is higher, the difference is paid on top as Elterngeld. [3]

Months in which Mutterschaftsleistungen are received for the same child count as months of **Basiselterngeld** — even if entitlement existed for only one day of that month. [3]

Offsetting is done to the day (**tageweise Verrechnung**), because Mutterschaftsleistungen are calculated in days while Elterngeld is not. If the payments end partway through a month of life (**Lebensmonat**), Elterngeld is paid pro rata for the remaining days. [4] The source's example: child born 20 May, Mutterschaftsleistungen for the first 8 weeks ending 14 July. The first Lebensmonat (20 May–19 June) brings no Basiselterngeld. The second (20 June–19 July) has 5 remaining days out of 30, so one sixth of the monthly amount is paid. From the third Lebensmonat, the full amount. [4]

## What I don't have

- **How the Mutterschaftsgeld amount itself is calculated.** The documents only mention the 13 euros per day paid by the Krankenkasse as part of the supplement calculation. [1] Your statutory health insurer (**Krankenkasse**) holds the rules and the process for this.
- **How the Elterngeld amount is calculated** from prior income. That would come from Familienportal des Bundes or the Elterngeldstelle in your Land.
- **Salary during the Mutterschutzfrist.** Nothing in these documents covers how ordinary pay is handled during the protection period, apart from the supplement rules above. Your employer would hold this.

These pages are from Familienportal des Bundes, which is published in German; I have translated the relevant passages.

Sources
[1] Familienportal des Bundes — verified 2026-08-03
    fam_mutterschaftsleistungen__wie-hoch-ist-der-arbeitgeberzuschuss-zum-mutterschaftsgeld__79c5220d
[2] Familienportal des Bundes — verified 2026-08-03
    fam_mutterschaftsleistungen__wie-kann-ich-den-arbeitgeberzuschuss-zum-mutterschaftsgeld-b__6767b2c2
[3] Familienportal des Bundes — verified 2026-08-03
    fam_elterngeld_faq__kann-ich-elterngeld-und-mutterschaftsleistungen-bekommen__93d50023
[4] Familienportal des Bundes — verified 2026-08-03
    fam_elterngeld_faq__kann-ich-elterngeld-und-mutterschaftsleistungen-bekommen__7b2a66e9

---

## L28 / hybrid_rerank  (expected: answer)

**Question:** What workplace protections apply during pregnancy, such as restrictions on heavy lifting, night shifts, overtime, dangerous substances or long periods of standing?

**Judge reason:** The answer comprehensively covers restrictions on heavy lifting, night shifts, standing, and dangerous substances from official federal sources, but explicitly acknowledges one gap: whether pregnant workers may voluntarily consent to night or Sunday work despite the ban, noting the full source would be needed for that detail.

**Cited chunks:** ['fam_mutterschutz__was-ist-ein-vorlaeufiges-beschaeftigungsverbot__6b212f50', 'fam_mutterschutz__was-ist-ein-vorlaeufiges-beschaeftigungsverbot__46231bfd', 'fam_mutterschutz__was-sind-die-beschaeftigungsverbote-durch-den-arbeitgeber-od__317681ed', 'fam_mutterschutz__was-ist-mutterschutz__83a8026c']
**Retrieved top-5:** [('fam_mutterschutz__was-ist-ein-vorlaeufiges-beschaeftigungsverbot__6b212f50', 0.0147), ('fam_mutterschutz__was-ist-ein-vorlaeufiges-beschaeftigungsverbot__46231bfd', 0.0114), ('fam_mutterschutz__was-sind-die-beschaeftigungsverbote-durch-den-arbeitgeber-od__317681ed', 0.0087), ('fam_mutterschutz__was-ist-mutterschutz__83a8026c', 0.0118), ('fam_mutterschutz__welche-frauen-werden-geschuetzt__9d20eeda', 0.0111)]
**Citation validity:** 19/19

**Answer:**

Pregnancy protections at work in Germany fall under **Mutterschutz** (maternity protection). Here's what the official federal source says.

**Note on language:** this comes from Familienportal des Bundes, which is available in German only. I've translated the relevant passages and kept the German terms.

## The general framework

Mutterschutz applies to women in an employment relationship who are pregnant or breastfeeding, and protects both mother and child, before and after birth. It includes health protection at the workplace, special protection against dismissal (**Kündigungsschutz**), an employment ban in the weeks before and after birth, and income security during that ban. [1]

Students, pupils and people in the Bundesfreiwilligendienst also have a claim to Mutterschutz. [1]

Your employer must identify risks in advance through a risk assessment (**Gefährdungsbeurteilung**). You have a right to a personal conversation with your employer about making your working conditions suitable during pregnancy. The earlier you tell your employer about the pregnancy, the better they can put effective protection in place. [1]

## Work you may not do (unverantwortbare Gefährdung)

If you are exposed to particular strains at work that constitute an unacceptable risk (**unverantwortbare Gefährdung**), you may not do that work. This applies for example to: [4]

- **Lifting:** work where you regularly or occasionally lift, or move loads over 5 kilograms without mechanical aids
- **Night work** (**Nachtarbeit**), meaning work between 8:00 pm and 6:00 am
- Work on **Sundays or public holidays**
- **Standing:** from the 6th month of pregnancy, if you have to stand continuously for four hours a day with little movement
- Work with substances hazardous to health, radiation, dust, gases, vapours, heat, cold, wet, vibration, noise or infectious material
- Work with increased risk of accident
- Piecework and assembly-line work (**Akkord-Arbeit und Fließband-Arbeit**)
- Work involving frequent stretching, bending, squatting or stooping
- Operating equipment or machines that place particular strain on your feet
- Work with a particular risk of developing an occupational disease
- Driving or operating vehicles yourself

## Maximum working hours (Höchstarbeitszeiten)

These are set in the Mutterschutzgesetz: [3]

- **Under 18:** no more than 8 hours per day, and no more than 80 hours in 2 consecutive weeks
- **18 and over:** no more than 8.5 hours per day, maximum 90 hours per double week

In addition, your employer may not employ you beyond the contractually agreed weekly working time, averaged over the month. Statutory rest breaks and travel time between home and work do not count as working time. If you work for several employers, the hours are added together — and you must tell your employer about your hours with the others. [3]

## The three kinds of employment ban (Beschäftigungsverbot)

- **Betriebliches Beschäftigungsverbot** — issued by your employer
- **Behördliches Beschäftigungsverbot** — issued by the responsible supervisory authority (**Aufsichtsbehörde**)
- **Ärztliches Beschäftigungsverbot** — issued by a doctor

The first two depend on the work you do, not on your state of health. A medical ban depends on your health or that of your (unborn) child. [2]

Before an employment ban happens, your employer must check whether they can adapt your working conditions to comply with Mutterschutz, or whether you could continue working at a different workplace. [1] The employer must exhaust all possibilities for continuing to employ you, and the ban applies only to the extent necessary to avoid risks to you or your child. [2]

**Vorläufiges Beschäftigungsverbot** (provisional ban): if your employer has not taken the required protective measures — for example because they haven't updated the Gefährdungsbeurteilung for your tasks and workplace — they may not employ you until those measures are in place. [3]

## Who to ask

The **Aufsichtsbehörde** responsible for your workplace can answer questions about Mutterschutz [1] and can confirm what options for continued employment your employer must offer you if you are in doubt. [3][2] If your employer hasn't put protective measures in place, you can contact the Aufsichtsbehörde to clarify — and if necessary your gynaecologist can certify a corresponding ban. [3]

One gap: the source raises the question of whether you may work Sundays or nights voluntarily if you want to, but the retrieved text does not contain the answer. The Aufsichtsbehörde for your workplace, or the full Familienportal page, would cover that.

Sources
[1] Familienportal des Bundes — verified 2026-08-03
    fam_mutterschutz__was-ist-mutterschutz__83a8026c
[2] Familienportal des Bundes — verified 2026-08-03
    fam_mutterschutz__was-sind-die-beschaeftigungsverbote-durch-den-arbeitgeber-od__317681ed
[3] Familienportal des Bundes — verified 2026-08-03
    fam_mutterschutz__was-ist-ein-vorlaeufiges-beschaeftigungsverbot__46231bfd
[4] Familienportal des Bundes — verified 2026-08-03
    fam_mutterschutz__was-ist-ein-vorlaeufiges-beschaeftigungsverbot__6b212f50

---

## L30 / hybrid_rerank  (expected: answer)

**Question:** Can I attend prenatal appointments during working hours, and will I continue to be paid?

**Judge reason:** The assistant declines to answer the main question about pay during prenatal appointments, correctly identifying it as outside the provided corpus, but helpfully directs the user to the Mutterschutzgesetz and relevant authorities while providing related information (appointment frequency) that is covered.

**Cited chunks:** ['tk_maternity_benefits__pregnancy-benefits__52dff011', 'fam_mutterschutz__was-ist-ein-vorlaeufiges-beschaeftigungsverbot__46231bfd']
**Retrieved top-5:** [('fam_mutterschaftsleistungen__kann-ich-auch-dann-mutterschaftsgeld-bekommen-wenn-ich-in-de__2a3fba6b', 0.0089), ('tk_maternity_benefits__pregnancy-benefits__52dff011', 0.0315), ('tk_maternity_pay__how-much-maternity-pay-will-i-get__0a5004f4', 0.0277), ('fam_mutterschutz__was-ist-ein-vorlaeufiges-beschaeftigungsverbot__46231bfd', 0.008), ('fam_mutterschutz__gibt-es-mutterschutz-fuer-studentinnen__22189573', 0.0139)]
**Citation validity:** 2/2

**Answer:**

I don't have information on this. The documents I have don't cover time off from work for antenatal appointments (Untersuchungen) or whether pay continues during them.

What I can tell you about where to look:

- These workplace rules sit in the **Mutterschutzgesetz** (the Maternity Protection Act), which is the law that also governs maximum working hours during pregnancy. [1] The **Familienportal des Bundes** section on Mutterschutz is the federal source that explains it.
- Your employer is the first point of contact for how this is handled at your workplace.
- For questions about your employer's obligations under Mutterschutz, the supervisory authority — **Aufsichtsbehörde** — is the body you can contact for clarification. [1] Which office this is depends on your Bundesland.

One related thing the documents do cover, in case it's useful for planning: Techniker Krankenkasse describes the normal schedule of routine antenatal check-ups — every four weeks during an uncomplicated pregnancy, and every two weeks during the last two months before birth. [2] That's the medical schedule only, not your rights at work.

Sources
[1] Familienportal des Bundes — verified 2026-08-03 (German only)
    fam_mutterschutz__was-ist-ein-vorlaeufiges-beschaeftigungsverbot__46231bfd
[2] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__pregnancy-benefits__52dff011

---

## L39 / hybrid_rerank  (expected: answer)

**Question:** What should be prepared before birth, including the hospital bag, baby clothing, car seat, important documents and arrangements for returning home?

**Judge reason:** The answer covers hospital bag, baby clothing, important documents, and general birth preparation from official sources, but explicitly acknowledges that car seat requirements and detailed journey-home arrangements are not in the corpus and directs the user to BZgA resources and their midwife/hospital for those topics.

**Cited chunks:** ['gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f', 'tk_maternity_benefits__on-call-midwifery-service__adac2a20', 'gesund_geburtsvorbereitung_en__what-needs-to-be-sorted-after-the-birth__70bcb197', 'gesund_geburtsvorbereitung_en__how-can-i-prepare-myself-for-the-birth-of-my-baby__7fc0b179']
**Retrieved top-5:** [('gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f', 0.0333), ('tk_maternity_benefits__on-call-midwifery-service__adac2a20', 0.0305), ('gesund_geburtsvorbereitung_en__what-needs-to-be-sorted-after-the-birth__70bcb197', 0.0313), ('gesund_geburtsvorbereitung_en__how-can-i-prepare-myself-for-the-birth-of-my-baby__7fc0b179', 0.0276), ('gesund_unterstuetzung_de__welche-herausforderungen-bestehen-in-der-zeit-nach-der-gebur__1ec5db19', 0.0194)]
**Citation validity:** 8/8

**Answer:**

Here's what the official sources cover.

**Pack the bag a few weeks before the due date.** Labour can start earlier than expected, so the bag should be ready ahead of time — including if you plan a home birth or an outpatient hospital delivery, in case of an emergency. Label everything with the mother's name if possible. [1]

**Important documents to pack** [1]
- maternity record (**Mutterpass**)
- personal identification card
- health insurance card
- family register or marriage certificate (**Stammbuch/Heiratsurkunde**); birth certificate for single mothers

Techniker Krankenkasse adds that you should bring your Mutterpass and personal identification (identity card, passport or similar) to the hospital, plus your marriage certificate if you are married. [2]

**For the birth** [1]
Comfortable clothes, T-shirts to change into, warm socks and a warm fleece jacket or cardigan, hairband, favourite music, massage/aromatherapy/bath oil, essential aids such as glasses or hearing aids, phone or camera plus charger, energy-rich snacks or fruit, and a list of phone numbers for people to inform after the birth.

**For a hospital stay** [1]
Comfortable clothes for after the birth (roughly what fitted in the sixth month of pregnancy), nightdress or pyjamas, slippers, dressing gown, breastfeeding bra and pads, nursing tops or loose wide shirts, towels and washcloths, toiletries.

**Baby clothing and items** [1]
- baby vests in size 56 to 62
- sleepsuits or soft trousers, tops, socks
- newborn jacket and hat
- baby blanket
- diapers for the trip home

**Other preparation before the birth**
Expectant parents need to choose a midwife (**Hebamme**) and decide where to have the baby. Information is available from hospital or birthing-centre information events, birthing classes, and counselling services. [3] Register at the hospital where you plan to give birth as early as possible. [2]

Some of the paperwork that follows the birth can also be started or completed beforehand. [4] It is also worth going through the packing list with your hospital or midwife in advance. [1]

**What I don't have**

The documents say nothing about a **car seat (Kindersitz)** or about arrangements for the journey home beyond packing diapers for the trip. [1] For those, the sources point to the detailed checklists published by the Bundeszentrale für gesundheitliche Aufklärung (BZgA) at familienplanung.de. [1][4] Your midwife or hospital can also advise on the trip home.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f
[2] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__on-call-midwifery-service__adac2a20
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-can-i-prepare-myself-for-the-birth-of-my-baby__7fc0b179
[4] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__what-needs-to-be-sorted-after-the-birth__70bcb197

---

## c06 / hybrid_rerank  (expected: answer)

**Question:** Ich studiere und bin schwanger — gilt der Mutterschutz auch für mich?

**Judge reason:** The answer comprehensively addresses maternity protection for students but explicitly hedges on financial support ('unter Umständen aber besondere Unterstützung') without naming the specific support programs or eligibility criteria, leaving a gap in the completeness of the financial guidance.

**Cited chunks:** ['fam_mutterschutz__gibt-es-mutterschutz-fuer-studentinnen__22189573', 'fam_staatliche_leistungen__mutterschutz-und-mutterschaftsleistungen__a9bb8567']
**Retrieved top-5:** [('fam_mutterschutz__gibt-es-mutterschutz-fuer-studentinnen__22189573', 0.0331), ('fam_mutterschutz__gibt-es-mutterschutz-fuer-schuelerinnen__f28e39aa', 0.0328), ('fam_mutterschutz__gibt-es-mutterschutz-in-der-ausbildung__0c3eaaaf', 0.0312), ('fam_staatliche_leistungen__mutterschutz-und-mutterschaftsleistungen__a9bb8567', 0.0317), ('fam_mutterschutz__gibt-es-mutterschutz-fuer-studentinnen__0bc9b840', 0.0292)]
**Citation validity:** 6/6

**Answer:**

**Ja — Mutterschutz gilt auch für Studentinnen.** [1]

Konkret heißt das: Sie dürfen bei verpflichtenden Veranstaltungen, Prüfungen oder Praktika fehlen, wenn diese für Sie oder Ihr Kind eine unverantwortbare Gefährdung darstellen. Daraus dürfen Ihnen keine Nachteile entstehen. Innerhalb der **Mutterschutzfristen** gilt das unabhängig davon, ob eine Gefährdung vorliegt. [1]

Besonderheiten für Studentinnen:

- Sie **können** auch während der Mutterschutzfristen an Veranstaltungen, Prüfungen oder Praktika teilnehmen, wenn Sie das möchten. Dafür müssen Sie das gegenüber Ihrer Hochschule ausdrücklich verlangen. Sie können diese Erklärung jederzeit für die Zukunft widerrufen. [1]
- Zwischen 20 und 22 Uhr sowie an Sonn- und Feiertagen dürfen Sie tätig werden, wenn Sie einwilligen und es für Ihre Studienzwecke erforderlich ist. Ein behördliches Genehmigungsverfahren ist nicht nötig; Ihre Hochschule muss die Teilnahme zwischen 20 und 22 Uhr aber der zuständigen Aufsichtsbehörde melden. [1]
- Die besonderen Regelungen zu **Kündigungsschutz** und **Leistungen** sind auf Studentinnen **ohne Erwerbseinkommen** normalerweise nicht anzuwenden. [1]
- Studentinnen ohne Erwerbseinkommen können unter bestimmten Voraussetzungen aber Unterstützungen beantragen. [1]

Zum Geld: **Mutterschaftsgeld** können Studentinnen erhalten, wenn sie einen Nebenerwerb haben. Ohne Nebenjob gibt es kein Mutterschaftsgeld, unter Umständen aber besondere Unterstützung. [2]

Sources
[1] Familienportal des Bundes — verified 2026-08-03
    fam_mutterschutz__gibt-es-mutterschutz-fuer-studentinnen__22189573
[2] Familienportal des Bundes — verified 2026-08-03
    fam_staatliche_leistungen__mutterschutz-und-mutterschaftsleistungen__a9bb8567

---

## c08 / hybrid_rerank  (expected: answer)

**Question:** Ich bin verbeamtet und erwarte ein Kind — welcher Mutterschutz gilt für mich?

**Judge reason:** The answer correctly identifies that civil servants have special maternity protections distinct from the general law and directs to the appropriate authority tier (employer HR office), but explicitly acknowledges that detailed rules (protection periods, benefits, employment prohibitions) vary by state and are not provided in the sources.

**Cited chunks:** ['fam_mutterschutz__welche-regelungen-fuer-den-mutterschutz-gelten-fuer-beamtinn__eb325d8b', 'fam_elterngeld_faq__kann-ich-elterngeld-und-mutterschaftsleistungen-bekommen__93d50023']
**Retrieved top-5:** [('fam_mutterschutz__welche-regelungen-fuer-den-mutterschutz-gelten-fuer-beamtinn__eb325d8b', 0.0328), ('fam_staatliche_leistungen__mutterschutz-und-mutterschaftsleistungen__a9bb8567', 0.0318), ('fam_elterngeld_faq__kann-ich-elterngeld-und-mutterschaftsleistungen-bekommen__93d50023', 0.0299), ('fam_elterngeld_faq__wie-lange-kann-ich-elterngeld-bekommen__5479b3ba', 0.0137), ('fam_elterngeld_antrag__welche-nachweise-muss-ich-dem-antrag-beifuegen__49e736fe', 0.0154)]
**Citation validity:** 6/6

**Answer:**

Für Beamtinnen gilt der Mutterschutz nach besonderen Regelungen — nicht nach dem allgemeinen Mutterschutzgesetz. [1] Welche genau für Sie gelten, hängt davon ab, ob Sie Bundes- oder Landesbeamtin sind:

- **Bundesbeamtin:** Es gilt die **Mutterschutzverordnung des Bundes**. [1]
- **Landesbeamtin:** Es gilt die **Mutterschutzverordnung Ihres Bundeslandes**. In einigen Bundesländern gilt ebenfalls die Mutterschutzverordnung des Bundes. [1]

Die inhaltlichen Einzelheiten dieser Verordnungen — also Schutzfristen, Leistungen und Beschäftigungsverbote für Beamtinnen — sind in meinen Unterlagen ausdrücklich nicht enthalten, weil sie sich je nach Bundesland unterscheiden. [1]

Die Stelle, die Ihnen das verbindlich sagen kann, ist die **Personalstelle in Ihrer Behörde**. [1] Wenden Sie sich dorthin, um die für Sie geltenden Regelungen und Leistungen zu erfahren.

Ein Hinweis, falls später Elterngeld eine Rolle spielt: Die **Dienstbezüge für Beamtinnen während des Mutterschutzes** gelten als Mutterschaftsleistung und werden auf das Elterngeld angerechnet. [2]

Sources
[1] Familienportal des Bundes — verified 2026-08-03
    fam_mutterschutz__welche-regelungen-fuer-den-mutterschutz-gelten-fuer-beamtinn__eb325d8b
[2] Familienportal des Bundes — verified 2026-08-03
    fam_elterngeld_faq__kann-ich-elterngeld-und-mutterschaftsleistungen-bekommen__93d50023

---

## h2 / hybrid_rerank  (expected: answer)

**Question:** Ich bekomme wegen eines Beschäftigungsverbots während der Schwangerschaft kein Gehalt — ist das Mutterschaftsgeld oder etwas anderes?

**Judge reason:** The answer correctly distinguishes between Mutterschutzlohn and Mutterschaftsgeld from the sources, but explicitly acknowledges gaps: it states nothing is available in the sources about the amount of Mutterschutzlohn or who pays it, referring the user to their employer or health insurance instead.

**Cited chunks:** ['fam_mutterschaftsleistungen__was-sind-mutterschaftsleistungen-mutterschutzlohn-und-mutter__3572c161', 'fam_mutterschutz__was-ist-mutterschutz__59f28ae5']
**Retrieved top-5:** [('fam_mutterschaftsleistungen__was-sind-mutterschaftsleistungen-mutterschutzlohn-und-mutter__3572c161', 0.0305), ('fam_mutterschaftsleistungen__kann-ich-mutterschaftsgeld-bekommen-wenn-mir-waehrend-der-sc__46ed6aac', 0.031), ('fam_mutterschaftsleistungen__kann-ich-mutterschaftsgeld-des-bundesamtes-fuer-soziale-sich__d5708176', 0.0272), ('fam_mutterschutz__was-ist-mutterschutz__59f28ae5', 0.0244), ('fam_mutterschaftsleistungen__wann-und-wie-kann-ich-den-arbeitgeberzuschuss-zum-mutterscha__fdb63e59', 0.0233)]
**Citation validity:** 3/3

**Answer:**

Das ist in der Regel nicht Mutterschaftsgeld, sondern **Mutterschutzlohn**.

Die Familienportal-Seite unterscheidet so:

- **Mutterschutzlohn** bekommen Sie vor und nach der Mutterschutzfrist, wenn Sie nicht arbeiten dürfen – zum Beispiel wegen eines ärztlichen Beschäftigungsverbots. [1]
- **Mutterschaftsgeld** gehört zu den Leistungen während der **Mutterschutzfrist**, also grundsätzlich in den letzten 6 Wochen vor der Geburt, am Tag der Entbindung und 8 Wochen nach der Geburt. [1]

Ein **Beschäftigungsverbot** kann auch entstehen, wenn Ihr Arbeitgeber Gefährdungen für Ihre Gesundheit oder die des Kindes nicht durch Schutzmaßnahmen ausschließen kann. Es darf nur so weit reichen, wie es zum Schutz nötig ist, und kann sich auch auf bestimmte Tätigkeiten oder Arbeitszeiten beschränken. [2]

Welche Mutterschaftsleistungen für Sie in Frage kommen, hängt laut Quelle von Ihrer Arbeitssituation, Ihrer Krankenversicherung und davon ab, ob Sie sich in den Mutterschutzfristen befinden. [1] Rechtsgrundlage sind §§ 18 ff. Mutterschutzgesetz (MuSchG). [1]

Zur Höhe des Mutterschutzlohns und dazu, wer ihn auszahlt, steht in den mir vorliegenden Unterlagen nichts – das wäre eine Frage an Ihren Arbeitgeber bzw. an Ihre Krankenkasse.

Die Informationen stammen vom Familienportal des Bundes, das hier nur auf Deutsch vorliegt.

Sources
[1] Familienportal des Bundes — verified 2026-08-03
    fam_mutterschaftsleistungen__was-sind-mutterschaftsleistungen-mutterschutzlohn-und-mutter__3572c161
[2] Familienportal des Bundes — verified 2026-08-03
    fam_mutterschutz__was-ist-mutterschutz__59f28ae5