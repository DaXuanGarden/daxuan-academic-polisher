# Prior-art research

Research date: 2026-10-21. Sources were read from their public GitHub pages or raw files;
no candidate was executed. Repository stars and catalog installs are discovery signals, not
quality ratings.

| Category | Candidate | What was inspected | Useful idea | Boundary or rejection |
| --- | --- | --- | --- | --- |
| Direct | [nature-polishing](https://github.com/Yuan1z0825/nature-skills/tree/main/skills/nature-polishing) | `SKILL.md`, manifest and references | Route by section, venue and language; load guidance on demand | Its Nature-specific corpus and zh-to-en default do not fit same-language routing |
| Direct | [scientific-writing-editor](https://github.com/royurvieta/scientific-writing-editor) | `SKILL.md`, README, fidelity reference, check script | Scientific-fidelity priority, evidence ledger, minimal edits and alarm-style checks | English/Spanish only; semantic check still needs human reading |
| Direct Chinese | [Scientific-Writing-zh](https://github.com/YuanZHAO321/Scientific-Writing-zh) | `SKILL.md`, README and reference tree | Document → paragraph → sentence → word editing funnel; progressive disclosure | Broader lifecycle scope includes drafting/review; retain only the editing funnel |
| Craft | [scientific-writing-skills](https://github.com/dvdsosa/scientific-writing-skills) | README, `sciwrite-prose`, audit scripts | Structure/upshot before sentence edits; explainable candidates rather than verdicts | English-centered rules; do not copy its passive/keyword defaults into Chinese |
| Craft | [skill-deslop](https://github.com/stephenturner/skill-deslop) | `SKILL.md`, references and examples | Progressive anti-pattern references and explicit Methods passive boundary | General anti-AI trigger and rubric are too broad for a conservative scientific editor |
| Adjacent orchestration | [academic-writing-agents](https://github.com/andrehuang/academic-writing-agents) | academic skill and prose-polisher agent | Diagnose before edit; keep findings for incremental review | Twelve-agent/Claude-specific orchestration adds friction and was not adopted |
| Adjacent critical writing | [humanmade-antislop](https://github.com/machinemade-mm/humanmade-antislop) | root skill and writing principles | Claim calibration, causal boundary, facts over praise | Absolute word/mark rules can harm technical and Chinese prose |
| Adjacent review | [deer-flow academic-paper-review](https://github.com/bytedance/deer-flow/tree/main/skills/public/academic-paper-review) | public review skill | Keep evidence assessment separate from language editing | Review verdicts are outside this skill's trigger and output |
| Adjacent pipeline | [academic-research-skills](https://github.com/Imbad0202/academic-research-skills/tree/main/academic-paper) | root skill and quality reference | Contextual quality prompts and explicit boundaries | Multi-agent pipeline and unclear reuse license were not copied |

## Decision

The niche is real: authors routinely need a conservative language pass in Chinese or English,
and the most damaging failure is silent evidence drift. The existing package already had the
right core contract, but its first evidence layer was weak: routing counted technical IDs as
English, preservation missed units and additions, and fixtures implied unsupported deletion.
The improved package keeps a small root entrypoint, separates language/section references,
adds deterministic routing and protected-token regressions, and labels authored fixtures as
non-model evidence.

## Open evidence

Provider-backed runs, blind human preference, semantic equivalence, and journal-specific
compliance remain unverified. Those gaps are recorded as watch items rather than converted to
quality claims.
