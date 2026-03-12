import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: 'AI编程启蒙课',
  description: '写给初中生的 Claude Code 入门教程',
  base: '/beloved/',

  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/favicon.svg' }],
    ['meta', { property: 'og:type', content: 'website' }],
    ['meta', { property: 'og:title', content: 'AI编程启蒙课' }],
    ['meta', { property: 'og:description', content: '用 Claude Code 开启你的编程之旅 —— 写给初中生的零基础 AI 编程教程' }],
    ['meta', { name: 'twitter:card', content: 'summary' }],
    ['meta', { name: 'theme-color', content: '#7c3aed' }],
  ],

  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '课前准备', link: '/prepare' },
      { text: '开始学习', link: '/lessons/01-meet-ai' }
    ],

    sidebar: [
      {
        text: '开始之前',
        items: [
          { text: '课前准备', link: '/prepare' }
        ]
      },
      {
        text: '课程内容',
        items: [
          { text: '第1课：认识AI与Claude Code', link: '/lessons/01-meet-ai' },
          { text: '第2课：用AI做你的第一个网页', link: '/lessons/02-first-webpage' },
          { text: '第3课：让网页动起来', link: '/lessons/03-interactive' },
          { text: '第4课：做一个实用小工具', link: '/lessons/04-mini-tool' },
          { text: '第5课：做一个创意小游戏', link: '/lessons/05-mini-game' },
          { text: '第6课：给作品加上AI超能力', link: '/lessons/06-ai-power' },
          { text: '第7课：展示你的作品集', link: '/lessons/07-showcase' }
        ]
      }
    ],

    outline: {
      label: '本页目录'
    },

    docFooter: {
      prev: '上一课',
      next: '下一课'
    },

    lastUpdated: {
      text: '最后更新于'
    },

    darkModeSwitchLabel: '主题',
    sidebarMenuLabel: '目录',
    returnToTopLabel: '回到顶部'
  }
})
