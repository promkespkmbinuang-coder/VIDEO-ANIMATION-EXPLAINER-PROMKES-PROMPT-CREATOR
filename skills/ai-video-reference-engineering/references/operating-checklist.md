# S08 Operating Checklist — Prompt-to-Reference

- [ ] Output explicitly says `REFERENCE PACK`, not prompt-to-video.
- [ ] No prompt instructs a video model to render/animate a complete scene.
- [ ] Master style prompt follows S05 visual canon.
- [ ] Character/expression/pose references carry canonical IDs and MCG lock versions.
- [ ] Environment and prop references carry stable IDs.
- [ ] Scene references describe a still/keyframe/shot reference, not a moving clip.
- [ ] Motion/timing values remain in S07 reference data.
- [ ] Storyboard/framing ownership remains with S06.
- [ ] Exact factual text, date, logo, CTA and health copy remain separate overlay data.
- [ ] Prompt and generated/selected asset statuses are distinct.
- [ ] Renderer-neutral manifest maps scenes to reference asset IDs.
- [ ] No TSX, Remotion render command, or rendered file is claimed by default.
- [ ] Handoff identifies required downstream render implementation and open items.
