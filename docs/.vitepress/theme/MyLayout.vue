<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import LessonProgress from './components/LessonProgress.vue'
import LessonFeedback from './components/LessonFeedback.vue'
import Comments from './components/Comments.vue'

const { Layout } = DefaultTheme
</script>

<template>
  <Layout>
    <template #doc-before>
      <LessonProgress />
    </template>
    <template #doc-footer-before>
      <LessonFeedback />
    </template>
    <template #doc-after>
      <Comments />
    </template>
  </Layout>
</template>
