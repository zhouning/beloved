<script setup lang="ts">
import { ref, computed } from 'vue'

interface Question {
  q: string
  options: string[]
  answer: number
}

const props = defineProps<{
  questions: Question[]
}>()

const selected = ref<(number | null)[]>(props.questions.map(() => null))
const revealed = ref<boolean[]>(props.questions.map(() => false))

const correctCount = computed(() => {
  return props.questions.reduce((count, question, i) => {
    return count + (revealed.value[i] && selected.value[i] === question.answer ? 1 : 0)
  }, 0)
})

const allRevealed = computed(() => revealed.value.every(Boolean))

function select(qi: number, oi: number) {
  if (revealed.value[qi]) return
  selected.value[qi] = oi
  revealed.value[qi] = true
}

function getOptionClass(qi: number, oi: number) {
  if (!revealed.value[qi]) return ''
  if (oi === props.questions[qi].answer) return 'correct'
  if (oi === selected.value[qi]) return 'wrong'
  return ''
}
</script>

<template>
  <div class="quiz-container">
    <div v-for="(question, qi) in questions" :key="qi" class="quiz-question">
      <p class="quiz-question-text">{{ qi + 1 }}. {{ question.q }}</p>
      <div class="quiz-options">
        <button
          v-for="(option, oi) in question.options"
          :key="oi"
          class="quiz-option"
          :class="getOptionClass(qi, oi)"
          :disabled="revealed[qi]"
          @click="select(qi, oi)"
        >
          {{ String.fromCharCode(65 + oi) }}. {{ option }}
        </button>
      </div>
      <p v-if="revealed[qi] && selected[qi] === question.answer" class="quiz-feedback correct">
        答对了！
      </p>
      <p v-else-if="revealed[qi]" class="quiz-feedback wrong">
        再想想哦！正确答案是 {{ String.fromCharCode(65 + question.answer) }}
      </p>
    </div>
    <div v-if="allRevealed" class="quiz-summary">
      你答对了 {{ correctCount }} / {{ questions.length }} 题
      <span v-if="correctCount === questions.length">，太棒了！全对！</span>
      <span v-else-if="correctCount >= questions.length * 0.7">，做得不错！</span>
      <span v-else>，继续加油！回顾一下课程内容吧～</span>
    </div>
  </div>
</template>
