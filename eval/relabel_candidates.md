# Relabel candidates — out_of_corpus cases the system answered

For each: the question, what the system DID (judged), the source it used, and its answer.
Confirm individually which should be relabelled (answer / answer_partial). Not changed yet.


---

## L03  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** How can I find a suitable gynaecologist, or Frauenärztin/Frauenarzt, in Germany?

**Top sources retrieved:** ['gesund_geburtsvorbereitung_en', 'tk_find_midwife']
**Cited:** ['gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286', 'tk_find_midwife__quick-access__c48e2aea']
**Judge reason:** The answer explicitly acknowledges that the sources do not cover how to find a gynaecologist and states the gap (directing the user to their health insurance provider instead), while providing complete information on the related but different topic of finding a midwife.

**Answer:**

I don't have information on how to find a gynaecologist. My sources cover finding a **midwife (Hebamme)** and preparing for birth, not doctor searches. For finding a **Frauenärztin/Frauenarzt**, your health insurance provider (Krankenkasse) is the place to ask — I have no document confirming what search tools exist, so please check with them directly.

What I can tell you, in case it's useful:

Gynaecologists (Frauenärztinnen/Frauenärzte) are listed as one place you can ask for a list of midwives near you. [1]

And on midwives, since that search often runs alongside finding a doctor:

- Every pregnant woman is entitled to the assistance of a midwife, covered by statutory health insurance. Midwives can handle antenatal care before the birth, support you with health issues, and assist with the birth in a hospital, birthing centre, or at home. [1]
- You can search at www.ammely.de, a platform developed with the Deutscher Hebammenverband e.V. [2] Other listed sources include your regional midwifery association (www.hebammenverband.de), the GKV-Spitzenverband (www.gkv-spitzenverband.de), your health insurance provider, the public health authority, and family education centres. [1]
- Start looking early — ideally at the end of the first trimester or the start of the second. Midwives are often fully booked. [2][1]

These sources are in English on German federal and insurer sites; the German terms are kept in German so you can use them on forms and when calling.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286
[2] Techniker Krankenkasse — verified 2026-08-03
    tk_find_midwife__quick-access__c48e2aea

---

## L04  (labelled out_of_corpus → system did: **answer**)

**Q:** When should I contact a gynaecologist after receiving a positive pregnancy test?

**Top sources retrieved:** ['tk_maternity_benefits', 'gesund_geburtsvorbereitung_en', 'gesund_vorsorge_en']
**Cited:** ['tk_maternity_benefits__pregnancy-benefits__52dff011', 'gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286']
**Judge reason:** The response provides a grounded, complete factual answer from German sources (Techniker Krankenkasse and Bundesministerium für Gesundheit) covering when to contact a gynaecologist, what the first appointment involves, the Mutterpass, routine scheduling, and midwife selection, with proper citations and appropriate medical disclaimers.

**Answer:**

**As soon as possible after the pregnancy is confirmed**, according to Techniker Krankenkasse. [1]

What that first appointment involves, per TK: the doctor asks about your medical history, carries out a physical and pelvic examination, takes your blood pressure and weight, and has your blood values, blood group and Rhesus factor determined in a laboratory. You will be informed about the risks of HIV and offered an HIV test, and given advice on the flu jab, oral hygiene and healthy eating during pregnancy. [1]

At these visits your findings are recorded in the **Mutterpass** (personal maternity notes). TK advises keeping it with you at all times, so a doctor who doesn't know you can respond appropriately in unforeseen circumstances. [1]

After that, routine antenatal check-ups are scheduled every four weeks in a normal pregnancy, and every fortnight during the last two months before childbirth. [1]

One more thing worth doing early: looking for a midwife — **Hebamme**. The Bundesministerium für Gesundheit notes that midwives are often fully booked because they care for women over long periods, so it recommends starting the search early in pregnancy. Every pregnant woman is entitled to midwife assistance, covered by statutory health insurance. You can search via www.ammely.de or your regional midwifery association at www.hebammenverband.de. [2]

If you have symptoms or health concerns right now, please speak to a doctor or midwife directly — or call 112 in an emergency. I can't advise on those.

Sources
[1] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__pregnancy-benefits__52dff011
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286

---

## L05  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** What can I do if gynaecologists in my area are not accepting new patients?

**Top sources retrieved:** ['gesund_vorsorge_en', 'tk_maternity_benefits', 'gesund_geburtsvorbereitung_en']
**Cited:** ['gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984', 'tk_maternity_benefits__postnatal-care__c0ec5b29']
**Judge reason:** The answer explicitly acknowledges the gap (no document covers finding a practice when full), then helpfully pivots to what the sources do cover (midwife alternatives and how to find one), making clear what is and is not available in the corpus.

**Answer:**

**I don't have a document that covers what to do when practices are full.** That's a real gap — the sources here describe what prenatal care includes and who may provide it, not how to find a place when nobody is taking new patients. Your health insurer (Krankenkasse) and the regional association of statutory health insurance physicians (Kassenärztliche Vereinigung) are the bodies that handle finding a practice.

What the documents *do* say that may help:

**A midwife (Hebamme) can carry out many check-ups.** Midwives can perform many check-ups during pregnancy if directed to do so by the doctor, or if the doctor has determined that the pregnancy is normal and there are no concerns. [1] This does not cover medical ultrasound scans and certain other special tests, such as urine testing for bacteria. [1] In a high-risk pregnancy, all check-ups have to be performed by a gynaecologist. [1]

**There is an official midwife search.** The National Association of Statutory Health Insurance Funds (GKV-Spitzenverband) provides a midwife search listing all midwives whose services are covered by statutory health insurance. [1] The German term to search for is **Hebammensuche**.

Getting to know a midwife early is also useful because she may later take over postpartum care (**Wochenbettbetreuung**) — you are entitled to midwifery-led postnatal care during the first twelve weeks after childbirth. [1][2]

One thing to note: because a doctor still has to direct the midwife-led check-ups or confirm the pregnancy is normal, a midwife does not fully replace a gynaecologist under these rules. [1] Your Krankenkasse is the right place to ask about getting an appointment.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984
[2] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__postnatal-care__c0ec5b29

---

## L06  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** What happens during the first pregnancy appointment, and which documents should I bring?

**Top sources retrieved:** ['tk_maternity_benefits', 'gesund_geburtsvorbereitung_en', 'gesund_vorsorge_en']
**Cited:** ['tk_maternity_benefits__on-call-midwifery-service__adac2a20', 'tk_maternity_benefits__pregnancy-benefits__52dff011', 'gesund_vorsorge_en__healthy-living-prenatal-care-check-ups-and-counseling__3b768553']
**Judge reason:** The answer comprehensively describes what happens at the first pregnancy appointment but explicitly acknowledges that the sources do not cover what documents to bring to that first appointment, naming this gap and suggesting the user contact their practice or insurer for that information.

**Answer:**

**At the first appointment**, TK describes a thorough examination: the doctor asks about your medical history, carries out a physical and pelvic examination, takes your blood pressure, measures your weight, and has your blood values, blood group, and Rhesus factor determined in a laboratory. [1] You are informed about the risks of HIV and offered an HIV test, and given advice on the flu jab, oral hygiene, and healthy eating during pregnancy. [1]

You should see a doctor for this examination as soon as possible after your pregnancy has been confirmed. [1]

**What you receive: the Mutterpass**

All medical findings and screening results are recorded in your personal maternity notes — the **Mutterpass**. [1] You should keep it with you at all times, so that a doctor who does not know you can respond appropriately in unforeseen circumstances. [1]

**After that**

Routine check-ups are scheduled every four weeks during a normal pregnancy, and every two weeks during the last two months before childbirth. [1] Most check-ups can be performed by doctors as well as midwives (**Hebammen**). [2] Three routine ultrasound scans are scheduled in an uncomplicated pregnancy, performed by a gynaecologist. [1][2] Costs are covered by statutory health insurance funds and, in most cases, also by private health insurance providers. [2]

**On documents — an important gap**

My sources do not say what to bring to the *first* appointment. That would be a question for the practice you are booking with, or your health insurer.

What the sources do cover is what to bring **to the hospital for the birth**: your Mutterpass, personal identification (identity card, passport or similar), and your marriage certificate if you are married. [3]

Note also for later: many hospitals register the birth with the local registry office (**Standesamt**) automatically; others leave that to the parents, in which case you receive the documents from the hospital and go yourself. [3]

Sources
[1] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__pregnancy-benefits__52dff011
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__healthy-living-prenatal-care-check-ups-and-counseling__3b768553
[3] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__on-call-midwifery-service__adac2a20

The Bundesministerium für Gesundheit source notes that this information cannot replace a medical consultation and must not be used for self-diagnosis or treatment. [2]

---

## L10  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** Which examinations are considered optional self-pay services, or IGeL-Leistungen?

**Top sources retrieved:** ['gesund_vorsorge_en', 'tk_maternity_pay_apply']
**Cited:** ['gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 'gesund_vorsorge_en__healthy-living-prenatal-care-check-ups-and-counseling__3b768553', 'gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f', 'gesund_vorsorge_en__where-are-all-the-important-rules-and-regulations-to-be-foun__e5e1b986']
**Judge reason:** The answer provides grounded examples of IGeL services (toxoplasmosis test, certain prenatal diagnostics) and important conditions for their coverage, but explicitly acknowledges that the sources do not provide an exhaustive list of all IGeL services and directs the user to the Mutterschafts-Richtlinien for completeness.

**Answer:**

**Short answer:** The sources name special tests such as the toxoplasmosis test (**Toxoplasmose-Test**) and certain prenatal diagnostic tests — for example those that can detect chromosomal abnormalities such as trisomy 21 — as not being part of the standard prenatal services defined by law. [1] Where they are not covered, they count as individual health services — **IGeL** (*individuelle Gesundheitsleistungen*) — and must be paid for by the patient. [1]

**Important condition on that:** health insurance providers *will* cover the costs of these tests if there is a well-founded suspicion of a disease, in the case of a high-risk pregnancy, or if abnormalities need to be clarified. [1] So the same test can be a covered benefit or a self-pay service depending on the medical situation — that is a decision for your doctor and your insurer, not something I can determine.

**Two further points:**

- IGeL services may only be performed with the expectant mother's consent, after she has been informed of the potential benefits and risks. [1]
- Additional ultrasound scans that are not medically necessary (sometimes called "baby TV") have been **prohibited** since the start of 2021 — so these are not available as a self-pay service at all. [1] Additional ultrasounds *are* possible where there are risks or abnormalities, and high-risk pregnancies usually require them. [2]

**Where the complete list lives:** the documents I have do not give an exhaustive list of IGeL services in pregnancy. All benefits covered by statutory health insurance during pregnancy and shortly after birth are set out in the maternity regulations — **Mutterschafts-Richtlinien** — issued by the Joint Federal Committee (**Gemeinsamer Bundesausschuss**, G-BA), which you can read and download on the G-BA website. [3] Anything not listed there is, in principle, where the self-pay question arises.

If you are privately insured, this may work differently — the sources only state that private providers cover prenatal care costs "in most cases" [4], and I don't have detail beyond that. Your private insurer would be the one to ask.

A note on language: these pages come from the Bundesministerium für Gesundheit in English, but the underlying Mutterschafts-Richtlinien on the G-BA site are in German.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__where-are-all-the-important-rules-and-regulations-to-be-foun__e5e1b986
[4] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__healthy-living-prenatal-care-check-ups-and-counseling__3b768553

---

## L11  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** What should I ask when my gynaecologist recommends an additional test that is not covered by insurance?

**Top sources retrieved:** ['gesund_vorsorge_en', 'tk_maternity_benefits']
**Cited:** ['gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 'gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984']
**Judge reason:** The answer covers what the sources say about IGeL tests, insurance coverage rules, and what to ask the doctor, but explicitly declines to advise whether the test is medically necessary (referring that to the gynaecologist) and cannot confirm whether the user's specific situation qualifies for insurance coverage.

**Answer:**

The documents don't give a checklist of questions, but they do describe the rules around these tests — and those point to what's worth clarifying.

**What the sources say**

Tests like the toxoplasmosis test and certain prenatal diagnostic tests (for example, to detect chromosomal abnormalities such as trisomy 21) are not part of standard prenatal services as defined by law. [1] They are classified as individual health services — **individuelle Gesundheitsleistungen**, usually shortened to **IGeL**. [1]

Two things follow from that, both stated in the source:

- An IGeL test may only be performed if you consent and if you have been informed of the potential benefits and risks. [1] So you can ask your doctor to explain both before you decide.
- IGeL tests are paid for by the patient. [1]

**But insurance may still cover it.** Health insurance providers do cover the costs if there is a well-founded suspicion of a disease, in the case of high-risk pregnancies, or if abnormalities need to be clarified. [1] So a reasonable thing to ask your doctor is whether one of those applies in your case — and to confirm with your own insurer, since they decide what they pay for. I can't tell you whether your situation falls into one of these categories.

One more thing from the same source: additional ultrasound scans that are not medically necessary have been prohibited since the start of 2021. [1]

**What I can't help with:** whether the test is medically advisable for you. That's a question for your gynaecologist or your midwife (**Hebamme**). Note that in high-risk pregnancies all check-ups have to be performed by a gynaecologist, not a midwife. [2]

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984

---

## L13  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** Can I take time to decide about an additional prenatal test, or must I agree during the appointment?

**Top sources retrieved:** ['gesund_vorsorge_en', 'tk_maternity_benefits']
**Cited:** ['gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 'gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984']
**Judge reason:** The answer confirms that consent is required and that no appointment-deadline exists in the sources, but explicitly identifies missing information: no rule on timing/cooling-off periods and no medical time-window guidance (which the assistant correctly refers to the doctor/midwife)

**Answer:**

The documents don't set a deadline for deciding — but they do say the test can't happen without your consent.

What the source states: additional tests such as toxoplasmosis testing or certain prenatal diagnostics are not part of standard prenatal care covered by law. If there's no well-founded suspicion of a disease, no high-risk pregnancy, and no abnormality to clarify, they count as individual health services — **individuelle Gesundheitsleistungen (IGeL)**. These "can only be performed if the expectant mother grants her consent and has been informed of the potential benefits and risks," and they must be paid for by the patient. [1]

So the test requires your informed consent. Nothing in these documents says that consent has to be given during the appointment itself, and nothing says how long you may take.

What I don't have:
- Any rule on timing or a cooling-off period for agreeing to an IGeL. That would come from your health insurance fund (Krankenkasse) or the practice's own patient information.
- Whether a specific test has a medical time window in the pregnancy. That's a question for your doctor or midwife (**Hebamme**) — they can also tell you whether the cost would be covered in your case. [2]

One note: these documents are the English-language pages of the Bundesministerium für Gesundheit, so no translation was needed here.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984

---

## L15  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** Under what circumstances will health insurance cover additional prenatal tests?

**Top sources retrieved:** ['gesund_vorsorge_en']
**Cited:** ['gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 'gesund_vorsorge_en__what-do-prenatal-check-ups-involve__b2799a30']
**Judge reason:** The answer covers statutory health insurance comprehensively and cites federal sources, but explicitly acknowledges that private insurers may differ and that it lacks documentation for private coverage—a deliberate and appropriate disclosure of gaps in the corpus.

**Answer:**

Health insurance providers will cover the cost of special tests — such as the toxoplasmosis test or certain prenatal diagnostic tests (for example, to detect chromosomal abnormalities like trisomy 21) — in three situations: [1]

- if there is a well-founded suspicion of a disease
- in the case of high-risk pregnancies
- if abnormalities need to be clarified

These tests are **not** part of the standard prenatal services defined by law. [1]

Otherwise, they count as individual health services — **IGeL** (*individuelle Gesundheitsleistungen*) — which patients have to pay for themselves. They can only be carried out with the expectant mother's consent, after she has been informed of the potential benefits and risks. [1]

For comparison, the standard prenatal care covered by statutory health insurance includes counselling, blood pressure monitoring and blood tests, monitoring of high-risk pregnancies, ultrasound diagnostics, infection screening (HIV, hepatitis B, syphilis, chlamydia), and determining the rhesus factor. [2]

Whether a specific test in your case will be covered is decided by your health insurer — that is not something I can determine. Your insurer (**Krankenkasse**) or the doctor ordering the test can confirm before it is carried out.

One note: this comes from the Federal Ministry of Health's English-language pages, which describe statutory health insurance. Private insurers may handle this differently, and I don't have documents covering private cover for additional tests.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__b2799a30

---

## L16  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** Which services may be covered differently by statutory insurance and private insurance?

**Top sources retrieved:** ['gesund_vorsorge_en', 'tk_maternity_benefits']
**Cited:** ['gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 'tk_maternity_benefits__postnatal-care__c0ec5b29', 'gesund_vorsorge_en__healthy-living-prenatal-care-check-ups-and-counseling__3b768553']
**Judge reason:** The answer identifies prenatal care as a service with documented differences between statutory and private insurance (with the caveat 'in most cases'), but explicitly acknowledges that the sources do not provide a detailed comparison and do not specify which cases fall outside private coverage, limiting the completeness of the response.

**Answer:**

The documents only touch on this in one place, and they don't give a detailed comparison.

**Prenatal care check-ups (Vorsorgeuntersuchungen)** — the costs are covered by statutory health insurance funds (gesetzliche Krankenkassen) and, "in most cases," also by private health insurance providers. [1] That "in most cases" is the only difference the sources name between statutory and private coverage — they don't say which cases fall outside it.

Two related points from the sources, though these are about what statutory insurance covers rather than a statutory/private contrast:

- **Lactation consultant (Stillberatung)** — Techniker Krankenkasse states it cannot cover these costs, because this is not a statutory health insurance benefit. [2]
- **Additional tests (IGeL — individuelle Gesundheitsleistungen)**, such as the toxoplasmosis test or certain prenatal diagnostics, are not part of standard statutory prenatal services. Insurers do cover them where there is a well-founded suspicion of disease, in high-risk pregnancies, or where abnormalities need clarifying. Otherwise the patient pays. [3]

**What I don't have:** the documents contain no information on what private health insurers (private Krankenversicherung) cover for pregnancy beyond that one phrase. Private policies vary by contract — your insurer is the only place that can tell you what your tariff covers. If you are statutorily insured, your Krankenkasse can confirm what is included.

Note: the Bundesministerium für Gesundheit pages here are the English-language versions.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__healthy-living-prenatal-care-check-ups-and-counseling__3b768553
[2] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__postnatal-care__c0ec5b29
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38

---

## L17  (labelled out_of_corpus → system did: **answer**)

**Q:** When should I start searching for a midwife, or Hebamme?

**Top sources retrieved:** ['tk_find_midwife', 'gesund_geburtsvorbereitung_en']
**Cited:** ['tk_find_midwife__quick-access__c48e2aea', 'gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286']
**Judge reason:** The response provides a complete, grounded factual answer from German sources (federal health ministry and statutory insurer) covering when to start searching, why, types of midwives, where to look, entitlements, and optional extras—no gaps left unnamed or medical aspects involved.

**Answer:**

Start early — ideally at the end of the first trimester or the beginning of the second. [1]

**Why so early:** Midwives are often fully booked, because they care for each family over a long period. You may need to contact several before one has capacity. [2]

**If you want your own midwife with you during a hospital birth**, you need a **Beleghebamme** (attending midwife). These are in especially high demand, so the advice is to start looking even sooner. [1] If you give birth in hospital without one, the hospital's own midwives will assist you during the delivery. [1][2]

**Where to look:**
- **www.ammely.de** — a search and booking platform developed with the Deutscher Hebammenverband e.V. [German Midwifery Association] [1][2]
- **www.hebammenverband.de** — midwife lists from your regional midwifery association [2]
- **www.gkv-spitzenverband.de** — list from the National Association of Statutory Health Insurance Funds [2]
- Also: your health insurer, gynaecologists, hospitals and birthing centres, the public health authority (Gesundheitsamt), and family education centres [2]

One thing worth knowing: every pregnant woman is entitled to midwife support, covered by statutory health insurance. This covers care during pregnancy, the birth, and afterwards — midwives support families for up to 9 months after the birth, by phone or through home visits. [2]

Note: some insurers offer extra services on top of this. Techniker Krankenkasse, for example, runs a free midwife consultation service for its own insurees, reachable by chat or phone daily from 7 a.m. to 10 p.m. [1] If you're insured elsewhere, ask your own Krankenkasse what they offer.

Sources
[1] Techniker Krankenkasse — verified 2026-08-03
    tk_find_midwife__quick-access__c48e2aea
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286

---

## L18  (labelled out_of_corpus → system did: **answer**)

**Q:** Where can I find midwives who provide prenatal care and postpartum home visits?

**Top sources retrieved:** ['gesund_geburtsvorbereitung_en', 'gesund_vorsorge_en']
**Cited:** ['gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286', 'gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984', 'gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f']
**Judge reason:** The response provides a complete, grounded answer from official German health ministry sources covering where to find midwives, what prenatal and postpartum services are covered by statutory health insurance, and explicitly notes the limitation that private insurance may differ.

**Answer:**

Midwives — **Hebammen** — can be found through several official directories. Start early: midwives are often fully booked because they care for each family over a long period, and you may need to contact several. [1]

**Where to look**

- Your regional midwifery association (**Hebammenverband**): www.hebammenverband.de [1]
- The search engine run with the German Midwifery Association: www.ammely.de [1]
- The National Association of Statutory Health Insurance Funds (**GKV-Spitzenverband**): www.gkv-spitzenverband.de — this lists all midwives whose services are covered by statutory health insurance [1][2]
- Midwifery and ob-gyn practices, gynecologists, hospitals and birthing centres [1]
- Your health insurance provider, the public health authority (**Gesundheitsamt**), family education centres, and city or regional midwife lists [1]

If you give birth in a hospital, the hospital provides a midwife for the birth itself. [1]

**What midwives cover**

Every pregnant woman is entitled to midwife assistance, covered by statutory health insurance. [1] A midwife can carry out many prenatal check-ups if the doctor directs this or has established that the pregnancy is normal — though not ultrasound scans or certain special tests, and in high-risk pregnancies all check-ups must be done by a gynecologist. [2]

**After the birth**

Postpartum midwife care begins immediately after the birth or after discharge from hospital, and the costs are covered by health insurance. [3] New mothers are entitled to consult a midwife at least once a day for up to 10 days after the birth, and the midwife will visit at home up to 16 times in the first 12 weeks. [3] If there are problems — with breastfeeding, for example — additional visits are also covered. [3] Support by phone or home visit is available for up to 9 months after the birth. [1]

A note on entitlement: these sources describe cover under statutory health insurance (**gesetzliche Krankenversicherung**). If you are privately insured or insured another way, your own insurer is the one to confirm what applies to you.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f

---

## L19  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** What should I write or say when contacting a midwife for the first time?

**Top sources retrieved:** ['gesund_geburtsvorbereitung_en', 'gesund_vorsorge_en', 'tk_find_midwife']
**Cited:** ['gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286', 'tk_find_midwife__quick-access__c48e2aea']
**Judge reason:** The answer explicitly acknowledges that no source covers the specific question (what to write or say in first contact), then provides relevant context from sources about timing, expectations, and where to find midwives to help frame that contact—a deliberate and transparent statement of the gap.

**Answer:**

I don't have a source that covers what to write or say in a first message to a midwife — no template, no checklist of what to mention. That would be something the German Midwifery Association (Deutscher Hebammenverband, www.hebammenverband.de) or your health insurer's midwife service could help with. [2]

Here's what the documents do say, which may help you frame that first contact:

**Start early.** Midwives are often fully booked, because they care for each family over a long period. It's recommended to begin looking early in the pregnancy [2] — the Techniker Krankenkasse suggests the end of the first trimester or beginning of the second. [1] If you want your own midwife present at a hospital birth, you need a **Beleghebamme** (attending midwife), and these are in especially high demand, so the advice is to start even earlier. [1]

**Expect to contact several.** You may well need to approach more than one midwife before finding one with capacity. [2]

**What a midwife covers.** Antenatal care before the birth, support with health issues, assistance at the birth (hospital, birthing centre, or home), birthing classes, and postnatal support for up to 9 months. [2] Knowing which parts you're looking for may be useful to state up front.

**Where to look:** the regional midwifery association list (www.hebammenverband.de), the search service www.ammely.de, the GKV-Spitzenverband list (www.gkv-spitzenverband.de), midwifery and ob-gyn practices, your health insurer, the public health authority (Gesundheitsamt), family education centres, hospitals and birthing centres. [2]

If you are insured with Techniker Krankenkasse, they offer a free midwife consultation service via a partner, reachable by chat or phone daily 7 a.m.–10 p.m. [1] If you're with a different insurer or privately insured, I don't have information on what they offer — ask your insurer directly.

One note: every pregnant woman is entitled to midwife support, covered by statutory health insurance. [2]

Sources
[1] Techniker Krankenkasse — verified 2026-08-03
    tk_find_midwife__quick-access__c48e2aea
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286

---

## L21  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** Which midwife services are covered by health insurance, and are there any additional charges?

**Top sources retrieved:** ['gesund_vorsorge_en', 'tk_maternity_benefits', 'gesund_geburtsvorbereitung_en']
**Cited:** ['gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f', 'gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984', 'tk_maternity_benefits__postnatal-care__c0ec5b29', 'gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286']
**Judge reason:** The answer covers what statutory health insurance includes and excludes for midwife services but explicitly acknowledges gaps: it does not address private insurance coverage or provide a comprehensive list of possible extra charges beyond what is documented.

**Answer:**

Statutory health insurance covers midwife (**Hebamme**) care through pregnancy, birth and the first months after — one service named in the documents is *not* covered: lactation consultants.

**What's covered**

- Every pregnant woman is entitled to the assistance of a midwife, covered by statutory health insurance. Midwives can provide antenatal care, support with health issues, and assist with the birth in a hospital, birthing centre or at home. [1]
- Midwives may carry out many prenatal check-ups if the doctor directs this or has determined the pregnancy is normal. This does **not** include ultrasound scans and certain special tests (such as urine testing for bacteria). In high-risk pregnancies, all check-ups must be done by a gynaecologist. [3]
- Postnatal care at home: you are entitled to midwife-led postnatal care during the first twelve weeks after birth. Your doctor can prescribe additional postnatal care if necessary. [2]
- In detail: at least one midwife consultation per day for up to 10 days after the birth, and up to 16 home visits in the first 12 weeks. Costs are covered by health insurance. If there are problems — for example with breastfeeding — the costs of additional midwife visits are also covered. [4]

**What is not covered**

- Support from a lactation consultant (breastfeeding consultant) is not a statutory health insurance benefit, so Techniker Krankenkasse states it cannot bear these costs. [2]

**Finding a midwife whose services are covered**

The GKV-Spitzenverband (National Association of Statutory Health Insurance Funds) midwife search lists all midwives whose services are covered by statutory health insurance. [3] Other listings: www.hebammenverband.de and www.ammely.de. [1] Midwives are often fully booked, so it helps to start looking early in the pregnancy. [1]

**Two gaps worth knowing about**

These documents describe **statutory** health insurance (gesetzliche Krankenversicherung). I don't have information on how midwife services are covered under private insurance — your insurer would be the one to confirm that.

I also don't have a document listing every possible extra charge (for example, a midwife's on-call fee for a home birth, or fees for birthing classes beyond what's covered). Your own Krankenkasse can tell you exactly what they reimburse and what you would pay yourself.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286
[2] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__postnatal-care__c0ec5b29
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984
[4] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f

---

## L22  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** What can I do if I cannot find an available midwife in my area?

**Top sources retrieved:** ['gesund_geburtsvorbereitung_en', 'gesund_vorsorge_en', 'tk_find_midwife']
**Cited:** ['gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286', 'gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984', 'tk_find_midwife__quick-access__c48e2aea']
**Judge reason:** The answer provides substantial grounded guidance on how to search for a midwife (multiple directories, resources, and timelines) and clarifies that hospital births have midwife coverage, but explicitly acknowledges the gap: what happens if the search fails entirely (fallback services, waiting lists, insurer obligations)—and invites the user to provide their insurance type for more specific information.

**Answer:**

I don't have a document that addresses directly what to do when no midwife is available. Here's what the sources do say about searching, plus where the gap is.

**Contact several midwives, and start early**

The Federal Ministry of Health notes that you may well need to contact several midwives, because they are often fully booked due to the long periods for which they provide care — which is why it's advised to begin looking early in the pregnancy. [1] Techniker Krankenkasse suggests starting at the end of the first trimester or beginning of the second, and even earlier if you want a **Beleghebamme** (attending midwife) present at a hospital birth, as these are in especially high demand. [2]

**Lists to try beyond the obvious ones**

The Ministry lists a number of places to look, not just one directory: [1]

- your regional midwifery association — **Hebammenverband** (www.hebammenverband.de)
- www.ammely.de, a search service run with the German Midwifery Association [1][2]
- the list from the National Association of Statutory Health Insurance Funds — **GKV-Spitzenverband** (www.gkv-spitzenverband.de), which lists all midwives whose services are covered by statutory insurance [1][3]
- midwifery and obstetric practices, gynecologists, hospitals and birthing centers
- your city or regional midwife list
- your health insurance provider
- the public health authority — **Gesundheitsamt**
- family education centers — **Familienbildungsstätten**

**If you give birth in hospital**

Both sources state that the hospital provides a midwife for the birth itself. [1][2] So a hospital birth does not depend on finding your own midwife beforehand.

**One insurer-specific option**

Techniker Krankenkasse offers a free midwife consultation service for TK insurees, reachable by chat or phone daily 7 a.m.–10 p.m., with a stated response within 15 minutes. [2] This applies only to people insured with TK. If you're with a different **Krankenkasse**, it's worth asking them directly whether they run something similar — I don't have documents covering other insurers.

**What I don't have**

None of these documents cover what happens if the search fails entirely — for example, whether there's a fallback service, a waiting list, or any obligation on an insurer to arrange care. That question would go to your own **Krankenkasse** or to your regional **Hebammenverband**.

If you tell me which health insurer you're with, I can check whether I have anything specific to them.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286
[2] Techniker Krankenkasse — verified 2026-08-03
    tk_find_midwife__quick-access__c48e2aea
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__who-conducts-prenatal-check-ups__8661e984

---

## L23  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** How can organisations such as Caritas, Pro Familia or pregnancy counselling centres help with pregnancy, financial support, maternity protection and parental leave?

**Top sources retrieved:** ['gesund_geburtsvorbereitung_en', 'gesund_vorsorge_en']
**Cited:** ['gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286', 'gesund_geburtsvorbereitung_en__what-happens-at-a-birthing-class__ec0222fa']
**Judge reason:** The answer explicitly states what is not covered (counselling services, financial support, maternity protection, parental leave from those organisations) and redirects to appropriate authorities, but does provide grounded information about midwife entitlements and birthing classes from federal sources, with clear delineation of what the corpus covers and what it does not.

**Answer:**

I don't have information about what Caritas, Pro Familia or pregnancy counselling centres offer. None of the documents I can access cover counselling services, financial support, maternity protection or parental leave.

Here's where that information sits:

- **Pregnancy counselling centres** (Schwangerschaftsberatungsstellen) — Caritas, Diakonie, Pro Familia, Donum Vitae and the local health authority all run them. Contact one directly to ask what they cover.
- **Maternity protection (Mutterschutz) and parental leave (Elternzeit)** — Familienportal des Bundes, run by the Bundesministerium für Familie, Senioren, Frauen und Jugend. For your own situation, your employer and the supervisory authority for Mutterschutz in your Bundesland.
- **Elterngeld and other family benefits** — the Elterngeldstelle in your area.
- **Mutterschaftsgeld** — your health insurer.

What I *can* tell you from my sources is about midwife and birth preparation support:

Every pregnant woman is entitled to the assistance of a midwife (**Hebamme**), covered by statutory health insurance. [1] A midwife can provide antenatal care, support with health issues, and assist with the birth in a hospital, a birthing centre or at home. After the birth, midwives support young families for up to 9 months, by phone or through home visits. [1]

To find one, you can use the midwife lists from your regional midwifery association (hebammenverband.de), the search engine ammely.de, or the list from the National Association of Statutory Health Insurance Funds (GKV-Spitzenverband). [1] Gynaecologists, hospitals, birthing centres, family education centres and the public health authority can also help you find one. [1] Start early — midwives are often fully booked. [1]

Birthing classes (**Geburtsvorbereitungskurse**) cover the birth process, the postnatal recovery period, breastfeeding, infant care, and the changes parenthood may bring. [2] Many midwives offer them. [1]

If you tell me whether you're employed, self-employed, in training or a student, and whether you have statutory or private insurance, I can look for more specific information — though based on what I currently have, I'd likely need to point you to the offices above.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__what-happens-at-a-birthing-class__ec0222fa

---

## L32  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** When and how should I register for delivery at the chosen hospital?

**Top sources retrieved:** ['tk_maternity_benefits', 'gesund_geburtsvorbereitung_en']
**Cited:** ['tk_maternity_benefits__on-call-midwifery-service__adac2a20', 'gesund_geburtsvorbereitung_en__where-will-i-have-the-baby__270a9a89', 'gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286']
**Judge reason:** The answer provides grounded guidance on registering early and what to bring, but explicitly acknowledges that the sources do not describe the specific registration procedure (phone, online, or in-person) or exact timing in weeks, directing the user to contact the hospital directly for those details.

**Answer:**

**Register as early as possible.** Techniker Krankenkasse states that you choose the contract hospital where you want to have your baby and should register there as early as you can. [1]

A few related points from the sources:

- The hospital settles the costs of delivery and follow-up care directly with TK via your TK eHealth card, and you make no co-payments during that time. [1]
- If you choose a hospital further away, contact TK about possible additional costs. [1]
- If you're having your baby in hospital, the hospital will provide a midwife — **Hebamme** — for the birth. [2]
- If you're planning a home birth, the Bundesministerium für Gesundheit advises registering with a nearby hospital anyway, so your medical details are on file in case of an emergency or a change of plan. [3]

**What to bring when you go in to give birth:** your **Mutterpass** (personal maternity notes), photo ID (identity card or passport), and your marriage certificate if you are married. [1]

**What I don't have:** the documents don't describe the registration procedure itself — whether it's done by phone, online, or at an in-person appointment (often called an **Anmeldung zur Geburt**), or exactly how many weeks beforehand. That varies by hospital. Contact the hospital's maternity ward (**Kreißsaal** or **Geburtshilfe**) directly, or ask your gynaecologist or midwife.

One note on sources: the TK document is written for people insured with Techniker Krankenkasse. If you're with a different insurer or privately insured, the cost and eHealth card details may differ — check with your own insurer.

Sources
[1] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__on-call-midwifery-service__adac2a20
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__how-do-i-find-a-midwife__8fc45286
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__where-will-i-have-the-baby__270a9a89

---

## L33  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** What questions should I ask during a hospital information evening or registration appointment?

**Top sources retrieved:** ['gesund_geburtsvorbereitung_en', 'tk_maternity_benefits']
**Cited:** ['gesund_geburtsvorbereitung_en__healthy-living-preparing-for-birth__955b8a97', 'tk_maternity_benefits__on-call-midwifery-service__adac2a20', 'gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f']
**Judge reason:** The answer acknowledges that a definitive checklist of questions is not in the corpus and directs the user to the appropriate authoritative source (familienplanung.de), but then provides grounded, source-specific guidance on practical topics worth raising at the appointment (registration timing, documents, birth registration, costs, hospital bag, and birth setting options).

**Answer:**

I don't have a source that lists questions to ask at a hospital information evening (Informationsabend) or registration appointment. That kind of checklist isn't in the documents I can see — the Bundeszentrale für gesundheitliche Aufklärung (familienplanung.de) is named as the place that publishes detailed checklists for birth preparation, so that would be a good place to look. [1]

Here is what the documents do say about that appointment, which may help you shape your own questions:

**Register early.** You choose the contract hospital where you want to give birth, and you should register there as early as possible. [2]

**Bring these documents to the birth:** your Mutterpass (personal maternity notes), personal identification (identity card or passport), and your marriage certificate if you are married. [2] A fuller list — including health insurance card, and for single mothers a birth certificate — is given for the hospital bag. [3]

**One thing worth confirming with the hospital: birth registration.** Many hospitals automatically register the birth with the local registry office (Standesamt). Others leave that to the parents. If yours does, the hospital gives you the papers and you go to the registry office yourself for a free birth certificate. [2]

**Costs.** Delivery and follow-up care are settled directly with the insurer via the eHealth card, with no co-payment. If you choose a hospital further away, contact your insurer about additional costs. [2] (This describes Techniker Krankenkasse; if you're with another insurer, ask them.)

**Go through your hospital bag list with them.** The Bundesministerium für Gesundheit suggests discussing that list with the hospital or your midwife (Hebamme) in advance. [1]

You can also ask about where the birth takes place — hospital inpatient or outpatient, a birthing centre (Geburtshaus), or at home are all named as options. [4]

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f
[2] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__on-call-midwifery-service__adac2a20
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f
[4] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__healthy-living-preparing-for-birth__955b8a97

---

## L34  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** Do I need a backup hospital, and what happens if my chosen hospital has no available delivery room when labour begins?

**Top sources retrieved:** ['gesund_geburtsvorbereitung_en', 'tk_maternity_benefits']
**Cited:** ['gesund_geburtsvorbereitung_en__where-will-i-have-the-baby__270a9a89', 'tk_maternity_benefits__on-call-midwifery-service__adac2a20', 'gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f']
**Judge reason:** The answer covers what the sources say about backup hospitals for home births and advises on hospital registration, but explicitly names the gap: the sources do not cover what happens if a chosen hospital has no available delivery room when labour begins.

**Answer:**

**Short answer: the documents only describe a backup hospital for home births — and they don't cover what happens if a hospital has no free delivery room.**

**On a backup hospital**

If you plan a home birth, the Bundesministerium für Gesundheit says that for safety you should also register with a nearby hospital. That hospital then has your medical details on file in case an emergency arises, or if you change your mind at the last minute and decide on a hospital birth. [1]

A home birth is only an option if no risks or complications are foreseen — the doctor and midwife caring for you assess this carefully. [1]

If you're planning to give birth in a birthing centre, the sources advise considering travel distance, because labour can progress so quickly that long journeys can't be undertaken. [1]

For a hospital birth, Techniker Krankenkasse advises registering at your chosen contract hospital as early as possible. [2] The documents don't say that a second, backup hospital is needed in that case.

Also useful: even if you plan a home birth or an outpatient hospital delivery, you should have a bag packed and ready in preparation for an emergency. [3] Bring your **Mutterpass** (maternity record) and personal identification with you. [2][3]

**What I don't have**

Nothing in these documents covers what happens if your chosen hospital is full or has no delivery room free when labour starts — no rule on transfer, no procedure, no cost consequences. That question would be answered by the hospital itself (ask when you register), your midwife (**Hebamme**), or your health insurer.

One related point the sources do cover: TK says to contact them about additional costs if you choose to deliver at a hospital further away. [2] So if a change of hospital could affect costs, your insurer is the one to ask.

If labour has started and you are unsure where to go, call your midwife or the hospital directly — or 112 in an emergency.

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__where-will-i-have-the-baby__270a9a89
[2] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__on-call-midwifery-service__adac2a20
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f

---

## L38  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** Is an ambulance covered by health insurance, and in which situations should emergency number 112 be used?

**Top sources retrieved:** ['gesund_geburtsvorbereitung_en', 'gesund_vorsorge_en', 'tk_maternity_benefits']
**Cited:** ['gesund_geburtsvorbereitung_en__where-will-i-have-the-baby__270a9a89', 'gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38', 'tk_maternity_benefits__postnatal-care__c0ec5b29']
**Judge reason:** The assistant explicitly states it lacks information on ambulance coverage and emergency criteria, but does answer what related coverage is available (prenatal care, home birth costs, postnatal care) and appropriately directs the user to their insurer and medical professionals for the missing parts.

**Answer:**

I don't have information about ambulance costs or emergency criteria in the documents available to me.

**On ambulance coverage (Krankentransport / Rettungsdienst):** none of the sources I have cover emergency transport or who pays for it. Your health insurer (Krankenkasse) is the right place to ask — they decide what transport costs they cover and under what conditions.

**On when to call 112:** I can't tell you which situations count as an emergency. That's a medical judgement, and I don't make those. If you think you or your baby may be in danger, call **112** — you don't need to be sure first. For questions that feel urgent but not like an emergency, your midwife (**Hebamme**) or your doctor can advise you, including outside office hours.

What the documents I have *do* cover, in case it's useful: prenatal check-ups and postpartum counselling are paid for by statutory health insurance [1], as are the costs of a home birth [2], and you're entitled to midwifery-led postnatal care (**Wochenbettbetreuung**) for the first twelve weeks after birth [3].

Sources
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_vorsorge_en__what-do-prenatal-check-ups-involve__a056ec38
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    gesund_geburtsvorbereitung_en__where-will-i-have-the-baby__270a9a89
[3] Techniker Krankenkasse — verified 2026-08-03
    tk_maternity_benefits__postnatal-care__c0ec5b29

---

## L40  (labelled out_of_corpus → system did: **answer_partial**)

**Q:** What usually happens after birth regarding the hospital stay, care of the mother and baby, birth registration, U1 and U2 examinations, newborn screening, finding a paediatrician and arranging the first appointments?

**Top sources retrieved:** ['gesund_vorsorge_en', 'gesund_geburtsvorbereitung_en']
**Cited:** ['gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f', 'gesund_geburtsvorbereitung_en__healthy-living-preparing-for-birth__955b8a97', 'gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f']
**Judge reason:** The answer covers midwife care and maternal check-ups from the sources but explicitly names and describes what is missing: hospital stay organization, birth registration, U1/U2 examinations, newborn screening, and finding a paediatrician.

**Answer:**

I can cover part of this. The documents I have describe care for mother and baby after the birth. They do **not** cover the hospital stay itself, birth registration, the U1 and U2 examinations, newborn screening, or finding a paediatrician.

## What the documents do say

**Midwife care after the birth (Hebamme)**
Midwife assistance for postpartum care begins immediately after the birth, or after discharge from the hospital. The costs are covered by health insurance providers. [1]

- The midwife usually visits at home, examines and weighs the baby regularly, and advises on physical complaints, breastfeeding, diapering, and sleeping. [1]
- New mothers are entitled to consult a midwife **at least once a day for up to 10 days** after the birth. [1]
- In the **first 12 weeks** after the birth, the midwife will visit at home **up to 16 times**. If there are problems — for example with breastfeeding — the cost of additional visits is covered by health insurance. [1]

**Check-ups for the mother**
Two check-ups are scheduled after the birth. [1]

- Within the first week: a blood test to check the hemoglobin level and detect a possible iron deficiency. [1]
- Six to eight weeks after the birth: a general check-up and a gynecological exam. Blood pressure is measured and urine checked for protein, sugar and infections. The mother is also given advice on questions about her newborn. [1]

**General**
After the birth, both mother and baby need plenty of rest, care, and support. Much of the paperwork and the applications for the newborn can be prepared or completed in advance during pregnancy. [2]

## What I don't have

- **Length and organisation of the hospital stay** — ask the hospital (Krankenhaus) or your midwife.
- **Birth registration (Geburtsurkunde)** — this is handled by the local registry office, the **Standesamt**. Many hospitals help forward the notification.
- **U1 and U2 examinations (U-Untersuchungen)** and **newborn screening (Neugeborenen-Screening)** — not in my documents. The hospital, your midwife, or your health insurer (Krankenkasse) can tell you the timing and what is covered.
- **Finding a paediatrician (Kinderarzt / Kinderärztin) and booking first appointments** — not covered here. Your health insurer or midwife can point you to practices taking new patients.

One more thing worth knowing: it is useful to discuss preparations with the hospital or midwife in advance. [3]

These documents are the English-language pages of the Bundesministerium für Gesundheit.

**Sources**
[1] Bundesministerium für Gesundheit — verified 2026-08-03
    `gesund_vorsorge_en__which-prenatal-check-ups-are-scheduled-at-which-points-in-th__9594805f`
[2] Bundesministerium für Gesundheit — verified 2026-08-03
    `gesund_geburtsvorbereitung_en__healthy-living-preparing-for-birth__955b8a97`
[3] Bundesministerium für Gesundheit — verified 2026-08-03
    `gesund_geburtsvorbereitung_en__what-needs-to-be-packed-in-the-hospital-bag__64b4996f`