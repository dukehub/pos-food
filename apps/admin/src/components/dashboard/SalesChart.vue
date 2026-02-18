<script setup lang="ts">
// Mock chart using CSS for now, as we don't have a charting lib installed yet
// and instructions say "Mock Data" / "CSS-based"
const bars = [40, 70, 45, 90, 60, 80, 50]
const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="text-base font-semibold text-gray-900 dark:text-white">Revenue (7 Days)</h3>
        <USelectMenu :options="['Last 7 days', 'Last 30 days']" model-value="Last 7 days" size="xs" />
      </div>
    </template>

    <div class="h-64 flex items-end justify-between gap-2 mt-4 px-2">
      <div v-for="(bar, index) in bars" :key="index" class="flex flex-col items-center flex-1 group">
         <div class="relative w-full flex items-end justify-center h-full">
            <div 
                class="w-full max-w-[40px] bg-primary-500 dark:bg-primary-400 rounded-t-sm transition-all duration-500 group-hover:bg-primary-600"
                :style="{ height: `${bar}%` }"
            >
                <UTooltip :text="`$${bar * 10}`" :popper="{ placement: 'top' }">
                    <div class="w-full h-full absolute inset-0"></div>
                </UTooltip>
            </div>
         </div>
         <span class="text-xs text-gray-500 mt-2">{{ days[index] }}</span>
      </div>
    </div>
  </UCard>
</template>
