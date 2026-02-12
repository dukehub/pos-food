<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { PageHeader } from '@pos-food/ui'

const { t } = useI18n()
const router = useRouter()

const form = ref({
  name: '',
  description: '',
  price: 0,
  categoryId: '',
  taxRate: 20,
  barcode: '',
  isActive: true,
})

function handleSubmit() {
  // TODO: Zod validation + API call
  router.push('/products')
}
</script>

<template>
  <div class="flex flex-1 flex-col overflow-auto">
    <PageHeader :title="t('common.create') + ' — ' + t('admin.nav.products')">
      <template #actions>
        <UButton
          :label="t('common.back')"
          icon="i-lucide-arrow-left"
          variant="ghost"
          to="/products"
        />
      </template>
    </PageHeader>

    <div class="flex-1 p-6">
      <UCard class="mx-auto max-w-2xl">
        <form @submit.prevent="handleSubmit" class="space-y-4">
          <div>
            <label class="mb-1 block text-sm font-medium">{{ t('common.name') }} *</label>
            <UInput v-model="form.name" required size="lg" class="w-full" />
          </div>

          <div>
            <label class="mb-1 block text-sm font-medium">{{ t('common.description') }}</label>
            <UTextarea v-model="form.description" class="w-full" />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="mb-1 block text-sm font-medium">{{ t('common.price') }} (€) *</label>
              <UInput v-model.number="form.price" type="number" step="0.01" min="0" required size="lg" class="w-full" />
            </div>
            <div>
              <label class="mb-1 block text-sm font-medium">{{ t('common.tax') }} (%) *</label>
              <UInput v-model.number="form.taxRate" type="number" min="0" max="100" required size="lg" class="w-full" />
            </div>
          </div>

          <div>
            <label class="mb-1 block text-sm font-medium">Code-barres</label>
            <UInput v-model="form.barcode" class="w-full" />
          </div>

          <div class="flex items-center gap-2 pt-2">
            <UToggle v-model="form.isActive" />
            <span class="text-sm">Produit actif</span>
          </div>

          <div class="flex justify-end gap-2 pt-4">
            <UButton :label="t('common.cancel')" variant="outline" to="/products" />
            <UButton :label="t('common.save')" type="submit" color="primary" />
          </div>
        </form>
      </UCard>
    </div>
  </div>
</template>
