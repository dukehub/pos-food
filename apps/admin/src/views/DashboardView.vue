<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ExtensionPoint } from '@pos/ui'

const { t } = useI18n()

// Demo context for the product tabs extension point
const productCtx = {
  productId: 'prod-001',
  productName: 'Burger Classic'
}
</script>

<template>
  <div class="min-h-screen flex flex-col gap-8 p-8">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <UIcon name="i-lucide-layout-dashboard" class="size-8 text-primary" />
        <h1 class="text-2xl font-bold">{{ t('nav.dashboard') }} — Admin</h1>
      </div>
    </div>

    <!-- Products Toolbar — with ExtensionPoint for plugin actions -->
    <UCard>
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold">{{ t('nav.products') }}</h2>
          <div class="flex items-center gap-2">
            <UButton :label="t('common.add')" icon="i-lucide-plus" size="sm" />

            <!-- Plugin-contributed toolbar actions appear here -->
            <ExtensionPoint
              name="admin.products.toolbar.actions"
              tag="div"
              class="flex items-center gap-2"
            >
              <template #empty>
                <!-- No plugins: nothing rendered -->
              </template>
            </ExtensionPoint>
          </div>
        </div>
      </template>

      <p class="text-muted">{{ t('common.loading') }}</p>
    </UCard>

    <!-- Product Detail Tabs — with ExtensionPoint for plugin tabs -->
    <UCard>
      <template #header>
        <h2 class="text-lg font-semibold">{{ productCtx.productName }}</h2>
      </template>

      <!-- Core tabs would go here -->
      <div class="flex flex-col gap-4">
        <p class="text-sm text-muted">Fiche produit (onglets core ici...)</p>

        <!-- Plugin-contributed tabs appear here -->
        <ExtensionPoint
          name="admin.product.tabs"
          :ctx="productCtx"
          tag="div"
          class="flex flex-col gap-4"
        >
          <template #empty>
            <p class="text-xs text-muted italic">Aucun plugin actif pour cet emplacement.</p>
          </template>
        </ExtensionPoint>
      </div>
    </UCard>
  </div>
</template>
