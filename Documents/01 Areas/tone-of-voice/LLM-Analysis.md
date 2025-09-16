# LLM Language Review – Simple Mode

Purpose: fast, human‑in‑the‑loop language review using a single, locked prompt – no knobs to tweak.

## What it does
- Prepares a JSONL batch: one item per field (label/help + minimal context).
- You run the batch through your preferred LLM runner (OpenAI/Azure/local).
- Merges responses into a CSV for at‑scale human review.

No rules to edit. The prompt encodes good writing defaults: short, second person, active voice, no new facts.

## Commands

```bash
# 1) Prepare prompts for the journey (JSONL)
cd apps/prototype
pnpm analyze:prepare    # writes data/generated/analysis/<journey>/llm_batch.jsonl

# 2) Run the JSONL through your LLM tool of choice
#    Save responses as: apps/prototype/data/generated/analysis/<journey>/llm_responses.jsonl

# 3) Merge responses into a CSV review sheet
pnpm analyze:merge      # writes data/generated/analysis/<journey>/language-llm.csv
```

## JSONL format
Each line contains `messages` ready for chat‑style LLMs. Responses should return strict JSON matching the provided `expected_schema`.

Example line:
```json
{
  "id": "non-lux-1-1:GENCompanyName",
  "journey": "non-lux-1-1",
  "key": "GENCompanyName",
  "section": "Details of the new customer account",
  "required": true,
  "messages": [
    { "role": "system", "content": "You are an expert product writer..." },
    { "role": "user", "content": "FIELD CONTEXT...\nTASK: Return JSON only, matching this schema: { \"rewritten_label\": \"\", ... }" }
  ],
  "expected_schema": { "rewritten_label": "", "rewritten_help": null, "tags": ["ok"], "risk": "low", "rationale": "" }
}
```

Expected response JSON (per line):
```json
{ "rewritten_label": "...", "rewritten_help": null, "tags": ["ok"], "risk": "low", "rationale": "..." }
```

## Guardrails
- Prompt forbids adding facts/options/numbers not in the original.
- If uncertain, keep the original and tag `insufficient_context`.
- Merge step tolerates different runner formats as long as the JSON is present per line.

## Review output
`language-llm.csv` columns:
- key, original_label, rewritten_label, original_help, rewritten_help, section, required, tags, risk, rationale

Use this file for bulk human review; accept/reject changes and capture notes in your own workflow.

