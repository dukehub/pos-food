<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

defineProps<{
  productId?: string
  productName?: string
}>()

// Demo nutrition data
const nutritionData = {
  calories: 250,
  protein: 12,
  carbs: 30,
  fat: 8
}
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center gap-2">
        <UIcon name="i-lucide-apple" class="text-primary" />
        <span class="font-semibold">{{ t('plugins.productNutrition.tabTitle') }}</span>
        <UBadge v-if="productName" variant="subtle" size="sm">{{ productName }}</UBadge>
      </div>
    </template>

    <div class="grid grid-cols-2 gap-4">
      <div class="flex flex-col items-center p-4 rounded-lg bg-primary/5">
        <span class="text-2xl font-bold text-primary">{{ nutritionData.calories }}</span>
        <span class="text-sm text-muted">{{ t('plugins.productNutrition.calories') }}</span>
      </div>
      <div class="flex flex-col items-center p-4 rounded-lg bg-primary/5">
        <span class="text-2xl font-bold text-primary">{{ nutritionData.protein }}g</span>
        <span class="text-sm text-muted">{{ t('plugins.productNutrition.protein') }}</span>
      </div>
      <div class="flex flex-col items-center p-4 rounded-lg bg-primary/5">
        <span class="text-2xl font-bold text-primary">{{ nutritionData.carbs }}g</span>
        <span class="text-sm text-muted">{{ t('plugins.productNutrition.carbs') }}</span>
      </div>
      <div class="flex flex-col items-center p-4 rounded-lg bg-primary/5">
        <span class="text-2xl font-bold text-primary">{{ nutritionData.fat }}g</span>
        <span class="text-sm text-muted">{{ t('plugins.productNutrition.fat') }}</span>
      </div>
    </div>
  </UCard>
</template>
