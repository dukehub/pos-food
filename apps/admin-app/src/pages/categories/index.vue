<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { PageHeader } from '@pos-food/ui'
import { useProductsStore } from '../../stores/products'

const { t } = useI18n()
const productsStore = useProductsStore()

// Demo categories
productsStore.setCategories([
  {
    id: '1', name: 'Plats', description: 'Plats principaux', color: '#3b82f6',
    sortOrder: 0, isActive: true,
    createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
  },
  {
    id: '2', name: 'Pizzas', description: 'Pizzas et focaccias', color: '#ef4444',
    sortOrder: 1, isActive: true,
    createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
  },
  {
    id: '3', name: 'Boissons', description: 'Boissons fraîches et chaudes', color: '#22c55e',
    sortOrder: 2, isActive: true,
    createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
  },
])
</script>

<template>
  <div class="flex flex-1 flex-col overflow-auto">
    <PageHeader :title="t('admin.nav.categories')">
      <template #actions>
        <UButton
          :label="t('common.create')"
          icon="i-lucide-plus"
          color="primary"
        />
      </template>
    </PageHeader>

    <div class="flex-1 p-6">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
        <UCard
          v-for="category in productsStore.activeCategories"
          :key="category.id"
        >
          <div class="flex items-start justify-between">
            <div class="flex items-center gap-3">
              <div
                class="size-4 rounded-full"
                :style="{ backgroundColor: category.color }"
              />
              <div>
                <p class="font-medium">{{ category.name }}</p>
                <p class="text-sm text-[var(--ui-text-muted)]">{{ category.description }}</p>
              </div>
            </div>
            <div class="flex gap-1">
              <UButton variant="ghost" icon="i-lucide-pencil" size="xs" />
              <UButton variant="ghost" icon="i-lucide-trash-2" size="xs" color="error" />
            </div>
          </div>
        </UCard>
      </div>

      <div v-if="productsStore.activeCategories.length === 0" class="py-12 text-center text-[var(--ui-text-muted)]">
        {{ t('common.no_results') }}
      </div>
    </div>
  </div>
</template>
