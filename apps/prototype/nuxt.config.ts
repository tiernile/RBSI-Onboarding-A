import { defineNuxtConfig } from 'nuxt/config'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const here = fileURLToPath(new URL('.', import.meta.url))
const defaultDataDir = process.env.DATA_DIR || process.env.NUXT_DATA_DIR || path.resolve(here, '..', '..', 'data')

export default defineNuxtConfig({
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
