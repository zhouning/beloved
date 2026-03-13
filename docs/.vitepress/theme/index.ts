import DefaultTheme from 'vitepress/theme'
import MyLayout from './MyLayout.vue'
import Quiz from './components/Quiz.vue'
import CodePreview from './components/CodePreview.vue'
import ShowcaseCard from './components/ShowcaseCard.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: MyLayout,
  enhanceApp({ app }) {
    app.component('Quiz', Quiz)
    app.component('CodePreview', CodePreview)
    app.component('ShowcaseCard', ShowcaseCard)
  }
}
