<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { ExtensionPoint } from '@pos/ui'
import KpiCards from '@/components/dashboard/KpiCards.vue'
import SalesChart from '@/components/dashboard/SalesChart.vue'
import TopProducts from '@/components/dashboard/TopProducts.vue'
import RecentOrders from '@/components/dashboard/RecentOrders.vue'
import AlertsPanel from '@/components/dashboard/AlertsPanel.vue'
import QuickActions from '@/components/dashboard/QuickActions.vue'

const { t } = useI18n()
</script>

<template>
  <UDashboardPanel id="dashboard">
    <!-- Header: Navbar -->
    <template #header>
      <UDashboardNavbar :title="t('dashboard.title')">
        <template #leading>
          <UDashboardSidebarCollapse />
        </template>

        <template #right>
          <UTooltip text="Notifications">
            <UButton
              color="neutral"
              variant="ghost"
              icon="i-lucide-bell"
              square
            />
          </UTooltip>

          <UColorModeButton />
        </template>
      </UDashboardNavbar>
    </template>

    <!-- Body: Dashboard Content -->
    <template #body>
      <div class="flex flex-col gap-6">
        <!-- KPI Cards -->
        <KpiCards />
        <ExtensionPoint name="admin.dashboard.kpis" />

        <!-- Main + Side Grid -->
        <div class="grid grid-cols-1 gap-6 xl:grid-cols-3">
          <!-- Main Column (2/3) -->
          <div class="flex flex-col gap-6 xl:col-span-2">
            <SalesChart />
            <ExtensionPoint name="admin.dashboard.widgets.main" />
            <TopProducts />
            <RecentOrders />
          </div>

          <!-- Side Column (1/3) -->
          <div class="flex flex-col gap-6">
            <AlertsPanel />
            <QuickActions />
            <ExtensionPoint name="admin.dashboard.quickActions" />
            <ExtensionPoint name="admin.dashboard.widgets.side" />
          </div>
        </div>
      </div>
    </template>
  </UDashboardPanel>
</template>
