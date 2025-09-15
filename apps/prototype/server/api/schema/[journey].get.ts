import { H3Event, getRouterParams, sendError, createError } from 'h3'
import { loadYamlFromData } from '~/server/utils/data'
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
    // Check for KYCP format first, then fall back to legacy format
    let parsed
    let isKycpFormat = false
    
    try {
      // Try KYCP format first
      parsed = await loadYamlFromData(event, `schemas/${journey}/schema-kycp.yaml`)
      isKycpFormat = true
    } catch {
      // Fall back to legacy format
      parsed = await loadYamlFromData(event, `schemas/${journey}/schema.yaml`)
    }
    
    // Skip validation for KYCP format (has different structure)
    if (!isKycpFormat) {
      // Validate schema structure for legacy format
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
    }
    
    // Return KYCP format directly
    return parsed
  } catch (err: any) {
    // Don't expose file system errors to client
    console.error(`Failed to load schema for journey ${journey}:`, err)
    return sendError(event, createError({ 
      statusCode: 404, 
      statusMessage: 'Schema not found' 
    }))
  }
})
