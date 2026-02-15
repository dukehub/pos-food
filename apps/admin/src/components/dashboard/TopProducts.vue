<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const columns = [
  { accessorKey: 'rank', header: () => t('dashboard.topProducts.rank') },
  { accessorKey: 'product', header: () => t('dashboard.topProducts.product') },
  { accessorKey: 'category', header: () => t('dashboard.topProducts.category') },
  { accessorKey: 'qty', header: () => t('dashboard.topProducts.qty') },
  { accessorKey: 'revenue', header: () => t('dashboard.topProducts.revenue') }
]

const rows = [
  { rank: 1, product: 'Pizza Margherita', category: 'Pizzas', qty: 42, revenue: '25 200 DA' },
  { rank: 2, product: 'Burger Classic', category: 'Burgers', qty: 38, revenue: '22 800 DA' },
  { rank: 3, product: 'Salade César', category: 'Salades', qty: 27, revenue: '10 800 DA' },
  { rank: 4, product: 'Tacos Poulet', category: 'Tacos', qty: 24, revenue: '12 000 DA' },
  { rank: 5, product: 'Limonade Maison', category: 'Boissons', qty: 56, revenue: '11 200 DA' }
]
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-trophy" class="text-amber-500 size-5" />
        <h3 class="text-base font-semibold">{{ t('dashboard.topProducts.title') }}</h3>
      </div>
    </template>

    <UTable :data="rows" :columns="columns" />
  </UCard>
</template>
