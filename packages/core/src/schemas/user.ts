import { z } from 'zod'

// ─── User Role ─────────────────────────────────────────────
export const UserRoleEnum = z.enum([
    'admin',
    'manager',
    'cashier',
    'waiter',
])

export type UserRole = z.infer<typeof UserRoleEnum>

// ─── User ──────────────────────────────────────────────────
export const UserSchema = z.object({
    id: z.string().uuid(),
    email: z.string().email(),
    firstName: z.string().min(1),
    lastName: z.string().min(1),
    role: UserRoleEnum,
    pin: z.string().length(4).optional(),
    isActive: z.boolean().default(true),
    createdAt: z.string().datetime(),
    updatedAt: z.string().datetime(),
})

export type User = z.infer<typeof UserSchema>

export const UserCreateSchema = UserSchema.omit({
    id: true,
    createdAt: true,
    updatedAt: true,
})

export type UserCreate = z.infer<typeof UserCreateSchema>

// ─── Login ─────────────────────────────────────────────────
export const LoginSchema = z.object({
    email: z.string().email(),
    password: z.string().min(6),
})

export type LoginCredentials = z.infer<typeof LoginSchema>

export const PinLoginSchema = z.object({
    pin: z.string().length(4),
})

export type PinLoginCredentials = z.infer<typeof PinLoginSchema>
