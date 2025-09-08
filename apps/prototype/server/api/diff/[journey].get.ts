import { H3Event, setHeader } from 'h3'
import { readFile, mkdir, writeFile } from 'node:fs/promises'
import { join } from 'node:path'
import YAML from 'yaml'

function esc(s: string) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
}

export default defineEventHandler(async (event: H3Event) => {
  const { journey } = getRouterParams(event)
  const config = useRuntimeConfig(event)
  const dataDir = config.dataDir
  const schemaPath = join(dataDir, 'schemas', journey, 'schema.yaml')
  const raw = await readFile(schemaPath, 'utf8')
  const schema = YAML.parse(raw) as any

  const rows = (schema.items || []).map((it: any) => {
    const vis = (it.visibility?.all || []).join(' && ')
    const opts = (it.options || []).join(', ')
    const src = it.meta?.source_row_ref || ''
    return {
      id: it.id,
      label: it.label,
      control: it.control,
      data_type: it.data_type,
      options: opts,
      mandatory: it.mandatory ? 'Yes' : 'No',
      visibility: vis,
      section: it.section || '',
      stage: it.stage || '',
      source: src
    }
  })

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  const outDir = join(dataDir, 'generated', 'diffs', String(journey))
  await mkdir(outDir, { recursive: true })

  const html = `<!doctype html>
  <html><head><meta charset="utf-8" />
  <title>Diff – ${esc(journey as string)} – ${timestamp}</title>
  <style>
  body{font-family:system-ui,-apple-system,Segoe UI,Roboto; margin:20px}
  h1{margin:0 0 12px 0}
  table{border-collapse:collapse; width:100%}
  th,td{border:1px solid #ddd; padding:6px 8px; vertical-align:top}
  th{background:#f7f7f7}
  code{background:#f0f0f0; padding:1px 4px; border-radius:4px}
  .muted{color:#666}
  </style></head><body>
  <h1>Schema Report – ${esc(schema.name || journey)}</h1>
  <p class="muted">Generated: ${timestamp}</p>
  <table>
    <thead>
      <tr>
        <th>ID</th><th>Label</th><th>Control</th><th>Data type</th><th>Options</th><th>Mandatory</th><th>Visibility</th><th>Section</th><th>Stage</th><th>Source</th>
      </tr>
    </thead>
    <tbody>
      ${rows.map(r => `<tr>
        <td><code>${esc(r.id)}</code></td>
        <td>${esc(r.label || '')}</td>
        <td>${esc(r.control || '')}</td>
        <td>${esc(r.data_type || '')}</td>
        <td>${esc(r.options || '')}</td>
        <td>${esc(r.mandatory)}</td>
        <td>${esc(r.visibility || '')}</td>
        <td>${esc(r.section || '')}</td>
        <td>${esc(r.stage || '')}</td>
        <td>${esc(r.source || '')}</td>
      </tr>`).join('\n')}
    </tbody>
  </table>
  <p class="muted">Note: PoC report lists schema details mapped to source row refs; spreadsheet round-trip diffing will be added.</p>
  </body></html>`

  const outPath = join(outDir, `${timestamp}.html`)
  await writeFile(outPath, html, 'utf8')
  setHeader(event, 'Content-Type', 'text/html; charset=utf-8')
  return html
})

