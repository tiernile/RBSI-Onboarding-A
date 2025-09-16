#!/usr/bin/env node
// Prepare JSONL batch prompts for LLM language review/rewrite (simple mode)
// Usage: node scripts/prepare_llm_batch.mjs non-lux-1-1
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import YAML from 'yaml'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const appDir = path.resolve(__dirname, '..')

function loadKycp(journey) {
  const p = path.join(appDir, 'data', 'schemas', journey, 'schema-kycp.yaml')
  const raw = fs.readFileSync(p, 'utf8')
  return YAML.parse(raw)
}

function buildSystemPrompt() {
  return (
    'You are an expert product writer for regulated banking onboarding. '
    + 'Review and, if beneficial, rewrite a single field label and optional help text. '
    + 'Preserve meaning. Do not add new facts, numbers, policies or options. '
    + 'Be clear, direct, and polite. Use second person (you/your). Prefer active voice. '
    + 'Keep questions short (< 20 words) and help concise (< 40 words). '
    + 'Avoid slashes (use "or"). If an acronym is not universally known, expand at first mention. '
    + 'If you lack context, keep the original and note "insufficient_context". '
    + 'Output strict JSON matching the provided schema. Do not include any extra keys or prose.'
  )
}

function buildUserPrompt(field) {
  const parts = []
  parts.push('FIELD CONTEXT:')
  parts.push(`key: ${field.key}`)
  parts.push(`section: ${field._section || 'General'}`)
  parts.push(`required: ${field.validation?.required ? 'Yes' : 'No'}`)
  parts.push(`type: ${field.type || field.style || 'field'}`)
  if (field.options && field.options.length) {
    const sample = field.options.slice(0, 6).map((o) => o.label || o.value).join(', ')
    parts.push(`options_sample: ${sample}${field.options.length > 6 ? ' …' : ''}`)
  }
  parts.push('ORIGINAL TEXT:')
  parts.push(`label: ${field.label || ''}`)
  if (field.description) parts.push(`help: ${field.description}`)
  parts.push('\nTASK: Return JSON only, matching this schema:')
  parts.push(JSON.stringify(outputSchema(), null, 2))
  return parts.join('\n')
}

function outputSchema() {
  // This is an example object; keys define the contract
  return {
    rewritten_label: '',
    rewritten_help: null,
    tags: ['ok'], // e.g., ["too_long","passive","double_question","jargon","insufficient_context","ok"]
    risk: 'low', // one of: low|medium|high
    rationale: '' // one sentence
  }
}

function main() {
  const journey = process.argv[2] || 'non-lux-1-1'
  const schema = loadKycp(journey)
  const fields = (schema.fields || []).filter((f) => !f.internal && !f.internal_only)
  const userFacing = fields.filter((f) => (f.style || 'field') === 'field')

  const outDir = path.join(appDir, 'data', 'generated', 'analysis', journey)
  fs.mkdirSync(outDir, { recursive: true })
  const outPath = path.join(outDir, 'llm_batch.jsonl')
  const sys = buildSystemPrompt()

  const stream = fs.createWriteStream(outPath, 'utf8')
  for (const f of userFacing) {
    const record = {
      id: `${journey}:${f.key}`,
      journey,
      key: f.key,
      section: f._section || 'General',
      required: !!(f.validation && f.validation.required),
      messages: [
        { role: 'system', content: sys },
        { role: 'user', content: buildUserPrompt(f) }
      ],
      expected_schema: outputSchema()
    }
    stream.write(JSON.stringify(record) + '\n')
  }
  stream.end()
  console.log(`[prepare] Wrote batch: ${path.relative(process.cwd(), outPath)} (${userFacing.length} items)`) 
}

main()

