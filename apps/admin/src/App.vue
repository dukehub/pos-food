<script setup lang="ts">
/**
 * Admin App root — DashboardGroup shell with sidebar + RouterView
 */
import AppSidebar from '@/components/AppSidebar.vue'
</script>

<template>
  <UApp>
    <UDashboardGroup unit="rem" storage="local">
      <AppSidebar />
      <RouterView />
    </UDashboardGroup>
  </UApp>
</template>
