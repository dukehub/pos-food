<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { pluginRegistry, useAuthStore } from '@pos/core'

const { t } = useI18n()
const authStore = useAuthStore()

// Fetch plugin navigation items if any
const pluginNavItems = pluginRegistry.getNavigation('admin')

const navLinks = computed(() => [
  {
    label: t('nav.dashboard') || 'Dashboard',
    icon: 'i-heroicons-squares-2x2',
    to: '/'
  },
  {
    label: 'Restaurant Plan',
    icon: 'i-heroicons-map',
    to: '/floor-plan'
  },
  {
    label: t('nav.catalog') || 'Catalog',
    icon: 'i-heroicons-tag',
    to: '/catalog'
  },
  {
    label: 'Printers & Devices',
    icon: 'i-heroicons-printer',
    to: '/printers'
  },
  {
    label: 'Customers',
    icon: 'i-heroicons-users',
    to: '/customers'
  },
  {
    label: 'Orders',
    icon: 'i-heroicons-clipboard-document-list',
    to: '/orders'
  },
  ...pluginNavItems
])

const settingsLinks = computed(() => [
    {
        label: t('nav.settings') || 'Settings',
        icon: 'i-heroicons-cog-6-tooth',
        children: [
             {
                label: 'General',
                to: '/settings',
                icon: 'i-heroicons-adjustments-horizontal'
             },
             {
                label: 'Business Profile',
                to: '/settings?tab=business', // Assuming query param or sub-route
                icon: 'i-heroicons-building-storefront'
             },
             {
                label: 'Users',
                to: '/users',
                icon: 'i-heroicons-user-group'
             }
        ]
    }
])

const userDropdownItems = computed(() => [
  [{
    label: 'Profile',
    icon: 'i-heroicons-user-circle'
  }, {
    label: 'Appearance',
    icon: 'i-heroicons-moon',
    click: () => { /* toggle dark mode logic if needed manually, or just link */ }
  }],
  [{
    label: 'Logout',
    icon: 'i-heroicons-arrow-left-on-rectangle',
    click: () => authStore.logout()
  }]
])
</script>

<template>
  <UDashboardSidebar
    id="admin-sidebar"
    collapsible
    resizable
    class="bg-gray-50 dark:bg-gray-950"
    :ui="{ footer: 'lg:border-t lg:border-gray-200 dark:lg:border-gray-800' }"
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
        :items="navLinks"
        orientation="vertical"
        :tooltip="collapsed"
      />
      
      <div class="mt-auto"></div>

      <UNavigationMenu
        :collapsed="collapsed"
        :items="settingsLinks"
        orientation="vertical"
        :tooltip="collapsed"
      />
    </template>

    <!-- Footer: User Dropdown -->
    <template #footer="{ collapsed }">
       <UDropdownMenu :items="userDropdownItems" :popper="{ placement: 'right-end' }" class="w-full">
            <div class="flex items-center gap-2 w-full p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-md cursor-pointer">
                <UAvatar
                src=""
                alt="Admin"
                size="sm"
                icon="i-heroicons-user"
                />
                <Transition name="fade">
                <div v-if="!collapsed" class="flex-1 min-w-0 text-start">
                    <p class="text-sm font-medium truncate">{{ authStore.user?.username || 'Admin' }}</p>
                    <p class="text-xs text-gray-500 dark:text-gray-400 truncate">admin@posfood.dz</p>
                </div>
                </Transition>
                <UIcon v-if="!collapsed" name="i-heroicons-chevron-right" class="w-4 h-4 text-gray-400" />
            </div>
       </UDropdownMenu>
       
       <!-- Collapse Button separately or included? Usually sidebar has its own collapse trigger logic or component -->
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
