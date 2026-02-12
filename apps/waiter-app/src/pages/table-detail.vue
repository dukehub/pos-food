<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useTablesStore } from '../stores/tables'

const { t } = useI18n()
const route = useRoute()
const tablesStore = useTablesStore()

const tableId = computed(() => route.params.id as string)
const table = computed(() => tablesStore.tables.find(t => t.id === tableId.value))

const demoMenu = [
  { id: '1', name: 'Burger Classic', price: 12.50, category: 'Plats' },
  { id: '2', name: 'Pizza Margherita', price: 11.00, category: 'Pizzas' },
  { id: '3', name: 'Salade César', price: 9.50, category: 'Plats' },
  { id: '4', name: 'Coca-Cola', price: 3.50, category: 'Boissons' },
  { id: '5', name: 'Eau Minérale', price: 2.50, category: 'Boissons' },
  { id: '6', name: 'Tiramisu', price: 7.00, category: 'Desserts' },
]
</script>

<template>
  <div class="flex flex-1 flex-col p-4">
    <!-- Header -->
    <div class="mb-4 flex items-center gap-3">
      <UButton
        icon="i-lucide-arrow-left"
        variant="ghost"
        to="/"
      />
      <h1 class="text-xl font-bold">
        {{ table ? `Table ${table.number}` : 'Table' }}
      </h1>
      <UBadge v-if="table" :color="table.status === 'free' ? 'success' : 'error'" size="xs">
        {{ table.status }}
      </UBadge>
    </div>

    <div v-if="table">
      <!-- Info -->
      <UCard class="mb-4">
        <div class="flex items-center justify-between">
          <div>
            <p class="text-sm text-[var(--ui-text-muted)]">{{ table.seats }} places · {{ table.zone }}</p>
          </div>
          <div class="flex gap-2">
            <UButton
              :label="t('waiter.order.new_order')"
              icon="i-lucide-plus"
              size="sm"
              color="primary"
            />
            <UButton
              :label="t('waiter.order.request_bill')"
              icon="i-lucide-receipt"
              size="sm"
              variant="outline"
            />
          </div>
        </div>
      </UCard>

      <!-- Quick add menu -->
      <h2 class="mb-3 text-sm font-medium text-[var(--ui-text-muted)] uppercase">
        {{ t('waiter.order.add_item') }}
      </h2>

      <div class="grid grid-cols-2 gap-2">
        <button
          v-for="item in demoMenu"
          :key="item.id"
          class="flex items-center justify-between rounded-lg border border-[var(--ui-border)] bg-[var(--ui-bg)] p-3 text-left transition-all active:scale-95"
        >
          <div>
            <p class="text-sm font-medium">{{ item.name }}</p>
            <p class="text-xs text-[var(--ui-text-muted)]">{{ item.category }}</p>
          </div>
          <span class="text-sm font-bold">{{ item.price.toFixed(2) }} €</span>
        </button>
      </div>

      <!-- Send to kitchen -->
      <div class="mt-6">
        <UButton
          :label="t('waiter.order.send_kitchen')"
          icon="i-lucide-chef-hat"
          block
          size="xl"
          color="primary"
        />
      </div>
    </div>

    <div v-else class="flex flex-1 items-center justify-center text-[var(--ui-text-muted)]">
      <p>Table introuvable</p>
    </div>
  </div>
</template>
