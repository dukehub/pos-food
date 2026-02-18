<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { apiClient } from '@pos/api'

interface AppSetting {
    id: string
    module: string
    key: string
    value_json: any
    value_type: 'string' | 'number' | 'boolean' | 'object' | 'array' | 'any'
    description?: string
    is_active: boolean
    scope: string
}

const settings = ref<AppSetting[]>([])
const loading = ref(false)
const saving = ref(false)

async function loadSettings() {
    loading.value = true
    try {
        const res = await apiClient.get<AppSetting[]>('/plugins/app_settings/')
        settings.value = res.data
    } catch (e) {
        console.error(e)
    } finally {
        loading.value = false
    }
}

async function saveSettings() {
    saving.value = true
    try {
        const payload = {
            settings: settings.value.map(s => ({
                module: s.module,
                key: s.key,
                value_json: s.value_json,
                value_type: s.value_type,
                description: s.description,
                is_active: s.is_active,
                scope: s.scope
            }))
        }
        await apiClient.put('/plugins/app_settings/bulk', payload)
    } catch (e) {
        console.error(e)
    } finally {
        saving.value = false
    }
}

const groupedSettings = computed(() => {
    const groups: Record<string, AppSetting[]> = {}
    for (const s of settings.value) {
        if (!groups[s.module]) groups[s.module] = []
        groups[s.module].push(s)
    }
    return groups
})

onMounted(() => {
    loadSettings()
})
</script>

<template>
  <div class="space-y-6">
    <div v-if="loading" class="flex justify-center p-4">
        <UIcon name="i-heroicons-arrow-path" class="animate-spin text-2xl" />
    </div>
    
    <div v-else-if="settings.length === 0" class="text-center p-4 text-gray-500">
        No settings found.
    </div>

    <div v-else class="space-y-8">
        <UCard v-for="(groupSettings, moduleName) in groupedSettings" :key="moduleName">
            <template #header>
                <div class="capitalize font-bold text-lg">{{ moduleName }} Settings</div>
            </template>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div v-for="setting in groupSettings" :key="setting.id" class="space-y-1">
                    <div class="flex items-center justify-between">
                         <label class="block text-sm font-medium text-gray-700 dark:text-gray-200">
                             {{ setting.key }}
                         </label>
                         <UToggle v-if="setting.value_type === 'boolean'" v-model="setting.value_json" />
                    </div>
                    
                    <p v-if="setting.description" class="text-xs text-gray-500 mb-1">
                        {{ setting.description }}
                    </p>

                    <div v-if="setting.value_type !== 'boolean'">
                        <UInput 
                            v-if="setting.value_type === 'string'" 
                            v-model="setting.value_json" 
                        />
                        <UInput 
                            v-else-if="setting.value_type === 'number'" 
                            v-model.number="setting.value_json" 
                            type="number" 
                        />
                         <!-- Fallback for JSON/Object/Array -->
                        <UTextarea 
                            v-else 
                            :model-value="JSON.stringify(setting.value_json, null, 2)"
                            @update:model-value="(val: string) => { try { setting.value_json = JSON.parse(val) } catch {} }"
                            :rows="4"
                            class="font-mono text-xs"
                        />
                    </div>
                </div>
            </div>
        </UCard>
    </div>

    <div class="flex justify-end sticky bottom-4 bg-white/80 dark:bg-gray-900/80 p-4 backdrop-blur-sm border-t border-gray-200 dark:border-gray-800">
        <UButton :loading="saving" @click="saveSettings" size="lg">
            Save All Settings
        </UButton>
    </div>
  </div>
</template>
