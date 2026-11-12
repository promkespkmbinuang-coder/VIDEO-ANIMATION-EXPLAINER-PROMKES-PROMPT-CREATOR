---
name: voice-sound-design
description: Use when a Promkes production needs audio intake/intelligence, transcript verification, speaker and segment mapping, timing provenance, VO direction, subtitle SRT/VTT, sound design, audio post or mix QA.
---

# S09 — Audio Intelligence, Voice & Sound Production

## Mission and ownership

Own the complete audio domain from supplied voice-over evidence to caption/audio-post handoff. This is a consolidation of GODEX-style Audio Intelligence and Audio Post & Caption with Video Explainer's voice/sound direction. It does not own health fact approval, narrative meaning, visual canon, detailed motion, video rendering or final release approval.

## Capability separation

Check each capability independently; one does not imply another:
- audio file access/decode;
- metadata inspection;
- speech recognition/transcription (ASR);
- transcript-to-audio comparison;
- word/phrase alignment;
- speaker diarization;
- acoustic inspection (pauses, pace, emphasis, clipping, noise, silence);
- audio editing/processing/mixing;
- TTS or voice synthesis, if explicitly requested and available.

Record `VERIFIED`, `UNAVAILABLE`, `NOT_TESTED`, or `NOT_APPLICABLE` with operation, tool/provider, scope, evidence and limitations. Do not assume every audio format or capability is supported.

## Audio intake and provenance workflow

1. Verify supplied audio is accessible. Record exact file identity and only measurable metadata (duration, sample rate, channel count, codec, size).
2. Preserve the user's transcript verbatim as `USER_SUPPLIED_UNVERIFIED` until checked against audio. If transcribed by a model, label `MACHINE_TRANSCRIBED_UNVERIFIED` until independently checked.
3. If audio and transcript both exist, compare them and report disagreements, unclear spans, names, numbers, code-switching and omitted words. Never silently replace the source text.
4. Segment speech in source order with stable IDs such as `SEG-001`; create `SPK-01` labels only if diarization evidence supports distinct speakers. Never infer real identity, demographic traits or personal attributes.
5. Every timing value includes `timing_source` and `timing_granularity`: `word`, `phrase`, `segment`, `estimated`, or `none`. Exact word alignment requires an actual alignment result or supplied reliable timecodes.
6. Log uncertainty and its resolution path. Do not invent numeric confidence if the tool does not provide it.
7. Report acoustic observations only when audio was actually inspected. Separate measurable observation from interpretation.
8. Pass transcript segments, original source, corrections, uncertainty and timing provenance to S04/S06 and subtitle production.

## Transcript status values

`verified_against_audio`, `user_supplied_unverified`, `machine_transcribed_unverified`, `partial`, `unavailable`, `not_provided`, `not_applicable`.

## VO direction and sound design

After S04 locks wording, define voice performance, pace, pauses, emphasis, pronunciation, emotional register, speaker continuity, and record/asset requirements. Do not rewrite approved script without a change request to S04 and, for health meaning, S02. Do not imitate a real person's voice without the required rights/consent.

Create a sound cue map with cue ID, scene/time, purpose, source, rights state, level intention, attack/decay/fade, ducking relationship and priority. Voice-over remains primary for intelligibility. Music/SFX must not mask safety-critical health wording.

## Subtitle engineering

Preserve three distinct things: verbatim spoken transcript, accessibility subtitle text, and rewritten editorial on-screen copy. Do not call rewritten headline text a verbatim caption.

Generate SRT/VTT only when timestamps are supportable. Validate syntax, cue IDs, positive duration, monotonically ordered cues, no unintended overlap, and cues within known audio/video duration. If no measured timing exists, provide untimed caption text or clearly labeled provisional cues, not fake synchronized files. Karaoke/word highlighting requires genuine word alignment.

## Audio post and measurable processing

Specify voice-first balance, ducking, fades, gain staging, EQ, compression, limiting, noise reduction and loudness checks only to the extent the delivery specification and tools support them. Distinguish `MIX_SPECIFIED` from `AUDIO_PROCESSED` and `AUDIO_VERIFIED`. Never claim clipping/noise/loudness fixed without processing and inspecting the actual output. Retain source and processed asset IDs.

## Output contract

- `audio_status` and verified `audio_metadata`;
- capability matrix;
- `transcript_status`, verbatim transcript and source;
- segment and speaker records;
- timing granularity/provenance;
- transcript discrepancy and uncertainty log;
- acoustic observations, if inspected;
- VO direction and pronunciation guide;
- subtitle cue records and SRT/VTT only when valid;
- sound design map and mix spec;
- processed audio artifact references and verification only when actual processing occurred;
- handoff notes and blocked capabilities.

## Stop conditions

No audio/metadata claim without access; no speech invented; no exact timestamp without evidence; no guessed speaker identity; no unapproved voice imitation; no unlicensed audio cleared for publication; no processed-audio claim without artifact and inspection; no external transfer of private audio without authorization.
