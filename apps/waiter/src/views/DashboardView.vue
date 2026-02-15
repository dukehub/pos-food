<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ExtensionPoint } from '@pos/ui'

const { t } = useI18n()

// Demo context for the table sidebar extension point
const tableCtx = {
  tableId: 'table-05',
  tableName: 'Table 5',
  zone: 'Terrasse',
  seats: 4
}
</script>

<template>
  <div class="min-h-screen flex flex-col gap-8 p-8">
    <!-- Header -->
    <div class="flex items-center gap-3">
      <UIcon name="i-lucide-users" class="size-8 text-primary" />
      <h1 class="text-2xl font-bold">Waiter — {{ t('nav.tables') }}</h1>
    </div>

    <!-- Table Detail with sidebar -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Main content -->
      <div class="md:col-span-2">
        <UCard>
          <template #header>
            <h2 class="text-lg font-semibold">{{ tableCtx.tableName }}</h2>
          </template>
          <p class="text-muted">{{ t('common.loading') }}</p>
          <template #footer>
            <div class="flex gap-2">
              <UButton :label="t('nav.orders')" icon="i-lucide-clipboard-list" variant="soft" />
            </div>
          </template>
        </UCard>
      </div>

      <!-- Sidebar — plugin widgets -->
      <div class="flex flex-col gap-4">
        <ExtensionPoint
          name="waiter.table.sidebar.widgets"
          :ctx="tableCtx"
          tag="div"
          class="flex flex-col gap-4"
        >
          <template #empty>
            <p class="text-xs text-muted italic">Aucun widget actif.</p>
          </template>
        </ExtensionPoint>
      </div>
    </div>
  </div>
</template>
