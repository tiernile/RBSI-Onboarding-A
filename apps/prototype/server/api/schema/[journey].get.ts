import { H3Event, getRouterParams, sendError, createError } from 'h3'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'
import YAML from 'yaml'

export default defineEventHandler(async (event: H3Event) => {
  const { journey } = getRouterParams(event)
  const config = useRuntimeConfig(event)
  try {
    const p = join(config.dataDir, 'schemas', journey, 'schema.yaml')
    const raw = await readFile(p, 'utf8')
    const parsed = YAML.parse(raw)
    return parsed
  } catch (err: any) {
    return sendError(event, createError({ statusCode: 500, statusMessage: 'Failed to load schema', data: String(err?.message || err) }))
  }
})
