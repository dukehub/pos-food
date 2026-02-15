<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const props = defineProps<{
  tableId?: string
  tableName?: string
  zone?: string
  seats?: number
}>()
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-info" class="text-primary" />
        <span class="font-semibold">{{ t('plugins.tableInfo.title') }}</span>
      </div>
    </template>

    <div class="flex flex-col gap-3">
      <div class="flex items-center justify-between">
        <span class="text-sm text-muted">{{ t('plugins.tableInfo.zone') }}</span>
        <UBadge variant="subtle" size="sm">{{ zone ?? '—' }}</UBadge>
      </div>
      <USeparator />
      <div class="flex items-center justify-between">
        <span class="text-sm text-muted">{{ t('plugins.tableInfo.seats') }}</span>
        <span class="font-semibold">{{ seats ?? '—' }}</span>
      </div>
      <USeparator />
      <div class="flex items-center justify-between">
        <span class="text-sm text-muted">{{ t('plugins.tableInfo.status') }}</span>
        <UBadge color="success" variant="subtle" size="sm">
          {{ t('plugins.tableInfo.free') }}
        </UBadge>
      </div>
    </div>
  </UCard>
</template>
