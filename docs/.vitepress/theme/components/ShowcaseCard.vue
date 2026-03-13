<script setup lang="ts">
defineProps<{
  title: string
  author: string
  lesson?: string
  description: string
  link?: string
}>()
</script>

<template>
  <div class="showcase-card">
    <div class="showcase-card-header">
      <h3 class="showcase-card-title">{{ title }}</h3>
      <span v-if="lesson" class="showcase-card-lesson">{{ lesson }}</span>
    </div>
    <p class="showcase-card-desc">{{ description }}</p>
    <div class="showcase-card-footer">
      <span class="showcase-card-author">by {{ author }}</span>
      <a
        v-if="link"
        :href="link"
        target="_blank"
        rel="noopener noreferrer"
        class="showcase-card-link"
      >
        查看作品
      </a>
    </div>
  </div>
</template>
