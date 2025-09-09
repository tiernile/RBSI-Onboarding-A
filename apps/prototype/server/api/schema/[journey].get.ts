import { H3Event, getRouterParams, sendError, createError } from 'h3'
import { readFile } from 'node:fs/promises'
import { join } from 'node:path'
import YAML from 'yaml'
import { validateJourneySlug } from '~/server/utils/validation'

export default defineEventHandler(async (event: H3Event) => {
  const { journey } = getRouterParams(event)
  const config = useRuntimeConfig(event)
  
  // Validate journey parameter to prevent path traversal
  if (!validateJourneySlug(journey)) {
    return sendError(event, createError({ 
      statusCode: 400, 
      statusMessage: 'Invalid journey identifier' 
    }))
  }
  
  try {
    const p = join(config.dataDir, 'schemas', journey, 'schema.yaml')
    const raw = await readFile(p, 'utf8')
    const parsed = YAML.parse(raw)
    
    // Validate schema structure
    const { validateSchema } = await import('~/server/utils/schema-validator')
    const validation = validateSchema(parsed)
    
    if (!validation.valid) {
      console.error(`Invalid schema for journey ${journey}:`, validation.errors)
      return sendError(event, createError({ 
        statusCode: 500, 
        statusMessage: 'Schema validation failed',
        data: process.env.NODE_ENV === 'development' ? validation.errors : undefined
      }))
    }
    
    return validation.data
  } catch (err: any) {
    // Don't expose file system errors to client
    console.error(`Failed to load schema for journey ${journey}:`, err)
    return sendError(event, createError({ 
      statusCode: 404, 
      statusMessage: 'Schema not found' 
    }))
  }
})
