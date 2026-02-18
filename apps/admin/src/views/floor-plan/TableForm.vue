<script setup lang="ts">
import { ref, reactive, watch } from 'vue'
import { apiClient } from '@pos/api'

const props = defineProps<{
    table: any | null
    zones: any[]
}>()

const emit = defineEmits(['close', 'refresh'])

const state = reactive({
    code: '',
    zone_id: '',
    capacity: 4,
    status: 'FREE',
    is_active: true
})
const loading = ref(false)

watch(() => props.table, (newVal) => {
    if (newVal) {
        state.code = newVal.code
        state.zone_id = newVal.zone_id
        state.capacity = newVal.capacity
        state.status = newVal.status
        state.is_active = newVal.is_active
    } else {
        state.code = ''
        state.zone_id = props.zones.length > 0 ? props.zones[0].id : ''
        state.capacity = 4
        state.status = 'FREE'
        state.is_active = true
    }
}, { immediate: true })

async function submit() {
    loading.value = true
    try {
        if (props.table) {
            await apiClient.put(`/plugins/floor_plan/tables/${props.table.id}`, state)
        } else {
            await apiClient.post('/plugins/floor_plan/tables', state)
        }
        emit('refresh')
        emit('close')
    } catch (e) {
        console.error(e)
        alert('Failed to save table')
    } finally {
        loading.value = false
    }
}
</script>

<template>
  <form @submit.prevent="submit" class="space-y-4">
    <UFormGroup label="Code/Number" name="code" required>
        <UInput v-model="state.code" />
    </UFormGroup>
    
    <UFormGroup label="Zone" name="zone_id" required>
        <USelectMenu 
            v-model="state.zone_id" 
            :options="zones" 
            value-attribute="id" 
            option-attribute="name"
        />
    </UFormGroup>

    <div class="grid grid-cols-2 gap-4">
        <UFormGroup label="Capacity" name="capacity">
            <UInput v-model.number="state.capacity" type="number" :min="1" :max="20" />
        </UFormGroup>
        
        <UFormGroup label="Status" name="status">
             <USelectMenu 
                v-model="state.status" 
                :options="['FREE', 'OCCUPIED', 'CLEANING']" 
            />
        </UFormGroup>
    </div>

    <div class="flex justify-end gap-2 mt-6">
        <UButton color="neutral" variant="ghost" @click="$emit('close')">Cancel</UButton>
        <UButton type="submit" :loading="loading" color="primary">Save</UButton>
    </div>
  </form>
</template>
