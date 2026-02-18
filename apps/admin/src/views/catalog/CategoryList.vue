<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiClient } from '@pos/api'

interface Category {
    id: string
    name: string
    slug: string
    is_active: boolean
    sort_order: number
}

const categories = ref<Category[]>([])
const loading = ref(false)
const isModalOpen = ref(false)
const selectedCategory = ref<Category | null>(null)
const formData = ref({ name: '', slug: '', is_active: true, sort_order: 0 })

const columns = [
    { key: 'name', label: 'Name' },
    { key: 'slug', label: 'Slug' },
    { key: 'sort_order', label: 'Order' },
    { key: 'is_active', label: 'Status' },
    { key: 'actions', label: '' }
] as any[]

async function loadCategories() {
    loading.value = true
    try {
        const res = await apiClient.get<Category[]>('/plugins/catalog_product/categories')
        categories.value = res.data
    } catch {} finally {
        loading.value = false
    }
}

function openCreate() {
    selectedCategory.value = null
    formData.value = { name: '', slug: '', is_active: true, sort_order: 0 }
    isModalOpen.value = true
}

function openEdit(cat: Category) {
    selectedCategory.value = cat
    formData.value = { ...cat }
    isModalOpen.value = true
}

async function submit() {
    try {
        if (selectedCategory.value) {
            await apiClient.put(`/plugins/catalog_product/categories/${selectedCategory.value.id}`, formData.value)
        } else {
            await apiClient.post('/plugins/catalog_product/categories', formData.value)
        }
        isModalOpen.value = false
        loadCategories()
    } catch (e) {
        alert('Failed to save category')
    }
}

async function deleteCategory(cat: Category) {
    if (!confirm('Delete category?')) return
    try {
        await apiClient.delete(`/plugins/catalog_product/categories/${cat.id}`)
        loadCategories()
    } catch {}
}

onMounted(() => loadCategories())
</script>

<template>
  <UCard>
    <template #header>
        <div class="flex justify-between items-center">
            <h3 class="font-semibold">Categories</h3>
            <UButton size="xs" icon="i-heroicons-plus" @click="openCreate">Add</UButton>
        </div>
    </template>
    
    <UTable :rows="categories" :columns="columns" :loading="loading">
        <template #is_active-data="props">
            <UBadge :color="(props as any).row.is_active ? 'success' : 'neutral'" variant="subtle" size="xs">
                {{ (props as any).row.is_active ? 'Active' : 'Inactive' }}
            </UBadge>
        </template>
        <template #actions-data="props">
             <div class="flex gap-2 justify-end">
                <UButton icon="i-heroicons-pencil-square" variant="ghost" size="xs" @click="openEdit((props as any).row)" />
                <UButton icon="i-heroicons-trash" color="error" variant="ghost" size="xs" @click="deleteCategory((props as any).row)" />
             </div>
        </template>
    </UTable>

    <UModal v-model="isModalOpen">
        <div class="p-6 space-y-4">
            <h3 class="font-bold">{{ selectedCategory ? 'Edit' : 'New' }} Category</h3>
            <UFormGroup label="Name" required>
                <UInput v-model="formData.name" />
            </UFormGroup>
            <UFormGroup label="Slug" required>
                <UInput v-model="formData.slug" />
            </UFormGroup>
            <div class="grid grid-cols-2 gap-2">
                 <UFormGroup label="Order">
                    <UInput v-model.number="formData.sort_order" type="number" />
                </UFormGroup>
                <UFormGroup label="Status">
                     <UToggle v-model="formData.is_active" />
                </UFormGroup>
            </div>
            <div class="flex justify-end gap-2">
                <UButton variant="ghost" @click="isModalOpen = false">Cancel</UButton>
                <UButton @click="submit">Save</UButton>
            </div>
        </div>
    </UModal>
  </UCard>
</template>
