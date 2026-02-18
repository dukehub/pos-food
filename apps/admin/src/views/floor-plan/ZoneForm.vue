<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { apiClient } from '@pos/api'

const props = defineProps<{
    zone: any | null
}>()

const emit = defineEmits(['close', 'refresh'])

const state = reactive({
    name: '',
    display_order: 0,
    is_active: true
})
const loading = ref(false)

watch(() => props.zone, (newVal) => {
    if (newVal) {
        state.name = newVal.name
        state.display_order = newVal.display_order
        state.is_active = newVal.is_active
    } else {
        state.name = ''
        state.display_order = 0
        state.is_active = true
    }
}, { immediate: true })

async function submit() {
    loading.value = true
    try {
        if (props.zone) {
            await apiClient.put(`/plugins/floor_plan/zones/${props.zone.id}`, state)
        } else {
            await apiClient.post('/plugins/floor_plan/zones', state)
        }
        emit('refresh')
        emit('close')
    } catch (e) {
        console.error(e)
        alert('Failed to save zone')
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <form @submit.prevent="submit" class="space-y-4">
    <UFormGroup label="Name" name="name" required>
        <UInput v-model="state.name" />
    </UFormGroup>
    
    <div class="grid grid-cols-2 gap-4">
        <UFormGroup label="Order" name="display_order">
            <UInput v-model.number="state.display_order" type="number" />
        </UFormGroup>
        
        <UFormGroup label="Status" name="is_active">
             <div class="flex items-center h-9">
                <UToggle v-model="state.is_active" />
                <span class="ms-2 text-sm">{{ state.is_active ? 'Active' : 'Inactive' }}</span>
             </div>
        </UFormGroup>
    </div>

    <div class="flex justify-end gap-2 mt-6">
        <UButton color="neutral" variant="ghost" @click="$emit('close')">Cancel</UButton>
        <UButton type="submit" :loading="loading" color="primary">Save</UButton>
    </div>
  </form>
</template>
