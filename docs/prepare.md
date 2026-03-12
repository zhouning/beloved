# 课前准备

在开始学习之前，我们需要准备好几样工具。别担心，跟着下面的步骤一步一步来就好！

## 你需要准备什么

- 一台电脑（Windows、Mac 都可以）
- 网络连接

## 第一步：安装 VS Code

VS Code 是一个代码编辑器，你可以把它想象成一个"超级记事本"，专门用来写代码的。

1. 打开浏览器，访问 [VS Code 官网](https://code.visualstudio.com/)
2. 点击下载按钮，选择你的操作系统
3. 下载完成后，双击安装包，按照提示一路点"下一步"就好

::: tip 小贴士
安装时建议勾选"添加到 PATH"选项，这样后面使用起来会更方便。
:::

## 第二步：安装 Node.js

Node.js 是让我们的网页程序能运行起来的"引擎"。

1. 打开浏览器，访问 [Node.js 官网](https://nodejs.org/)
2. 下载 **LTS（长期支持）** 版本（左边的绿色按钮）
3. 双击安装包，一路点"下一步"

安装完成后，打开终端（在 VS Code 里按 `` Ctrl+` ``），输入：

```bash
node --version
```

如果看到类似 `v20.x.x` 的输出，说明安装成功了！

## 第三步：安装 Claude Code

Claude Code 就是你的 AI 编程搭档，它会直接在终端里帮你写代码。

在终端里输入：

```bash
npm install -g @anthropic-ai/claude-code
```

等待安装完成后，输入：

```bash
claude
```

如果看到 Claude Code 的欢迎界面，恭喜你，准备工作就完成了！

::: tip 第一次使用
第一次运行 `claude` 时，它会要求你登录 Anthropic 账号。按照屏幕上的提示操作就好——如果遇到问题，可以让爸爸/妈妈帮忙。
:::

## 第四步：创建你的工作文件夹

我们需要一个专门的文件夹来存放你的所有作品。

1. 在终端里输入：

```bash
mkdir my-ai-projects
cd my-ai-projects
```

2. 这样你就有了一个叫 `my-ai-projects` 的文件夹，以后所有的课程作品都会放在这里。

## 准备好了吗？

如果上面的步骤都完成了，你已经准备好开始你的 AI 编程之旅了！

点击下方链接进入第一课吧：

[开始第1课：认识AI与Claude Code →](/lessons/01-meet-ai)
