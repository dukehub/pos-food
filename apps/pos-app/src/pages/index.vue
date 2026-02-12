<script setup lang="ts">
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCartStore } from '../stores/cart'
import { useProductsStore } from '../stores/products'
import type { Product } from '@pos-food/core'

const { t } = useI18n()
const cart = useCartStore()
const productsStore = useProductsStore()
const barcodeInput = ref('')

// Demo data
const demoCategories = [
  { id: '1', name: 'Plats', color: '#3b82f6' },
  { id: '2', name: 'Pizzas', color: '#ef4444' },
  { id: '3', name: 'Boissons', color: '#22c55e' },
  { id: '4', name: 'Desserts', color: '#f59e0b' },
]

const demoProducts: Product[] = [
  { id: '1', name: 'Burger Classic', price: 12.50, categoryId: '1', taxRate: 10, isActive: true, sortOrder: 0, createdAt: '', updatedAt: '' },
  { id: '2', name: 'Pizza Margherita', price: 11.00, categoryId: '2', taxRate: 10, isActive: true, sortOrder: 1, createdAt: '', updatedAt: '' },
  { id: '3', name: 'Salade César', price: 9.50, categoryId: '1', taxRate: 10, isActive: true, sortOrder: 2, createdAt: '', updatedAt: '' },
  { id: '4', name: 'Coca-Cola', price: 3.50, categoryId: '3', taxRate: 20, isActive: true, sortOrder: 0, createdAt: '', updatedAt: '' },
  { id: '5', name: 'Eau Minérale', price: 2.50, categoryId: '3', taxRate: 20, isActive: true, sortOrder: 1, createdAt: '', updatedAt: '' },
  { id: '6', name: 'Pizza 4 Fromages', price: 13.00, categoryId: '2', taxRate: 10, isActive: true, sortOrder: 2, createdAt: '', updatedAt: '' },
  { id: '7', name: 'Tiramisu', price: 7.00, categoryId: '4', taxRate: 10, isActive: true, sortOrder: 0, createdAt: '', updatedAt: '' },
  { id: '8', name: 'Steak Frites', price: 16.50, categoryId: '1', taxRate: 10, isActive: true, sortOrder: 3, createdAt: '', updatedAt: '' },
]

productsStore.setProducts(demoProducts)

function addToCart(product: Product) {
  cart.addItem(product)
}

function handleBarcode() {
  const product = productsStore.findByBarcode(barcodeInput.value)
  if (product) {
    cart.addItem(product)
  }
  barcodeInput.value = ''
}

function formatPrice(value: number): string {
  return value.toFixed(2).replace('.', ',')
}
</script>

<template>
  <div class="flex h-full flex-col">
    <div class="grid flex-1 grid-cols-3 gap-0 overflow-hidden">
      <!-- Product area (2/3) -->
      <div class="col-span-2 flex flex-col overflow-hidden border-r border-[var(--ui-border)]">
        <!-- Barcode input -->
        <div class="border-b border-[var(--ui-border)] p-4">
          <UInput
            v-model="barcodeInput"
            :placeholder="t('pos.sale.scan_barcode')"
            icon="i-lucide-search"
            size="lg"
            class="w-full"
            @keydown.enter="handleBarcode"
          />
        </div>

        <!-- Category tabs -->
        <div class="flex gap-2 border-b border-[var(--ui-border)] px-4 py-2">
          <UButton
            label="Tout"
            :variant="!productsStore.selectedCategoryId ? 'solid' : 'outline'"
            size="sm"
            @click="productsStore.selectCategory(null)"
          />
          <UButton
            v-for="cat in demoCategories"
            :key="cat.id"
            :label="cat.name"
            :variant="productsStore.selectedCategoryId === cat.id ? 'solid' : 'outline'"
            size="sm"
            @click="productsStore.selectCategory(cat.id)"
          />
        </div>

        <!-- Product grid -->
        <div class="flex-1 overflow-auto p-4">
          <div class="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
            <button
              v-for="product in productsStore.filteredProducts"
              :key="product.id"
              class="flex flex-col items-center rounded-xl border border-[var(--ui-border)] bg-[var(--ui-bg)] p-4 text-center transition-all hover:border-[var(--ui-primary)] hover:shadow-md active:scale-95"
              @click="addToCart(product)"
            >
              <UIcon name="i-lucide-package" class="mb-2 size-8 text-[var(--ui-text-muted)]" />
              <p class="text-sm font-medium">{{ product.name }}</p>
              <p class="mt-1 text-lg font-bold text-[var(--ui-primary)]">{{ formatPrice(product.price) }} €</p>
            </button>
          </div>
        </div>
      </div>

      <!-- Cart (1/3) -->
      <div class="flex flex-col">
        <div class="flex items-center justify-between border-b border-[var(--ui-border)] p-4">
          <h2 class="text-lg font-semibold">{{ t('pos.sale.title') }}</h2>
          <UBadge v-if="cart.itemCount > 0" color="primary">{{ cart.itemCount }}</UBadge>
        </div>

        <!-- Cart items -->
        <div class="flex-1 overflow-auto">
          <div v-if="cart.items.length === 0" class="flex h-full items-center justify-center text-[var(--ui-text-muted)]">
            <div class="text-center">
              <UIcon name="i-lucide-shopping-cart" class="mx-auto mb-2 size-8" />
              <p class="text-sm">{{ t('common.no_results') }}</p>
            </div>
          </div>

          <div v-else class="divide-y divide-[var(--ui-border)]">
            <div
              v-for="item in cart.items"
              :key="item.product.id"
              class="flex items-center gap-2 px-4 py-3"
            >
              <div class="flex-1">
                <p class="text-sm font-medium">{{ item.product.name }}</p>
                <p class="text-xs text-[var(--ui-text-muted)]">{{ formatPrice(item.product.price) }} € × {{ item.quantity }}</p>
              </div>
              <div class="flex items-center gap-1">
                <UButton
                  icon="i-lucide-minus"
                  variant="outline"
                  size="xs"
                  @click="cart.decrementQuantity(item.product.id)"
                />
                <span class="w-8 text-center text-sm font-medium">{{ item.quantity }}</span>
                <UButton
                  icon="i-lucide-plus"
                  variant="outline"
                  size="xs"
                  @click="cart.incrementQuantity(item.product.id)"
                />
              </div>
              <p class="w-16 text-right text-sm font-bold">
                {{ formatPrice(item.product.price * item.quantity) }} €
              </p>
            </div>
          </div>
        </div>

        <!-- Totals + Pay -->
        <div class="border-t border-[var(--ui-border)] p-4">
          <div class="mb-3 space-y-1">
            <div class="flex justify-between text-sm">
              <span>{{ t('common.subtotal') }}</span>
              <span>{{ formatPrice(cart.subtotal) }} €</span>
            </div>
            <div class="flex justify-between text-sm">
              <span>{{ t('common.tax') }}</span>
              <span>{{ formatPrice(cart.taxTotal) }} €</span>
            </div>
            <div class="flex justify-between text-lg font-bold">
              <span>{{ t('common.total') }}</span>
              <span>{{ formatPrice(cart.total) }} €</span>
            </div>
          </div>

          <div class="flex gap-2">
            <UButton
              v-if="cart.items.length > 0"
              icon="i-lucide-trash-2"
              variant="outline"
              color="error"
              @click="cart.clear()"
            />
            <UButton
              :label="t('pos.sale.pay') + (cart.total > 0 ? ` — ${formatPrice(cart.total)} €` : '')"
              icon="i-lucide-credit-card"
              block
              size="xl"
              color="primary"
              :disabled="cart.items.length === 0"
              class="flex-1"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
