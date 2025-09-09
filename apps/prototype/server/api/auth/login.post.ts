import { H3Event, readBody, setCookie, getHeader } from 'h3'
import bcrypt from 'bcryptjs'

type Attempts = { fails: number; until?: number }
const attempts = new Map<string, Attempts>()

export default defineEventHandler(async (event: H3Event) => {
  const config = useRuntimeConfig(event)
  const { password } = await readBody<{ password: string }>(event)

  // Basic IP-based rate limit/lockout (in-memory)
  const ip = getHeader(event, 'x-forwarded-for')?.split(',')[0]?.trim() || (event.node.req.socket.remoteAddress || 'unknown')
  const rec = attempts.get(ip) || { fails: 0 }
  const now = Date.now()
  if (rec.until && rec.until > now) {
    const secs = Math.ceil((rec.until - now) / 1000)
    return { ok: false, error: `Too many attempts. Try again in ${secs}s.` }
  }

  const hash = config.adminPasswordHash || process.env.NUXT_ADMIN_PASSWORD_HASH || process.env.NEXT_ADMIN_PASSWORD_HASH || ''
  if (!hash) {
    return { ok: false, error: 'Admin hash not configured. Set NUXT_ADMIN_PASSWORD_HASH in apps/prototype/.env' }
  }

  const ok = await bcrypt.compare(password || '', hash)
  if (!ok) {
    rec.fails = (rec.fails || 0) + 1
    if (rec.fails >= 5) {
      rec.until = now + 15 * 60 * 1000 // 15 minutes lockout
      rec.fails = 0
    }
    attempts.set(ip, rec)
    return { ok: false, error: 'Invalid credentials' }
  }

  // success → reset attempts
  attempts.delete(ip)

  // Simple session cookie for admin with production security
  const isProduction = process.env.NODE_ENV === 'production'
  setCookie(event, 'admin', 'true', {
    httpOnly: true,
    secure: isProduction, // Require HTTPS in production
    sameSite: 'strict',
    path: '/',
    maxAge: 60 * 60 // 1 hour
  })
  return { ok: true }
})
