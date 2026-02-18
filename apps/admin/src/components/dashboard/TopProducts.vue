<script setup lang="ts">
const products = [
  { name: 'Cheeseburger', qty: 145, revenue: '$1,250' },
  { name: 'French Fries', qty: 300, revenue: '$900' },
  { name: 'Coke', qty: 250, revenue: '$500' },
  { name: 'Pizza Margherita', qty: 80, revenue: '$1,100' },
]

const columns = [
  { key: 'name', label: 'Product', id: 'name' },
  { key: 'qty', label: 'Sold', id: 'qty' },
  { key: 'revenue', label: 'Revenue', id: 'revenue' },
] as any[]
</script>

<template>
  <UCard>
    <template #header>
      <h3 class="text-base font-semibold">Top Products</h3>
    </template>
    <UTable :rows="products" :columns="columns" />
  </UCard>
</template>
