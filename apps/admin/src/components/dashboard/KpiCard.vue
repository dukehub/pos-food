<script setup lang="ts">
defineProps<{
  title: string
  value: string | number
  icon?: string
  color?: string
  trend?: number
  trendLabel?: string
}>()
</script>

<template>
  <UCard class="hover:ring-2 hover:ring-primary-500/50 transition-all duration-200">
    <div class="flex justify-between items-start">
      <div>
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ title }}</p>
        <h3 class="text-2xl font-bold mt-1 text-gray-900 dark:text-white">{{ value }}</h3>
      </div>
      <div v-if="icon" :class="`p-2 rounded-lg bg-${color}-50 dark:bg-${color}-900/20 text-${color}-500`">
        <UIcon :name="icon" class="w-6 h-6" />
      </div>
    </div>
    
    <div v-if="trend !== undefined" class="mt-4 flex items-center text-sm">
      <UIcon 
        :name="trend >= 0 ? 'i-heroicons-arrow-trending-up' : 'i-heroicons-arrow-trending-down'" 
        :class="trend >= 0 ? 'text-green-500' : 'text-red-500'" 
        class="w-4 h-4 me-1"
      />
      <span :class="trend >= 0 ? 'text-green-500' : 'text-red-500'" class="font-medium">
        {{ Math.abs(trend) }}%
      </span>
      <span class="text-gray-500 dark:text-gray-400 ms-1" v-if="trendLabel">
        {{ trendLabel }}
      </span>
    </div>
  </UCard>
</template>
