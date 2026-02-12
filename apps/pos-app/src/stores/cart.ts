import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Product } from '@pos-food/core'

export interface CartItem {
    product: Product
    quantity: number
}

export const useCartStore = defineStore('cart', () => {
    const items = ref<CartItem[]>([])

    const itemCount = computed(() =>
        items.value.reduce((sum, item) => sum + item.quantity, 0),
    )

    const subtotal = computed(() =>
        items.value.reduce((sum, item) => sum + item.product.price * item.quantity, 0),
    )

    const taxTotal = computed(() =>
        items.value.reduce(
            (sum, item) => sum + (item.product.price * item.quantity * item.product.taxRate) / 100,
            0,
        ),
    )

    const total = computed(() => subtotal.value + taxTotal.value)

    function addItem(product: Product, quantity = 1) {
        const existing = items.value.find(i => i.product.id === product.id)
        if (existing) {
            existing.quantity += quantity
        }
        else {
            items.value.push({ product, quantity })
        }
    }

    function removeItem(productId: string) {
        items.value = items.value.filter(i => i.product.id !== productId)
    }

    function updateQuantity(productId: string, quantity: number) {
        const item = items.value.find(i => i.product.id === productId)
        if (item) {
            if (quantity <= 0) {
                removeItem(productId)
            }
            else {
                item.quantity = quantity
            }
        }
    }

    function incrementQuantity(productId: string) {
        const item = items.value.find(i => i.product.id === productId)
        if (item) {
            item.quantity++
        }
    }

    function decrementQuantity(productId: string) {
        const item = items.value.find(i => i.product.id === productId)
        if (item) {
            if (item.quantity <= 1) {
                removeItem(productId)
            }
            else {
                item.quantity--
            }
        }
    }

    function clear() {
        items.value = []
    }

    return {
        items,
        itemCount,
        subtotal,
        taxTotal,
        total,
        addItem,
        removeItem,
        updateQuantity,
        incrementQuantity,
        decrementQuantity,
        clear,
    }
})
