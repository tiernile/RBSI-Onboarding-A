import { H3Event, getRouterParams, sendError, createError, setHeader, getQuery } from 'h3'
import { loadYamlFromData } from '~/server/utils/data'
import { validateJourneySlug } from '~/server/utils/validation'

type KycpField = {
  key: string
  label?: string
  type?: string
  options?: Array<{ value: string; label: string }>
  visibility?: Array<{ allConditionsMustMatch?: boolean; conditions?: Array<{ sourceKey: string; operator: string; value: any }> }>
}

function normalizeBooleanText(s: string) {
  const v = (s || '').trim().toLowerCase()
  if (v === 'y' || v === 'yes' || v === 'true') return 'yes'
  if (v === 'n' || v === 'no' || v === 'false') return 'no'
  return s
}

// Very small parser for legacy visibility strings (e.g., "A = Yes && B <> No")
function parseLegacyExpr(expr: string) {
  if (!expr || !expr.trim()) return [] as Array<{ sourceKey: string; operator: string; value: any }>
  let e = expr.replace(/\n/g, ' ')
  e = e.replace(/\bAND\b/gi, '&&').replace(/\bOR\b/gi, '||')
  e = e.replace(/<>/g, '!=')
  e = e.replace(/([^=])=([^=])/g, '$1==$2')
  const parts = e.split('&&').map(p => p.trim()).filter(Boolean)
  const out: Array<{ sourceKey: string; operator: string; value: any }> = []
  for (const p of parts) {
    const op = p.includes('==') ? '==' : (p.includes('!=') ? '!=' : null)
    if (!op) continue
    const [left, right] = p.split(op)
    let val = (right || '').trim()
    if ((val.startsWith('"') && val.endsWith('"')) || (val.startsWith("'") && val.endsWith("'"))) {
      val = val.slice(1, -1)
    }
    out.push({ sourceKey: (left || '').trim(), operator: op, value: val })
  }
  return out
}

export default defineEventHandler(async (event: H3Event) => {
  const { journey } = getRouterParams(event)
  if (!validateJourneySlug(journey)) {
    return sendError(event, createError({ statusCode: 400, statusMessage: 'Invalid journey identifier' }))
  }

  let schema: any
  let isKycp = false
  try {
    try {
      schema = await loadYamlFromData(event, `schemas/${journey}/schema-kycp.yaml`)
      isKycp = true
    } catch {
      schema = await loadYamlFromData(event, `schemas/${journey}/schema.yaml`)
    }
  } catch (err: any) {
    return sendError(event, createError({ statusCode: 404, statusMessage: 'Schema not found' }))
  }

  const fields: KycpField[] = isKycp ? (schema.fields || []) : ((schema.items || []).map((it: any) => {
    const conds = (it.visibility?.all || []) as string[]
    const parsed = conds.flatMap(expr => parseLegacyExpr(expr))
    return {
      key: it.id,
      label: it.label,
      type: it.control || it.data_type,
      options: (it.options || []).map((v: any) => ({ value: String(v), label: String(v) })),
      visibility: parsed.length ? [{ allConditionsMustMatch: true, conditions: parsed }] : []
    } as KycpField
  }))

  const fieldMap = new Map<string, KycpField>()
  fields.forEach(f => fieldMap.set(f.key, f))

  // Simple alias map for values
  const valueAliases: Record<string, string[]> = {
    'uk': ['united kingdom'],
    'united kingdom': ['uk'],
    'yes': ['y', 'true'],
    'no': ['n', 'false']
  }

  const lints: any[] = []
  const edges: Array<[string, string]> = [] // source -> target

  function optionSetFor(fieldKey: string) {
    const src = fieldMap.get(fieldKey)
    const set = new Set<string>()
    if (src && src.options && src.options.length) {
      for (const o of src.options) {
        set.add((o.value ?? o.label ?? '').toString().toLowerCase())
        set.add((o.label ?? o.value ?? '').toString().toLowerCase())
      }
    }
    return set
  }

  for (const f of fields) {
    const issues: any[] = []
    const vis = f.visibility || []
    for (const rule of vis) {
      const conds = rule.conditions || []
      for (const c of conds) {
        const left = c.sourceKey
        const op = c.operator
        const rawVal = (c.value ?? '').toString()
        const valLc = normalizeBooleanText(rawVal).toString().toLowerCase()
        if (!fieldMap.has(left)) {
          issues.push({ type: 'unresolved_key', message: `Unknown controller '${left}'` })
        } else {
          edges.push([left, f.key])
          const srcField = fieldMap.get(left)!
          if ((op === '==' || op === '!=') && (srcField.type === 'lookup' || srcField.type === 'enum')) {
            const set = optionSetFor(left)
            const expanded = new Set<string>([valLc, ...(valueAliases[valLc] || [])])
            const match = Array.from(expanded).some(v => set.has(v))
            if (!match) {
              issues.push({ type: 'option_mismatch', message: `Value '${rawVal}' not found in options of '${left}'`, options: Array.from(set) })
            }
          }
        }
        if (/^\d+(?:\.\d+)?$/.test(rawVal)) {
          issues.push({ type: 'suspicious_numeric_value', message: `Numeric value '${rawVal}' in condition may be a group index` })
        }
      }
    }
    if (issues.length) lints.push({ key: f.key, label: f.label, issues })
  }

  // Detect dependency cycles
  const graph = new Map<string, string[]>()
  for (const [a, b] of edges) {
    graph.set(a, (graph.get(a) || []).concat(b))
  }
  const cycles: string[][] = []
  const temp = new Set<string>()
  const perm = new Set<string>()
  const stack: string[] = []
  function dfs(n: string) {
    if (perm.has(n)) return
    if (temp.has(n)) {
      const i = stack.indexOf(n)
      cycles.push(stack.slice(i).concat(n))
      return
    }
    temp.add(n); stack.push(n)
    for (const m of (graph.get(n) || [])) dfs(m)
    temp.delete(n); perm.add(n); stack.pop()
  }
  for (const n of graph.keys()) dfs(n)

  const report = {
    journey,
    isKycp,
    totals: {
      fields: fields.length,
      withVisibility: fields.filter(f => (f.visibility || []).length).length,
      lints: lints.length,
      edges: edges.length,
      cycles: cycles.length
    },
    lints,
    cycles
  }

  const query = getQuery(event) as any
  if (query && (query.format === 'html' || query.format === 'HTML')) {
    setHeader(event, 'Content-Type', 'text/html; charset=utf-8')
    const rows = lints.map(li => `<tr><td><code>${li.key}</code></td><td>${li.label || ''}</td><td>${li.issues.map((i: any) => i.type).join(', ')}</td></tr>`).join('\n')
    return `<!doctype html><html><head><meta charset="utf-8"/><title>Conditions Report – ${journey}</title>
    <style>body{font-family:system-ui,-apple-system,Segoe UI,Roboto; margin:20px} table{border-collapse:collapse;width:100%} th,td{border:1px solid #ddd;padding:6px 8px} th{background:#f7f7f7}</style>
    </head><body>
      <h1>Conditions Report – ${journey}</h1>
      <p>Fields: ${report.totals.fields} · With visibility: ${report.totals.withVisibility} · Lints: ${report.totals.lints} · Cycles: ${report.totals.cycles}</p>
      <table><thead><tr><th>Key</th><th>Label</th><th>Issues</th></tr></thead><tbody>${rows}</tbody></table>
    </body></html>`
  }

  return report
})

