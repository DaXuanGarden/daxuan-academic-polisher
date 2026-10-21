# Examples and reproducible showcase

These examples are synthetic, authored fixtures designed to test the output contract. They
contain no private manuscript or patient data. They are not provider-backed model runs and
are not evidence that every model will produce the shown wording.

| Fixture | Before | After | What it checks |
| --- | --- | --- | --- |
| Chinese result | [zh-before.md](zh-before.md) | [zh-after.md](zh-after.md) | source-language routing, experiment count, p-value, filler removal |
| English Methods | [en-before.md](en-before.md) | [en-after.md](en-after.md) | same-language editing, passive Methods voice, citation preservation |

Regenerate the local workflow diagram from the skill contract:

```bash
python3 scripts/build_showcase.py
```

The generated [workflow SVG](../assets/showcase/polishing-workflow.svg) is a readable static map of
the routing and preservation contract. `reports/showcase-evidence.json` records that
`model_run` is false. It is a documentation asset, not a model-quality benchmark.
