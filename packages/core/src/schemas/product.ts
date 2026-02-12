import { z } from 'zod'

// ─── Category ──────────────────────────────────────────────
export const CategorySchema = z.object({
    id: z.string().uuid(),
    name: z.string().min(1),
    description: z.string().optional(),
    color: z.string().optional(),
    icon: z.string().optional(),
    sortOrder: z.number().int().default(0),
    isActive: z.boolean().default(true),
    createdAt: z.string().datetime(),
    updatedAt: z.string().datetime(),
})

export type Category = z.infer<typeof CategorySchema>

export const CategoryCreateSchema = CategorySchema.omit({
    id: true,
    createdAt: true,
    updatedAt: true,
})

export type CategoryCreate = z.infer<typeof CategoryCreateSchema>

// ─── Product ───────────────────────────────────────────────
export const ProductSchema = z.object({
    id: z.string().uuid(),
    name: z.string().min(1),
    description: z.string().optional(),
    price: z.number().positive(),
    categoryId: z.string().uuid(),
    image: z.string().url().optional(),
    barcode: z.string().optional(),
    sku: z.string().optional(),
    taxRate: z.number().min(0).max(100).default(20),
    isActive: z.boolean().default(true),
    sortOrder: z.number().int().default(0),
    createdAt: z.string().datetime(),
    updatedAt: z.string().datetime(),
})

export type Product = z.infer<typeof ProductSchema>

export const ProductCreateSchema = ProductSchema.omit({
    id: true,
    createdAt: true,
    updatedAt: true,
})

export type ProductCreate = z.infer<typeof ProductCreateSchema>
