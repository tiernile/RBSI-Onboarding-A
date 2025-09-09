import { H3Event } from 'h3'
import { access } from 'node:fs/promises'
import { join } from 'node:path'
import YAML from 'yaml'
import { readFile } from 'node:fs/promises'

export default defineEventHandler(async (event: H3Event) => {
  const config = useRuntimeConfig(event)
  const dataDir = String(config.dataDir || '')
  const manifestPath = join(dataDir, 'schemas', 'manifest.yaml')
  let manifestExists = false
  let journeyCount = 0
  try {
    await access(manifestPath)
    manifestExists = true
    try {
      const raw = await readFile(manifestPath, 'utf8')
      const m = YAML.parse(raw)
      journeyCount = Array.isArray(m?.active) ? m.active.length : 0
    } catch {}
  } catch {}
  return { dataDir, manifestPath, manifestExists, journeyCount }
})

