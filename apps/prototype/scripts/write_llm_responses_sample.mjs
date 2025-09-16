#!/usr/bin/env node
// Create a small LLM responses file for the first few fields (demo in-Codex processing)
// Usage: node scripts/write_llm_responses_sample.mjs non-lux-1-1 7
import fs from 'node:fs'
import path from 'node:path'

const journey = process.argv[2] || 'non-lux-1-1'
const limit = parseInt(process.argv[3] || '7', 10)
const dir = path.join(process.cwd(), 'apps/prototype/data/generated/analysis', journey)
const batchPath = path.join(dir, 'llm_batch.jsonl')
const outPath = path.join(dir, 'llm_responses.jsonl')

const mapping = {
  GENBankAccountJurisdiction: {
    rewritten_label: 'Where do you want to open the account?',
    rewritten_help: null,
    tags: ['rewritten'],
    risk: 'low',
    rationale: 'Simplified wording; preserves meaning.'
  },
  GENIndicativeAppetiteCustomerApplicationTypeFundsandFundsRelated: {
    rewritten_label: 'Which option best describes your application?',
    rewritten_help: null,
    tags: ['ok'],
    risk: 'low',
    rationale: 'Clear and concise; no change needed.'
  },
  GENIndicativeAppetiteQuestions: {
    rewritten_label: 'Do you want to answer pre‑application questions to check RBSI’s appetite to open this account?',
    rewritten_help: null,
    tags: ['rewritten', 'too_long'],
    risk: 'low',
    rationale: 'Shortened and clarified while preserving meaning.'
  },
  GENIndicativeAppetite3rdPartyAdministrator: {
    rewritten_label: 'Does your customer have a third‑party administrator?',
    rewritten_help: null,
    tags: ['rewritten', 'second_person'],
    risk: 'low',
    rationale: 'Recast to second person; simplified phrasing.'
  },
  GENIndicativeAppetiteFundAdminDomicile: {
    rewritten_label: 'Where is the third‑party administrator domiciled?',
    rewritten_help: null,
    tags: ['rewritten', 'style'],
    risk: 'low',
    rationale: 'Standardised “third‑party” and tightened wording.'
  },
  GENIndicativeAppetiteFundAdminDomicileUSA: {
    rewritten_label: 'Is it Delaware or non‑Delaware?',
    rewritten_help: null,
    tags: ['rewritten'],
    risk: 'low',
    rationale: 'Minor style fix; retains meaning and options.'
  },
  GENIndicativeAppetiteCountryRegistration: {
    rewritten_label: 'Which country is the entity registered, formed, or established in?',
    rewritten_help: null,
    tags: ['rewritten', 'no_slashes', 'too_long'],
    risk: 'low',
    rationale: 'Removed slashes; shortened while preserving legal terms.'
  }
}

const lines = fs.readFileSync(batchPath, 'utf8').split(/\r?\n/).filter(Boolean)
const out = fs.createWriteStream(outPath, 'utf8')
let count = 0
for (const line of lines) {
  if (count >= limit) break
  const obj = JSON.parse(line)
  const key = obj.key
  if (mapping[key]) {
    obj.response_json = mapping[key]
    out.write(JSON.stringify(obj) + '\n')
    count++
  }
}
out.end()
console.log(`[sample] Wrote ${count} responses → ${path.relative(process.cwd(), outPath)}`)

