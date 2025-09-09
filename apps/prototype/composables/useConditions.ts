type Answers = Record<string, any>

// Tokenizer and parser for a small, safe expression language used in visibility rules.
// Supports: identifiers, string/number/boolean literals, parentheses, &&, ||,
// operators: ==, !=, <, <=, >, >=, includes

type Token =
  | { t: 'id'; v: string }
  | { t: 'str'; v: string }
  | { t: 'num'; v: number }
  | { t: 'bool'; v: boolean }
  | { t: 'op'; v: string }

function tokenize(input: string): Token[] {
  const s = input.trim()
  const tokens: Token[] = []
  let i = 0
  const isIdStart = (ch: string) => /[A-Za-z_]/.test(ch)
  const isId = (ch: string) => /[A-Za-z0-9_]/.test(ch)
  const skipWs = () => { while (i < s.length && /\s/.test(s[i]!)) i++ }
  while (i < s.length) {
    skipWs()
    const ch = s[i]
    if (!ch) break
    // Parentheses
    if (ch === '(' || ch === ')') { tokens.push({ t: 'op', v: ch as any }); i++; continue }
    // Logical ops
    if (s.startsWith('&&', i)) { tokens.push({ t: 'op', v: '&&' }); i += 2; continue }
    if (s.startsWith('||', i)) { tokens.push({ t: 'op', v: '||' }); i += 2; continue }
    // Comparison ops
    if (s.startsWith('>=', i)) { tokens.push({ t: 'op', v: '>=' }); i += 2; continue }
    if (s.startsWith('<=', i)) { tokens.push({ t: 'op', v: '<=' }); i += 2; continue }
    if (s.startsWith('==', i)) { tokens.push({ t: 'op', v: '==' }); i += 2; continue }
    if (s.startsWith('!=', i)) { tokens.push({ t: 'op', v: '!=' }); i += 2; continue }
    if (s[i] === '>') { tokens.push({ t: 'op', v: '>' }); i++; continue }
    if (s[i] === '<') { tokens.push({ t: 'op', v: '<' }); i++; continue }
    // includes keyword
    if (/^includes\b/.test(s.slice(i))) { tokens.push({ t: 'op', v: 'includes' }); i += 'includes'.length; continue }
    // String literal (single or double quotes)
    if (ch === '"' || ch === "'") {
      const quote = ch
      i++
      let buf = ''
      while (i < s.length && s[i] !== quote) {
        if (s[i] === '\\' && i + 1 < s.length) { buf += s[i+1]; i += 2; continue }
        buf += s[i]
        i++
      }
      if (s[i] === quote) i++
      tokens.push({ t: 'str', v: buf })
      continue
    }
    // Number
    if (/[0-9]/.test(ch)) {
      let start = i
      while (i < s.length && /[0-9.]/.test(s[i]!)) i++
      const num = Number(s.slice(start, i))
      tokens.push({ t: 'num', v: num })
      continue
    }
    // Identifier / boolean
    if (isIdStart(ch)) {
      let start = i; i++
      while (i < s.length && isId(s[i]!)) i++
      const ident = s.slice(start, i)
      const low = ident.toLowerCase()
      if (low === 'true' || low === 'false') tokens.push({ t: 'bool', v: low === 'true' })
      else tokens.push({ t: 'id', v: ident })
      continue
    }
    // Unknown token → bail
    return []
  }
  return tokens
}

function evalComparison(left: any, op: Token['v'], right: any): boolean {
  const toNum = (v: any) => (v === '' || v === null || v === undefined ? NaN : Number(v))
  switch (op) {
    case '==':
      if (typeof left === 'string' && typeof right === 'string') return left.toLowerCase() === right.toLowerCase()
      return String(left) === String(right)
    case '!=':
      if (typeof left === 'string' && typeof right === 'string') return left.toLowerCase() !== right.toLowerCase()
      return String(left) !== String(right)
    case '<': return toNum(left) < toNum(right)
    case '<=': return toNum(left) <= toNum(right)
    case '>': return toNum(left) > toNum(right)
    case '>=': return toNum(left) >= toNum(right)
    case 'includes':
      return Array.isArray(left) ? left.map(String).includes(String(right)) : false
    default: return false
  }
}

// Recursive‑descent parser
function parseAndEval(tokens: Token[], answers: Answers): boolean {
  let pos = 0

  function peek(): Token | undefined { return tokens[pos] }
  function consume(): Token | undefined { return tokens[pos++] }

  function parsePrimary(): any {
    const t = consume()
    if (!t) return undefined
    if (t.t === 'id') return { kind: 'id', v: t.v }
    if (t.t === 'str' || t.t === 'num' || t.t === 'bool') return { kind: 'lit', v: t.v }
    if (t.t === 'op' && t.v === '(') {
      const v = parseOr()
      const r = consume()
      if (!r || r.t !== 'op' || r.v !== ')') return false
      return { kind: 'lit', v }
    }
    return undefined
  }

  function valueOf(node: any): any {
    if (!node) return undefined
    if (node.kind === 'lit') return node.v
    if (node.kind === 'id') return answers[node.v]
    return undefined
  }

  function parseComparison(): boolean {
    const leftNode = parsePrimary()
    const op = peek()
    if (!op || op.t !== 'op' || !['==','!=','<','<=','>','>=','includes'].includes(op.v)) {
      // Single value resolves to truthiness
      const v = valueOf(leftNode)
      return !!v
    }
    consume() // op
    const rightNode = parsePrimary()
    const left = valueOf(leftNode)
    const right = valueOf(rightNode)
    return evalComparison(left, op.v, right)
  }

  function parseAnd(): boolean {
    let val = parseComparison()
    while (peek() && peek()!.t === 'op' && peek()!.v === '&&') {
      consume()
      const rhs = parseComparison()
      val = val && rhs
    }
    return val
  }

  function parseOr(): boolean {
    let val = parseAnd()
    while (peek() && peek()!.t === 'op' && peek()!.v === '||') {
      consume()
      const rhs = parseAnd()
      val = val || rhs
    }
    return val
  }

  return parseOr()
}

export function evalExpr(expr: string, answers: Answers) {
  if (!expr || !expr.trim()) return true
  const tokens = tokenize(expr)
  if (!tokens.length) return false
  try {
    return !!parseAndEval(tokens, answers)
  } catch {
    return false
  }
}

export function isVisible(visibility: { all?: string[] }|undefined, answers: Answers) {
  if (!visibility || !visibility.all || visibility.all.length === 0) return true
  return visibility.all.every(expr => evalExpr(expr, answers))
}
