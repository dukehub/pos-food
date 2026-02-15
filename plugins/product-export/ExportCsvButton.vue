<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

function handleExport() {
  // TODO: implement actual CSV export
  console.log('[product-export] Exporting products to CSV...')
}
</script>

<template>
  <UButton
    :label="t('plugins.productExport.exportCsv')"
    icon="i-lucide-download"
    variant="outline"
    size="sm"
    @click="handleExport"
  />
</template>
