import type { PluginRegistry } from '@pos/core'

/**
 * Plugin: Table Info
 *
 * Contributes a "Table Info" widget to the waiter table sidebar.
 * mountPoint: waiter.table.sidebar.widgets
 */
export function registerTableInfoPlugin(registry: PluginRegistry): void {
  registry.register({
    manifest: {
      id: 'table-info',
      name: 'Table Info Widget',
      version: '0.1.0',
      targets: ['waiter']
    },
    contributions: [
      {
        mountPoint: 'waiter.table.sidebar.widgets',
        component: () => import('./TableInfoWidget.vue'),
        order: 10,
        label: 'Table Info Widget',
        resolveProps: (ctx) => ({
          tableId: ctx.tableId,
          tableName: ctx.tableName,
          zone: ctx.zone,
          seats: ctx.seats
        })
      }
    ],
    messages: {
      fr: {
        plugins: {
          tableInfo: {
            title: 'Infos table',
            zone: 'Zone',
            seats: 'Places',
            status: 'Statut',
            free: 'Libre',
            occupied: 'Occupée',
            reserved: 'Réservée'
          }
        }
      },
      ar: {
        plugins: {
          tableInfo: {
            title: 'معلومات الطاولة',
            zone: 'المنطقة',
            seats: 'المقاعد',
            status: 'الحالة',
            free: 'متاحة',
            occupied: 'مشغولة',
            reserved: 'محجوزة'
          }
        }
      },
      en: {
        plugins: {
          tableInfo: {
            title: 'Table Info',
            zone: 'Zone',
            seats: 'Seats',
            status: 'Status',
            free: 'Free',
            occupied: 'Occupied',
            reserved: 'Reserved'
          }
        }
      }
    }
  })
}
