import { H3Event } from 'h3'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'
import YAML from 'yaml'

/**
 * Load a YAML file from the data directory with a fallback to Nitro server assets.
 * Works in local dev, node server, and serverless (e.g., Vercel).
 */
export async function loadYamlFromData<T = any>(event: H3Event, relativePath: string): Promise<T> {
  const config = useRuntimeConfig(event)
  const rel = relativePath.replace(/^\/+/, '')
  const fsPath = join(String(config.dataDir || ''), rel)

  // Try filesystem path from runtime config
  try {
    const raw = await readFile(fsPath, 'utf8')
    return YAML.parse(raw) as T
  } catch (err) {
    // Fallback to server assets storage: assets:data/<relativePath>
    try {
      const storage = useStorage()
      // Nitro stores under namespace 'assets', with baseName used as a folder
      const key = `assets:data/${rel}`
      const raw = await storage.getItem<string | Buffer>(key)
      if (raw !== null && raw !== undefined) {
        const text = typeof raw === 'string' ? raw : String(raw)
        return YAML.parse(text) as T
      }
    } catch {}
    throw err
  }
}

