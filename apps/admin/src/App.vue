<script setup lang="ts">
/**
 * Admin App root
 */
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import DefaultLayout from '@/layouts/default.vue'
import AuthLayout from '@/layouts/auth.vue'
import { useLocaleDirection } from '@/composables/useLocaleDirection'

const route = useRoute()
const { initLocaleDirection } = useLocaleDirection()

onMounted(() => {
  initLocaleDirection()
})

const layout = computed(() => {
  return route.meta.layout === 'auth' ? AuthLayout : DefaultLayout
})
</script>

<template>
  <UApp>
    <component :is="layout">
      <RouterView />
    </component>
  </UApp>
</template>
