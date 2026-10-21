# Luban polish report — Daxuan Academic Polisher 0.2.0

> Review state: prepared for a GitHub branch/PR. A merge, tag, release, or registry publication is a separate gate.

## 1. Premise

The recurring need is credible: researchers want an editorial pass that improves clarity while
keeping the draft's language and evidence. The niche is differentiated by source-language
routing and conservative preservation, but a prompt alone cannot prove semantic fidelity.

## 2. Baseline frozen

The 0.1.0 package was copied to the local baseline archive before edits. Its deterministic
trigger smoke test passed 19/19, but the evidence was lexical only. The baseline score was
56/100: the router counted identifiers as English, the preservation script missed units and
additions, Skill IR workflow fields were empty, README commands used private paths, and one
fixture deleted a potentially meaningful experiment fact.

## 3. Peer evidence

Eight inspected projects cover direct polishing, Chinese writing, audit craft, orchestration,
and adjacent review. The strongest transferable ideas were a scientific-fidelity contract,
structure-before-sentence editing, progressive references, and alarm-style checks. Their URLs
and adoption decisions are recorded in [prior-art-research.md](prior-art-research.md).

## 4. Directions considered

A was metadata-only repair; B was a verified, portable single-skill output; C was a larger
suite of section, journal, citation, and review skills. B is the right first round because it
improves the observable contract without widening unsupported claims or trigger scope.

## 5. Changes made

The public name, frontmatter, adapters, manifest, license, README, examples, and Claude
metadata now use Daxuan branding. The root entrypoint has exact `Router Rules`, `Compact
Workflow`, and `Output Contract` headings so the IR exporter retains them. References add an
optional style anchor and richer Chinese/English/NSFC guidance. Fixtures retain source facts
and put the polish body before notes.

## 6. Failure modes addressed

The detector masks code, URLs, paths, citations, DOI/PMID, isolated IDs, and delimited math;
statistical prose around `p<0.001` remains visible. It reports `und`/`mixed` for uncertain
inputs. The preservation checker keeps signs, ranges, exponents, conservative units,
statistics, citations, figure/table references, DOI/PMID and identifiers, and reports both
missing/changed and unexpected/added tokens.

## 7. Reproducible outputs

`examples/` contains synthetic fixtures. `scripts/build_showcase.py` generated
`assets/showcase/polish-card.svg` and `assets/showcase/demo.gif`; `reports/showcase-evidence.json`
records `model_run: false`. The visual is a contract replay, not a provider-backed result.

## 8. Verification performed

The final local run passed `scripts/validate_package.py`, `scripts/run_regression.py` (7 routing
cases, protected fixture and negative drift), trigger evaluation (21/21), and Skill IR export
with populated workflow arrays. The meta-skill validator exited 0 with three lexical README
warnings about examples/verification/upstream wording; the content is present and the warnings
are recorded rather than hidden. The GitHub workflow repeats dependency-free package and
regression checks on supported Python versions. Remote `npx skills add` verification remains
pending until a public revision exists.

## 9. Nine-dimension score

| Dimension (weight) | Baseline | Candidate | Evidence |
| --- | ---: | ---: | --- |
| Frontmatter/trigger (7) | 5 | 7 | Rich bilingual description, positive and negative boundaries |
| Workflow (12) | 8 | 11 | Exact IR headings plus router/compact/output sections |
| Failure modes (12) | 6 | 11 | Technical-token and mixed/uncertain regressions |
| Checkpoints (6) | 3 | 6 | Self-contained validator, regression script, preservation alarm |
| Executable specificity (17) | 12 | 15 | References, mode contracts, style anchor, runnable scripts |
| Resource integration (4) | 2 | 4 | On-demand language/section/style references and examples |
| Architecture (12) | 8 | 11 | Root skill, adapters, plugin metadata, CI and reports |
| Observed performance (23) | 8 | 15 | Deterministic checks and fixture replay; no model/human score claimed |
| Counterexamples (7) | 4 | 6 | Technical-only, short, mixed, p-value and negative drift cases |
| **Total** | **56** | **86** | Evidence-bound estimate, not a language-quality rating |

## 10. Security and privacy

The skill treats attachments as data, requires an explicit request before writing a revised
file, makes no network call for polishing, and does not send external messages. Public
fixtures contain no private manuscript or patient data. The token checker reads local text
only.

## 11. GitHub publication plan

The current workspace was not a Git repository and the discovered `gwas-for-paper-skills`
repository is a narrowly scoped private GWAS controller. The aligned target is a new standalone
`DaXuanGarden/daxuan-academic-polisher` repository. The reviewable action is a feature branch
and pull request; the default branch, tag, release, and registry publication remain explicit
approval gates.

## 12. Known limits and watch list

No provider-backed polishing run, blind human preference study, semantic equivalence proof,
or editor-specific journal compliance has been run. Next observations should compare two real
models on the same synthetic and de-identified passages, measure false positives on tables and
references, and add a Chinese/English human review panel before changing maturity from beta.

## 13. Decision

The package is ready for a reviewable GitHub branch/PR after the final local checks. It is not
ready to claim model-quality superiority or a merged release. Keep the standalone scope and
revisit a suite split only when real usage shows that section- or journal-specific guidance
needs separate triggers.
