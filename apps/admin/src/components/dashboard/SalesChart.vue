<script setup lang="ts">
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// Demo 7-day data
const days = ['Lun', 'Mar', 'Mer', 'Jeu', 'Ven', 'Sam', 'Dim']
const values = [8200, 9400, 7800, 11200, 13500, 15800, 12450]
const max = Math.max(...values)
const chartHeight = 200
const chartWidth = 600
const padding = 40

// Build SVG path
function buildPath(): string {
  const stepX = (chartWidth - padding * 2) / (values.length - 1)
  return values
    .map((v, i) => {
      const x = padding + i * stepX
      const y = chartHeight - padding - ((v / max) * (chartHeight - padding * 2))
      return `${i === 0 ? 'M' : 'L'} ${x} ${y}`
    })
    .join(' ')
}

function buildAreaPath(): string {
  const stepX = (chartWidth - padding * 2) / (values.length - 1)
  const linePath = values
    .map((v, i) => {
      const x = padding + i * stepX
      const y = chartHeight - padding - ((v / max) * (chartHeight - padding * 2))
      return `${i === 0 ? 'M' : 'L'} ${x} ${y}`
    })
    .join(' ')
  const lastX = padding + (values.length - 1) * stepX
  const baseY = chartHeight - padding
  return `${linePath} L ${lastX} ${baseY} L ${padding} ${baseY} Z`
}

const linePath = buildPath()
const areaPath = buildAreaPath()
</script>

<template>
  <UCard>
    <template #header>
      <div class="flex items-center justify-between">
        <h3 class="text-base font-semibold">{{ t('dashboard.chart.salesTitle') }}</h3>
        <UBadge color="primary" variant="subtle">7j</UBadge>
      </div>
    </template>

    <svg
      :viewBox="`0 0 ${chartWidth} ${chartHeight}`"
      class="w-full h-auto"
      preserveAspectRatio="xMidYMid meet"
    >
      <defs>
        <linearGradient id="areaGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" class="[stop-color:var(--color-primary-500)] [stop-opacity:0.3]" />
          <stop offset="100%" class="[stop-color:var(--color-primary-500)] [stop-opacity:0.02]" />
        </linearGradient>
      </defs>

      <!-- Grid lines -->
      <line
        v-for="i in 4"
        :key="i"
        :x1="padding"
        :x2="chartWidth - padding"
        :y1="padding + ((i - 1) * (chartHeight - padding * 2)) / 3"
        :y2="padding + ((i - 1) * (chartHeight - padding * 2)) / 3"
        class="stroke-default"
        stroke-width="0.5"
        stroke-dasharray="4 4"
      />

      <!-- Area fill -->
      <path :d="areaPath" fill="url(#areaGrad)" />

      <!-- Line -->
      <path
        :d="linePath"
        fill="none"
        class="stroke-primary"
        stroke-width="2.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      />

      <!-- Dots + labels -->
      <g v-for="(val, i) in values" :key="i">
        <circle
          :cx="padding + i * ((chartWidth - padding * 2) / (values.length - 1))"
          :cy="chartHeight - padding - ((val / max) * (chartHeight - padding * 2))"
          r="4"
          class="fill-primary stroke-background"
          stroke-width="2"
        />
        <text
          :x="padding + i * ((chartWidth - padding * 2) / (values.length - 1))"
          :y="chartHeight - 10"
          text-anchor="middle"
          class="fill-muted text-xs"
          font-size="12"
        >
          {{ days[i] }}
        </text>
      </g>
    </svg>
  </UCard>
</template>
