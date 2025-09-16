#!/usr/bin/env node
// Field inventory analysis for KYCP schema
// Usage: node scripts/analyze_fields.mjs non-lux-1-1
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import YAML from 'yaml'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const appDir = path.resolve(__dirname, '..')

function loadSchema(journey) {
  const p = path.join(appDir, 'data', 'schemas', journey, 'schema-kycp.yaml')
  const raw = fs.readFileSync(p, 'utf8')
  return YAML.parse(raw)
}

function toCsvRow(arr) {
  return arr
    .map((x) => {
      const v = x == null ? '' : String(x)
      if (/[",\n]/.test(v)) return '"' + v.replace(/"/g, '""') + '"'
      return v
    })
    .join(',')
}

function analyze(journey) {
  const schema = loadSchema(journey)
  const fields = schema.fields || []
  const byType = {}
  const controllersCount = {}
  const sections = {}
  let withVisibility = 0
  let requiredCount = 0
  let lookupNoOptions = 0
  let complexParents = 0
  let complexChildren = 0

  const keySet = new Set(fields.map((f) => f.key))
  const unresolvedControllers = new Set()

  const rows = []
  for (const f of fields) {
    const type = f.type || f.style || 'field'
    byType[type] = (byType[type] || 0) + 1
    const sec = f._section || 'General'
    sections[sec] = (sections[sec] || 0) + 1
    const vis = f.visibility || []
    if (vis.length) withVisibility++
    const req = !!(f.validation && f.validation.required)
    if (req) requiredCount++
    if ((type === 'lookup' || type === 'enum') && !(f.options && f.options.length)) lookupNoOptions++
    if (type === 'complex') complexParents++
    if (f._complex) complexChildren++

    // controllers used
    const controllers = new Set()
    for (const r of vis) {
      for (const c of r.conditions || []) {
        controllers.add(c.sourceKey)
        if (!keySet.has(c.sourceKey)) unresolvedControllers.add(c.sourceKey)
      }
    }

    rows.push([
      f.key,
      f.label || '',
      sec,
      type,
      f.style || '',
      req ? 'Y' : 'N',
      f._complex || '',
      (f.options || []).length || '',
      vis.length || 0,
      Array.from(controllers).join('|'),
      f.scriptId || ''
    ])
  }

  const summary = {
    journey,
    totals: {
      fields: fields.length,
      withVisibility,
      required: requiredCount,
      complexParents,
      complexChildren,
      lookupNoOptions
    },
    byType,
    bySection: sections,
    topControllers: Object.entries(
      rows
        .flatMap((r) => (r[9] ? r[9].split('|') : []))
        .reduce((acc, k) => ((acc[k] = (acc[k] || 0) + 1), acc), {})
    )
      .sort((a, b) => b[1] - a[1])
      .slice(0, 20),
    unresolvedControllers: Array.from(unresolvedControllers)
  }

  const outDir = path.join(appDir, 'data', 'generated', 'analysis', journey)
  fs.mkdirSync(outDir, { recursive: true })
  const csvPath = path.join(outDir, 'fields.csv')
  const sumPath = path.join(outDir, 'summary.json')
  const header = [
    'key',
    'label',
    'section',
    'type',
    'style',
    'required',
    'complex_parent',
    'options_count',
    'visibility_rules',
    'controllers',
    'scriptId'
  ]
  const csv = [toCsvRow(header)].concat(rows.map(toCsvRow)).join('\n')
  fs.writeFileSync(csvPath, csv)
  fs.writeFileSync(sumPath, JSON.stringify(summary, null, 2))
  return { csvPath, sumPath, summary }
}

async function main() {
  const journey = process.argv[2] || 'non-lux-1-1'
  const res = analyze(journey)
  console.log(`[fields] Wrote ${journey}:`)
  console.log(`  CSV: ${path.relative(process.cwd(), res.csvPath)}`)
  console.log(`  JSON: ${path.relative(process.cwd(), res.sumPath)}`)
  console.log(`  Totals:`, res.summary.totals)
}

main().catch((e) => {
  console.error('[fields] failed:', e?.stack || e?.message || e)
  process.exit(1)
})

