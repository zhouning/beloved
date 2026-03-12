# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个面向初中生（零编程基础）的 AI 编程启蒙课程网站，使用 VitePress 构建。课程通过 7 节课教学生用 Claude Code 开发小应用。

## 常用命令

```bash
# 本地开发预览
npm run docs:dev

# 构建生产版本
npm run docs:build

# 预览构建结果
npm run docs:preview
```

## 项目结构

- `docs/` — 所有网站内容
  - `.vitepress/config.ts` — VitePress 配置（导航、侧边栏、中文本地化）
  - `.vitepress/theme/` — 自定义主题和样式
  - `index.md` — 首页（Hero 布局）
  - `prepare.md` — 课前环境搭建指南
  - `lessons/` — 7 课教程内容（01 到 07）

## 编写规范

- **语言**：所有内容使用中文，包括代码注释
- **语气**：友好、鼓励、像和朋友聊天——目标读者是 13 岁的初中生
- **每课结构**：学习目标 → 概念讲解 → 动手环节 → 魔法咒语（prompt 示例）→ 挑战任务
- **VitePress 提示块**：
  - `::: tip 小贴士` — 实用建议
  - `::: info 魔法咒语` — 可复制给 Claude Code 的 prompt 示例
  - `::: warning 注意` — 重要提醒
  - `::: details 想了解更多？` — 可选的深入解释
