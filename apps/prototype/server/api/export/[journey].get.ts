import { H3Event, setHeader } from 'h3'
import { readFile, mkdir, writeFile } from 'node:fs/promises'
import { join } from 'node:path'
import YAML from 'yaml'

function toCsvCell(v: any) {
  const s = String(v ?? '')
  if (s.includes(',') || s.includes('\n') || s.includes('"')) {
    return '"' + s.replace(/"/g, '""') + '"'
  }
  return s
}

export default defineEventHandler(async (event: H3Event) => {
  const { journey } = getRouterParams(event)
  const config = useRuntimeConfig(event)
  const dataDir = config.dataDir
  const schemaPath = join(dataDir, 'schemas', journey, 'schema.yaml')
  const raw = await readFile(schemaPath, 'utf8')
  const schema = YAML.parse(raw) as any

  const header = ['REF','KEYNAME','FIELD NAME','DATA TYPE','CONTROL','OPTIONS','MANDATORY','VISIBILITY','SECTION','STAGE']
  const lines = [header.join(',')]
  for (const it of (schema.items || [])) {
    const ref = (it.meta?.source_row_ref || '').split('|')[0].replace('ROW:', '')
    const vis = (it.visibility?.all || []).join(' && ')
    const opts = (it.options || []).join('; ')
    const row = [ref, it.id, it.label, it.data_type, it.control, opts, it.mandatory ? 'Y' : 'N', vis, it.section || '', it.stage || '']
    lines.push(row.map(toCsvCell).join(','))
  }

  const csv = lines.join('\n')
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-')
  const outDir = join(dataDir, 'generated', 'exports', String(journey))
  await mkdir(outDir, { recursive: true })
  const outPath = join(outDir, `${timestamp}.csv`)
  await writeFile(outPath, csv, 'utf8')

  setHeader(event, 'Content-Type', 'text/csv; charset=utf-8')
  setHeader(event, 'Content-Disposition', `attachment; filename="${journey}-${timestamp}.csv"`)
  return csv
})

