import { H3Event } from 'h3'
import { loadYamlFromData } from '~/server/utils/data'

export default defineEventHandler(async (event: H3Event) => {
  const config = useRuntimeConfig(event)
  const dataDir = String(config.dataDir || '')
  let manifestExists = false
  let journeyCount = 0
  let error: string | undefined
  try {
    const m = await loadYamlFromData<any>(event, 'schemas/manifest.yaml')
    manifestExists = true
    journeyCount = Array.isArray(m?.active) ? m.active.length : 0
  } catch (e: any) {
    error = e?.message || String(e)
  }
  return { dataDir, manifestExists, journeyCount, error }
})
