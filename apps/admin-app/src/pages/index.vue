<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { PageHeader } from '@pos-food/ui'

const { t } = useI18n()
</script>

<template>
  <div class="flex flex-1 flex-col overflow-auto">
    <PageHeader :title="t('admin.dashboard.title')" />

    <div class="flex-1 p-6">
      <div class="mb-6">
        <h2 class="text-2xl font-bold">
          {{ t('admin.dashboard.welcome') }}
        </h2>
        <p class="mt-1 text-[var(--ui-text-muted)]">
          {{ t('admin.title') }}
        </p>
      </div>

      <!-- Dashboard cards placeholder -->
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-receipt" class="size-5 text-[var(--ui-primary)]" />
              <span class="font-medium">{{ t('admin.nav.orders') }}</span>
            </div>
          </template>
          <p class="text-3xl font-bold">0</p>
        </UCard>

        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-package" class="size-5 text-[var(--ui-primary)]" />
              <span class="font-medium">{{ t('admin.nav.products') }}</span>
            </div>
          </template>
          <p class="text-3xl font-bold">0</p>
        </UCard>

        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-grid-2x2" class="size-5 text-[var(--ui-primary)]" />
              <span class="font-medium">{{ t('admin.nav.tables') }}</span>
            </div>
          </template>
          <p class="text-3xl font-bold">0</p>
        </UCard>

        <UCard>
          <template #header>
            <div class="flex items-center gap-2">
              <UIcon name="i-lucide-users" class="size-5 text-[var(--ui-primary)]" />
              <span class="font-medium">{{ t('admin.nav.users') }}</span>
            </div>
          </template>
          <p class="text-3xl font-bold">0</p>
        </UCard>
      </div>
    </div>
  </div>
</template>
