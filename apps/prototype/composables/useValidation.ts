export type SchemaItem = {
  id: string
  label: string
  mandatory?: boolean
  validation?: { regex?: string | null }
  visibility?: { all?: string[] }
}

import { isVisible } from './useConditions'

export function useValidation(items: SchemaItem[], answers: Record<string, any>) {
  const errors = reactive<Record<string, string>>({})

  function validate() {
    Object.keys(errors).forEach(k => delete errors[k])
    for (const item of items) {
      const visible = isVisible(item.visibility as any, answers)
      if (!visible) continue
      const val = answers[item.id]
      if (item.mandatory && (val === undefined || val === null || String(val).trim() === '')) {
        errors[item.id] = `${item.label} is required`
        continue
      }
      const regex = item.validation?.regex
      if (regex && val) {
        try {
          const re = new RegExp(regex)
          if (!re.test(String(val))) {
            errors[item.id] = `${item.label} is in the wrong format`
          }
        } catch {}
      }
    }
    return Object.keys(errors).length === 0
  }

  return { errors, validate }
}

