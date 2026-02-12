import { z } from 'zod'

// ─── Table Status ──────────────────────────────────────────
export const TableStatusEnum = z.enum([
    'free',
    'occupied',
    'reserved',
    'cleaning',
])

export type TableStatus = z.infer<typeof TableStatusEnum>

// ─── Restaurant Table ──────────────────────────────────────
export const RestaurantTableSchema = z.object({
    id: z.string().uuid(),
    number: z.number().int().positive(),
    name: z.string().min(1),
    seats: z.number().int().positive(),
    zone: z.string().optional(),
    status: TableStatusEnum.default('free'),
    currentOrderId: z.string().uuid().optional(),
    posX: z.number().optional(),
    posY: z.number().optional(),
    isActive: z.boolean().default(true),
    createdAt: z.string().datetime(),
    updatedAt: z.string().datetime(),
})

export type RestaurantTable = z.infer<typeof RestaurantTableSchema>

export const RestaurantTableCreateSchema = RestaurantTableSchema.omit({
    id: true,
    currentOrderId: true,
    createdAt: true,
    updatedAt: true,
})

export type RestaurantTableCreate = z.infer<typeof RestaurantTableCreateSchema>
