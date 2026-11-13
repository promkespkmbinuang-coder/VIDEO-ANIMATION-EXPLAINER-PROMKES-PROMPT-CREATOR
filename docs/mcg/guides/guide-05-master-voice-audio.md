# GUIDE-05 — Master Voice & Audio Guide

Sole primary owner: S09 voice-sound-design. Private package uses the equivalent S09 skill slug voice-audio-intelligence; this is a package alias, not a second canonical owner.

## Ownership boundary
Speaker/voice references, audio provenance, pronunciation, delivery, timing, sound identity, subtitle/audio cue relationships and audio constraints. Does not rewrite screenplay facts or clinical claims.

## Required instance fields
project_id, guide_id, guide_version, status, primary_owner, source_refs, speaker_refs, segment_refs, timing_provenance, canonical_decisions, assumptions, unknowns, dependencies, affected_scenes, approval_record_ids and change_history_ref.

## Adaptive continuity
Core speaker identity may be IMMUTABLE; approved delivery energy or pacing may be CONTROLLED_VARIATION; segment timing, emotion and audio cue state are SCENE_DEPENDENT. Transcription confidence and diarization remain evidence-bound.

## Approval and change
LOCKED requires human approval bound to the exact Guide hash/version/scope. Audio/transcript/source changes use CHG-ID and invalidate dependent VO timing, subtitles and scene synchronization.
