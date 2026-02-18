<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiClient } from '@pos/api'
import type { ApiResponse } from '@pos/api'

interface BusinessProfile {
    name: string
    slug: string
    currency: string
    locale: string
    address: string
    phone: string
    email: string
    tax_nif: string
    tax_rc: string
    tax_ai: string
}

const profile = ref<BusinessProfile>({
    name: '',
    slug: '',
    currency: 'USD',
    locale: 'fr',
    address: '',
    phone: '',
    email: '',
    tax_nif: '',
    tax_rc: '',
    tax_ai: ''
})

const loading = ref(false)
const saving = ref(false)

async function loadProfile() {
    loading.value = true
    try {
        const res = await apiClient.get<BusinessProfile>('/plugins/business_profile/restaurant')
        Object.assign(profile.value, res.data)
    } finally {
        loading.value = false
    }
}

async function saveProfile() {
    saving.value = true
    try {
        await apiClient.put('/plugins/business_profile/restaurant', profile.value)
    } catch (e) {
        console.error(e)
    } finally {
        saving.value = false
    }
}

onMounted(() => {
    loadProfile()
})
</script>

<template>
  <div class="space-y-6">
    <UCard>
      <template #header>
        <div class="flex justify-between items-center">
            <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
                Business Information
            </h3>
        </div>
      </template>

      <form @submit.prevent="saveProfile" class="grid grid-cols-1 md:grid-cols-2 gap-4">
         <UFormGroup label="Restaurant Name" name="name" class="md:col-span-2">
            <UInput v-model="profile.name" />
         </UFormGroup>

         <UFormGroup label="Slug (URL)" name="slug">
            <UInput v-model="profile.slug" />
         </UFormGroup>

         <UFormGroup label="Default Currency" name="currency">
            <USelect v-model="profile.currency" :options="['DZD', 'EUR', 'USD']" />
         </UFormGroup>

         <UFormGroup label="Default Locale" name="locale">
            <USelect v-model="profile.locale" :options="['fr', 'ar', 'en']" />
         </UFormGroup>

         <UFormGroup label="Email" name="email">
            <UInput v-model="profile.email" type="email" />
         </UFormGroup>
         
         <UFormGroup label="Phone" name="phone">
            <UInput v-model="profile.phone" />
         </UFormGroup>

         <UFormGroup label="Address" name="address" class="md:col-span-2">
            <UTextarea v-model="profile.address" />
         </UFormGroup>

         <div class="md:col-span-2 border-t border-gray-200 dark:border-gray-700 pt-4 mt-2">
             <h4 class="text-sm font-medium mb-4">Tax Information</h4>
             <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                 <UFormGroup label="NIF" name="tax_nif">
                    <UInput v-model="profile.tax_nif" />
                 </UFormGroup>
                 <UFormGroup label="RC" name="tax_rc">
                    <UInput v-model="profile.tax_rc" />
                 </UFormGroup>
                 <UFormGroup label="AI" name="tax_ai">
                    <UInput v-model="profile.tax_ai" />
                 </UFormGroup>
             </div>
         </div>
      </form>
      
      <template #footer>
        <div class="flex justify-end save-button">
            <UButton :loading="saving" @click="saveProfile">
                Save Changes
            </UButton>
        </div>
      </template>
    </UCard>
  </div>
</template>
