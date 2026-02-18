<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ZoneList from './ZoneList.vue'
import TableList from './TableList.vue'

const route = useRoute()
const router = useRouter()

const items = [{
  slot: 'zones',
  label: 'Zones'
}, {
  slot: 'tables',
  label: 'Tables'
}]

const selectedTab = computed({
  get() {
    const index = items.findIndex(item => item.slot === route.query.tab)
    return index === -1 ? 0 : index
  },
  set(value) {
    router.replace({ query: { tab: items[value].slot } })
  }
})

// Provide shared state or refresh triggers if needed, or keeping it decoupled
</script>

<template>
  <div class="space-y-6">
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Floor Plan</h1>
    </div>

    <UTabs v-model="selectedTab" :items="items" class="w-full">
      <template #zones="{ item }">
        <ZoneList />
      </template>
      <template #tables="{ item }">
        <TableList />
      </template>
    </UTabs>
  </div>
</template>
