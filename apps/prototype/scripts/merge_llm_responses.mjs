#!/usr/bin/env node
// Merge JSONL LLM responses into a CSV review sheet
// Usage: node scripts/merge_llm_responses.mjs non-lux-1-1 path/to/responses.jsonl
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const appDir = path.resolve(__dirname, '..')

function toCsvRow(arr) {
  return arr
    .map((x) => {
      const v = x == null ? '' : String(x)
      if (/[",\n]/.test(v)) return '"' + v.replace(/"/g, '""') + '"'
      return v
    })
    .join(',')
}

function parseResponse(line) {
  // Expect either { response_json: {...} } or content as string containing JSON
  try {
    const obj = JSON.parse(line)
    if (obj.response_json && typeof obj.response_json === 'object') return obj.response_json
    if (obj.output && typeof obj.output === 'object') return obj.output
    const txt = obj.response || obj.content || obj.assistant || ''
    if (typeof txt === 'string') {
      const start = txt.indexOf('{')
      const end = txt.lastIndexOf('}')
      if (start >= 0 && end > start) {
        return JSON.parse(txt.slice(start, end + 1))
      }
    }
  } catch (e) {
    // ignore
  }
  return null
}

function main() {
  const journey = process.argv[2] || 'non-lux-1-1'
  const inPath = process.argv[3]
  if (!inPath) {
    console.error('Usage: node scripts/merge_llm_responses.mjs <journey> <responses.jsonl>')
    process.exit(1)
  }
  const outDir = path.join(appDir, 'data', 'generated', 'analysis', journey)
  const outPath = path.join(outDir, 'language-llm.csv')
  const header = [
    'key', 'original_label', 'rewritten_label', 'original_help', 'rewritten_help',
    'section', 'required', 'tags', 'risk', 'rationale'
  ]

  const lines = fs.readFileSync(inPath, 'utf8').split(/\r?\n/).filter(Boolean)
  const rows = [toCsvRow(header)]
  for (const line of lines) {
    try {
      const obj = JSON.parse(line)
      const key = obj.key || (obj.id && String(obj.id).split(':')[1]) || ''
      const section = obj.section || ''
      const required = obj.required ? 'Yes' : 'No'
      const userMsg = (obj.messages || []).find((m) => m.role === 'user')?.content || ''
      const labelMatch = userMsg.match(/label: (.*)/)
      const helpMatch = userMsg.match(/help: (.*)/)
      const originalLabel = labelMatch ? labelMatch[1] : ''
      const originalHelp = helpMatch ? helpMatch[1] : ''
      const resp = parseResponse(line) || parseResponse(obj.response || '{}') || {}
      const rewrittenLabel = resp.rewritten_label || ''
      const rewrittenHelp = resp.rewritten_help || ''
      const tags = Array.isArray(resp.tags) ? resp.tags.join('|') : ''
      const risk = resp.risk || ''
      const rationale = resp.rationale || ''
      rows.push(
        toCsvRow([
          key, originalLabel, rewrittenLabel, originalHelp, rewrittenHelp,
          section, required, tags, risk, rationale
        ])
      )
    } catch (e) {
      // skip bad lines
    }
  }
  fs.mkdirSync(outDir, { recursive: true })
  fs.writeFileSync(outPath, rows.join('\n'))
  console.log(`[merge] Wrote: ${path.relative(process.cwd(), outPath)} (${rows.length - 1} items)`) 
}

main()

