# S02 V2 Operational Protocol — Health Evidence & Safety

## Ownership and boundary
S02 is the sole skill owner of the Health Truth Registry, atomic health-claim records, evidence applicability assessment, terminology safety, plain-language simplification review, misinformation screening and health fact locks. S02 does not confer professional credentials on the model and cannot replace a licensed clinician or institutionally authorized reviewer. The human clinician is the final approver for material clinical claims.

## Seven micro-module procedures

| Micro-module | Required procedure | Output |
|---|---|---|
| Health Claim Extractor | Extract every material proposition from poster, caption, script, VO transcript and overlays; split compound sentences; preserve original wording and provenance | Atomic claim records with stable `claim_id` |
| Medical Evidence Verifier | Resolve source snapshot; validate source bytes/hash, authority, publication date, jurisdiction, population, applicability, quote and counterevidence | Claim–Evidence Matrix and provenance result |
| Health Terminology Validator | Check clinical term meaning, ambiguity, stigma, scope, units, numerators/denominators and population wording | Terminology findings and approved alternatives |
| Health Literacy Simplifier | Rewrite only after source wording is locked; preserve negation, modality, uncertainty, population, causal strength and instructions | Simplified wording + semantic-delta check |
| Medical Misinformation Detector | Flag unsupported, contradicted, exaggerated, causal, guaranteed, outdated and context-shifted statements | Risk and contradiction register |
| Health Ethics & Safety Controller | Inspect stigma, blame, fear, privacy, vulnerable audience, harmful advice and misuse | Ethics disposition and escalation |
| Fact Lock Manager | Lock only source-supported and human-approved claims; assign version/hash; invalidate dependents on change | Health Truth Registry and lock events |

## Decision procedure
1. Create one record per proposition; use stable IDs and retain the exact source string.
2. Classify the statement as `OBSERVED`, `USER_PROVIDED`, `SOURCE_CLAIM`, `VERIFIED_SOURCE`, `INFERENCE`, `CREATIVE`, or `UNKNOWN`.
3. Verify actual source bytes and provenance. A URL, title, citation, formatted hash, or `VERIFIED` label is not proof that source bytes were inspected.
4. Record exact supporting quote and its page/section/paragraph/locator. Test numbers, units, polarity, population, date, jurisdiction and counterevidence.
5. Apply conservative semantic screening. Lexical support is only a pre-screen; it cannot issue clinical truth.
6. Route material claims to the authorized human reviewer. Record person/role, authority evidence, decision, scope, timestamp and artifact hashes through the external trust workflow.
7. Only then can wording be locked. A model-generated status cannot self-authorize approval.

## Status and stop rules
- `VERIFIED_SOURCE`: source bytes and provenance verified; this is not yet a clinically approved claim.
- `SUPPORTED_LEXICALLY`: machine pre-screen found quote/number/word overlap; never synonymous with `CLINICALLY_APPROVED`.
- `PENDING_HUMAN_APPROVAL`: evidence review complete but human clinical approval absent.
- `UNVERIFIED`, `CONTRADICTED`, `STALE`, `MIXED_OR_CONTESTED`, `UNKNOWN`: cannot authorize production wording.
- `HOLD`: use for material conflict, missing authority, context mismatch or unsupported high-consequence claim.

## Negative and boundary cases
Missing/inaccessible snapshot, hash mismatch, source date/jurisdiction/population mismatch, absent quote, unsupported statistic, negation reversal, correlation-to-causation strengthening, guarantee/cure wording, paraphrase that broadens population, and a metaphor that creates a health proposition all require `UNVERIFIED`, `HUMAN_REVIEW`, or `HOLD`—never a silent PASS.

## Required handoff
Include claim IDs, exact quotes, source snapshot refs/hash, context, support status, counterevidence, approved and forbidden wording, human approval reference (when present), inherited immutable constraints, dependent artifacts and acceptance checks. The universal handoff envelope is mandatory.

## Acceptance
A recipient can reconstruct why every material statement is permitted, limited, held or rejected. No factual claim reaches S03/S04/S08/S10/S11 as approved solely because a semantic heuristic returned a match.
