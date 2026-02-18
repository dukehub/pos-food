<script setup lang="ts">
import BusinessProfileForm from './BusinessProfileForm.vue'
import AppSettingsForm from './AppSettingsForm.vue'

const items = [
  {
    slot: 'profile',
    label: 'Business Profile',
    icon: 'i-heroicons-building-storefront'
  },
  {
    slot: 'config',
    label: 'App Configuration',
    icon: 'i-heroicons-cog-6-tooth'
  }
]
</script>

<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-6">Settings</h1>
    
    <UTabs :items="items" class="w-full">
      <template #profile>
        <BusinessProfileForm />
      </template>

      <template #config>
        <AppSettingsForm />
      </template>
    </UTabs>
  </div>
</template>
