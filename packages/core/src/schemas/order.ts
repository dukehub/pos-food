import { z } from 'zod'

// ─── Order Status ──────────────────────────────────────────
export const OrderStatusEnum = z.enum([
    'draft',
    'open',
    'sent_to_kitchen',
    'in_preparation',
    'ready',
    'served',
    'paid',
    'cancelled',
])

export type OrderStatus = z.infer<typeof OrderStatusEnum>

// ─── Payment Method ────────────────────────────────────────
export const PaymentMethodEnum = z.enum([
    'cash',
    'card',
    'mixed',
])

export type PaymentMethod = z.infer<typeof PaymentMethodEnum>

// ─── Order Item ────────────────────────────────────────────
export const OrderItemSchema = z.object({
    id: z.string().uuid(),
    productId: z.string().uuid(),
    productName: z.string(),
    quantity: z.number().int().positive(),
    unitPrice: z.number().positive(),
    taxRate: z.number().min(0).max(100),
    notes: z.string().optional(),
    status: OrderStatusEnum.default('draft'),
})

export type OrderItem = z.infer<typeof OrderItemSchema>

export const OrderItemCreateSchema = OrderItemSchema.omit({
    id: true,
    productName: true,
    status: true,
})

export type OrderItemCreate = z.infer<typeof OrderItemCreateSchema>

// ─── Order ─────────────────────────────────────────────────
export const OrderSchema = z.object({
    id: z.string().uuid(),
    tableId: z.string().uuid().optional(),
    status: OrderStatusEnum.default('draft'),
    items: z.array(OrderItemSchema),
    subtotal: z.number().min(0),
    taxTotal: z.number().min(0),
    total: z.number().min(0),
    paymentMethod: PaymentMethodEnum.optional(),
    paidAmount: z.number().min(0).optional(),
    changeAmount: z.number().min(0).optional(),
    notes: z.string().optional(),
    createdBy: z.string().uuid(),
    createdAt: z.string().datetime(),
    updatedAt: z.string().datetime(),
})

export type Order = z.infer<typeof OrderSchema>

export const OrderCreateSchema = OrderSchema.omit({
    id: true,
    subtotal: true,
    taxTotal: true,
    total: true,
    paidAmount: true,
    changeAmount: true,
    createdAt: true,
    updatedAt: true,
})

export type OrderCreate = z.infer<typeof OrderCreateSchema>
