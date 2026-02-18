<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { apiClient } from '@pos/api'

const props = defineProps<{
    printer: any | null
}>()

const emit = defineEmits(['close', 'refresh'])

const state = reactive({
    name: '',
    driver_type: 'windows',
    system_printer_name: '',
    ip_address: '',
    port: 9100,
    paper_width: 80,
    is_active: true
})

const loading = ref(false)

const driverTypes = [
    { label: 'Windows (Raw)', value: 'windows' },
    { label: 'Network (ESC/POS)', value: 'network' },
    { label: 'USB', value: 'usb' },
    { label: 'Bluetooth', value: 'bluetooth' }
]

watch(() => props.printer, (newVal) => {
    if (newVal) {
        Object.assign(state, {
            name: newVal.name,
            driver_type: newVal.driver_type,
            system_printer_name: newVal.system_printer_name,
            ip_address: newVal.ip_address,
            port: newVal.port,
            paper_width: newVal.paper_width,
            is_active: newVal.is_active
        })
    } else {
        Object.assign(state, {
            name: '',
            driver_type: 'windows',
            system_printer_name: '',
            ip_address: '',
            port: 9100,
            paper_width: 80,
            is_active: true
        })
    }
}, { immediate: true })

async function submit() {
    loading.value = true
    try {
        const payload = { ...state }
        if (props.printer) {
            await apiClient.put(`/plugins/printer/printers/${props.printer.id}`, payload)
        } else {
            await apiClient.post('/plugins/printer/printers', payload)
        }
        emit('refresh')
        emit('close')
    } catch (e) {
        console.error(e)
        alert('Failed to save printer')
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <form @submit.prevent="submit" class="space-y-4">
    <UFormGroup label="Name" required>
        <UInput v-model="state.name" placeholder="Receipt Printer 1" />
    </UFormGroup>

    <UFormGroup label="Driver Type">
        <USelectMenu 
            v-model="state.driver_type" 
            :options="driverTypes" 
            value-attribute="value" 
            option-attribute="label"
        />
    </UFormGroup>

    <div v-if="state.driver_type === 'windows'" class="space-y-4">
        <UFormGroup label="System Printer Name" required>
            <UInput v-model="state.system_printer_name" placeholder="EPSON TM-T20III" />
            <span class="text-xs text-gray-500">Must match exact name in OS settings</span>
        </UFormGroup>
    </div>

    <div v-else-if="state.driver_type === 'network'" class="grid grid-cols-3 gap-4">
        <UFormGroup label="IP Address" class="col-span-2" required>
            <UInput v-model="state.ip_address" placeholder="192.168.1.100" />
        </UFormGroup>
        <UFormGroup label="Port" required>
            <UInput v-model.number="state.port" type="number" />
        </UFormGroup>
    </div>

    <div class="grid grid-cols-2 gap-4">
         <UFormGroup label="Paper Width (mm)">
            <UInput v-model.number="state.paper_width" type="number" />
        </UFormGroup>
         <UFormGroup label="Status">
            <UToggle v-model="state.is_active" />
            <span class="ms-2 text-sm">{{ state.is_active ? 'Active' : 'Inactive' }}</span>
        </UFormGroup>
    </div>

    <div class="flex justify-end gap-2 mt-4 pt-4 border-t">
        <UButton variant="ghost" @click="$emit('close')">Cancel</UButton>
        <UButton type="submit" :loading="loading">Save</UButton>
    </div>
  </form>
</template>
