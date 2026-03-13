<script setup lang="ts">
import { computed } from 'vue'
import { useRoute, useData } from 'vitepress'
import Giscus from '@giscus/vue'

const route = useRoute()
const { isDark } = useData()

const showComments = computed(() => {
  const path = route.path
  return path.includes('/lessons/') || path.includes('/faq')
})

const theme = computed(() => isDark.value ? 'dark' : 'light')
</script>

<template>
  <div v-if="showComments" class="comments-container">
    <h2 class="comments-title">留言讨论</h2>
    <Giscus
      :key="route.path"
      repo="zhouning/beloved"
      repo-id=""
      category="Announcements"
      category-id=""
      mapping="pathname"
      strict="0"
      reactions-enabled="1"
      emit-metadata="0"
      input-position="top"
      :theme="theme"
      lang="zh-CN"
      loading="lazy"
    />
  </div>
</template>
