# Creation handoff

- Skill: `daxuan-academic-polisher` 0.2.0
- Job: polish existing Chinese or English academic prose in its detected source language
  while preserving evidence, claims, terminology, voice, and structure.
- Local package: `skills/daxuan-academic-polisher/`
- Intended publication: standalone `DaXuanGarden/daxuan-academic-polisher` repository.

## Chosen direction

Luban's three directions were evaluated:

- **A — small fix:** rename and repair metadata only. Too small; it would leave the detector,
  preservation checker, and misleading fixtures unchanged.
- **B — verified output:** rename, repair the two high-risk scripts, add self-contained
  regression cases, portable documentation, and an authored showcase. **Chosen.**
- **C — suite:** split language, section, citation, and journal-specific skills. Deferred;
  it would widen the trigger surface and require model/human evidence not available here.

## What changed from 0.1.0

- Renamed the user-facing skill and package to `daxuan-academic-polisher`; ownership is Daxuan.
- Preserved source-language routing and made mixed prose use the dominant language with local
  handling for quoted terms.
- Replaced broad language counts with masked technical-token detection and `und`/`mixed`
  uncertainty states.
- Rebuilt protected-token extraction for values, signs, units, ranges, statistics, citations,
  figure/table references, DOI/PMID and common identifiers; additions are reported as well as
  omissions.
- Added an optional style-anchor reference and restored useful Chinese/English section rules.
- Corrected fixtures so polish output retains facts and includes a body before notes.
- Added portable validation, routing/preservation regressions, CI metadata, examples and a
  fixture-only SVG workflow showcase.

## Verification boundary

The package has deterministic local checks and an install smoke test. The showcase is an
`authored_fixture` with `model_run: false`; no provider-backed quality or blind human review
is claimed.
