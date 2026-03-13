<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vitepress'

const route = useRoute()

const lessons = [
  '/lessons/01-',
  '/lessons/02-',
  '/lessons/03-',
  '/lessons/04-',
  '/lessons/05-',
  '/lessons/06-',
  '/lessons/07-'
]

const totalLessons = lessons.length

const currentLesson = computed(() => {
  const path = route.path
  const index = lessons.findIndex(prefix => path.includes(prefix))
  return index >= 0 ? index + 1 : 0
})

const progressPercent = computed(() => {
  return currentLesson.value > 0
    ? Math.round((currentLesson.value / totalLessons) * 100)
    : 0
})
</script>

<template>
  <div v-if="currentLesson > 0" class="lesson-progress">
    <span class="lesson-progress-text">
      第 {{ currentLesson }} 课 / 共 {{ totalLessons }} 课
    </span>
    <div class="lesson-progress-bar">
      <div
        class="lesson-progress-fill"
        :style="{ width: progressPercent + '%' }"
      />
    </div>
  </div>
</template>
