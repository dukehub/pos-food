<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiClient } from '@pos/api'
import CategoryList from './CategoryList.vue'
import ProductForm from './ProductForm.vue'

interface Product {
    id: string
    name: string
    sku: string
    is_active: boolean
    variants: any[]
}

const products = ref<Product[]>([])
const loading = ref(false)
const isSlideoverOpen = ref(false)
const selectedProductId = ref<string | null>(null)

const columns = [
    { key: 'name', label: 'Product' },
    { key: 'sku', label: 'SKU' },
    { key: 'variants', label: 'Variants' },
    { key: 'is_active', label: 'Status' },
    { key: 'actions', label: '' }
] as any[]

async function loadProducts() {
    loading.value = true
    try {
        const res = await apiClient.get<Product[]>('/plugins/catalog_product/products')
        products.value = res.data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

function openCreate() {
    selectedProductId.value = null
    isSlideoverOpen.value = true
}

function openEdit(product: Product) {
    selectedProductId.value = product.id
    isSlideoverOpen.value = true
}

async function deleteProduct(product: Product) {
    if (!confirm(`Delete product "${product.name}"?`)) return
    try {
        await apiClient.delete(`/plugins/catalog_product/products/${product.id}`)
        loadProducts()
    } catch (e) {
        alert('Failed to delete product')
    }
}

onMounted(() => loadProducts())
</script>

<template>
  <div class="flex flex-col lg:flex-row gap-6 h-full">
    <!-- Categories Sidebar -->
    <div class="lg:w-1/4">
        <CategoryList />
    </div>

    <!-- Products Main -->
    <div class="flex-1 space-y-4">
        <div class="flex justify-between items-center">
             <h1 class="text-2xl font-bold">Products</h1>
             <UButton icon="i-heroicons-plus" @click="openCreate">Add Product</UButton>
        </div>

        <UCard>
            <UTable :rows="products" :columns="columns" :loading="loading">
                <template #variants-data="props">
                    <UBadge color="neutral" variant="subtle" size="xs">
                        {{ (props as any).row.variants?.length || 0 }} variants
                    </UBadge>
                </template>
                <template #is_active-data="props">
                    <UBadge :color="(props as any).row.is_active ? 'success' : 'neutral'" variant="subtle" size="xs">
                        {{ (props as any).row.is_active ? 'Active' : 'Inactive' }}
                    </UBadge>
                </template>
                 <template #actions-data="props">
                    <div class="flex gap-2 justify-end">
                        <UButton icon="i-heroicons-pencil-square" variant="ghost" size="xs" @click="openEdit((props as any).row)" />
                        <UButton icon="i-heroicons-trash" color="error" variant="ghost" size="xs" @click="deleteProduct((props as any).row)" />
                    </div>
                </template>
            </UTable>
        </UCard>
    </div>

    <USlideover v-model="isSlideoverOpen" :ui="{ content: 'w-screen max-w-2xl' }">
        <UCard class="flex flex-col flex-1" :ui="{ body: 'flex-1' }">
            <template #header>
                <div class="flex items-center justify-between">
                    <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
                        {{ selectedProductId ? 'Edit Product' : 'New Product' }}
                    </h3>
                    <UButton color="neutral" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1" @click="isSlideoverOpen = false" />
                </div>
            </template>

            <ProductForm :product-id="selectedProductId" @close="isSlideoverOpen = false" @refresh="loadProducts" />
        </UCard>
    </USlideover>
  </div>
</template>
