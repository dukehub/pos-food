<script setup lang="ts">
import { ref, reactive, watch, onMounted } from 'vue'
import { apiClient } from '@pos/api'

const props = defineProps<{
    productId?: string | null
}>()

const emit = defineEmits(['close', 'refresh'])

const categories = ref<any[]>([])
const loading = ref(false)

// State
const form = reactive({
    name: '',
    slug: '',
    description: '',
    sku: '',
    is_active: true,
    category_id: '',
    modifier_group_ids: [] as string[],
    variants: [] as any[]
})

const modifierGroups = ref<any[]>([])

// Tabs
const items = [{
  slot: 'general',
  label: 'General'
}, {
  slot: 'variants',
  label: 'Variants'
}, {
  slot: 'modifiers',
  label: 'Modifiers'
}]
const selectedTab = ref(0)
const selectedTabItem = ref('general')

function onTabChange(index: number) {
    selectedTab.value = index
    selectedTabItem.value = items[index].slot
}

// Load Data
onMounted(async () => {
    try {
        const [catsRes, modsRes] = await Promise.all([
            apiClient.get<any[]>('/plugins/catalog_product/categories'),
            apiClient.get<any[]>('/plugins/catalog_product/modifiers')
        ])
        categories.value = catsRes.data
        modifierGroups.value = modsRes.data

        if (props.productId) {
            loading.value = true
            const res = await apiClient.get<any>(`/plugins/catalog_product/products/${props.productId}`)
            const data = res.data
            Object.assign(form, {
                name: data.name,
                slug: data.slug,
                description: data.description,
                sku: data.sku,
                is_active: data.is_active,
                category_id: data.category_id,
                modifier_group_ids: data.modifier_groups.map((g: any) => g.id),
                variants: data.variants || []
            })
            loading.value = false
        }
    } catch (e) {
        console.error(e)
    }
})

// Variant Management
function addVariant() {
    form.variants.push({
        name: '',
        variant_key: '',
        default_price: 0,
        sku: '',
        is_active: true,
        modifier_group_ids: []
    })
}

function removeVariant(index: number) {
    form.variants.splice(index, 1)
}

// Submit
async function submit() {
    loading.value = true
    try {
        if (props.productId) {
             await apiClient.put(`/plugins/catalog_product/products/${props.productId}`, form)
        } else {
             await apiClient.post('/plugins/catalog_product/products', form)
        }
        emit('refresh')
        emit('close')
    } catch (e) {
        console.error(e)
        alert('Failed to save product')
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <div class="h-full flex flex-col">
    <UTabs v-model="selectedTab" :items="items" class="w-full" @change="onTabChange">
        <template #general="{ item }">
            <div class="space-y-4 py-4">
                <UFormGroup label="Name" required>
                    <UInput v-model="form.name" />
                </UFormGroup>
                <UFormGroup label="Slug" required>
                    <UInput v-model="form.slug" />
                </UFormGroup>
                 <div class="grid grid-cols-2 gap-4">
                    <UFormGroup label="Category">
                        <USelectMenu 
                            v-model="form.category_id" 
                            :options="categories" 
                            value-attribute="id" 
                            option-attribute="name"
                        />
                    </UFormGroup>
                    <UFormGroup label="SKU">
                        <UInput v-model="form.sku" />
                    </UFormGroup>
                </div>
                <UFormGroup label="Description">
                    <UTextarea v-model="form.description" :rows="3" />
                </UFormGroup>
                <UFormGroup label="Status">
                     <UToggle v-model="form.is_active" />
                </UFormGroup>
            </div>
        </template>

        <template #variants="{ item }">
            <div class="space-y-4 py-4">
                <div class="flex justify-end">
                    <UButton size="xs" icon="i-heroicons-plus" @click="addVariant">Add Variant</UButton>
                </div>
                <div v-for="(variant, index) in form.variants" :key="index" class="p-4 border rounded-md relative space-y-2">
                    <UButton icon="i-heroicons-trash" color="error" variant="ghost" size="xs" class="absolute top-2 right-2" @click="removeVariant(index)" />
                    <div class="grid grid-cols-2 gap-4">
                        <UFormGroup label="Name" required>
                            <UInput v-model="variant.name" placeholder="Small, Large..." />
                        </UFormGroup>
                        <UFormGroup label="Key" required>
                            <UInput v-model="variant.variant_key" placeholder="small, large" />
                        </UFormGroup>
                        <UFormGroup label="Price" required>
                            <UInput v-model.number="variant.default_price" type="number" step="0.01" />
                        </UFormGroup>
                         <UFormGroup label="SKU">
                            <UInput v-model="variant.sku" />
                        </UFormGroup>
                    </div>
                </div>
                 <div v-if="form.variants.length === 0" class="text-center text-gray-500 py-8">
                    No variants added.
                </div>
            </div>
        </template>

        <template #modifiers="{ item }">
             <div class="space-y-4 py-4">
                 <UFormGroup label="Available Modifier Groups">
                    <USelectMenu 
                        v-model="form.modifier_group_ids" 
                        :options="modifierGroups" 
                        value-attribute="id" 
                        option-attribute="name" 
                        multiple 
                    />
                </UFormGroup>
                <p class="text-sm text-gray-500">Selected groups will be available for all variants unless overridden.</p>
             </div>
        </template>
    </UTabs>

    <div class="mt-auto pt-4 flex justify-end gap-2 border-t">
        <UButton variant="ghost" @click="$emit('close')">Cancel</UButton>
        <UButton :loading="loading" @click="submit">Save Product</UButton>
    </div>
  </div>
</template>
