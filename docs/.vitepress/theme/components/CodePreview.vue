<script setup lang="ts">
import { ref, computed } from 'vue'

const props = defineProps<{
  html?: string
  css?: string
  js?: string
  height?: string
}>()

const activeTab = ref<'preview' | 'code'>('preview')
const frameHeight = props.height || '300px'

const srcdoc = computed(() => {
  return `<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>body{font-family:system-ui,sans-serif;margin:16px;}${props.css || ''}</style>
</head>
<body>
${props.html || ''}
<script>${props.js || ''}<\/script>
</body>
</html>`
})

const sourceCode = computed(() => {
  let parts: string[] = []
  if (props.html) parts.push(`<!-- HTML -->\n${props.html}`)
  if (props.css) parts.push(`/* CSS */\n${props.css}`)
  if (props.js) parts.push(`// JavaScript\n${props.js}`)
  return parts.join('\n\n')
})
</script>

<template>
  <div class="code-preview">
    <div class="code-preview-toolbar">
      <button
        class="code-preview-tab"
        :class="{ active: activeTab === 'preview' }"
        @click="activeTab = 'preview'"
      >
        预览效果
      </button>
      <button
        class="code-preview-tab"
        :class="{ active: activeTab === 'code' }"
        @click="activeTab = 'code'"
      >
        查看代码
      </button>
    </div>
    <div v-show="activeTab === 'preview'" class="code-preview-frame">
      <iframe
        :srcdoc="srcdoc"
        sandbox="allow-scripts"
        :style="{ height: frameHeight }"
      />
    </div>
    <div v-show="activeTab === 'code'" class="code-preview-source">
      <pre><code>{{ sourceCode }}</code></pre>
    </div>
  </div>
</template>
