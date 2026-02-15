<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const navLinks = computed(() => [
  [
    {
      label: t('nav.dashboard'),
      icon: 'i-lucide-layout-dashboard',
      to: '/'
    },
    {
      label: t('nav.products'),
      icon: 'i-lucide-package',
      to: '/products'
    },
    {
      label: t('nav.categories'),
      icon: 'i-lucide-tags',
      to: '/categories'
    },
    {
      label: t('nav.orders'),
      icon: 'i-lucide-clipboard-list',
      to: '/orders',
      badge: '12'
    },
    {
      label: t('nav.tables'),
      icon: 'i-lucide-armchair',
      to: '/tables'
    }
  ],
  [
    {
      label: t('nav.settings'),
      icon: 'i-lucide-settings',
      to: '/settings'
    }
  ]
])
</script>

<template>
  <UDashboardSidebar
    id="admin-sidebar"
    collapsible
    resizable
    class="bg-elevated/25"
    :ui="{ footer: 'lg:border-t lg:border-default' }"
  >
    <!-- Logo / Brand -->
    <template #header="{ collapsed }">
      <div class="flex items-center gap-3 px-2 py-1">
        <div class="flex size-8 shrink-0 items-center justify-center rounded-lg bg-primary font-bold text-white text-sm">
          P
        </div>
        <Transition name="fade">
          <span v-if="!collapsed" class="text-sm font-semibold truncate">
            POS Food
          </span>
        </Transition>
      </div>
    </template>

    <!-- Navigation -->
    <template #default="{ collapsed }">
      <UNavigationMenu
        :collapsed="collapsed"
        :items="navLinks[0]"
        orientation="vertical"
        :tooltip="collapsed"
      />

      <UNavigationMenu
        :collapsed="collapsed"
        :items="navLinks[1]"
        orientation="vertical"
        :tooltip="collapsed"
        class="mt-auto"
      />
    </template>

    <!-- Footer: User + Collapse -->
    <template #footer="{ collapsed }">
      <div class="flex items-center gap-2">
        <UAvatar
          src=""
          alt="Admin"
          size="sm"
          icon="i-lucide-user"
        />
        <Transition name="fade">
          <div v-if="!collapsed" class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">Admin</p>
            <p class="text-xs text-muted truncate">admin@posfood.dz</p>
          </div>
        </Transition>
        <UColorModeButton v-if="!collapsed" size="sm" />
      </div>
      <UDashboardSidebarCollapse />
    </template>
  </UDashboardSidebar>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.15s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
