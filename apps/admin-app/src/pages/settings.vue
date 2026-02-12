<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { PageHeader } from '@pos-food/ui'

const { t } = useI18n()
</script>

<template>
  <div class="flex flex-1 flex-col overflow-auto">
    <PageHeader :title="t('admin.nav.settings')" />

    <div class="flex-1 p-6">
      <div class="mx-auto max-w-2xl space-y-6">
        <UCard>
          <template #header>
            <p class="font-medium">Général</p>
          </template>
          <div class="space-y-4">
            <div>
              <label class="mb-1 block text-sm font-medium">Nom du restaurant</label>
              <UInput model-value="POS Food" size="lg" class="w-full" />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium">Devise</label>
              <UInput model-value="EUR (€)" size="lg" class="w-full" disabled />
            </div>
          </div>
        </UCard>

        <UCard>
          <template #header>
            <p class="font-medium">Impression</p>
          </template>
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <span class="text-sm">Impression automatique après paiement</span>
              <UToggle :model-value="true" />
            </div>
            <div class="flex items-center justify-between">
              <span class="text-sm">Impression ticket cuisine</span>
              <UToggle :model-value="true" />
            </div>
          </div>
        </UCard>

        <div class="flex justify-end">
          <UButton :label="t('common.save')" color="primary" />
        </div>
      </div>
    </div>
  </div>
</template>
