/**
 * @pos/validation — Shared Zod v4 schemas + VeeValidate integration
 */
export { toTypedSchema } from '@vee-validate/zod'
export { z } from 'zod'

// ---------- Common Schemas (Zod v4 API) ----------

import { z } from 'zod'

/** Non-empty trimmed string */
export const requiredString = z.string().check(
  z.minLength(1)
)

/** Email address */
export const emailSchema = z.email()

/** URL */
export const urlSchema = z.url()

/** Positive currency amount */
export const currencyAmount = z.number().check(
  z.positive(),
  z.multipleOf(0.01)
)

/** Positive integer quantity */
export const quantitySchema = z.int().check(z.positive())

/** UUID */
export const uuidSchema = z.uuid()
