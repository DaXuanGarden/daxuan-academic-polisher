# Output contract and follow-up behavior

## Normal polish

Return the polished text first. Keep paragraph, heading, list, inline-code, equation, and
citation structure unless the user requests a structural change. Do not write “以下是润色
版本” or “Here is the polished version”. Then write one notes line in the user's conversation
language:

- Chinese: `修改说明：` followed by at most five short flags, or `修改说明：无`.
- English: `Notes:` followed by at most five short flags, or `Notes: none.`

Notes are for real decisions only: `[待核实: ...]` / `[CHECK: ...]`, claims that read
stronger or weaker than the evidence shown, terminology unified across the passage, or a
source ambiguity. Do not narrate every edit.

## Follow-ups

“还是太啰嗦”, “too long”, or “restore sentence 3” refers to the immediately preceding
polish. Return the corrected passage in the established language and register. A new journal,
section, or output-language instruction re-routes the affected pass.

## Audit and draft modes

For `audit`, report the smallest useful list of problems, quote the relevant phrase, and give
a targeted repair suggestion without silently replacing the whole passage. For `draft`, make
the requested prose from supplied notes, keep unsupported claims visibly marked, and state
which required input is missing.

## Optional style anchor

If the user supplies `<style_anchor>...</style_anchor>`, match rhythm and register after the
evidence pass. Never copy facts or wording from the anchor, and mention a conflict only when
it changes an evidence boundary or a venue requirement.
