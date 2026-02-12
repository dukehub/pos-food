import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Product, Category } from '@pos-food/core'

export const useProductsStore = defineStore('products', () => {
    const products = ref<Product[]>([])
    const categories = ref<Category[]>([])
    const isLoading = ref(false)
    const error = ref<string | null>(null)
    const searchQuery = ref('')

    const filteredProducts = computed(() => {
        if (!searchQuery.value) return products.value
        const q = searchQuery.value.toLowerCase()
        return products.value.filter(
            p => p.name.toLowerCase().includes(q)
                || p.barcode?.toLowerCase().includes(q)
                || p.sku?.toLowerCase().includes(q),
        )
    })

    const productsByCategory = computed(() => {
        const map = new Map<string, Product[]>()
        for (const product of products.value) {
            const list = map.get(product.categoryId) ?? []
            list.push(product)
            map.set(product.categoryId, list)
        }
        return map
    })

    const activeProducts = computed(() =>
        products.value.filter(p => p.isActive),
    )

    const activeCategories = computed(() =>
        categories.value.filter(c => c.isActive),
    )

    // --- Actions (will connect to API later) ---

    function setProducts(data: Product[]) {
        products.value = data
    }

    function setCategories(data: Category[]) {
        categories.value = data
    }

    function addProduct(product: Product) {
        products.value.push(product)
    }

    function updateProduct(updated: Product) {
        const index = products.value.findIndex(p => p.id === updated.id)
        if (index !== -1) {
            products.value[index] = updated
        }
    }

    function removeProduct(id: string) {
        products.value = products.value.filter(p => p.id !== id)
    }

    function addCategory(category: Category) {
        categories.value.push(category)
    }

    function updateCategory(updated: Category) {
        const index = categories.value.findIndex(c => c.id === updated.id)
        if (index !== -1) {
            categories.value[index] = updated
        }
    }

    function removeCategory(id: string) {
        categories.value = categories.value.filter(c => c.id !== id)
    }

    return {
        products,
        categories,
        isLoading,
        error,
        searchQuery,
        filteredProducts,
        productsByCategory,
        activeProducts,
        activeCategories,
        setProducts,
        setCategories,
        addProduct,
        updateProduct,
        removeProduct,
        addCategory,
        updateCategory,
        removeCategory,
    }
})
