<script setup lang="ts">
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import AppSidebar from '@/components/AppSidebar.vue'
import { useLocaleDirection } from '@/composables/useLocaleDirection'

const { t } = useI18n()
const { locale: storedLocale, setLocale } = useLocaleDirection()
const isNotificationsOpen = ref(false)

const locales = [
  { code: 'en', name: 'English', icon: 'i-heroicons-language' },
  { code: 'fr', name: 'Français', icon: 'i-heroicons-language' },
  { code: 'ar', name: 'العربية', icon: 'i-heroicons-language', dir: 'rtl' }
]

const currentLocale = computed({
  get: () => locales.find(l => l.code === storedLocale.value) || locales[0],
  set: (val) => {
    setLocale(val.code)
  }
})

const notifications = [
    { id: 1, title: 'New Order #1234', time: '5 min ago', unread: true },
    { id: 2, title: 'Kitchen Printer Error', time: '10 min ago', unread: true },
    { id: 3, title: 'Daily Report Ready', time: '1 hour ago', unread: false }
]
</script>

<template>
  <UDashboardGroup>
    <AppSidebar />
    
    <div class="flex flex-1 flex-col min-w-0 overflow-hidden">
        <header class="flex items-center justify-between px-4 py-3 border-b border-gray-200 dark:border-gray-800 bg-white dark:bg-gray-900">
            <h1 class="text-lg font-semibold text-gray-900 dark:text-white">
                <!-- Page Title could be dynamic -->
            </h1>
            <div class="flex items-center gap-2">
                 <USelectMenu
                    v-model="currentLocale"
                    :items="locales"
                    variant="ghost" 
                    color="neutral"
                    class="w-32"
                 >
                    <template #default="{ open }">
                        <UButton color="neutral" variant="ghost" :icon="currentLocale.icon">
                            {{ currentLocale.name }}
                            <template #trailing>
                               <UIcon name="i-heroicons-chevron-down" class="w-4 h-4 transition-transform" :class="[open && 'rotate-180']" />
                            </template>
                        </UButton>
                    </template>
                    
                    <template #item="{ item }">
                         <span class="truncate">{{ item.name }}</span>
                         <UIcon :name="item.icon" class="ms-auto w-4 h-4 text-gray-400 dark:text-gray-500" />
                    </template>
                 </USelectMenu>

                 <UButton 
                    icon="i-heroicons-bell" 
                    color="neutral" 
                    variant="ghost" 
                    @click="isNotificationsOpen = true"
                 >
                    <template #trailing>
                        <span class="absolute top-2 right-2 block h-2 w-2 rounded-full ring-2 ring-white dark:ring-gray-900 bg-red-500" />
                    </template>
                 </UButton>
                 <UColorModeButton />
            </div>
        </header>

        <main class="flex-1 overflow-y-auto p-4">
             <slot />
        </main>
    </div>

    <USlideover v-model:open="isNotificationsOpen" :title="t('notifications.title')" :description="t('notifications.description') || 'Recent system notifications'">
        <template #body>
            <div class="space-y-4">
                 <div v-for="notif in notifications" :key="notif.id" class="p-4 rounded-lg bg-gray-50 dark:bg-gray-800 relative border border-gray-100 dark:border-gray-700">
                    <div v-if="notif.unread" class="absolute top-4 right-4 h-2 w-2 rounded-full bg-primary-500" />
                    <h4 class="font-medium text-sm text-gray-900 dark:text-white">{{ notif.title }}</h4>
                    <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">{{ notif.time }}</p>
                 </div>
            </div>
        </template>
    </USlideover>
  </UDashboardGroup>
</template>
