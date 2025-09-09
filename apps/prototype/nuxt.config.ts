import { defineNuxtConfig } from 'nuxt/config'
import path from 'node:path'
import fs from 'node:fs'
import { fileURLToPath } from 'node:url'

const here = fileURLToPath(new URL('.', import.meta.url))
const repoData = path.resolve(here, '..', '..', 'data')
const localData = path.resolve(here, 'data')

const defaultDataDir = (() => {
  // Prefer explicit env vars
  const fromEnv = process.env.DATA_DIR || process.env.NUXT_DATA_DIR
  if (fromEnv) return fromEnv
  // If deploying from apps/prototype only, allow ./data beside the app
  if (fs.existsSync(localData)) return localData
  // Fallback to monorepo layout ../../data
  if (fs.existsSync(repoData)) return repoData
  // Fallback to Nitro server assets path (Vercel serverless)
  const serverAssetsData = path.resolve(here, 'assets', 'data')
  return serverAssetsData
})()

export default defineNuxtConfig({
  nitro: {
    // Bundle a /data directory into the server output so Vercel serverless can read it
    serverAssets: [
      { baseName: 'data', dir: fs.existsSync(localData) ? localData : repoData }
    ]
  },
  typescript: { strict: true },
  runtimeConfig: {
    adminPasswordHash: process.env.NEXT_ADMIN_PASSWORD_HASH || process.env.NUXT_ADMIN_PASSWORD_HASH || '',
    adminPasswordPlain: process.env.NEXT_ADMIN_PASSWORD_PLAIN || process.env.NUXT_ADMIN_PASSWORD_PLAIN || '',
    mcVisible: process.env.MC_VISIBLE || '',
    mcStatus: process.env.MC_STATUS || '',
    dataDir: defaultDataDir,
    public: {}
  }
})
