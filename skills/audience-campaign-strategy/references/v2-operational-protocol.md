# S03 V2 Operational Protocol — Audience & Campaign Strategy

## Ownership and boundary
S03 owns audience framing, behavior objective, barrier/benefit analysis, key message, behavioral proposition, primary CTA and campaign strategy. S03 does not own clinical truth (S02), screenplay wording (S04), official demographic facts without evidence, or publication permissions.

## Procedure
1. Parse the campaign brief into explicit requirements, assumptions, proposals and non-goals.
2. Identify the audience using source-backed attributes only. Record geography, age, occupation, language, access and vulnerability as `EVIDENCED`, `USER_PROVIDED`, `ASSUMED` or `UNKNOWN`.
3. Define one primary behavior objective, one key message and one primary CTA. Secondary objectives are permitted only when their priority and relationship are explicit.
4. Map audience insight → barrier → motivation → message → behavior → CTA. Each transition must be internally consistent.
5. Check every factual health proposition against S02 claim IDs; strategy cannot introduce clinical facts.
6. Evaluate cultural/local language. Local dialect is optional, brief-grounded and reviewed for clarity; unsupported demographic generalizations must be removed or marked as assumptions.
7. Create a campaign blueprint with success indicators separated into communication outputs, audience outcomes and long-term impact.

## Decision rules
- Exactly one `PRIMARY` objective and one `PRIMARY` CTA by default.
- The CTA must implement the objective's `behavior_id`; mismatches are `CONFLICTED` and routed to M00/user.
- Multiple primary CTAs require a documented brief justification and a hierarchy; no silent accumulation.
- Local behavior, dialect or demographic claims without evidence are `ASSUMPTION` or omitted.
- Reach, virality, FYP, engagement or algorithmic performance are aspirations, never guarantees.

## Negative cases
Competing objectives; CTAs that prompt a different behavior; audience segment inferred from a place name alone; dialect that narrows comprehension; fear-based persuasion; engagement metric replacing health objective; and unsupported behavioral causal claims.

## Output contract
`Campaign Strategy Blueprint`: audience register, evidence basis, behavior model, barriers/motivators, objective tree, key message, primary/secondary CTA map, channel assumptions, risk and exclusion review, measurement plan, unknowns, S02 refs and handoff acceptance checks.

## Acceptance
The next stage can identify exactly whom the campaign addresses, what behavior should change, why the message is relevant, and what action is requested—without mistaking assumptions or engagement aspirations for verified facts.
