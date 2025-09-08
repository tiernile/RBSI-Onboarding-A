import { readFile } from 'node:fs/promises'
import { join } from 'node:path'
import YAML from 'yaml'
import { H3Event, sendError, getCookie, createError } from 'h3'

type Journey = {
  key: string
  name: string
  version: string
  variant?: string
  owner?: string
  display?: { group?: string; order?: number; visible?: boolean; status?: string }
}

type Manifest = { active: Journey[]; deprecated?: Journey[] }

export default defineEventHandler(async (event: H3Event) => {
  const config = useRuntimeConfig(event)
  try {
    const manifestPath = join(config.dataDir, 'schemas', 'manifest.yaml')
    const raw = await readFile(manifestPath, 'utf8')
    const manifest = YAML.parse(raw) as Manifest

    const visibleEnv = (config.mcVisible || '').split(',').map(s => s.trim()).filter(Boolean)
    let statusEnv: Record<string, string> = {}
    try { statusEnv = JSON.parse(config.mcStatus || '{}') } catch {}

    const adminCookie = getCookie(event, 'admin')
    const isAdmin = adminCookie === 'true'

    const active = (manifest.active || []).map(j => {
      const display = { ...(j.display || {}) }
      if (visibleEnv.length) {
        display.visible = visibleEnv.includes(j.key)
      }
      if (statusEnv[j.key]) {
        display.status = statusEnv[j.key]
      }
      return { ...j, display }
    })

    // Sort by group then order
    active.sort((a, b) => {
      const ga = a.display?.group || ''
      const gb = b.display?.group || ''
      if (ga !== gb) return ga.localeCompare(gb)
      const oa = a.display?.order ?? 0
      const ob = b.display?.order ?? 0
      return oa - ob
    })

    return { isAdmin, active }
  } catch (err: any) {
    return sendError(event, createError({ statusCode: 500, statusMessage: 'Failed to load manifest', data: String(err?.message || err) }))
  }
})
