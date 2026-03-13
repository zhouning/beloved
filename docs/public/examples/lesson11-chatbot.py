"""
第11课示例：规则型聊天机器人"小智"
运行方式：python chatbot.py
功能：基于关键词匹配的校园助手聊天机器人（路线B，不需要 API）
"""

import random
from datetime import datetime

# ========== 知识库 ==========

# 课程表
SCHEDULE = {
    0: "语文、数学、英语、体育、音乐",       # 周一
    1: "数学、物理、语文、美术、历史",         # 周二
    2: "英语、化学、数学、体育、地理",         # 周三
    3: "语文、数学、英语、物理、政治",         # 周四
    4: "数学、英语、语文、班会、自习",         # 周五
}

# 笑话库
JOKES = [
    "为什么程序员总是分不清万圣节和圣诞节？\n因为 Oct 31 = Dec 25（八进制31 = 十进制25）😄",
    "一个 SQL 查询走进酒吧，看到两张表，走上前问：\n"我能 JOIN 你们吗？"",
    "为什么 Java 程序员要戴眼镜？\n因为他们看不到 C#（看不清）",
    "程序员的孩子问：爸爸，为什么太阳从东边升起？\n程序员：你测试过了吗？没有的话不要下结论。",
    "今天的天气真好，适合写 bug... 不对，适合写代码！",
    "有人问我会不会 Python，我说：会一点。\n他说太好了，帮我抓条蛇。🐍",
]

# 名言库
QUOTES = [
    "学而不思则罔，思而不学则殆。—— 孔子",
    "天才是百分之一的灵感加百分之九十九的汗水。—— 爱迪生",
    "千里之行，始于足下。—— 老子",
    "我思故我在。—— 笛卡尔",
    "人生苦短，我用 Python。—— 程序员名言",
    "任何足够先进的技术，都与魔法无异。—— 阿瑟·克拉克",
    "Stay hungry, stay foolish. —— 乔布斯",
    "不积跬步，无以至千里。—— 荀子",
]

# 学习建议
STUDY_TIPS = [
    "📖 番茄工作法：学习25分钟，休息5分钟。集中注意力效率更高！",
    "✍️ 费曼学习法：试着把你学的东西讲给别人听。如果讲不清楚，说明还没真正理解。",
    "🧠 间隔重复：今天学的东西，明天复习一次，一周后再复习一次，记得更牢！",
    "📝 做笔记时用自己的话改写，不要照抄课本。理解比记忆更重要。",
    "🎯 每天列出3个最重要的学习任务，优先完成它们。",
]

# 默认回复
DEFAULT_REPLIES = [
    "嗯嗯，我在听呢~ 你可以试试问我课表、作业，或者让我讲个笑话 😊",
    "这个问题好有趣！不过我还在学习中，试试输入"帮助"看看我能做什么吧~",
    "我还不太明白你的意思呢，你可以换个方式问问我~",
    "哇，你说的好高级！可惜我只是一个简单的小机器人 😅 输入"帮助"看看我的技能包吧~",
]

# ========== 核心逻辑 ==========

class Chatbot:
    """校园聊天机器人"小智" """

    def __init__(self):
        self.user_name = None
        self.chat_count = 0
        self.last_topic = None

    def get_greeting(self):
        """根据时间返回问候语"""
        hour = datetime.now().hour
        if hour < 6:
            return "夜深了还没睡呀？早点休息对身体好哦 🌙"
        elif hour < 12:
            return "早上好！新的一天，元气满满！☀️"
        elif hour < 14:
            return "中午好！吃饱了吗？下午继续加油！🍚"
        elif hour < 18:
            return "下午好！学习辛苦了，记得适当休息哦 ☕"
        else:
            return "晚上好！今天过得怎么样？🌆"

    def match_keywords(self, message):
        """关键词匹配，返回回复"""
        msg = message.lower().strip()

        # 打招呼
        if any(word in msg for word in ["你好", "嗨", "hello", "hi", "在吗", "哈喽"]):
            name_part = f"，{self.user_name}" if self.user_name else ""
            greeting = self.get_greeting()
            return f"你好{name_part}！{greeting}"

        # 记住名字
        if "我叫" in msg or "我是" in msg:
            for prefix in ["我叫", "我是"]:
                if prefix in msg:
                    name = msg.split(prefix)[-1].strip().rstrip("。！!.～~")
                    if name:
                        self.user_name = name
                        return f"你好 {name}！很高兴认识你！以后我就叫你 {name} 啦 😊"
            return "嗯嗯，你好呀！"

        # 查课表
        if any(word in msg for word in ["课表", "课程", "什么课", "上课", "今天有"]):
            self.last_topic = "schedule"
            weekday = datetime.now().weekday()
            if weekday in SCHEDULE:
                day_name = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"][weekday]
                return f"📅 今天是{day_name}，课程安排：\n{SCHEDULE[weekday]}\n\n好好上课哦！"
            else:
                return "🎉 今天是周末，没有课哦！好好休息或者做点自己喜欢的事吧！"

        # 讲笑话
        if any(word in msg for word in ["笑话", "开心", "无聊", "好玩", "搞笑", "逗我"]):
            self.last_topic = "joke"
            return f"😄 来一个：\n\n{random.choice(JOKES)}"

        # 再来一个
        if any(word in msg for word in ["再来", "还要", "再讲", "下一个"]):
            if self.last_topic == "joke":
                return f"😄 再来一个：\n\n{random.choice(JOKES)}"
            elif self.last_topic == "quote":
                return f"📜 再来一条：\n\n{random.choice(QUOTES)}"
            else:
                return "再来什么呢？想听笑话还是名言？告诉我吧~"

        # 名言
        if any(word in msg for word in ["名言", "励志", "加油", "鼓励", "座右铭"]):
            self.last_topic = "quote"
            return f"📜 送你一句话：\n\n{random.choice(QUOTES)}"

        # 学习建议
        if any(word in msg for word in ["怎么学", "学习方法", "学习建议", "学不进", "学习技巧"]):
            return f"🎓 学习小妙招：\n\n{random.choice(STUDY_TIPS)}"

        # 简单计算
        if any(word in msg for word in ["计算", "算一下", "等于多少", "多少"]):
            return self.try_calculate(msg)

        # 时间
        if any(word in msg for word in ["几点", "时间", "现在"]):
            now = datetime.now().strftime("%H:%M:%S")
            return f"🕐 现在是 {now}"

        # 情绪识别 - 开心
        if any(word in msg for word in ["开心", "高兴", "哈哈", "太好了", "耶"]):
            return random.choice([
                "看到你开心我也好开心呀！😄",
                "好棒！保持好心情，好运自然来！🌈",
                "开心就对了！快乐是最好的状态！✨",
            ])

        # 情绪识别 - 难过
        if any(word in msg for word in ["难过", "伤心", "不开心", "烦", "郁闷", "唉"]):
            return random.choice([
                "抱抱你 🤗 不开心的事情总会过去的，明天一定会更好！",
                "难过的时候深呼吸，听听喜欢的音乐，或者找朋友聊聊天 🎵",
                "每个人都会有不开心的时候，这很正常。要不要和我说说怎么了？💛",
            ])

        # 帮助
        if any(word in msg for word in ["帮助", "help", "功能", "你能", "会什么"]):
            return """🤖 我是校园小助手"小智"，我会这些：

📅 查课表 — 输入"课表"或"今天什么课"
😄 讲笑话 — 输入"讲个笑话"或"无聊"
📜 名言警句 — 输入"来句名言"或"励志"
🎓 学习建议 — 输入"学习方法"或"怎么学"
🧮 简单计算 — 输入"算一下 1+2+3"
🕐 查时间 — 输入"几点了"
💬 聊天 — 你说什么我都会回应哦~

试试看吧！"""

        # 告别
        if any(word in msg for word in ["拜拜", "再见", "bye", "退出", "quit"]):
            name_part = f"，{self.user_name}" if self.user_name else ""
            return f"QUIT:拜拜{name_part}！下次再聊哦！👋"

        # 默认回复
        return random.choice(DEFAULT_REPLIES)

    def try_calculate(self, msg):
        """尝试计算数学表达式"""
        import re
        # 从消息中提取数学表达式
        # 只允许数字、运算符、小数点、括号
        expressions = re.findall(r'[\d+\-*/().]+[\d+\-*/().]+', msg)
        if expressions:
            expr = expressions[0]
            try:
                # 安全检查：只允许数学字符
                if re.match(r'^[\d+\-*/().%\s]+$', expr):
                    result = eval(expr)
                    return f"🧮 {expr} = {result}"
            except Exception:
                pass
        return "🤔 我没找到算式呢。试试这样问：算一下 12*5+3"

# ========== 主程序 ==========

def main():
    bot = Chatbot()

    print("=" * 50)
    print("  🤖 校园小助手「小智」")
    print("=" * 50)
    print(f"  {bot.get_greeting()}")
    print("  输入"帮助"看看我能做什么")
    print("  输入"退出"结束对话")
    print("=" * 50)

    while True:
        user_input = input("\n你：").strip()
        if not user_input:
            continue

        bot.chat_count += 1
        reply = bot.match_keywords(user_input)

        # 检查是否要退出
        if reply.startswith("QUIT:"):
            print(f"\n小智：{reply[5:]}")
            print(f"\n📊 本次对话了 {bot.chat_count} 轮，感谢你的陪伴！")
            break

        print(f"\n小智：{reply}")

if __name__ == "__main__":
    main()
