type Answers = Record<string, any>

const ops = {
  '==': (a: any, b: any) => String(a) === String(b),
  '!=': (a: any, b: any) => String(a) !== String(b),
  includes: (a: any[], b: any) => Array.isArray(a) && a.includes(b)
}

export function evalExpr(expr: string, answers: Answers) {
  // Very small expression evaluator for patterns like: KEY == "Yes" or KEY != "UK"
  // Supports && and || between simple comparisons.
  const tokens = expr.split(/\s+(\&\&|\|\|)\s+/)
  let result: boolean | null = null
  let pendingOp: '&&'|'||'|null = null
  for (const t of tokens) {
    if (t === '&&' || t === '||') { pendingOp = t as any; continue }
    const m = t.match(/^([A-Za-z0-9_]+)\s*(==|!=)\s*\"([^\"]*)\"$/)
    if (!m) return false
    const [, key, op, val] = m
    const ok = (ops as any)[op]?.(answers[key], val) ?? false
    if (result === null) result = ok
    else if (pendingOp === '&&') result = (result && ok)
    else if (pendingOp === '||') result = (result || ok)
  }
  return !!result
}

export function isVisible(visibility: { all?: string[] }|undefined, answers: Answers) {
  if (!visibility || !visibility.all || visibility.all.length === 0) return true
  return visibility.all.every(expr => evalExpr(expr, answers))
}

