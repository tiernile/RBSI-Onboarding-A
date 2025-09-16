#!/usr/bin/env node
// Simple scenario checks for KYCP schemas (no server required)
// Usage: node scripts/scenarios.mjs non-lux-1-1
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import YAML from 'yaml'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const appDir = path.resolve(__dirname, '..')

function loadKycpSchema(journey) {
  const p = path.join(appDir, 'data', 'schemas', journey, 'schema-kycp.yaml')
  const raw = fs.readFileSync(p, 'utf8')
  return YAML.parse(raw)
}

function buildFieldMap(schema) {
  const map = new Map()
  for (const f of schema.fields || []) map.set(f.key, f)
  return map
}

function evalVisibility(field, model) {
  const vis = field.visibility || []
  if (!vis.length) return true
  const getVal = (k) => model[k]
  for (const rule of vis) {
    const all = rule.allConditionsMustMatch !== false
    const conds = rule.conditions || []
    const test = (c) => {
      const sv = getVal(c.sourceKey)
      const tv = c.value
      const svn = typeof sv === 'string' ? sv.toLowerCase() : sv
      const tvn = typeof tv === 'string' ? tv.toLowerCase() : tv
      if (c.operator === 'eq' || c.operator === '==') return svn == tvn
      if (c.operator === 'neq' || c.operator === '!=') return svn != tvn
      return true
    }
    if (all && !conds.every(test)) return false
    if (!all && !conds.some(test)) return false
  }
  return true
}

function assertEqual(actual, expected, msg) {
  if (actual !== expected) {
    throw new Error(`${msg} (expected ${expected}, got ${actual})`)
  }
}

function runScenarios(journey) {
  const schema = loadKycpSchema(journey)
  const fmap = buildFieldMap(schema)
  function field(key) {
    const f = fmap.get(key)
    if (!f) throw new Error(`Field not found: ${key}`)
    return f
  }

  const scenarios = []

  // Scenario A: UK path
  scenarios.push(() => {
    const model = { GENBankAccountJurisdiction: 'United Kingdom' }
    const preApp = evalVisibility(field('GENIndicativeAppetiteQuestions'), model)
    // For UK path, Fund Manager question requires Pre-App = Yes per visibility overrides
    model.GENIndicativeAppetiteQuestions = 'Yes'
    const ukFM = evalVisibility(field('GENUKIndicativeAppetiteFundMng'), model)
    const ukFMDom_before = evalVisibility(field('GENUKIndicativeAppetiteFundMngDom'), model)
    // Now set Fund Manager = Yes
    model.GENUKIndicativeAppetiteFundMng = 'Yes'
    const ukFMDom_after = evalVisibility(field('GENUKIndicativeAppetiteFundMngDom'), model)

    assertEqual(preApp, false, 'UK: Pre-Application question should be hidden')
    assertEqual(ukFM, true, 'UK: Fund Manager question should be visible when Pre-App = Yes')
    assertEqual(ukFMDom_before, false, 'UK: Fund Manager domicile hidden until FM = Yes')
    assertEqual(ukFMDom_after, true, 'UK: Fund Manager domicile visible when FM = Yes')
  })

  // Scenario B: Non-UK + Pre-App = Yes
  scenarios.push(() => {
    const model = { GENBankAccountJurisdiction: 'Jersey', GENIndicativeAppetiteQuestions: 'Yes' }
    const preApp = evalVisibility(field('GENIndicativeAppetiteQuestions'), model)
    const ukFM = evalVisibility(field('GENUKIndicativeAppetiteFundMng'), model)
    assertEqual(preApp, true, 'Non-UK: Pre-Application question should be visible')
    assertEqual(ukFM, false, 'Non-UK: Fund Manager (UK only) should be hidden')
  })

  // Scenario C: Investment Adviser USA fork
  scenarios.push(() => {
    const model = { GENOpeningInvestmentAdviser: 'Yes', GENOpeningInvestmentAdviserLocation: 'United States' }
    const usaFork = evalVisibility(field('GENOpeningInvestmentAdviserLocationUSA'), model)
    assertEqual(usaFork, true, 'Adviser USA fork should be visible when location is United States')
  })

  // Execute
  for (const fn of scenarios) fn()
  return { ok: true, count: scenarios.length }
}

async function main() {
  const journey = process.argv[2] || 'non-lux-1-1'
  const res = runScenarios(journey)
  console.log(`[scenarios] ${journey} → ${res.count} passed`)
}

main().catch((e) => {
  console.error('[scenarios] failed:', e.message || e)
  process.exit(1)
})
