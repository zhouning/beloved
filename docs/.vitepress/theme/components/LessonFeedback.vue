<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vitepress'

const route = useRoute()

const isLesson = computed(() => {
  return route.path.includes('/lessons/')
})
</script>

<template>
  <div v-if="isLesson" class="lesson-feedback">
    <p class="lesson-feedback-text">
      这节课学得怎么样？有问题或建议都可以告诉我们！
    </p>
    <a
      href="https://github.com/zhouning/beloved/discussions"
      target="_blank"
      rel="noopener noreferrer"
      class="lesson-feedback-link"
    >
      去留言反馈
    </a>
  </div>
</template>
