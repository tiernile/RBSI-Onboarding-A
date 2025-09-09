/**
 * Server-side validation utilities for security
 */

/**
 * Validate journey slug to prevent path traversal
 * Only allows alphanumeric characters and hyphens
 */
export function validateJourneySlug(journey: string): boolean {
  if (!journey || typeof journey !== 'string') {
    return false;
  }
  
  // Reject if contains path traversal patterns
  if (journey.includes('..') || journey.includes('/') || journey.includes('\\')) {
    return false;
  }
  
  // Only allow safe slug format
  return /^[a-z0-9-]+$/i.test(journey);
}

/**
 * Escape CSV cell value to prevent injection attacks
 * Prefixes formula triggers and properly quotes special characters
 */
export function escapeCSVCell(value: any): string {
  if (value === null || value === undefined) {
    return '';
  }
  
  let stringValue = String(value);
  
  // Prefix formula triggers with single quote to prevent execution
  if (/^[=+@\-]/.test(stringValue)) {
    stringValue = "'" + stringValue;
  }
  
  // Quote if contains comma, newline, or quote
  if (/[,\n\r"]/.test(stringValue)) {
    stringValue = '"' + stringValue.replace(/"/g, '""') + '"';
  }
  
  return stringValue;
}

/**
 * Sanitize file path to prevent directory traversal
 */
export function sanitizePath(path: string): string {
  // Remove any directory traversal attempts
  return path.replace(/\.\./g, '').replace(/[\/\\]/g, '-');
}

/**
 * Validate that a value is a valid enum option
 */
export function validateEnum<T extends string>(
  value: unknown,
  validOptions: readonly T[]
): value is T {
  return typeof value === 'string' && validOptions.includes(value as T);
}

/**
 * Create CSV-safe header row
 */
export function createCSVHeader(columns: string[]): string {
  return columns.map(col => escapeCSVCell(col)).join(',');
}

/**
 * Create CSV-safe data row
 */
export function createCSVRow(values: any[]): string {
  return values.map(val => escapeCSVCell(val)).join(',');
}

/**
 * Validate origin for CSRF protection
 */
export function validateOrigin(origin: string | null, allowedOrigins: string[]): boolean {
  if (!origin) return false;
  
  // In development, allow localhost
  if (process.env.NODE_ENV === 'development') {
    if (origin.includes('localhost') || origin.includes('127.0.0.1')) {
      return true;
    }
  }
  
  return allowedOrigins.includes(origin);
}