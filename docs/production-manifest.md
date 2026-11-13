# Production Manifest — V4.1.6 canonical continuity contract

The production manifest links one canonical MCG ID/version, exactly seven single-owner Guide refs and exactly three protocol refs. The MCG schema is at `schemas/v4/mcg-manifest.schema.json`; the DRAFT fixture is `docs/mcg/mcg-manifest.example.json`; semantic checks are in `scripts/validate_mcg_manifest.py`.

An affected scene cannot advance to S08 until S13 refreshes GUIDE-07 after storyboard and after S07 motion, S09 audio/time and S10 edit context are available. MCG stores S02-owned claim IDs, statuses, source/evidence refs and hashes only; it never duplicates or rewrites clinical facts. LOCKED Guide/lock records require an authorized human approval bound to exact artifact hash, version and scope.

Static schema/semantic checks do not prove external model capability, runtime, rights, consent, renderer execution, media QA or human approval.
