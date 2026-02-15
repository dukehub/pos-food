import type { PluginRegistry } from '@pos/core'

/**
 * Plugin: Product Export
 *
 * Contributes an "Export CSV" button to the admin products toolbar.
 * mountPoint: admin.products.toolbar.actions
 */
export function registerProductExportPlugin(registry: PluginRegistry): void {
  registry.register({
    manifest: {
      id: 'product-export',
      name: 'Product Export',
      version: '0.1.0',
      targets: ['admin']
    },
    contributions: [
      {
        mountPoint: 'admin.products.toolbar.actions',
        component: () => import('./ExportCsvButton.vue'),
        order: 10,
        label: 'Export CSV Button'
      }
    ],
    messages: {
      fr: {
        plugins: {
          productExport: {
            exportCsv: 'Exporter CSV',
            exporting: 'Export en cours...',
            exportSuccess: 'Export réussi'
          }
        }
      },
      ar: {
        plugins: {
          productExport: {
            exportCsv: 'تصدير CSV',
            exporting: 'جاري التصدير...',
            exportSuccess: 'تم التصدير بنجاح'
          }
        }
      },
      en: {
        plugins: {
          productExport: {
            exportCsv: 'Export CSV',
            exporting: 'Exporting...',
            exportSuccess: 'Export successful'
          }
        }
      }
    }
  })
}
