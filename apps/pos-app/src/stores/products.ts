import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { Product, Category } from '@pos-food/core'

export const useProductsStore = defineStore('products', () => {
    const products = ref<Product[]>([])
    const categories = ref<Category[]>([])
    const isLoading = ref(false)
    const selectedCategoryId = ref<string | null>(null)

    const activeProducts = computed(() =>
        products.value.filter(p => p.isActive),
    )

    const activeCategories = computed(() =>
        categories.value.filter(c => c.isActive),
    )

    const filteredProducts = computed(() => {
        const list = activeProducts.value
        if (!selectedCategoryId.value) return list
        return list.filter(p => p.categoryId === selectedCategoryId.value)
    })

    function setProducts(data: Product[]) {
        products.value = data
    }

    function setCategories(data: Category[]) {
        categories.value = data
    }

    function selectCategory(id: string | null) {
        selectedCategoryId.value = id
    }

    function findByBarcode(barcode: string): Product | undefined {
        return products.value.find(p => p.barcode === barcode && p.isActive)
    }

    return {
        products,
        categories,
        isLoading,
        selectedCategoryId,
        activeProducts,
        activeCategories,
        filteredProducts,
        setProducts,
        setCategories,
        selectCategory,
        findByBarcode,
    }
})
