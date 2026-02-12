<script setup lang="ts">
defineProps<{
  title: string
}>()
</script>

<template>
  <header class="flex h-16 items-center justify-between border-b border-[var(--ui-border)] px-6">
    <h1 class="text-xl font-semibold">
      {{ title }}
    </h1>
    <div class="flex items-center gap-2">
      <slot name="actions" />
    </div>
  </header>
</template>
