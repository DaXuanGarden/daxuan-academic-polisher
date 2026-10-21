# Language routing

The source draft determines the editing language. The language of the user's request is
context, not evidence that the draft should be translated.

## Decision order

1. Honor an explicit output-language request (`润色成中文`, `润色成英文`, `polish in
   English`, or an equivalent). If the user asks for translation only, do not silently turn
   it into a polishing job.
2. Otherwise inspect prose after masking URLs, code, file paths, citation brackets, equations,
   DOI/PMID strings, and isolated technical identifiers. English technical terms inside an
   otherwise Chinese sentence count as local terms; they do not by themselves route the
   passage to English.
3. Use Chinese when Han prose clearly dominates, English when English prose clearly
   dominates, and `mixed` when both languages carry substantial prose. Short, tabular,
   formula-heavy, or identifier-only inputs may be `und`. The bundled detector is a
   reproducible signal, not a replacement for editorial judgment.
4. For `mixed`, use the dominant language for the paragraph and edit a quoted or embedded
   passage in its own language. If both languages are equally substantive and the requested
   output is unclear, ask one short clarification rather than guessing.

## Practical thresholds

The script is intentionally conservative. Around twenty Han characters with only a few
English technical words usually routes to Chinese; around twenty ordinary Latin letters in
several words with little Han text routes to English. Near-balanced prose, very short text,
and technical-only text remains `mixed` or `und`. Always inspect the actual prose, especially
when a table or formula is supplied without surrounding sentences.

## Follow-up consistency

Once a passage has been routed, keep the same language and register for follow-up edits unless
the user explicitly changes them. A request such as “还是太啰嗦” refers to the last polished
text and should return only the corrected text plus the normal notes line.
