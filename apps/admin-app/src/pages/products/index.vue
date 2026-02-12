<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { PageHeader } from '@pos-food/ui'
import { useProductsStore } from '../../stores/products'

const { t } = useI18n()
const productsStore = useProductsStore()

// Demo data for now
productsStore.setProducts([
  {
    id: '1', name: 'Burger Classic', description: 'Boeuf, salade, tomate', price: 12.50,
    categoryId: '1', taxRate: 10, isActive: true, sortOrder: 0,
    createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
  },
  {
    id: '2', name: 'Pizza Margherita', description: 'Tomate, mozzarella, basilic', price: 11.00,
    categoryId: '2', taxRate: 10, isActive: true, sortOrder: 1,
    createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
  },
  {
    id: '3', name: 'Salade César', description: 'Poulet, parmesan, croûtons', price: 9.50,
    categoryId: '1', taxRate: 10, isActive: true, sortOrder: 2,
    createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
  },
  {
    id: '4', name: 'Coca-Cola', description: '33cl', price: 3.50,
    categoryId: '3', taxRate: 20, isActive: true, sortOrder: 0,
    createdAt: new Date().toISOString(), updatedAt: new Date().toISOString(),
  },
])
</script>

<template>
  <div class="flex flex-1 flex-col overflow-auto">
    <PageHeader :title="t('admin.nav.products')">
      <template #actions>
        <UInput
          v-model="productsStore.searchQuery"
          :placeholder="t('common.search')"
          icon="i-lucide-search"
          size="sm"
          class="w-64"
        />
        <UButton
          :label="t('common.create')"
          icon="i-lucide-plus"
          color="primary"
          to="/products/new"
        />
      </template>
    </PageHeader>

    <div class="flex-1 p-6">
      <UCard>
        <table class="w-full text-left text-sm">
          <thead>
            <tr class="border-b border-[var(--ui-border)]">
              <th class="pb-3 font-medium">{{ t('common.name') }}</th>
              <th class="pb-3 font-medium">{{ t('common.description') }}</th>
              <th class="pb-3 font-medium">{{ t('common.price') }}</th>
              <th class="pb-3 font-medium">{{ t('common.tax') }}</th>
              <th class="pb-3 font-medium">{{ t('common.status') }}</th>
              <th class="pb-3 font-medium">{{ t('common.actions') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="product in productsStore.filteredProducts"
              :key="product.id"
              class="border-b border-[var(--ui-border)] last:border-0"
            >
              <td class="py-3 font-medium">{{ product.name }}</td>
              <td class="py-3 text-[var(--ui-text-muted)]">{{ product.description }}</td>
              <td class="py-3">{{ product.price.toFixed(2) }} €</td>
              <td class="py-3">{{ product.taxRate }}%</td>
              <td class="py-3">
                <UBadge :color="product.isActive ? 'success' : 'neutral'">
                  {{ product.isActive ? 'Actif' : 'Inactif' }}
                </UBadge>
              </td>
              <td class="py-3">
                <div class="flex gap-1">
                  <UButton variant="ghost" icon="i-lucide-pencil" size="xs" />
                  <UButton variant="ghost" icon="i-lucide-trash-2" size="xs" color="error" />
                </div>
              </td>
            </tr>
          </tbody>
        </table>

        <div v-if="productsStore.filteredProducts.length === 0" class="py-8 text-center text-[var(--ui-text-muted)]">
          {{ t('common.no_results') }}
        </div>
      </UCard>
    </div>
  </div>
</template>
