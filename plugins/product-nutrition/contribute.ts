import type { PluginRegistry } from '@pos/core'

/**
 * Plugin: Product Nutrition
 *
 * Contributes a "Nutrition" tab to the admin product detail page.
 * mountPoint: admin.product.tabs
 *
 * Uses resolveProps to extract the product from the ctx.
 */
export function registerProductNutritionPlugin(registry: PluginRegistry): void {
  registry.register({
    manifest: {
      id: 'product-nutrition',
      name: 'Product Nutrition Info',
      version: '0.1.0',
      targets: ['admin']
    },
    contributions: [
      {
        mountPoint: 'admin.product.tabs',
        component: () => import('./NutritionTab.vue'),
        order: 20,
        label: 'Nutrition Tab',
        resolveProps: (ctx) => ({
          productId: ctx.productId,
          productName: ctx.productName
        })
      }
    ],
    messages: {
      fr: {
        plugins: {
          productNutrition: {
            tabTitle: 'Nutrition',
            calories: 'Calories',
            protein: 'Protéines',
            carbs: 'Glucides',
            fat: 'Lipides',
            noData: 'Aucune donnée nutritionnelle'
          }
        }
      },
      ar: {
        plugins: {
          productNutrition: {
            tabTitle: 'التغذية',
            calories: 'سعرات حرارية',
            protein: 'بروتين',
            carbs: 'كربوهيدرات',
            fat: 'دهون',
            noData: 'لا توجد بيانات غذائية'
          }
        }
      },
      en: {
        plugins: {
          productNutrition: {
            tabTitle: 'Nutrition',
            calories: 'Calories',
            protein: 'Protein',
            carbs: 'Carbs',
            fat: 'Fat',
            noData: 'No nutrition data available'
          }
        }
      }
    }
  })
}
