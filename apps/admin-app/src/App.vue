<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { AppShell } from '@pos-food/ui'
import type { NavigationItem } from '@pos-food/ui/src/components/AppShell.vue'

const { t } = useI18n()

const navigation: NavigationItem[] = [
  { label: t('admin.nav.dashboard'), icon: 'i-lucide-layout-dashboard', to: '/' },
  { label: t('admin.nav.products'), icon: 'i-lucide-package', to: '/products' },
  { label: t('admin.nav.categories'), icon: 'i-lucide-tags', to: '/categories' },
  { label: t('admin.nav.orders'), icon: 'i-lucide-receipt', to: '/orders' },
  { label: t('admin.nav.tables'), icon: 'i-lucide-grid-2x2', to: '/tables' },
  { label: t('admin.nav.users'), icon: 'i-lucide-users', to: '/users' },
  { label: t('admin.nav.settings'), icon: 'i-lucide-settings', to: '/settings' },
]
</script>

<template>
  <UApp>
    <AppShell :title="t('common.app_name')" :navigation="navigation">
      <RouterView />
    </AppShell>
  </UApp>
</template>
