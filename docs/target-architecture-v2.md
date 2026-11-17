# TARGET ARCHITECTURE V2
## Evolutionary Architecture Strengthening — Video Explainer Promkes

**Dokumen:** Target Architecture V2  
**Baseline:** `workspace.tar(2).gz`, direktori `repo/` dan paket `remediasi/`  
**Cakupan:** M00 + S01–S14, universal handoff, executable gates, dependency graph, acceptance dan integrasi  
**Status:** Target design / patch-ready specification; belum diterapkan ke repository  
**Prinsip:** memperkuat arsitektur secara evolusioner, bukan membangun ulang

---

## 1. Mandat, keputusan, dan batas perubahan

### 1.1 Mandat

Meningkatkan ketepatan batas kepemilikan, kedalaman operasional spesialis, integritas sumber dan otorisasi, validasi serah-terima, serta pembuktian kesiapan produksi Video Explainer Promkes.

### 1.2 Keputusan arsitektur yang dipertahankan

1. Identitas, nama, ID dan mandat utama M00 serta S01–S14 tidak berubah.
2. M00 tetap satu-satunya project orchestrator dan integrator akhir.
3. S02 tetap pemilik Health Truth Registry, claim status, safe wording dan Fact Lock; otoritas klinis final berada pada manusia yang sah.
4. S03 tetap pemilik audience strategy, behavior objective, key message dan CTA.
5. S04 tetap pemilik narrative/script/VO wording; S05 visual canon; S06 storyboard/camera; S07 motion specification.
6. S08 tetap reference-prompt/reference-asset engineering, bukan video-rendering engine.
7. S09 tetap pemilik audio intelligence, transcript provenance, timing, voice/sound direction dan subtitle/audio-post specification.
8. S10 tetap pemilik editing/post-production dan renderer engineering, dengan dua jalur operasional yang tegas.
9. S11 tetap pemilik aksesibilitas/distribusi; capaian algoritmik tidak dijamin.
10. S12 tetap pemeriksa independen; pembuat artefak tidak boleh mengesahkan sendiri pemeriksaan independen.
11. S13 tetap pemilik MCG, Guide registry, canonical locks, scene continuity ledger dan change-impact integration.
12. S14 tetap pemilik context classification dan release-change trace; bukan pemilik kebenaran klinis, kreativitas, QA atau otoritas manusia.

### 1.3 Baseline yang sudah tersedia

Pemeriksaan ulang arsip menunjukkan bahwa `repo/docs/architecture.md` sudah memuat topologi, domain ownership, authority hierarchy, input modes, dependency graph dan delivery classes. `repo/skills/editing-postproduction/SKILL.md` juga sudah menyatakan dua responsibility lanes: editing/post-production serta renderer/code engineering.

Karena itu, V2 **tidak memperkenalkan ulang** pemisahan S10. V2 mengubah pemisahan tekstual tersebut menjadi kontrak yang dapat diperiksa: batas keputusan, artefak keluaran, interface, test oracle dan kondisi eskalasi.

Setiap spesialis sudah menyebut field dasar handoff (`case_id`, `skill_id`, `status`, `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, `limitations`). Namun, baseline belum menyediakan satu JSON Schema universal untuk menguji struktur, tipe dan batas field handoff tersebut. Schema V4 yang ada memvalidasi project, claim, artifact, scene, capability dan conversation context; bukan universal handoff.

### 1.4 Non-goals

- Tidak mengganti atau menghapus skill M00–S14.
- Tidak mengubah pembagian otoritas domain yang masih valid.
- Tidak menambah klaim bahwa micro-module adalah agen independen.
- Tidak menjadikan JSON Schema sebagai bukti kebenaran klinis atau keamanan runtime.
- Tidak memaksa setiap proyek menjalankan semua tahap tingkat ADVANCED.
- Tidak otomatis menggabungkan folder `remediasi/` ke source utama tanpa review, migrasi dan retest.
- Tidak menyatakan render, plugin invocation, approval atau release telah terjadi hanya karena target design tersedia.

---

## 2. Target topology

```text
                         M00 — MASTER ORCHESTRATOR
       intake / routing / capabilities / manifest / dependency graph
                 gate arbitration / delivery aggregation
                                  |
          +-----------------------+-----------------------+
          |                       |                       |
    SOURCE & TRUTH          CREATIVE DESIGN          PRODUCTION
    S01 / S02 / S03         S04 / S05 / S06 / S07    S08 / S09 / S10 / S11
          |                       |                       |
          +-----------------------+-----------------------+
                                  |
                        UNIVERSAL HANDOFF CONTRACT
                    schema validation + semantic checks
                    provenance + owner + evidence + trace
                                  |
                   S12 INDEPENDENT QA + S13 CONTINUITY
                                  |
                      S14 CONTEXT / RELEASE PREFLIGHT
                                  |
                         M00 DELIVERY ARBITRATION
                                  |
          HUMAN clinical / institutional / rights / publication authority
```

S12, S13 dan S14 bukan satu tahap serial yang menggantikan spesialis lain. Mereka mempunyai fungsi assurance, continuity dan release trace yang masuk ke alur utama serta correction loop.

### 2.1 M00 responsibilities

M00:
- menerima dan mengklasifikasikan input `POSTER_FIRST`, `AUDIO_FIRST`, `HYBRID`, `SCRIPT_FIRST`;
- menetapkan project/case ID dan variabel proyek;
- memverifikasi kapabilitas, permission dan batas environment secara nyata;
- memeriksa handoff schema dan semantic contract sebelum menerima hasil;
- memelihara project manifest dan dependency graph;
- merutekan konflik ke pemilik domain;
- mengagregasi status gate dan delivery;
- tidak menulis ulang keputusan yang menjadi otoritas spesialis;
- tidak mengubah approval manusia menjadi PASS tanpa bukti otoritas eksternal.

### 2.2 Four governance boundaries

| Boundary | Owner | M00 role |
|---|---|---|
| Health truth | S02 + authorized human clinician | Menjaga alur dan memastikan gate terpenuhi |
| Campaign/story/creative canon | S03–S07, S13 by scope | Menghubungkan dependensi dan meminta resolusi konflik |
| Audio/media/render implementation | S09–S10 | Memeriksa capability, kontrak, bukti eksekusi |
| Independent QA/context/release trace | S12/S14 | Mengintegrasikan status tanpa mengambil alih independensi |

---

## 3. S10 — two-lane ownership contract

### 3.1 Identitas tetap

**External skill ID:** `S10`  
**Skill name/path:** `editing-postproduction` / `skills/editing-postproduction/SKILL.md`  
**Internal workstream IDs:** `S10-MP` dan `S10-RE`

`S10-MP` dan `S10-RE` adalah sub-lane dalam satu skill. Keduanya bukan skill/plugin baru dan tidak boleh dipresentasikan sebagai dua agent yang otomatis berjalan paralel.

### 3.2 Lane A — S10-MP: Media Production

**Decision owner:** editorial assembly, composition, timeline dan post-production choices.

**Owns**
- editorial decision list dan approved scene order;
- pacing, scene assembly, transition intent dan hold;
- composition, layer/z-order, framing/crop, safe area dan hierarchy;
- integration atas exact text, health wording, statistic, date, institutional name, logo dan CTA sebagai editable overlay;
- penempatan VO, musik, SFX, ambience dan subtitle ke timeline berdasarkan bukti S09;
- audio assembly/mix specification, ducking/fades dan finishing hanya pada tool yang benar-benar tersedia;
- color/visual finishing intent, mastering specification dan export requirements;
- dokumentasi editorial trade-off dan missing media.

**Does not own**
- tidak memvalidasi klaim kesehatan (S02);
- tidak mengganti tujuan/CTA (S03);
- tidak mengubah screenplay/VO copy yang disetujui (S04);
- tidak mengarang visual canon (S05/S13);
- tidak mengubah kamera/shot owner decision (S06);
- tidak membuat motion mechanics tanpa spesifikasi S07;
- tidak mengubah transcript/timing provenance atau membuat source audio claim (S09);
- tidak membuat adapter kode atau menyatakan runtime lulus (S10-RE);
- tidak mengesahkan hasil secara independen (S12).

**Required input**
Approved production manifest; scene/shot contracts; motion specifications; selected reference asset manifest; source/edited VO distinction; subtitle/audio cue records; accessibility/overlay requirements; rights state; render target and permission.

**Required output: `MEDIA-PRODUCTION-HANDOFF`**
- `editorial_decision_list_ref`;
- `composition_manifest_ref`;
- `scene_assembly_map_ref`;
- `layer_overlay_registry_ref`;
- `audio_integration_map_ref`;
- `subtitle_integration_map_ref`;
- `export_requirements_ref`;
- rights/assets dependency summary;
- unresolved issues and acceptance checks.

### 3.3 Lane B — S10-RE: Renderer Engineering

**Decision owner:** renderer selection evidence, adapter mapping, code/build/runtime and render execution.

**Owns**
- renderer capability discovery and exact version evidence;
- target-specific adapter and typed input mapping;
- mapping of renderer-neutral manifest to target schema/props/components;
- source code, project assembly and path containment;
- dependencies, fonts, codecs, permissions, runtime and resource checks;
- static validation, build and integration checks;
- proof render, render orchestration, bounded retry and diagnostics;
- exact output file evidence and technical metadata verification.

**Does not own**
- tidak mengambil alih editorial intent atau composition decisions;
- tidak mengubah fact lock, narrative, visual canon, camera intent atau motion design untuk menghindari kegagalan build;
- tidak mengklaim Remotion/native renderer tersedia tanpa inspeksi sesi dan runtime;
- tidak mengubah asset/status/rights dengan asumsi;
- tidak menggantikan S12 pada inspeksi independen.

**Required input**
Approved `MEDIA-PRODUCTION-HANDOFF`; renderer-neutral manifest; schema target; asset references; capability and rights records; output target; resource budget.

**Required output: `RENDERER-ENGINEERING-REPORT`**
- capability matrix;
- renderer route: `NATIVE`, `PROGRAMMATIC`, `HANDOFF`, `NONE`;
- exact renderer/runtime/dependency versions where verified;
- adapter specification and mapping coverage;
- static/build/runtime results;
- proof render status and observations;
- render log and bounded retry history;
- actual output artifact reference only if file exists;
- container/dimensions/fps/duration/stream checks where inspected;
- limitations and residual risks.

### 3.4 Lane interface: Composition Contract

A stable `composition_contract` must carry:
- project/composition ID;
- width, height, aspect ratio, fps and timebase (each with source/status);
- total duration and rounding convention;
- ordered scenes with half-open frame ranges `[start_frame, end_frame)`;
- source segment IDs and source timing precision;
- reference asset IDs and actual asset path/status;
- layer IDs, roles, order/z-index, transforms, crop and safe area;
- transition/overlap rules;
- exact overlay IDs and content refs;
- subtitle cue refs and time precision;
- audio cue refs, source/processed asset distinction and mix requirements;
- rights/privacy/capability dependencies;
- fallback or unsupported effect declarations.

**Interface rules**
1. S10-MP authors editorial meaning and desired composition; S10-RE maps it to supported renderer primitives.
2. S10-RE returns `TECHNICAL_CHANGE_REQUEST` if the target cannot implement an instruction exactly.
3. S10-MP accepts/rejects an editorial adaptation; M00 resolves cross-domain impacts.
4. Every accepted adaptation produces a change ID and invalidates only dependent artifacts.
5. Render success is not proof of editorial correctness. S12 performs independent QA.

### 3.5 S09/S10 boundary

| Work | Owner |
|---|---|
| Audio source inspection, metadata, transcript provenance, speaker/timing confidence | S09 |
| VO direction, sound design and subtitle segmentation/specification | S09 |
| Timeline placement of audio and subtitle cues | S10-MP |
| Technical processing/build of media assets when tools exist | S09 for audio processing; S10-RE for renderer integration |
| Final A/V and subtitle sync verification | S12, based on actual media and evidence |

---

## 4. Operational depth profiles for S02, S03, S04, S05, S06, S07 and S13

### 4.1 Common operating template

Each targeted skill must express the same operational layers without forcing identical content:

1. **Mandate and owner:** owned decisions, prohibited decisions, escalation owner.
2. **Inputs and preconditions:** required input refs, inherited locks, capability and authority.
3. **Procedure:** ordered, bounded steps with domain-specific method.
4. **Decision rules:** what makes a result accepted, partial, blocked or routed.
5. **Outputs:** stable artifact types/IDs and schema refs.
6. **Negative cases:** missing, conflicting, stale, adversarial or unsupported inputs.
7. **Acceptance tests:** observable oracle and evidence.
8. **Handoff:** universal envelope plus domain-specific artifact references.

Micro-modules remain named sub-procedures owned by the parent skill, not autonomous agents.

### 4.2 S02 — Health Evidence & Safety Auditor

**Mandate:** claim extraction, evidence suitability, safe wording, ethics and Fact Lock. No personal diagnosis; no creative/renderer authority.

| Procedure | Inputs and method | Decision/output | Negative case and routing |
|---|---|---|---|
| Health Claim Extractor | S01 dossier, caption, script, transcript; split every material sentence into atomic propositions; preserve literal wording and location | `CLM-ID`, claim type, source location, population/jurisdiction/time unknowns | Compound or ambiguous claim → split or `UNKNOWN`; never infer missing words |
| Medical Evidence Verifier | Candidate source, issuer, publication/update date, period, jurisdiction, population, method, directness, limitations and counterevidence; inspect actual source/snapshot | Evidence dossier and claim status: `VERIFIED`, `PARTIALLY_SUPPORTED`, `MIXED_OR_CONTESTED`, `BELUM_DIVERIFIKASI`, `CONTRADICTED`, `UNKNOWN`, `STALE` | Source inaccessible, stale or mismatched population → not verified; material conflict → `HOLD` |
| Health Terminology Validator | Approved proposition + trusted terminology/guidance; check medical term, common-language equivalence, units and ambiguity | Terminology map, preferred and forbidden formulations | Ambiguous or materially changed term → S02 review; clinician when clinically consequential |
| Health Literacy Simplifier | Fact-locked proposition; simplify one sentence at a time and compare meaning/qualifier/uncertainty | Plain-language wording mapped to same `CLM-ID`; allowed/forbidden wording | Simplification strengthens certainty, causation, scope or promise → reject and revise |
| Medical Misinformation Detector | Claims and drafts; inspect unsupported causality, guarantee, misleading statistic, false route/mechanism, omission and stigma | Flag register with severity, evidence and owner | Detector result alone never approves claim; uncertain result routed to verifier/human |
| Health Ethics & Safety Controller | Audience/context, content and planned CTA; inspect fear, stigma, victim-blaming, privacy, coercion, medical instructions and vulnerable groups | Ethics findings, restrictions and human-review requirements | Personal diagnosis/prescription, sensitive disclosure or dangerous advice → stop/route to qualified care or authorized reviewer |
| Fact Lock Manager | Accepted dossier and human approval record; assign versioned immutable lock per proposition and allowed wording | Health Truth Registry, Fact Lock IDs, approval refs, affected output refs | No valid authority or no direct support → lock cannot become `APPROVED`; upstream changes invalidate dependents |

**S02 required output**
- atomic Claim Register;
- Source Snapshot/Source Register;
- Claim–Evidence Matrix with direct support/contra and quotation locator;
- context/jurisdiction/date/population record;
- terminology and safe-language map;
- misinformation/ethics findings;
- Fact Lock Registry with approval provenance;
- unresolved claims and required human review.

**S02 acceptance:** every material claim is atomic; source content is actually inspected; hash is computed from source bytes/snapshot; claim support is explicitly assessed; claim language does not exceed source scope; unknown/contradicted/stale claims are not emitted as approved facts; human clinical review is proven by external authority evidence, not a self-asserted boolean.

### 4.3 S03 — Audience & Campaign Strategy Architect

**Mandate:** one primary audience, one primary behavior objective, one key message and one primary CTA unless the brief justifies a documented exception.

**Procedure**
1. Separate explicit audience facts from inferred audience context.
2. Describe literacy/accessibility assumptions and mark their evidence level.
3. Define behavior chain: desired action → current barrier → enabling insight → communication intervention.
4. State one measurable behavior objective, not a vague awareness aspiration.
5. Select one key message directly supported by S02 locks.
6. Select hook/emotional framing without fear exaggeration, shame or unsupported urgency.
7. Adapt local culture/language only with supplied/authentic evidence; otherwise use neutral Indonesian.
8. Construct one primary CTA and optional secondary supporting action only when scope requires it.
9. Define evaluation indicators separately from guaranteed social reach.

**Output: `Campaign Strategy Blueprint`**
- audience profile and provenance;
- literacy/accessibility assumptions;
- behavior objective and observable behavior;
- barriers/enablers;
- message hierarchy and `MSG-ID`;
- hook rationale;
- CTA and action path;
- cultural adaptation evidence;
- success indicators and limitations.

**Decision rules**
- Audience absent → general audience assumption, visible and reversible.
- Local dialect unverified → neutral Indonesian, no invented slang.
- More than one competing behavior objective → prioritize one or request a scoped brief.
- CTA unsupported by S02 or institutional policy → route to S02/M00; do not publish it as approved.
- Reach/FYP/virality requested → classify as aspiration, not outcome guarantee.

**Acceptance:** single dominant objective and CTA; message references approved fact locks; audience profiling does not invent demographic statistics; CTA is specific/actionable; no manipulative health fear or guaranteed algorithm claim.

### 4.4 S04 — Story & Screenplay Architect

**Mandate:** turn approved campaign message into narrative and screenplay without changing facts, CTA or creative canon owned elsewhere.

**Procedure**
1. Verify input readiness: S02 Fact Locks and S03 Campaign Blueprint.
2. Select narrative form based on behavior objective, audience, emotional tone, media format and duration constraints (e.g. problem–insight–action, character journey, demonstration, myth/fact correction). Record why it fits.
3. Write concept/logline/premise and identify the single audience takeaway.
4. Build a beat sheet; each beat has purpose, message ref and intended emotional function.
5. Write VO/dialogue; label verbatim source narration separately from edited creative wording.
6. Map every factual line to one or more `CLM-ID` / `MSG-ID`; a new health proposition returns to S02.
7. Estimate word count and runtime as `ESTIMATED`; exact timing remains unavailable until audio is measured by S09.
8. Run safety, pacing, audience comprehension and CTA checks.

**Output: `Master Story & Screenplay`**
- creative treatment and narrative choice;
- logline/premise;
- beat sheet;
- screenplay/dialogue;
- verbatim VO source and edited VO as distinct records;
- factual line map;
- timing estimate with method/confidence;
- open questions and revision record.

**Negative cases**
- Missing S02 lock → no factual script lock.
- New or strengthened health proposition → S02 review.
- Narrative uses fictional events that imply a new medical mechanism → revise or mark clearly as metaphor without medical implication.
- Script length conflicts with target duration → compress narrative without dropping safety message, or return a duration trade-off to M00/user.

**Acceptance:** every factual sentence traceable; one core message; verbatim and edited narration never conflated; estimates labeled; no unsupported cause, guarantee or diagnosis; story purpose and CTA align.

### 4.5 S05 — Visual Identity & Art Direction

**Mandate:** author detailed visual canon while leaving narrative meaning to S04, camera decisions to S06, motion values to S07 and registry integration to S13.

**Procedure**
1. Inventory brand rules, rights/consent and source references from S01.
2. Define art direction grammar: medium, render treatment, palette, shape language, line/texture, lighting, typography intent and prohibited drift.
3. Define character identity: stable ID, silhouette, proportion, face/hair/wardrobe/accessories, age range only when supported/required, distinguishing features and allowed variation.
4. Define environment/location and prop taxonomy with scale/relationship and stable IDs.
5. Separate official brand assets from proposed creative interpretation.
6. Set permitted and prohibited variations, including text/logo use.
7. Specify reference assets required; state `PROMPT_ONLY`, `GENERATED`, `SELECTED`, `APPROVED`, `MISSING` distinctly.
8. Submit canonical Guide records to S13 registry; S13 does not author S05's visual details.

**Output: `Master Visual Style Guide` + character/environment/prop registry**

**Decision rules**
- Rights/likeness unclear → generic/fictitious representation; no inferred identity.
- Logo unavailable or restricted → placeholder, not recreated substitute.
- Visual ambiguity → maintain alternatives as `PROPOSED`, not locked.
- Image prompt cannot preserve exact typography → exact text remains renderer overlay, never image-model factual text.

**Acceptance:** stable IDs and versions; all canonical elements have owner and lock status; permitted variation explicit; no unauthorized likeness or brand use; actual asset existence is not inferred from a prompt.

### 4.6 S06 — Storyboard & Cinematography Director

**Mandate:** translate approved screenplay and visual canon into scene/shot/camera/composition/time contracts. S06 owns shot intent; S07 owns movement mechanics.

**Procedure**
1. Segment screenplay by semantic beat and source segment, not arbitrary equal slices.
2. Assign `SCN-ID`, `SHOT-ID`, purpose, message/fact refs and duration provenance.
3. Choose framing, lens/viewpoint language, composition, focal hierarchy, lighting and camera intent.
4. Map character/environment/prop IDs and Guide/lock versions.
5. Define overlay safe area and contrast/readability requirements.
6. Reconcile scene durations and transitions, including overlap accounting.
7. Supply camera/motion intent refs to S07 without authoring detailed transforms/easing.
8. Update S13 scene continuity ledger and handoff to S08/S10/S12.

**Duration policy — replaces undefined “M00 default”**

- `PROVIDED`: explicit user/project brief duration; preserve as the target unless the user authorizes a change.
- `MEASURED`: fixed source audio duration measured by S09; use as the factual timing constraint when no explicit target supersedes it.
- `ESTIMATED`: no fixed audio and no explicit duration; estimate from VO word count, reading pace assumptions, message comprehension and shot needs. Record formula/assumptions and confidence.
- `DEFAULTED`: only use a default when M00's project policy explicitly supplies a named profile and value. Record the policy ID/version. No invisible numeric default.
- `MISSING`: if no defensible estimate/profile can be selected, hold only the duration-dependent decision and ask one focused question if essential.

Priority is explicit target > fixed/measured audio constraint (unless brief authorizes recut) > documented estimate > explicit M00 profile. If a fixed audio recording conflicts with the target, M00 asks the user/owner to choose edit, pace, trim or duration change; do not silently time-stretch or omit speech.

**Frame arithmetic**
- Require fps/timebase before exact frame conversion.
- Represent intervals as `[start_frame, end_frame)`.
- State rounding policy and source precision.
- For transitions, specify overlap explicitly and ensure total timeline duration reconciles.
- Do not claim exact sync from reading-speed estimates.

**Output: `Storyboard Script + Cinematography Shot List`**

**Acceptance:** every scene has purpose, IDs, message/fact refs and time provenance; total duration reconciles; every camera move has narrative purpose; no unapproved message change; unknown canon is a placeholder; no invisible default.

### 4.7 S07 — Animation & Motion Design Director

**Mandate:** specify animation states, mechanics, timing and feasibility separately from S06 camera intent and S05 visual canon.

**Procedure**
1. Read scene/shot contracts, Guide versions and scene in/out states.
2. Identify animated elements by stable `ELEMENT-ID` and role.
3. Define starting state, anticipation, action, follow-through, settle and hold as applicable.
4. Define property/transform, value, unit, coordinate space and path.
5. Define keyframes, easing name plus parameters, frame range, fps/timebase and timing source.
6. Separate subject/object/camera motion; camera motion remains referenced to S06.
7. State physical plausibility, interaction/collision and state continuity constraints.
8. Provide a lower-complexity or reduced-motion fallback where possible.
9. Map all scene state changes to S13 and renderer-neutral references to S08/S10.

**Output: `Animation & Motion Specification`**
- motion records by scene/element;
- state in/out;
- keyframes and ranges;
- path/transform and units;
- easing parameters;
- timing provenance/precision;
- dependencies and prohibited movement;
- accessibility/reduced-motion alternative;
- feasibility status and fallback.

**Acceptance:** no unitless values; ordered keyframes; half-open frame ranges valid; fps/timebase known for exact timing; no visual canon or camera ownership conflict; renderer limitations disclosed; state in/out reconciles with S13.

### 4.8 S13 — Character, Narrative & Style Continuity Guardian

**Mandate:** govern MCG as the index/control layer for seven Guide modules, canonical locks, scene state and change propagation. S13 integrates records; it does not take detailed Guide authoring away from the domain owners.

**Seven Guide ownership retained**

| Guide | Domain content owner | S13 responsibility |
|---|---|---|
| GUIDE-01 Master Character Guide | S05 | Register, version, lock state and scene dependents |
| GUIDE-02 Character Profile / Personality | S04 narrative; S05 visual | Preserve split ownership and reconcile cross-domain conflicts |
| GUIDE-03 Master Visual Style Guide | S05 | Register visual tokens and lock version |
| GUIDE-04 Master Narrative Style Guide | S04 | Register narrative voice/style constraints |
| GUIDE-05 Master Voice & Audio Guide | S09 | Register voice/audio identity and approved source refs |
| GUIDE-06 Master World & Environment Guide | S05 | Register world/environment/prop canon |
| GUIDE-07 Scene Continuity Guide | S13 integrates; S06/S07/S09/S10 contribute | Maintain scene ledger, in/out state and cross-domain links |

**Procedure**
1. Select complexity profile: `LITE`, `STANDARD`, or `ADVANCED`, based on scene count, recurring assets, episode reuse, domain dependencies and change risk.
2. Initialize MCG with project ID, title/topic, owners, status, source dossier and Health Truth Registry refs.
3. Create seven Guide records; set domain owner, version, status, dependencies and affected scenes.
4. Accept authoring inputs from their owning skills; do not overwrite domain content.
5. Create canonical lock records with exact accepted definition, owner, basis, version, scope, permitted/prohibited variants, dependents and approval state.
6. Maintain scene continuity-in/out ledger: character state, wardrobe/props, environment/time, emotion/action, audio state and lock versions.
7. For every upstream change, calculate impacted dependency closure, create CHG record, mark affected outputs `INVALIDATED`/`STALE` and route retests.
8. Preserve prior versions and superseded decisions; no silent retcon.
9. Perform cross-scene audit and hand off exact Guide/lock versions to S04–S10 and S12/M00.

**Decision rules**
- Missing Guide author → record `MISSING`/`BLOCKED`; S13 may not fabricate domain specifics.
- Conflicting canon → preserve both candidates and `HOLD` pending owner decision.
- Stale lock version → invalidate dependent prompts/assets/scenes/render and rerun closure.
- Prompt-only reference → never mark actual asset present.
- Model identity drift → report observed discrepancy and recommend inspection/manual correction; no guarantee.

**Acceptance:** seven Guide IDs each have one accountable domain owner; scene lock refs exist and are current; scene in/out states reconcile; old versions preserved; invalidation is transitive; actual asset state reflects observed file evidence.

---

## 5. Universal Inter-Skill Handoff Contract

### 5.1 Single schema

**Canonical target file:** `schemas/v4/handoff-envelope.schema.json`  
**Contract version:** `1.0.0`  
**Schema dialect:** JSON Schema Draft 2020-12  
**Provided in this design package:** `schemas/v4/handoff-envelope.schema.json`

One schema governs all handoffs from M00 and S01–S14. Domain-specific outputs retain their own artifact schemas. The handoff envelope carries references and provenance; it does not duplicate the full Production Manifest, Health Truth Registry, MCG or media files.

### 5.2 Required fields

| Field | Purpose | Validation rule |
|---|---|---|
| `contract_version` | Handoff contract evolution | Explicit semantic version |
| `handoff_id` | Immutable envelope identity | Stable unique ID |
| `project_id`, `case_id` | Project/case context | Must match active project/case |
| `skill_id`, `skill_version` | Producer provenance | Must exist in canonical skill registry |
| `lane_id` | S10 workstream | Required only for S10: `S10-MP` or `S10-RE` |
| `invocation_status` | Honest execution status | `INVOKED`, `PROCEDURE_APPLIED`, `UNAVAILABLE`, `NOT_USED` |
| `created_at` | Time anchor | RFC 3339 date-time; format assertion enabled |
| `status` | Handoff completion | `COMPLETE`, `PARTIAL`, `BLOCKED`, `NOT_APPLICABLE`, `STALE`, `INVALIDATED` |
| `input_refs` | Inputs consumed | Artifact refs with hash/status/type |
| `outputs` | Artifacts produced | Artifact refs with hash/status/type/schema |
| `decisions` | Decisions and owner | Domain, decision state, rationale, owner and evidence refs |
| `inferences` | Explicit inferences | Statement, confidence and basis refs |
| `assumptions` | Explicit assumptions | Statement, confidence and basis refs |
| `unknowns` | Unresolved values | Description, impact, blocking status and resolver owner |
| `conflicts` | Conflicting evidence/requirements | Severity, affected refs, status and owner |
| `inherited_constraints` | Upstream locks/constraints | Original owner, source ref, immutable flag and override rule |
| `trace_links` | Provenance graph | From/to refs and relation type |
| `acceptance_checks` | Producer's performed checks | Criterion, expected/observed, status, evidence, limitation |
| `handoff_to` | Intended recipient(s) | Canonical skill IDs; `USER` only for user-facing output |
| `limitations` | Boundaries of result | Mandatory explanation for blocked/not-applicable states |
| `payload_hash` | Tamper evidence | SHA-256 of canonicalized envelope excluding this field |

### 5.3 Status semantics

| Status | Meaning | Downstream behavior |
|---|---|---|
| `COMPLETE` | Required output delivered; producer checks pass | Eligible for semantic acceptance, not automatic approval |
| `PARTIAL` | Useful output exists but required items remain | Consume only unaffected/allowed parts; dependent gates remain open |
| `BLOCKED` | Cannot safely or correctly proceed | Stop dependent work; preserve reason and recovery owner |
| `NOT_APPLICABLE` | Function genuinely irrelevant in this case | Must state why; not equivalent to PASS |
| `STALE` | Input/lock/dependency version changed | Re-read and regenerate affected output |
| `INVALIDATED` | Upstream change explicitly invalidated output | Cannot be reused as current evidence |

**Important:** `COMPLETE` is not the same as `APPROVED`, `VERIFIED`, `RENDERED` or `RELEASED`. Those states belong to domain artifacts and gates.

### 5.4 Artifact-reference object

Every `input_refs` and `outputs` element contains:
- `ref_id`;
- `artifact_type`;
- `schema_id` and `schema_version` when governed by a schema;
- `status`;
- `content_hash`;
- `content_ref` (path or resolvable artifact locator, where available);
- `owner_skill_id`.

M00 semantic validation checks that every referenced artifact exists, its bytes match its hash, the schema/version exists, and its status has not been invalidated.

### 5.5 Semantic validator — checks beyond JSON Schema

JSON Schema validates local shape and types. A mandatory semantic validator must additionally check:

1. `project_id` and `case_id` match the current project context.
2. `skill_id` and `lane_id` are valid in the canonical ownership registry.
3. Producer is authorized to own every claimed output type.
4. `handoff_to` is a valid recipient for the producer/output type.
5. Every `input_ref`, `output`, evidence ref and trace endpoint resolves.
6. Every `content_hash` matches actual artifact bytes or canonical payload.
7. Dependency/lock versions are current and not `STALE`/`INVALIDATED`.
8. `COMPLETE` has at least one output and all mandatory acceptance checks are `PASS` or justified `NOT_APPLICABLE`.
9. `PARTIAL`/`BLOCKED` includes unresolved limitations and does not release dependent gates.
10. `NOT_APPLICABLE` contains an explicit rationale and is allowed for that task.
11. Critical unknowns, conflicts or missing authority prevent false completion.
12. A producer cannot self-assign human approval, clinical verification or independent QA.
13. A receiving skill acknowledgement is recorded separately by M00, keyed to immutable `handoff_id` + `payload_hash`; producer cannot edit the receiver's decision.

### 5.6 Handoff flow

```text
Producer creates envelope
        ↓
JSON Schema validation
        ↓
Artifact/hash/ownership/recipient semantic validation
        ↓
M00 records immutable handoff + validation evidence
        ↓
Recipient reviews inherited locks and inputs
        ↓
Recipient writes separate receipt: ACCEPTED / ACCEPTED_WITH_CAVEATS / REJECTED
        ↓
M00 updates dependency/gate state
```

A failed schema does not delete the producer's work; it marks the handoff `BLOCKED` and returns exact field/path errors. A semantic failure is separately labeled even if JSON Schema passes.

### 5.7 Compatibility mapping

Existing textual fields map without renaming:
- `skill_id` remains `skill_id`;
- `status` retains existing handoff status vocabulary;
- `input_refs`, `outputs`, `decisions`, `inferences`, `assumptions`, `unknowns`, `conflicts`, `inherited_constraints`, `trace_links`, `acceptance_checks`, `handoff_to`, `limitations` are preserved.

The change is from free-form text to typed structured objects. During migration, an adapter may translate old string references into `ref_id` objects only when the target artifact can be resolved. Unresolvable strings remain `UNKNOWN`; the adapter must not fabricate hashes, artifact types or versions.

---

## 6. Remediation architecture for FND-001 through FND-009

### FND-001 — External trust root and real authority binding

**Target severity:** P0 must remain release-blocking until corrected.

**Observed baseline issue:** project payload contains `authorized_approvers`, `trusted_signing_keys` and approval-level `authority_verified`; the active engine uses project-supplied trust data. A valid Ed25519 signature proves possession of the corresponding private key, not a person's institutional/clinical authority.

**Target design**
1. Remove project payload as a source of trusted public keys and role grants.
2. Load an external Trust Registry from a protected configuration/source separate from the audited project.
3. Pin the Trust Registry root fingerprint out-of-band in the validator/runtime release configuration.
4. If registry root signatures are claimed, actually verify the root signature against a pinned root key; fingerprint pinning alone must be described accurately and cannot be called signature verification.
5. Registry entries bind `approver_id`, `role`, `key_id`, public key, issuing authority, credential reference, active/revoked state, validity interval and allowed approval scope.
6. Provisioning/identity checks happen outside the project payload through an authoritative institutional process. A non-empty `credential_ref` is only a pointer, not proof that the credential is valid.
7. Approval signature binds canonical payload: approval ID, approver ID, role, decision, exact artifact hashes, scope, created/expiry time, nonce and trust-registry version.
8. Ignore/remove self-asserted `authority_verified`; derive authority from the external registry and credential/role validation.
9. Enforce role-specific quorum and distinct human identities for critical release decisions. Example quorum is a policy decision, not a universal assumption; clinician, rights owner and release approver are distinct scopes.
10. Support revocation, expiry, replay protection, key rotation and audit logs.
11. Fail closed when registry unavailable, key revoked/expired, role mismatch, hash mismatch or quorum missing.

**Implementation note on supplied remediation:** `remediasi/promkes_hardening/trust_anchor.py` is a useful prototype for external key lookup, revocation and quorum, but its `load()` path computes and compares a pinned fingerprint while excluding `root_signature`; it does not verify that root signature. The target implementation must either implement the claimed root-signature verification or accurately define the out-of-band fingerprint pin as its root trust mechanism. Credential validity also requires real authority verification.

### FND-002 — Prompt firewall connected to live intake and execution boundary

**Target severity:** P1.

**Target design**
1. Scan raw text extracted from poster, image OCR/visual reading, captions, documents, scripts, transcript, metadata, filenames and externally sourced references at G0.
2. Keep original bytes/text as immutable evidence; create normalized scan view separately. Never overwrite source material with normalized text.
3. Detect multilingual and obfuscated patterns (Indonesian/English, homoglyphs, invisible characters, URL/HTML encoding and common encodings) using heuristics plus structural boundary checks.
4. Every source chunk carries trust label, source ID, extraction provenance and scan result.
5. A positive/suspected hit enters quarantine. Quarantined source content may be quoted/analyzed as data but has no authority to alter system/developer/user instructions or invoke tools.
6. Isolate untrusted content structurally: no tool capability is inherited from data; no prompt content is concatenated into privileged instruction slots.
7. Re-scan any newly introduced or transformed untrusted content before it crosses a model/tool/renderer boundary. G4 consumes G0 scan evidence and requires re-scan when source hash or normalized content differs.
8. Scanner error, missing text payload or missing evidence is `NOT_RUN`/`BLOCKED`, never PASS.
9. No-match means only “no configured heuristic matched”; it is not a security certification.
10. Add false-positive review without releasing the source from untrusted-data status.

**Gate placement:** canonical control `V4-CTL-014` belongs to G0 intake because no untrusted input should enter the working context unclassified. G4 must verify the intake scan record and require a fresh scan for content changed/added after G0. Avoid duplicate manual gate ownership maps; model re-scan as an execution-boundary assertion tied to the same control evidence or a separately named, explicitly registered control.

**Implementation note on supplied remediation:** `firewall_id.py` adds Indonesian/English and obfuscation heuristics and quarantine decisions. It remains a heuristic, and its no-hit outcome must never imply safe content. The live CLI path must pass actual source texts, not user-provided booleans.

### FND-003 — Provenance integrity plus claim-to-source support

**Target severity:** P1.

**Target design**
1. Fetch/inspect the actual source where capability and permission allow; otherwise mark `UNVERIFIED`.
2. Preserve source snapshot bytes/text, URI, title/issuer, published/updated date, access time, jurisdiction, data period, population, method and limitations.
3. Compute content hash from the exact snapshot bytes; do not accept a format-valid hash as verification.
4. Record precise support locator (page/section/paragraph/timestamp) and verbatim quotation, if available.
5. Bind each `CLM-ID` to one or more source/evidence refs and record direct support, contradiction, partial support, context and applicability.
6. Distinguish integrity (bytes unchanged), provenance (where/when it came from), semantic support (source supports proposition) and clinical approval (authorized human judgement).
7. A lexical/number/negation filter can reject obvious mismatch but cannot prove clinical entailment. It is a triage layer only.
8. Human clinical review is separately evidenced and bound to exact Claim Registry/artifact hash.
9. A source update/withdrawal invalidates dependent claim records and downstream facts/scenes/overlays.

**Target statuses:** retain existing claim statuses and avoid upgrading `VERIFIED` without actual support evidence and required review. A schema PASS alone cannot produce VERIFIED.

**Implementation note:** `bukti_semantik.py` is a screening prototype for quotes, numeric consistency and negation. It must not be promoted to a clinical semantic adjudicator.

### FND-004 — One canonical control registry and one active evaluator

**Target severity:** P2.

**Target design**
1. `schemas/v4/control-registry.v4.json` becomes the single source of control identity, adapter, gate, risk, test ID, owner and required evidence.
2. Engine constructs runtime dispatch from the registry; remove duplicated hard-coded mappings of control IDs/gates/adapters.
3. Retain legacy `CTRL-*` only as explicit aliases to canonical `V4-CTL-*` during migration.
4. Alias table must map every old ID one-to-one or explicitly mark retired/replaced. Unknown alias fails validation.
5. Legacy function tests call the canonical active evaluator through a compatibility adapter; they must not validate a disconnected implementation and imply production-path coverage.
6. Record deprecation window and remove aliases only after dependent tests/consumer inventory is clean and compatibility decision is accepted.

### FND-005 — Full registry/engine parity

**Target severity:** P2.

At build/test time compare the complete control definition, not only ID and adapter:
- control ID;
- adapter name;
- gate assignment (including whether multi-gate control is explicitly allowed);
- risk/severity;
- owner skill;
- test ID(s);
- mandatory evidence fields;
- failure policy.

Preferred direction: engine reads the registry rather than maintaining a separate Python mapping. If an in-code adapter implementation exists, validate that every registered adapter resolves exactly once and that no unregistered adapter is reachable. A G0/G4 disagreement must fail release consistency validation.

### FND-006 — Independent invalidation oracle

**Target severity:** P2.

**Target design**
1. Treat the project dependency graph as the subject under test, not its expected answer as an oracle.
2. Compute reference transitive closure with a separate implementation/specification.
3. Compare engine output to reference closure for each changed node.
4. Reject cyclic dependency graphs unless the schema explicitly supports/normalizes cycles; current target expectation is a DAG.
5. Add property/metamorphic tests: idempotence; transitive closure; monotonicity under added edge; changed node excluded; deterministic ordering; no missed dependent nodes.
6. `expected_invalidated` supplied by project may remain a display/test fixture but must not determine PASS.
7. Validate that an invalidated artifact cannot remain accepted by any downstream gate.

**Prototype note:** `oracle_independen.py` has a reference closure and metamorphic checks. Its reference function and property tests should be independently reviewed; the target requirement is oracle independence from project-supplied expected result.

### FND-007 — Fail-closed resource ceilings

**Target severity:** P2.

Define a resource policy profile by route and project complexity. Fields may include:
- `budget_profile_id` and policy version;
- maximum asset bytes and total assets;
- maximum duration and resolution/fps class;
- maximum render runtime and memory;
- maximum retries;
- estimated/actual compute or provider cost, when measurable;
- maximum token/operation budget, when applicable;
- evidence/measurement source and owner.

Decision rules:
- budget required by the selected route but missing → `BLOCKED`;
- actual measurement unavailable → `NOT_VERIFIED`, not PASS;
- resource category genuinely irrelevant → `NOT_APPLICABLE` plus reason;
- exceeded hard ceiling → FAIL/BLOCKED and no further expensive execution;
- estimated cost is not represented as actual cost.

The project may carry requested budget values, but allowed ceilings and override authority come from external policy or an accepted project budget; a payload cannot silently relax a hard organizational ceiling.

### FND-008 — Operational depth for thin subskills and shared checklists

**Target severity:** P2.

Adopt the procedure template in Section 4. For S02, S03, S04, S05, S06, S07 and S13, replace generic repeated checklists as the sole operating method with domain-specific procedure references. Keep the generic checklist as a short pre/postflight only.

Each sub-procedure must have at least one positive, one negative, one missing-input/boundary and one conflict/recovery acceptance case. Complex/high-risk procedures need more than one case.

Do not create seven separate skills for S02 micro-modules. Do not promote specialist names to fictitious parallel agents. The parent skill owns the procedure and outputs.

### FND-009 — Explicit duration and timing policy

**Target severity:** P2.

Remove the undefined phrase “use M00 default” unless a policy object resolves it. Introduce `duration_policy` in the project context/manifest with:
- `basis`: `USER_PROVIDED`, `SOURCE_AUDIO_MEASURED`, `ESTIMATED`, `M00_PROFILE`, `UNKNOWN`;
- `target_duration_seconds`;
- `source_ref` where applicable;
- `estimate_method` and assumptions where estimated;
- `profile_id`/version when defaulted;
- `tolerance_seconds` only when explicitly defined;
- `review_status` and owner.

Priority: explicit user target → fixed measured source audio unless authorized to edit → documented estimate → named M00 profile. Never invent exact timing from reading speed. S06 remains owner of scene timing plan; S09 owns audio timing evidence; M00 owns project-level variable policy and conflict routing.

---

## 7. Dependency and ownership matrix

### 7.1 Primary handoff relationships

| Producer | Core outputs | Primary recipients | Dependency note |
|---|---|---|---|
| M00 | Intake/context, capability, project manifest, routing and delivery state | S01–S14 as needed; USER | Sole integrator; does not author domain truth |
| S01 | Source Material Dossier, extracted source/asset refs | S02, S03, M00 | S01/S09 intake may run independently in HYBRID when inputs differ |
| S02 | Health Validation Dossier, Claim Register, Health Truth Registry, Fact Locks | S03, S04, S08, S12, M00 | Required before health facts are locked into narrative/overlay |
| S03 | Campaign Strategy Blueprint | S04, S11, M00 | Needs S02 safe fact set and evidence-grounded audience context |
| S04 | Master Story & Screenplay, beat sheet, VO wording | S05, S06, S09, S13, S12, M00 | Every factual line must map to S02 claim/message IDs |
| S05 | Visual Style Guide, character/environment/prop canon | S13, S06, S07, S08, S12, M00 | S05 authors details; S13 registers and guards them |
| S06 | Storyboard Script, shot list, camera/composition contracts | S07, S08, S10, S13, S12, M00 | Requires S04, S05, S02 locks and duration policy |
| S07 | Animation & Motion Specification | S08, S10, S13, S12, M00 | Requires S06 shot intent and current Guide/scene states |
| S08 | Reference Prompt Pack, reference asset manifest | S10, S12, M00 | Reference prompts are stills; asset existence needs file evidence |
| S09 | Audio dossier, transcript/timing, SRT/VTT, sound cues/post spec | S04, S06, S10-MP, S10-RE as needed, S11, S12, M00 | Actual timing only if measured/grounded; never invent transcript |
| S10-MP | Media Production Handoff / Composition Manifest | S10-RE, S12, M00 | Editorial decisions stay in S10-MP |
| S10-RE | Adapter, build/runtime/render evidence, media output refs | S12, M00 | No output claim without actual file evidence |
| S11 | Platform/distribution/accessibility package | S12, M00 | Optional workstream; no algorithmic guarantee |
| S12 | Independent QA dossier, defect register, release recommendation | Domain owner(s), M00 | Routes defects; does not silently rewrite upstream artifact |
| S13 | MCG, seven Guide registry, locks, scene ledger, change impact | S04–S10, S12, M00 | Integrates owner-authored Guides; returns lock/version constraints |
| S14 | Context register, change impact and release parity preflight | M00 | Mandatory before relevant versioned update/publication as defined by M00 |

### 7.2 Dependency graph

```text
M00 intake
  ├── S01 source dossier ─────────┐
  └── S09 audio intake (optional) ├── S02 health claim/evidence/fact lock
                                 │          │
                                 │          └── S03 campaign blueprint
                                 │                    │
                                 └────────────────────┴── S04 screenplay/VO
                                                              │
                                       ┌──────────────────────┼─────────────────┐
                                       │                      │                 │
                                   S05 visual canon        S09 VO/audio      S13 MCG init
                                       │                      │                 │
                                       ├────── S13 Guide registration ◄────────┘
                                       │
                                   S06 storyboard/camera
                                       │
                                   S07 motion
                                       │
                                   S08 still/reference prompts
                                       │
                          S09 audio/subtitle timing integration
                                       │
                              S10-MP composition/editing
                                       │
                              S10-RE adapter/build/render
                                       │
                                   S12 independent QA
                                       │
                             M00 delivery aggregation
                                       │
                          human approvals / publication
```

This graph is a default dependency shape, not a requirement that all work be strictly serial. M00 may parallelize independent S01/S09 intake and selected visual-reference/audio preparation after upstream locks are approved. A dependency must never be skipped merely to preserve a parallel schedule.

### 7.3 Feedback and invalidation routes

| Change origin | Minimum dependent closure to reconsider |
|---|---|
| S01 source text/asset correction | S02 claims; S03 audience/message if source affects context; S04 lines; S06 scenes; S08 refs; S10 overlays; S12 QA |
| S02 claim/fact-lock change | S03 message/CTA; S04 factual lines; S06 scenes; S08 prompts/overlays; S11 copy; S10 composition; S12 QA |
| S03 objective/CTA change | S04 screenplay; S06 story beats; S08 refs if changed visuals; S10 overlays; S11 package; S12 QA |
| S04 story/VO change | S05 character/story needs; S06 scenes; S09 VO/subtitle timing; S13 Guides/ledger; S08 refs; S07 motion; S10 timeline; S12 QA |
| S05 visual canon change | S13 lock/Guide versions; S06 composition; S07 character motion; S08 prompts/assets; S10 compositions; S12 visual QA |
| S06 scene/shot/camera change | S07 motion; S08 keyframes; S09 cue alignment if scene timing changes; S13 ledger; S10 composition; S12 QA |
| S07 motion change | S08 pose/keyframe refs; S13 scene state; S10 adapter/timeline; S12 motion QA |
| S08 asset replacement | S10 asset mapping/render; S12 asset/rights/visual QA; S13 only if canon/lock changes |
| S09 transcript/timing/audio change | S04 script mapping; S06 scene times; S07 sync; S10 mix/timeline; S11 captions; S12 A/V QA |
| S10-MP editorial change | S10-RE composition mapping/render; S12 QA; S13 scene ledger if continuity state changes |
| S10-RE adapter/runtime change | Build/render evidence and technical QA; does not invalidate upstream creative locks unless mapping semantics changed |
| S13 Guide/lock change | All explicitly dependent scene/reference/assets/motion/render; preserve unaffected branches |
| S14 context or accepted requirement change | M00 change map and all owners in dependency closure; no direct domain rewrite |

M00 records `CHG-ID`, before/after hashes, affected IDs, invalidations, test closure and rollback. S13 owns continuity consequences; M00 owns project-wide dependency execution.

---

## 8. Gate integration criteria

Keep existing gate IDs to avoid compatibility break: `G0_INTAKE_OK`, `G1_FACT_LOCK`, `G2_NARRATIVE_LOCK`, `G3_VISUAL_LOCK`, `G4_PROMPT_PREFLIGHT`, `G5_MANIFEST_VALID`, `G6_CODE_VALID`, `G7_RELEASE_APPROVED`.

| Gate | Owning domain(s) | Minimum acceptance | Fail/hold behavior |
|---|---|---|---|
| G0_INTAKE_OK | M00, S01, S09, security controls | Input inventory; source IDs; rights/privacy classification; raw-source hash; actual untrusted text scanned; capability/access records | Unknown rights/privacy or scan not run blocks affected use; preserve safe intake only |
| G1_FACT_LOCK | S02 + authorized clinician | Atomic claims; source snapshot/hash; source locator; direct support/counterevidence; safe wording; externally verified approval if required | Unverified/contradicted/stale material fact cannot enter approved factual output |
| G2_NARRATIVE_LOCK | S03, S04 | Campaign objective/CTA; every factual script line mapped; VO source/edit distinction; narrative acceptance | New claim or CTA mismatch returns to owner |
| G3_VISUAL_LOCK | S05, S13 | Guide IDs/owners/versions; canonical lock status; rights/likeness basis; scene references use current lock | Unknown likeness/brand or conflict remains HOLD/placeholder |
| G4_PROMPT_PREFLIGHT | M00/security boundary | Intake scan evidence current for exact content hash; changed/new content rescanned; tool-less quarantine for flagged content | Missing/stale scan evidence or unresolved quarantine blocks use at privileged boundary |
| G5_MANIFEST_VALID | M00, S06–S10, S13 | Universal handoffs schema+semantic pass; stable refs; scene/timing arithmetic; current dependency closure; rights and budget state | Schema/semantic mismatch, missing required budget or invalid reference blocks render readiness |
| G6_CODE_VALID | S10-RE | Verified renderer route/version; adapter mapping; path/dependency checks; static/build/runtime checks; proof render where feasible | Unavailable runtime → HANDOFF; failed build/render → BLOCKED or safe correction loop |
| G7_RELEASE_APPROVED | S12, M00, human authorities | Independent QA evidence; exact output hash; external trust/approval quorum; required rights/privacy/clinical/institutional authorization | Any mandatory NOT_RUN/NOT_VERIFIED/BLOCKED or invalid authority prevents release PASS |

**Gate status discipline:** only executed controls with evidence can be PASS. `NOT_RUN`, `NOT_VERIFIED`, `BLOCKED`, `STALE`, `INVALIDATED`, `PARTIAL` are not PASS. `NOT_APPLICABLE` requires rationale and gate policy permission.

---

## 9. Acceptance test catalogue

The JSON companion `tests/target-architecture-v2-acceptance.json` is the test inventory and execution record for this target design. All 44 acceptance cases have been executed against the local additive implementation copy using deterministic code and fixture oracles; the companion records each observed result and test function. The local status is `PASS` for all 44. This does not imply that external providers, a live ChatGPT/plugin host, a clinician, a renderer or actual media were executed.

`TST-040`–`TST-042` PASS because the guards correctly refuse to infer a completed render or independent QA when evidence is absent. They are not evidence that a real MP4 was rendered or inspected.

### 9.1 Security, source and control-engine tests

| Test | Scenario | Expected result | Local executable test | Result |
|---|---|---|---|---|
| TST-001 | Project includes attacker-generated signing key and self-grants role | Rejected; project keys/roles cannot establish trust  | `test_tst_001_project_supplied_key_cannot_self_authorize` | PASS |
| TST-002 | Registered key is revoked, expired, wrong-role or wrong-person | Rejected with reason  | `test_tst_002_revoked_expired_wrong_role_and_wrong_person_rejected` | PASS |
| TST-003 | Approval has valid signature but no required role quorum/distinct approvers | Release remains BLOCKED  | `test_tst_003_release_quorum_requires_distinct_approvers` | PASS |
| TST-004 | Registry has altered body or invalid root signature/pin | Registry rejected; no fallback to project keys  | `test_tst_004_external_registry_root_pin_and_signature_are_verified` | PASS |
| TST-005 | Indonesian prompt override, exfiltration, prompt leak or fake approval instruction in poster/caption | Quarantined at G0 and not treated as authority  | `test_tst_005_indonesian_prompt_injection_quarantined_at_intake` | PASS |
| TST-006 | Obfuscated prompt using homoglyph/zero-width/encoding/HTML/URL encoding | Tested normalization path; confirmed hits quarantined; no-hit does not claim safe  | `test_tst_006_obfuscated_injection_is_detected` | PASS |
| TST-007 | New or transformed untrusted content appears after G0 | Re-scan required before G4/tool boundary  | `test_tst_007_transformed_untrusted_text_is_rescanned_before_tool_boundary` | PASS |
| TST-008 | Scanner missing, fails or receives no source text | NOT_RUN/BLOCKED; never PASS  | `test_tst_008_scanner_missing_text_or_error_fails_closed` | PASS |
| TST-009 | Source hash differs from source snapshot bytes | Provenance gate fails  | `test_tst_009_source_snapshot_hash_mismatch_fails` | PASS |
| TST-010 | Claim quotation absent, unsupported number or clear contradictory wording | Lexical evidence gate rejects/flags; does not claim clinical adjudication  | `test_tst_010_claim_quote_numbers_and_contradictions_fail_closed` | PASS |
| TST-011 | Claim source relevant but wrong jurisdiction/population/date | PARTIAL/UNVERIFIED or human review; not VERIFIED by citation presence alone  | `test_tst_011_context_mismatch_cannot_become_verified` | PASS |
| TST-012 | Project-supplied `expected_invalidated` is manipulated | Does not affect independent oracle result  | `test_tst_012_independent_invalidation_oracle_ignores_project_expected_list` | PASS |
| TST-013 | Dependency graph has a cycle or missed transitive dependent | Graph validation/invalidations fail  | `test_tst_013_dependency_cycles_and_missing_transitive_nodes_fail` | PASS |
| TST-014 | Required route has missing resource budget | BLOCKED  | `test_tst_014_missing_approved_resource_profile_blocks_route` | PASS |
| TST-015 | Resource is genuinely irrelevant with policy reason | NOT_APPLICABLE, not PASS  | `test_tst_015_resource_not_applicable_requires_reason_and_zero_required_categories` | PASS |
| TST-016 | Registry control ID/adapter/gate/risk/test/owner differs from runtime dispatch | Release consistency validation fails  | `test_tst_016_control_registry_full_metadata_drift_fails` | PASS |
| TST-017 | Legacy CTRL alias maps ambiguously or to unknown V4 control | Migration validation fails  | `test_tst_017_legacy_alias_missing_ambiguous_or_unknown_fails` | PASS |

### 9.2 Handoff and specialist-operation tests

| Test | Scenario | Expected result | Local executable test | Result |
|---|---|---|---|---|
| TST-018 | Handoff omits a required field or has invalid field type | JSON Schema validation fails with path-level diagnostics  | `test_tst_018_handoff_missing_field_and_wrong_type_rejected` | PASS |
| TST-019 | Handoff claims COMPLETE with zero outputs | Rejected by schema/semantic validator  | `test_tst_019_complete_handoff_requires_output_artifact` | PASS |
| TST-020 | Handoff references unknown artifact or wrong content hash | Semantic validation fails  | `test_tst_020_unknown_artifact_and_content_hash_mismatch_fail` | PASS |
| TST-021 | Handoff uses S10 without lane_id, or another skill with S10 lane_id | Schema fails  | `test_tst_021_s10_lane_is_required_only_for_s10` | PASS |
| TST-022 | Handoff claims human approval or independent QA outside owner's authority | Semantic ownership validator fails  | `test_tst_022_handoff_cannot_self_claim_clinical_or_independent_qa` | PASS |
| TST-023 | Handoff marked PARTIAL/BLOCKED but downstream gate tries to consume blocked dependent output | Gate remains blocked  | `test_tst_023_blocked_or_invalidated_prerequisite_blocks_downstream` | PASS |
| TST-024 | S02 receives compound health statement containing two propositions | Extractor emits separate atomic CLM IDs  | `test_tst_024_compound_health_sentence_decomposed_into_atomic_claims` | PASS |
| TST-025 | S02 evidence is inaccessible, stale, contradicted or scope-mismatched | Claim status remains non-approved; affected content held  | `test_tst_025_stale_missing_and_context_mismatch_claims_not_approved` | PASS |
| TST-026 | S02 simplification strengthens causality/guarantee/scope | Simplification rejected  | `test_tst_026_health_simplification_cannot_strengthen_claim` | PASS |
| TST-027 | S03 has no evidence for local demographic/dialect claim | Assumption marked or neutral Indonesian selected  | `test_tst_027_local_demographic_or_dialect_detail_without_evidence_is_flagged` | PASS |
| TST-028 | S03 blueprint has competing behavior objectives and unrelated CTAs | Reprioritization or clarification; not silently accepted  | `test_tst_028_campaign_requires_one_coherent_primary_objective_and_cta` | PASS |
| TST-029 | S04 factual sentence has no CLM/MSG trace | Narrative lock fails  | `test_tst_029_factual_screenplay_line_without_trace_fails_narrative_lock` | PASS |
| TST-030 | S04 creates a new health proposition via metaphor/dialogue | Routed to S02; no approval from S04  | `test_tst_030_metaphor_introducing_health_proposition_routes_to_s02` | PASS |
| TST-031 | S05 uses unapproved logo/real likeness or unstable character ID | Canon remains DRAFT/HOLD; generic alternative or permission request  | `test_tst_031_visual_plan_holds_unapproved_logo_likeness_and_stale_identity` | PASS |
| TST-032 | S06 receives no explicit duration/audio and uses undeclared numeric default | Acceptance fails; requires estimate or named M00 profile  | `test_tst_032_missing_duration_and_profile_fails_acceptance` | PASS |
| TST-033 | S06 scene ranges/overlap do not reconcile | Timeline acceptance fails  | `test_tst_033_scene_frame_arithmetic_rejects_unreconciled_overlap` | PASS |
| TST-034 | S07 motion value has no unit/fps/timebase or invalid keyframe order | Motion schema/acceptance fails  | `test_tst_034_motion_schema_rejects_missing_units_and_keyframe_order` | PASS |
| TST-035 | S07 state-out conflicts with next scene state-in | Route to S13; dependent scene held  | `test_tst_035_motion_state_discontinuity_routes_to_s13_and_holds` | PASS |
| TST-036 | S13 Guide registry duplicates owner or uses stale lock version | Continuity acceptance fails; affected artifacts invalidated  | `test_tst_036_guide_registry_duplicate_or_stale_lock_fails` | PASS |
| TST-037 | S13 change modifies GUIDE-03 and downstream assets | Dependency closure contains every dependent asset/scene/render and preserves unaffected branches  | `test_tst_037_guide_change_propagates_transitively_and_preserves_unaffected` | PASS |
| TST-038 | Handoff from S10-MP lacks composition fields required by S10-RE | S10-RE rejects receipt with missing-field report  | `test_tst_038_media_production_handoff_missing_composition_mapping_rejected` | PASS |
| TST-039 | Renderer is unavailable or unsupported | S10-RE outputs HANDOFF/NOT_AVAILABLE; no render claim  | `test_tst_039_renderer_unavailable_returns_handoff_without_render_claim` | PASS |
| TST-040 | Build passes but no actual MP4 exists | `RENDERED_VERIFIED` prohibited  | `test_tst_040_build_pass_without_mp4_does_not_claim_rendered_verified` | PASS |
| TST-041 | MP4 exists but not opened/inspected | Artifact QA remains NOT_RUN/NOT_VERIFIED  | `test_tst_041_existing_media_without_actual_inspection_remains_not_verified` | PASS |
| TST-042 | Manifest says QA PASS but S12 has not inspected actual media | S12 media layer remains NOT_RUN; release gate cannot infer PASS  | `test_tst_042_manifest_qa_pass_without_s12_inspection_cannot_release` | PASS |
| TST-043 | Existing M00/S01–S14 identity, path and trigger contract is checked after additive migration | No unapproved rename/removal/interface break  | `test_tst_043_compatibility_preserves_skill_ids_paths_triggers_and_states` | PASS |
| TST-044 | POSTER_FIRST, AUDIO_FIRST, HYBRID and SCRIPT_FIRST representative fixtures | Correct routing and explicit evidence/timing limits  | `test_tst_044_all_four_input_modes_route_and_preserve_timing_limits` | PASS |

### 9.3 Test evidence record

The final local execution ran 44/44 cases with pytest on the additive working-copy candidate. Exact case names, per-case status, duration, test-source SHA-256 and limitations are recorded in `tests/target-architecture-v2-acceptance.json`; JUnit evidence is in `reports/v2-acceptance-junit.xml`. The working copy is not associated with a verified Git commit SHA.

The machine-readable execution record carries test ID, originating requirement, owner/dependency links, test function, execution status, duration, test-source SHA-256, local environment and timestamp. Target host/model/renderer details are not applicable to these deterministic tests. Any future external/runtime test must add its exact runtime, artifact hash, inspection evidence, reviewer and limitations before PASS.

A test specification, test file presence, green static validation or previous release report is not a test execution result for the current target commit.

---

## 10. Integration acceptance criteria

A V2 integration is acceptable only when all applicable rows below are evidenced.

### 10.1 Structural integration
- [ ] All M00–S14 identity, folder names, manifest registration and triggers are preserved.
- [ ] S10-MP and S10-RE are internal lanes under S10, not duplicate public skill IDs.
- [ ] Universal handoff schema validates producer and recipient envelopes.
- [ ] Existing project/claim/artifact/scene/capability schemas remain authoritative for their data classes.
- [ ] MCG and Production Manifest remain distinct sources of truth with references, not duplicated bodies.
- [ ] One canonical control registry drives runtime dispatch.

### 10.2 Authority and security
- [ ] Project-supplied keys/approver lists cannot create trust.
- [ ] Trust registry root/pin and signer identity/role are externally verified.
- [ ] Revocation, expiry, scope, hash binding and quorum are tested.
- [ ] Untrusted input is actually inspected and structurally isolated.
- [ ] New/modified untrusted content is rescanned at the execution boundary.
- [ ] Missing firewall/authority evidence is fail-closed.

### 10.3 Evidence and health integrity
- [ ] Source hashes are computed from actual bytes/snapshots.
- [ ] Every approved material claim has a direct support locator and claim-evidence relation.
- [ ] Scope, time, jurisdiction, population and limitations are recorded.
- [ ] Lexical filters are never represented as clinical proof.
- [ ] Clinical approval binds exact claim/artifact hash and trusted human authority.

### 10.4 Operational and creative integration
- [ ] S02–S07 and S13 procedures have inputs, method, decision rules, outputs, negative cases and tests.
- [ ] S06 duration provenance is explicit; no undefined default remains.
- [ ] S07 motion specs have units, timing precision and valid state transitions.
- [ ] S13 registers exactly the seven Guide modules with their current owners.
- [ ] S10-MP/RE handoff fields reconcile and all relevant source/asset rights are explicit.

### 10.5 Runtime and media evidence
- [ ] S10-RE reports exact capability/version and permission evidence.
- [ ] Build, runtime, proof render and full render statuses are distinct.
- [ ] Output file existence, metadata, openability and inspection are evidenced separately.
- [ ] S12 remains independent of the implementation lane.
- [ ] Human approvals and publication state remain separate from technical PASS.

---

## 11. Compatibility and migration plan

### 11.1 Identity and interface compatibility

Preserve:
- plugin name, IDs, `plugin.json` and trigger routes;
- M00 and S01–S14 skill IDs, frontmatter `name`, directory paths and owner responsibilities;
- existing input modes, delivery states, claim statuses and gate IDs;
- existing artifact/manifest IDs and references unless a specific migration is approved.

New lane IDs are internal metadata only. `skill_id` remains `S10` in external references; `lane_id` distinguishes `S10-MP` or `S10-RE`.

### 11.2 Additive file plan

Proposed additions:
- `schemas/v4/handoff-envelope.schema.json` (provided in this package);
- `docs/target-architecture-v2.md` (this document);
- `docs/s10-lane-contract.md` or equivalent section/reference in S10;
- domain-specific operating references for S02, S03, S04, S05, S06, S07, S13;
- `tests/target-architecture-v2-acceptance.json` (provided in this package);
- validator and integration tests for schema plus semantic checks.

Proposed updates, only after approval:
- M00: handoff intake, semantic validator, duration policy, control registry use and dependency status;
- each targeted skill: point to its expanded procedure and envelope schema;
- S10: add lane IDs and lane contract references;
- S13: formalize Guide registry ownership and invalidation event;
- project schema: optionally add `handoff_refs` to point to immutable envelope records (do not embed full handoffs into the project object by default);
- `control-registry.v4.json` and engine: unify registry/runtime dispatch and correct control mapping.

### 11.3 Migration phases

**Phase 0 — baseline and compatibility inventory**
- Freeze current source refs/hashes and enumerate consumers.
- Capture current tests and exact commit/branch when repository baseline is available.
- Confirm no overlapping branch/PR and write access before repository changes.

**Phase 1 — additive contracts**
- Add handoff schema, semantic validator contract, sample payloads and negative fixtures.
- Keep textual handoff as an input-only legacy format temporarily; translate only resolvable refs.
- Add S10 lane contract without renaming S10.

**Phase 2 — specialist depth**
- Add operational runbooks for S02/S03/S04/S05/S06/S07/S13.
- Update skills to reference the runbooks and produce universal envelopes.
- Preserve current artifact formats and existing owners.

**Phase 3 — critical trust remediation**
- Externalize trust registry and approval verification.
- Connect firewall to real intake and execution boundary.
- Add source snapshot/quote/support validation.
- Fail closed on missing critical security/evidence data.

**Phase 4 — engine/registry/resource/oracle consolidation**
- Canonical registry drives dispatch.
- Map legacy IDs via aliases.
- Compare full registry/runtime metadata.
- Integrate independent invalidation oracle and budget policy.

**Phase 5 — acceptance, regression and release parity**
- Run all applicable new tests and existing base/reference-output suites.
- Exercise all four input modes, blocked paths, recovery and S10 lane contract.
- Verify plugin/repo manifests, skill inventory, schema refs and documentation parity.
- Read back every changed file; inspect complete diff; create PR only after authorized implementation and confirmed write access.

### 11.4 Rollback and stop conditions

- Do not delete legacy handoff parsing until every consumer and artifact is migrated.
- Do not remove `CTRL-*` aliases until regression coverage proves all consumers use canonical registry.
- Stop if trust root cannot be externally pinned/verified, required human authority cannot be checked, or critical claims cannot be safely locked.
- If a schema migration fails, preserve old records and mark migration BLOCKED; do not fabricate default refs/hashes.
- For concurrent source changes, reread latest baseline and reconcile; never overwrite stale SHA.

---

## 12. Recommendation and disposition register

| ID | Origin | Target change | Disposition | Acceptance evidence |
|---|---|---|---|---|
| REC-001 | FND-001 | External root registry, identity/role validation, revocation and scope/quorum | NEEDS_DECISION for institutional trust source and quorum policy; technical design ready | TST-001–004 |
| REC-002 | FND-002 | Live multilingual prompt firewall + quarantine and execution-boundary re-scan | AUTO_APPLY design; implementation must pass security review | TST-005–008 |
| REC-003 | FND-003 | Source snapshot/hash/quote and claim-support mapping + human clinical review | AUTO_APPLY design; clinical criteria require qualified owner | TST-009–011 |
| REC-004 | FND-004 | One canonical registry/evaluator with legacy aliases | NEEDS_DECISION for compatibility sunset | TST-016–017 |
| REC-005 | FND-005 | Full registry/runtime parity assertion | AUTO_APPLY | TST-016 |
| REC-006 | FND-006 | Independent reference closure and graph property tests | AUTO_APPLY | TST-012–013 |
| REC-007 | FND-007 | Route-specific resource budget and fail-closed status | NEEDS_DECISION for organizational hard ceilings; schema design ready | TST-014–015 |
| REC-008 | FND-008 | Domain runbooks for S02/S03/S04/S05/S06/S07/S13 | AUTO_APPLY, additive only | TST-024–037 |
| REC-009 | FND-009 | Explicit duration basis/provenance/profile policy | AUTO_APPLY, exact default profile values require project owner | TST-032–033 |
| REC-010 | S10 scope | Formalize two-lane interface under same S10 identity | AUTO_APPLY design; confirm editorial owner for adaptations | TST-021, TST-038–041 |
| REC-011 | Handoff gap | One universal handoff JSON Schema + semantic validator | AUTO_APPLY | TST-018–023 |

---

## 13. Target Definition of Done

Target Architecture V2 is **design-complete** when:
- S10 lane boundaries and interface are explicit;
- S02/S03/S04/S05/S06/S07/S13 runbooks define domain-specific operations and negative cases;
- one universal handoff schema is valid against Draft 2020-12 and is referenced by a semantic validator contract;
- FND-001–FND-009 each have target control, owner, disposition and acceptance test;
- dependency/feedback/invalidation routes are explicit;
- current gate IDs and skill identity compatibility are preserved;
- implementation sequence and stop/rollback rules are defined.

Target Architecture V2 is **implementation-ready** only after:
- human decisions on external trust authority, role provisioning, quorum policy and resource ceilings are resolved;
- test fixtures and reference oracles are implemented;
- all required schema/semantic/security/compatibility tests pass on the exact target branch/commit;
- changes are read back and complete diff reviewed.

Target Architecture V2 is **production-ready** only after:
- applicable dynamic workflow tests pass in the actual host/runtime;
- renderer and actual media verification are observed;
- S12 independent QA is complete at the relevant level;
- clinical/institutional/legal/rights/privacy/brand/accessibility approvals are valid and hash-bound;
- human release authority explicitly approves publication.

### Final status of this deliverable

**ARCHITECTURE DESIGNED · LOCAL IMPLEMENTATION OVERLAY CREATED · 44/44 ACCEPTANCE CASES PASS · 162/162 FULL REPOSITORY TESTS PASS.** The overlay adds executable deterministic enforcement helpers, schemas, skill references, test cases and CI configuration to a working copy of the uploaded repository. Existing public skill IDs, names, paths, frontmatter descriptions/triggers and plugin versions remain unchanged. The original uploaded archive remains untouched.

This is not yet a GitHub commit/PR or live Plugin Creator installation. GitHub CI has not run. Live ChatGPT host invocation, real issuer/clinician identity validation, clinical review, provider AI/ASR/TTS, Remotion installation/build/render, actual MP4 inspection, human rights/legal/privacy/brand/accessibility approvals and publication release remain `NOT_RUN`, `NOT_VERIFIED` or `BLOCKED` as appropriate. A local deterministic PASS is not a production-release PASS.
