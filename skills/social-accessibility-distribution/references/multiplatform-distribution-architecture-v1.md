# S11 Multiplatform Distribution Architecture V1

Status: design and implementation contract for S11  
Evidence checked: 17 November 2026  
Owner: S11 Social Accessibility & Distribution  
Orchestrator: M00  
Independent QA: S12  
Context/change preflight: S14  
Scope: Instagram, Facebook, TikTok and YouTube

## 1. Design intent

The Instagram Agent Skill is a feature catalogue, not an architecture to copy wholesale. Its capabilities are translated into the health-first Promkes production model. Some capabilities are reused from the existing engine, some extend existing Promkes foundations, and some are designed as new S11 procedures.

The design deliberately avoids claiming access to private platform ranking weights. It models observable discovery surfaces, published signal families, creator-facing guidance, eligibility constraints and account analytics. Platform rules and product surfaces change; every external observation must have a source, date, scope and confidence.

## 2. Classification of the 18 Instagram Agent capabilities

Classification describes the baseline Promkes capability and the implementation decision. ADOPTABLE means reuse an existing Promkes-native contract rather than importing Instagram code. PARTIAL means the core idea exists but lacks the Instagram-specific operating procedure, structured rubric, metrics or tooling. ABSENT means no dedicated equivalent was found in the inspected Promkes S11 package and architecture.

| ID | Instagram Agent capability | Class | Promkes baseline | Adaptation decision |
|---|---|---|---|---|
| IG-01 | Hook Formula Library | PARTIAL | S03/S04 already select audience-fit hooks and narrative approaches; no governed 26-formula catalogue | Extend with a source/claim-safe formula ledger, use cases, anti-patterns and objective tags |
| IG-02 | Hook Scoring Engine | ABSENT | No dedicated hook quality rubric or scoring utility | Build a non-predictive editorial rubric with hard safety vetoes before any score |
| IG-03 | Spoken vs on-screen hook pair | PARTIAL | S04 separates dialogue/VO and S11 can create overlays; no pair-level semantic check | Extend with paired wording, meaning consistency and reading/speech timing checks |
| IG-04 | Timed Reel beat sheet | ADOPTABLE | Promkes already has native beat-sheet schema, validator and source-to-beat/scene/motion trace | Reuse that contract; add social retention intent, surface and CTA notes without replacing beat or motion truth |
| IG-05 | Caption Linter | ABSENT | S11 writes captions but has no deterministic platform-profile linter | Build a profile-aware linter for opening clarity, topic terms, CTA, length guidance, tags, emoji, links and accessibility |
| IG-06 | Carousel Builder | PARTIAL | Visual/infographic and S11 content foundations exist; no dedicated Instagram carousel sequence workflow | Extend into cover, card sequence, one idea per card, claim trace, accessible copy and save/share utility |
| IG-07 | Instagram Story Planner | ABSENT | No Story-specific sequence/sticker/funnel contract | Build privacy-safe frame planner with polls/questions/quizzes, response moderation and CTA options |
| IG-08 | Profile Auditor | ABSENT | No dedicated social profile rubric | Build institutional profile audit for identity, service purpose, bio, contact path, highlights, pinned information and accessibility |
| IG-09 | Weekly Content Planner | ABSENT | S03 plans campaigns, not an account-operating calendar | Build capacity-aware editorial calendar linked to campaigns, service hours and review lead time |
| IG-10 | Comment Strategy | ABSENT | No dedicated outbound comment playbook | Build useful, contextual and authorized comment patterns; prohibit spam and engagement bait |
| IG-11 | Comment Reply Triage | ABSENT | No dedicated six-way response and escalation workflow | Build triage for information, questions, misinformation, complaints, personal data and urgent matters |
| IG-12 | DM Conversation Engine | ABSENT | No dedicated consent-aware DM workflow | Build user-initiated/opt-in response drafts, minimum-data rules, human escalation and no-diagnosis boundary |
| IG-13 | Competitor Content Intelligence | PARTIAL | Research and supplied analytics can inform campaign analysis; no social sampling/benchmark protocol | Extend to authorized manual public sampling, comparable cohorts, median/outlier review and anti-copy rules |
| IG-14 | Instagram Performance Auditor | PARTIAL | S11 can interpret supplied analytics and V4 outcome governance supports process metrics; no Instagram-specific metric map | Extend with surface-specific ratios, denominator/window controls and reach-versus-service outcome separation |
| IG-15 | Content Repurposing | PARTIAL | S01 ingests sources; S04/S11 create downstream assets; no social repurpose compiler | Extend with claim-preserving extraction and independent native format adaptation |
| IG-16 | Humanizer & Style Detector | ABSENT | S04/S11 voice guidance exists but no social language-quality tool | Build conservative language review with protected terms, units, Unicode and visible edit diffs |
| IG-17 | Creator Voice Profile | PARTIAL | Narrative, visual and voice Guides cover production canon; no social writer profile across captions/comments/DM drafts | Extend a scoped institutional communication voice profile; keep separate from GUIDE-04/05 ownership |
| IG-18 | Social Activity Log | PARTIAL | MCG and process outcome register exist; no privacy-minimized social content ledger | Extend with post IDs, formula/version, approved metrics, learning and retention/access controls |

### 2.1 Classification decision rules

- ADOPTABLE is not “ready-made Instagram functionality”. It means an existing Promkes contract is the canonical implementation base and should not be duplicated.
- PARTIAL never means that the existing skill automatically performs the entire Instagram feature. Only the named foundation is present.
- ABSENT is limited to the inspected S11 package and architecture; it is not a claim about every private or uninspected runtime.
- The 18-item inventory is Instagram-derived. Facebook, TikTok and YouTube require extra platform-native procedures, not a copy of this matrix.

## 3. Target S11 architecture

S11 remains one skill with five internal lanes:

| Lane | Responsibility | Core procedures |
|---|---|---|
| S11-A Editorial Intelligence | Editorial quality and social packaging | Hook library, hook review, spoken/on-screen pair, beat overlay, caption linter, voice application |
| S11-B Format Engineering | Format and accessibility by surface | Reels, feed, carousel, story, Facebook Page/Group, TikTok video/LIVE, YouTube long-form/Shorts/Live/Community |
| S11-C Platform Intelligence & Planning | Platform-aware account planning and analytics | Profile audit, calendar, authorized competitor review, performance audit, source drift observations |
| S11-D Community & Service Interaction | Safe human communication | Comment patterns, reply triage, DM draft, moderation and escalation |
| S11-E Repurposing & Learning | Evidence-safe derivatives and learning | Repurposing, language quality, voice profile, privacy-minimized ledger |

M00 remains the only orchestrator. No S15, no parallel autonomous platform agents, no new publication gate and no automatic cross-post engine are introduced.

## 4. Platform-specific discovery and packaging models

### 4.1 Instagram

Treat Instagram as distinct surfaces, not a single feed:

- **Feed:** relationship and prior interaction context plus post information and predicted viewer actions. Meta's public Feed System Card describes candidate sourcing, filtering, action prediction, integrity demotion and diversity controls; the card is explicitly last updated 23 February 2022 and must be treated as historical system documentation, not a current complete specification.
- **Reels:** short-form discovery and viewing. Use creator-facing guidance such as average watch time, likes per reach and sends per reach as diagnostic measures, not fixed weights or guarantees. The January 2025 Mosseri guidance is reported by a secondary industry publication and is surface-dependent.
- **Stories:** relationship and repeat audience context; sequence clarity, completion, replies and sticker response are useful content diagnostics. Do not imply that any one metric is a public ranking formula.
- **Explore and Search:** topic relevance and discovery intent; use clear subject language, accurate caption/context and relevant descriptors, not irrelevant hashtag stuffing.
- **Carousel:** educational sequence and save/share utility; one core idea per card, cited evidence for factual cards, readable text and a useful end card.
- **Profile and DMs:** institutional trust, service clarity and response boundaries. A profile audit is not a commercial conversion score.

Promkes adaptation: build one selected surface package at a time. A Reels version may use a short opening, early context, clear beats, legible overlays and a loop only where it does not distort meaning. A carousel needs a linear educational progression. A Story needs frame-level CTA and privacy-safe interactive prompts. Feed copy must stand alone and preserve source details.

Primary diagnostics when the account dashboard exposes them: average watch time, reach, plays/views, likes per reach, sends/shares per reach, saves per reach, follower/non-follower reach, profile actions, Story completion/exits/replies and carousel interactions. Record exact field names as shown in the dashboard; do not infer missing fields.

### 4.2 Facebook

Separate surfaces and social context:

- **Feed / Home:** personalized discovery and relevance. Meta announced in October 2026 that its “Your Algorithm” and feedback tools let people express interests in their own words for Feed and Reels. This is a viewer-side personalization feature; it is not a recipe for creator reach.
- **Feeds / followed connections:** distinguish discovery from content from Pages, friends and followed sources where the current product exposes that distinction.
- **Reels:** original contribution matters. Meta's March 2026 guidance says creator-produced material and substantial new information, analysis or storyline can qualify as original; minor edits, copied uploads or reactions that add no meaningful value can be deprioritized.
- **Pages:** official identity, service information, trust, accessible updates and clear public-service contact paths.
- **Groups:** useful community context and locally relevant discussion only where the Group rules and institutional role permit it. Do not treat Groups as a route to unsolicited promotion.

Promkes adaptation: emphasize locally useful explanation, original institutional contribution, clear source attribution, readable visuals, meaningful discussion and service information. Avoid repeated promotional cross-posting, comment bait, spam, engagement farming and content flooding. When repurposing third-party footage, confirm rights and add substantial, truthful explanation; never claim a superficial edit makes it original.

Primary diagnostics when available: reach, engaged distribution by surface, meaningful shares/comments, video retention/watch time, original-content performance, Page follows/actions, link clicks and Group conversation quality. Do not equate high comment volume with trust or health impact.

### 4.3 TikTok

Separate recommendation surfaces:

- **For You:** TikTok documents three major signal groups: user interactions, content information and user information. Interactions can include full watches/skips and watch time; content information can include sounds, hashtags, views and publication country; user information can include language, location, time zone, day and device. TikTok says the relative importance can change and varies by recommender system.
- **Following and Friends:** personalized relationship feeds; use them to understand follower/community context, not to assume For You behavior.
- **Search:** query match is especially relevant to Search ranking. Use a precise question/topic phrase, accurate caption and relevant hashtags/sound; never stuff keywords or mislabel content.
- **LIVE:** a distinct live interaction surface with its own moderation, safety and staffing requirements. Do not recommend LIVE when real-time professional moderation is unavailable.
- **Eligibility:** content may be permitted on TikTok but not eligible for For You recommendation. Recommendation eligibility is a hard preflight, separate from editorial quality or account engagement.

Promkes adaptation: make the subject understandable immediately, use a spoken/on-screen topic phrase that matches the actual question, keep each video focused, and ensure captions/overlays support comprehension. A search-friendly video should answer the query honestly rather than create an exaggerated curiosity gap. Creator Search Insights may be used only if the feature is available to that account/region and its current dashboard evidence is supplied.

Primary diagnostics when available: average watch time, full-watch/completion, viewed-versus-skipped behavior if exposed, rewatch, shares, saves/favorites, comments, follows, search queries and traffic source, plus any For You eligibility notice. Do not optimize retention by hiding a health answer, delaying urgent safety information or adding fear.

### 4.4 YouTube

Separate discovery systems and format intent:

- **Home:** personalized viewer discovery informed by watch history and satisfaction.
- **Suggested / Up Next:** topic and viewing-session relevance, including what viewers watch together.
- **Search:** query relevance and viewer satisfaction; title/description should accurately answer a search intent, not merely chase keywords.
- **Shorts:** a short-form discovery experience personalized by viewer history and content performance. Read Shorts-specific Studio fields separately from long-form metrics.
- **Subscriptions, Live and Community:** distinct relationship and notification paths; not interchangeable with Home/Search discovery.

YouTube's public guidance describes a goal of matching viewers to videos they are likely to watch and enjoy, with average view duration, average percentage viewed, likes and post-watch survey signals among performance considerations; topic interest, competition and seasonality also affect exposure. Its guidance does not identify a universally preferred video format and cautions against reducing performance to a single CTR number.

Promkes adaptation: package a clear viewer promise in title/thumbnail, answer the promised question early, structure chapters/sections for long-form, use playlists/series and end screens where useful, and create Shorts as complete, accurate micro-lessons rather than cut fragments that lose caveats. Use a sustainable cadence based on capacity and quality rather than forced volume.

Primary diagnostics when available: impressions and CTR in context, views from impressions, average view duration, average percentage viewed, watch time, audience retention, returning/unique viewers, traffic sources and Search terms. For Shorts, use Shorts-specific engaged-view and viewed/swiped fields only when the current Studio report exposes them. CTR without impressions/source/context is incomplete; no one metric is the whole system.

## 5. Shared S11 production contract

The shared sequence is:

**S01 source/provenance → S02 Fact Lock → S03 audience/objective/message/CTA → S04 canonical narrative where relevant → S11 platform/surface adapter → S12 independent QA → human institutional/publication authorization.**

When no video production is requested, S04 is invoked only where narrative or voice continuity is needed. S11 is optional downstream work; it must not turn every production into a social content calendar.

Each platform output is independent and records:
- project/source IDs and content version;
- S02 claim refs/status, and no unapproved claim;
- S03 objective/audience/key message/CTA;
- platform, surface, format and version of the playbook used;
- hook mode and spoken/on-screen pair where applicable;
- caption/title/script, search descriptors, hashtags only when useful, subtitles/captions, alt text and accessibility details;
- rights, consent, voice profile and human-review states;
- metrics available, numerator/denominator, observation window, cohort and missingness;
- platform sources and checked date;
- open defects, S12 disposition and publication authority state.

A multi-platform job creates four different output packages. It does not duplicate a single caption four times and rename the platform.

## 6. Editorial tools and rules

### 6.1 Hook library and quality review

The Hook Library is a governed set of objective-labelled patterns, not a formula that forces clickbait. Example pattern families include question-to-answer, common misconception, practical problem-to-action, myth-versus-fact, local service reminder, evidence reveal, human story and checklist. Every pattern has purpose, audience fit, safe example, anti-pattern, claim dependencies and platform surfaces where it may fit.

The hook review rubric can score clarity, specificity, audience relevance, truthful curiosity and next-step fit on an internal scale. Scores guide revision only. They are not trained platform predictions and must never be described as an estimate of views or virality.

Non-compensatory hard veto: unsupported health claim; exaggerated severity/probability; misleading promise; stigma; deceptive omission; prohibited personal information; unsafe or unauthorized CTA. A high creative score cannot offset a failed safety gate.

### 6.2 Spoken/on-screen pair

Store VO/spoken wording and overlay wording separately. They may complement one another but must not contradict, imply a stronger medical claim or make a qualifier unreadable. Check speech duration, reading time, subtitle accuracy, mobile safe areas and screen-reader/alt-text meaning.

### 6.3 Social beat overlay

Reuse the Promkes beat-sheet schema and semantic validator. S11 may add platform surface, hook purpose, retention question, viewer payoff and CTA placement annotations. It cannot change the underlying source timing, S06 shot design, S07 motion values, S09 audio timing or S13 scene continuity. Estimated timings remain estimates. Do not force a loop when a natural ending or safety message is more appropriate.

### 6.4 Caption linter

Lint by platform and surface profile version. Checks include opening clarity, factual trace, audience language, length guidance, key topic, CTA clarity, unnecessary tags/emoji/links, accessibility and duplication. Profile limits must be dated and source-backed; where a platform limit or current field is unknown, return NOT_CHECKED rather than invent a threshold. Linter outcomes: FAIL for truth/privacy/rights violation, WARN for quality/compatibility issue, PASS only for checks actually executed.

## 7. Account operations and community procedures

- **Profile audit:** identity and institutional legitimacy; purpose; bio clarity; contact/service path; pinned/featured service information; accessibility; currentness; consent/brand consistency. It is not a conversion-funnel score.
- **Editorial calendar:** built from campaign sequence, public-service calendar, staff capacity, review lead time, asset readiness and audience need. A posting frequency is selected from measured capacity, not imported as a universal rule.
- **Competitor review:** manual review of public, authorized samples. Separate median-view comparisons from follower-based ratios; do not mix denominators. Use themes and formats as learning, not copy. Avoid collecting private data or scraping.
- **Comment patterns:** explain, cite, thank, correct, clarify and route. No repetitive spam, fake agreement or engagement bait.
- **Reply triage:** classify routine public question, substantive request, misinformation, complaint, personal/sensitive disclosure, and urgent/safety-critical request. Sensitive or urgent categories are not handled with an automated public reply.
- **DM workflow:** reply to user-initiated contact or explicitly consented/authorized keyword workflows only. Give approved general information, direct to official verified channels, minimize data and escalate. Never diagnose or solicit clinical details.
- **Learning ledger:** store content IDs, source/formula/version, platform surface, approved aggregate analytics, review notes and action. Apply access control, retention and deletion policy. Never log private message content, handles, patient data or sensitive health disclosures unless a lawful, approved system requires it; this social ledger does not need them.

## 8. Repurposing and language integrity

Repurpose approved source material by extracting its core question, claim IDs, evidence, useful explanation, action, quote and limitations. Rebuild the sequence for each platform instead of simply clipping or trimming. Retain provenance and attribution. Third-party source reuse requires rights and meaningful transformation consistent with the platform's current rules.

Language review must preserve medical terms, numbers, dates, names, units, official service details, local script, punctuation that changes meaning and Unicode joiners/combining marks. Show edits or a before/after diff for material changes. Do not run a blanket Unicode Cf deletion. A style detector is heuristic; it cannot reliably identify AI authorship or prove human authorship.

## 9. Evaluation, privacy and risk

Separate at least four measurement layers:
1. **Distribution:** impressions, reach, recommendation surface and traffic source.
2. **Viewer response:** watch duration/completion, saves, shares, comments, satisfaction signals and follows where available.
3. **Service action:** verified link click, contact path, event/service inquiry or other permitted objective measure.
4. **Public-health outcome:** only a separately designed, ethical and authorized evaluation with validated measures; never infer from platform engagement alone.

For every metric record source, date, field definition, numerator, denominator, cohort, format, time window, missingness and limitation. Compare like with like; do not use a universal benchmark without a defensible reference population.

Privacy risks require minimum-data design. Story polls must ask general knowledge or content-preference questions, not personal diagnoses or symptoms. DM and comment triage must direct personal disclosures to verified, approved channels and avoid repeating personal data publicly. Store aggregate analytics only where possible.

Worst credible failures include: an algorithm-optimized hook making a false health claim; a Story sticker collecting identifiable patient information; a DM response mistaken for a clinical consultation; copied Reels deprioritized or infringing rights; cross-posting a caveat-free video; mixed-denominator competitor analysis leading to false decisions; and a high-engagement post being misreported as improved health behavior. Controls are fact locks, surface-specific lint, hard privacy veto, rights review, S12 QA, human authorization and metric separation.

## 10. Platform evidence register

Checked 17 November 2026. These references support the signal families and policy observations stated above; they are not ranking source code, guaranteed growth tactics or permanent specifications.

| Platform | Public evidence | Use and limitation |
|---|---|---|
| Instagram | Meta AI, Instagram Feed Ranking System Card: https://ai.meta.com/tools/system-cards/instagram-feed-ranking/ | Feed-only card; last updated 23 February 2022. Historical system transparency reference, not a complete current specification for Stories, Explore, Reels or Search. |
| Instagram | Social Media Today, 22 January 2025 report on Adam Mosseri creator guidance: https://www.socialmediatoday.com/news/instagram-shares-algorithm-insights-2025/738034/ | Secondary report of watch time, likes and sends as top creator-facing metrics; surface-specific variance is noted; no exact weights are disclosed. |
| Facebook | Meta, Rewarding Original Creators on Facebook, 13 March 2026: https://about.fb.com/news/2026/03/rewarding-original-creators-on-facebook/ | Official originality guidance for Feed/Reels; check current rules before reuse. |
| Facebook | Meta, Your Algorithm, Your Words, 13 October 2026: https://about.fb.com/news/2026/10/introducing-your-algorithm-facebook/ | Official announcement of viewer interest controls for Feed/Reels; not a creator ranking formula. |
| Facebook | Meta, Cracking Down on Spammy Content on Facebook, 24 April 2025 (updated 22 October 2025): https://about.fb.com/news/2025/04/cracking-down-on-spammy-content-facebook/ | Official anti-spam policy context; check latest policy before publication. |
| TikTok | TikTok Help Center, How TikTok recommends content: https://support.tiktok.com/id/using-tiktok/exploring-videos/how-tiktok-recommends-content | Official signal groups, surfaces and eligibility concepts; relative importance can change and differs by system. |
| TikTok | TikTok Newsroom, Creator Search Insights: https://newsroom.tiktok.com/en-us/creator-search-insights | Feature announcement; availability may differ by account/region and must be checked in the live product. |
| YouTube | YouTube Help, Search & discovery tips — Video: https://support.google.com/youtube/answer/11914225?hl=en | Official creator guidance on personalization, performance, average view duration, average percentage viewed, topic interest, competition and seasonality. |
| YouTube | YouTube Help, How YouTube recommendations work: https://support.google.com/youtube/answer/16089387?hl=en | Official viewer-signal overview; different surfaces/personalization paths must remain separate. |
| YouTube | YouTube Help, Search & discovery tips — Shorts: https://support.google.com/youtube/answer/11914225?co=YOUTUBE._YTVideoType%3Dshorts&hl=en | Shorts-specific guidance; use current Studio fields and don't transfer long-form benchmarks blindly. |

## 11. Change governance and completion criteria

External platform-document observations are immutable dated snapshots. S11 may flag a changed or unavailable source; M00/S14 records the impact and the human-approved baseline decision. A failed fetch or missing data is not proof that the platform has not changed.

The initial implementation is a package/design candidate. Social acceptance cases remain NOT_RUN until their individual oracles and evidence are executed. Static tests do not prove model behavior, current platform compatibility, dashboard accuracy, content quality in a live account, actual posting, clinical correctness or public-health impact.

Completion requires:
- feature inventory retains all 18 Instagram-derived capabilities and their three classifications;
- no new S15 and no duplicate ownership;
- four platform adapters expose distinct surfaces, signal families, formats, metrics and safety checks;
- S02/S03/S04/S12/S13/S14 contracts remain intact;
- privacy/rights/originality/community controls are explicit;
- the new social acceptance suite is separate from the existing 45 AT + 13 REF + 18 V2 inventories;
- exact branch commit, PR metadata, CI and test evidence are reported independently;
- no main merge, public release or account publication without separate authorization.
