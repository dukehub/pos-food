<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { apiClient } from '@pos/api'

const props = defineProps<{
    customer: any | null
}>()

const emit = defineEmits(['close', 'refresh'])

const state = reactive({
    name: '',
    phone: '',
    email: '',
    nif: '',
    ai: '',
    rc: '',
    tax_id: '',
    address: '',
    credit_limit: 0,
    payment_due_days: 30,
    phone_whatsapp: '',
    allow_notifications: true,
    is_active: true
})

const loading = ref(false)

watch(() => props.customer, (newVal) => {
    if (newVal) {
        Object.assign(state, {
            name: newVal.name,
            phone: newVal.phone,
            email: newVal.email,
            nif: newVal.nif,
            ai: newVal.ai,
            rc: newVal.rc,
            tax_id: newVal.tax_id,
            address: newVal.address,
            credit_limit: newVal.credit_limit || 0,
            payment_due_days: newVal.payment_due_days,
            phone_whatsapp: newVal.phone_whatsapp,
            allow_notifications: newVal.allow_notifications,
            is_active: newVal.is_active
        })
    } else {
        Object.assign(state, {
            name: '',
            phone: '',
            email: '',
            nif: '',
            ai: '',
            rc: '',
            tax_id: '',
            address: '',
            credit_limit: 0,
            payment_due_days: 30,
            phone_whatsapp: '',
            allow_notifications: true,
            is_active: true
        })
    }
}, { immediate: true })

async function submit() {
    loading.value = true
    try {
        const payload = { ...state }
        // Clean up empty strings to null if needed, but schema allows optional strings.
        // Pydantic empty string vs None: usually fine if schema allows str | None.
        
        if (props.customer) {
            await apiClient.put(`/plugins/customers/customers/${props.customer.id}`, payload)
        } else {
            await apiClient.post('/plugins/customers/customers', payload)
        }
        emit('refresh')
        emit('close')
    } catch (e) {
        console.error(e)
        alert('Failed to save customer')
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <form @submit.prevent="submit" class="space-y-4">
    <UFormGroup label="Name" required>
        <UInput v-model="state.name" />
    </UFormGroup>

    <div class="grid grid-cols-2 gap-4">
        <UFormGroup label="Phone">
            <UInput v-model="state.phone" />
        </UFormGroup>
        <UFormGroup label="Email">
            <UInput v-model="state.email" type="email" />
        </UFormGroup>
    </div>

    <UFormGroup label="Address">
        <UTextarea v-model="state.address" :rows="2" />
    </UFormGroup>

    <UDivider label="Fiscal Info" />

    <div class="grid grid-cols-2 gap-4">
        <UFormGroup label="NIF">
            <UInput v-model="state.nif" />
        </UFormGroup>
         <UFormGroup label="Tax ID">
            <UInput v-model="state.tax_id" />
        </UFormGroup>
        <UFormGroup label="AI">
            <UInput v-model="state.ai" />
        </UFormGroup>
        <UFormGroup label="RC">
            <UInput v-model="state.rc" />
        </UFormGroup>
    </div>

    <UDivider label="Financial" />

    <div class="grid grid-cols-2 gap-4">
        <UFormGroup label="Credit Limit">
            <UInput v-model.number="state.credit_limit" type="number" step="0.01" />
        </UFormGroup>
         <UFormGroup label="Payment Due (Days)">
            <UInput v-model.number="state.payment_due_days" type="number" />
        </UFormGroup>
    </div>

    <UDivider label="Settings" />
    
    <div class="flex gap-4">
        <UFormGroup label="Active">
            <UToggle v-model="state.is_active" />
        </UFormGroup>
         <UFormGroup label="Notifications">
            <UToggle v-model="state.allow_notifications" />
        </UFormGroup>
    </div>

    <div class="flex justify-end gap-2 mt-4 pt-4 border-t">
        <UButton variant="ghost" @click="$emit('close')">Cancel</UButton>
        <UButton type="submit" :loading="loading">Save</UButton>
    </div>
  </form>
</template>
