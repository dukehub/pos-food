<script setup lang="ts">
import { ref } from 'vue'
import KpiCard from '@/components/dashboard/KpiCard.vue'
import SalesChart from '@/components/dashboard/SalesChart.vue'
import RecentOrders from '@/components/dashboard/RecentOrders.vue'
import TopProducts from '@/components/dashboard/TopProducts.vue'
import { ExtensionPoint } from '@pos/ui'

// Mock Data for KPIs
const kpis = ref([
  { title: 'Total Revenue', value: '$12,450', icon: 'i-heroicons-currency-dollar', color: 'green', trend: 12.5, trendLabel: 'vs last week' },
  { title: 'Total Orders', value: '450', icon: 'i-heroicons-shopping-bag', color: 'blue', trend: 8.2, trendLabel: 'vs last week' },
  { title: 'Avg. Ticket', value: '$27.60', icon: 'i-heroicons-receipt-percent', color: 'orange', trend: -2.4, trendLabel: 'vs last week' },
  { title: 'Active Tables', value: '12/20', icon: 'i-heroicons-table-cells', color: 'purple' }
])
</script>

<template>
  <div class="space-y-6">
    <!-- Header / Quick Actions -->
    <div class="flex justify-between items-center">
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Dashboard</h1>
      <div class="flex items-center gap-2">
        <ExtensionPoint name="admin.dashboard.unique_actions" />
        <UButton icon="i-heroicons-arrow-path" color="neutral" variant="ghost" />
        <UButton icon="i-heroicons-printer" color="neutral" variant="ghost" />
        <UButton icon="i-heroicons-plus" color="primary">New Order</UButton>
      </div>
    </div>

    <!-- KPI Grid -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <!-- Core KPIs -->
      <KpiCard v-for="(kpi, index) in kpis" :key="index" v-bind="kpi" />
      
      <!-- Plugin KPIs -->
      <ExtensionPoint name="admin.dashboard.kpis" />
    </div>

    <!-- Main Content Grid -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      <!-- Left Column (Charts & Main Widgets) -->
      <div class="lg:col-span-2 space-y-6">
        <SalesChart />
        
        <ExtensionPoint name="admin.dashboard.widgets.main" />
        
        <RecentOrders />
      </div>

      <!-- Right Column (Side Widgets) -->
      <div class="space-y-6">
        <TopProducts />
        
        <ExtensionPoint name="admin.dashboard.widgets.side" />
        
        <UCard>
           <template #header>
             <h3 class="font-semibold">System Status</h3>
           </template>
           <div class="space-y-3">
             <div class="flex justify-between text-sm">
               <span>Database</span>
               <UBadge color="success" variant="subtle" size="xs">Connected</UBadge>
             </div>
             <div class="flex justify-between text-sm">
               <span>API</span>
               <UBadge color="success" variant="subtle" size="xs">Operational</UBadge>
             </div>
             <div class="flex justify-between text-sm">
               <span>Version</span>
               <span class="text-gray-500">v1.2.0</span>
             </div>
           </div>
        </UCard>
      </div>
    </div>
  </div>
</template>
