"""
第8课示例：文字冒险游戏 - 神秘洞穴探险
运行方式：python adventure-game.py
"""

import random
import time

# ========== 游戏配置 ==========

# 玩家初始状态
def create_player():
    """创建新玩家"""
    return {
        "生命值": 100,
        "背包": [],
        "成就": [],
        "选择次数": 0
    }

# ========== 工具函数 ==========

def slow_print(text, delay=0.03):
    """逐字打印，增加沉浸感"""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def show_status(player):
    """显示玩家状态"""
    print(f"\n❤️  生命值：{player['生命值']}  |  🎒 背包：{', '.join(player['背包']) if player['背包'] else '空'}")
    print("-" * 40)

def get_choice(options):
    """获取玩家选择"""
    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    while True:
        choice = input("\n请输入你的选择（数字）：").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        print("❌ 请输入有效的数字！")

# ========== 游戏场景 ==========

def intro(player):
    """开场"""
    slow_print("\n你是一个年轻的探险家，在一次徒步旅行中，")
    slow_print("你发现了一个隐藏在藤蔓后面的古老洞穴入口...")
    slow_print("洞口散发着微弱的蓝色光芒，空气中弥漫着一股神秘的气息。")

    print("\n你要怎么做？")
    choice = get_choice([
        "🔦 勇敢地走进洞穴",
        "👀 先在洞口仔细观察一下",
        "📱 拍张照发朋友圈再说"
    ])
    player["选择次数"] += 1

    if choice == 1:
        return cave_entrance(player)
    elif choice == 2:
        slow_print("\n你蹲下来观察洞口，发现地上有一把生锈的钥匙！🗝️")
        player["背包"].append("生锈的钥匙")
        player["成就"].append("细心观察者")
        print("✨ 获得物品：生锈的钥匙")
        print("🏆 解锁成就：细心观察者")
        return cave_entrance(player)
    else:
        slow_print("\n你掏出手机拍了张照片。")
        slow_print("突然，一阵风把你推进了洞穴！")
        slow_print("手机掉在了地上...📱💥")
        player["成就"].append("社交达人")
        print("🏆 解锁成就：社交达人（虽然手机没了）")
        return cave_entrance(player)

def cave_entrance(player):
    """洞穴入口"""
    show_status(player)
    slow_print("\n你进入了洞穴。里面比想象中宽敞得多。")
    slow_print("前方分成两条路——")
    slow_print("左边的小路传来流水声 💧")
    slow_print("右边的大路传来奇怪的回声 🔊")

    print("\n你选择哪条路？")
    choice = get_choice([
        "💧 左边的小路（有流水声）",
        "🔊 右边的大路（有回声）"
    ])
    player["选择次数"] += 1

    if choice == 1:
        return water_path(player)
    else:
        return echo_path(player)

def water_path(player):
    """流水小路"""
    show_status(player)
    slow_print("\n你沿着小路走了一会儿，来到了一个地下湖边。")
    slow_print("湖水清澈见底，在蓝色荧光的照耀下美极了 ✨")
    slow_print("湖中央有一个小岛，上面似乎放着什么东西。")
    slow_print("湖边有一条小船，但看起来很旧了...")

    print("\n你要怎么做？")
    choice = get_choice([
        "🚣 划船到小岛上去",
        "🏊 直接游过去",
        "🔙 回去走另一条路"
    ])
    player["选择次数"] += 1

    if choice == 1:
        slow_print("\n你小心翼翼地上了小船...")
        if random.random() > 0.3:
            slow_print("船虽然旧，但还能用！你成功到达了小岛。")
            return island(player)
        else:
            slow_print("船底有个洞！水开始涌入...")
            slow_print("你赶紧跳回岸边，但弄湿了鞋子 💦")
            player["生命值"] -= 10
            print("❤️ 生命值 -10")
            return island_from_swim(player)
    elif choice == 2:
        slow_print("\n你深吸一口气，跳入湖中...")
        slow_print("水很凉！但你坚持游到了小岛。")
        player["生命值"] -= 15
        player["成就"].append("勇敢的游泳者")
        print("❤️ 生命值 -15")
        print("🏆 解锁成就：勇敢的游泳者")
        return island_from_swim(player)
    else:
        return echo_path(player)

def island(player):
    """小岛"""
    slow_print("\n小岛上有一个古老的石台，上面放着一个发光的水晶球 🔮")
    slow_print("水晶球旁边还有一张羊皮纸。")

    player["背包"].append("水晶球")
    print("✨ 获得物品：水晶球")

    slow_print("\n羊皮纸上写着：")
    slow_print('"持水晶者，可见隐藏之门。"')

    return final_chamber(player)

def island_from_swim(player):
    """游泳到小岛"""
    slow_print("\n你湿漉漉地爬上小岛，发现了发光的水晶球 🔮")
    player["背包"].append("水晶球")
    print("✨ 获得物品：水晶球")
    return final_chamber(player)

def echo_path(player):
    """回声大路"""
    show_status(player)
    slow_print("\n你走在大路上，脚步声回荡在四周。")
    slow_print("突然，你看到前方有一扇巨大的石门 🚪")
    slow_print("石门上有一个钥匙孔。")

    if "生锈的钥匙" in player["背包"]:
        print("\n💡 你想起背包里有一把生锈的钥匙！")
        choice = get_choice([
            "🗝️ 用钥匙开门",
            "💪 尝试推开石门"
        ])
        player["选择次数"] += 1

        if choice == 1:
            slow_print("\n钥匙完美地插入了锁孔...")
            slow_print("咔嚓！石门缓缓打开了！")
            player["成就"].append("解锁大师")
            print("🏆 解锁成就：解锁大师")
            return treasure_room(player)
        else:
            return push_door(player)
    else:
        print("\n石门紧锁着，你没有钥匙。")
        choice = get_choice([
            "💪 尝试推开石门",
            "🔍 在附近寻找线索",
            "🔙 回去走另一条路"
        ])
        player["选择次数"] += 1

        if choice == 1:
            return push_door(player)
        elif choice == 2:
            slow_print("\n你在墙壁上发现了一个暗格！")
            slow_print("里面有一把钥匙 🗝️")
            player["背包"].append("生锈的钥匙")
            print("✨ 获得物品：生锈的钥匙")
            slow_print("\n你用钥匙打开了石门！")
            return treasure_room(player)
        else:
            return water_path(player)

def push_door(player):
    """推门"""
    slow_print("\n你用力推石门...")
    slow_print("门纹丝不动...但你发现门上有一段文字：")
    slow_print('"回答谜题，门将为你敞开。"')

    slow_print("\n谜题：什么东西早上四条腿，中午两条腿，晚上三条腿？")
    answer = input("你的答案：").strip()
    player["选择次数"] += 1

    if "人" in answer:
        slow_print("\n✅ 回答正确！石门轰然打开！")
        player["成就"].append("智慧解谜者")
        print("🏆 解锁成就：智慧解谜者")
        return treasure_room(player)
    else:
        slow_print("\n❌ 回答错误...石门上射出一道光！")
        player["生命值"] -= 20
        print("❤️ 生命值 -20")
        slow_print("不过门还是打开了一条缝，你挤了进去。")
        return treasure_room(player)

def treasure_room(player):
    """宝藏室"""
    show_status(player)
    slow_print("\n你进入了一个金碧辉煌的大厅！🏛️")
    slow_print("到处都是闪闪发光的宝石和金币！")
    slow_print("在大厅的尽头，有一个王座，上面坐着一个石像。")
    slow_print("石像开口说话了：")
    slow_print('"勇敢的探险家，你可以带走一样宝物。"')

    print("\n你选择哪样？")
    choice = get_choice([
        "👑 金色王冠（象征权力）",
        "📖 古老魔法书（象征知识）",
        "💎 永恒钻石（象征财富）"
    ])
    player["选择次数"] += 1

    if choice == 1:
        return ending_crown(player)
    elif choice == 2:
        return ending_book(player)
    else:
        return ending_diamond(player)

def final_chamber(player):
    """水晶球持有者的最终房间"""
    show_status(player)
    slow_print("\n水晶球突然发出耀眼的光芒！")
    slow_print("你面前的墙壁上显现出一扇隐藏的门 🚪✨")
    slow_print("你推开门，发现了一个比宝藏室更神奇的地方——")
    slow_print("一个充满星光的房间，仿佛置身于宇宙之中 🌌")

    slow_print("\n一个声音在你耳边响起：")
    slow_print('"你找到了洞穴的真正秘密。选择你的命运。"')

    print("\n你要怎么做？")
    choice = get_choice([
        "🌟 触摸最亮的那颗星星",
        "🏠 许愿回家",
        "🔮 用水晶球照亮整个房间"
    ])
    player["选择次数"] += 1

    if choice == 1:
        return ending_star(player)
    elif choice == 2:
        return ending_home(player)
    else:
        return ending_crystal(player)

# ========== 结局 ==========

def ending_crown(player):
    """王冠结局"""
    player["成就"].append("荣耀之王")
    slow_print("\n👑 你拿起了金色王冠，戴在头上。")
    slow_print("整个洞穴开始震动...你被传送回了地面。")
    slow_print("从此你成为了传说中的探险家之王！")
    print("\n🎬 结局：荣耀之王 👑")
    show_final(player)

def ending_book(player):
    """魔法书结局"""
    player["成就"].append("知识追求者")
    slow_print("\n📖 你翻开了古老的魔法书。")
    slow_print("书中的知识如洪水般涌入你的脑海...")
    slow_print("你领悟了编程的终极奥义——万物皆可用代码创造！")
    print("\n🎬 结局：知识追求者 📖")
    show_final(player)

def ending_diamond(player):
    """钻石结局"""
    player["成就"].append("财富猎人")
    slow_print("\n💎 你拿起了永恒钻石。")
    slow_print("但钻石突然变得越来越重...你丢下了它。")
    slow_print("石像笑了：'真正的宝藏不是金银财宝，而是这段冒险的经历。'")
    slow_print("你空手走出了洞穴，但心中充满了领悟。")
    print("\n🎬 结局：领悟者 💎")
    show_final(player)

def ending_star(player):
    """星星结局"""
    player["成就"].append("追星者")
    slow_print("\n🌟 你伸手触摸了那颗最亮的星星。")
    slow_print("瞬间，你感觉自己在宇宙中飞翔...")
    slow_print("当你睁开眼，发现自己站在山顶，看着日出。")
    slow_print("那是你见过的最美的风景。")
    print("\n🎬 结局：星空旅行者 🌟")
    show_final(player)

def ending_home(player):
    """回家结局"""
    player["成就"].append("温暖归人")
    slow_print("\n🏠 你闭上眼许愿：'我想回家。'")
    slow_print("温暖的光芒包围了你...")
    slow_print("当你睁开眼，你站在家门口，手里握着水晶球。")
    slow_print("妈妈打开门：'回来啦？正好，饭做好了。'")
    slow_print("你笑了。有时候，最好的冒险就是回家。")
    print("\n🎬 结局：温暖归人 🏠")
    show_final(player)

def ending_crystal(player):
    """水晶球结局"""
    player["成就"].append("真相发现者")
    slow_print("\n🔮 你举起水晶球，它发出了耀眼的光芒。")
    slow_print("整个星空房间亮了起来，你看到了洞穴的全貌——")
    slow_print("原来这是一个古老文明留下的图书馆！")
    slow_print("墙壁上的星星是知识的索引，水晶球是读取的钥匙。")
    slow_print("你成为了这个图书馆新的守护者。")
    print("\n🎬 结局：知识的守护者 🔮（隐藏最佳结局！）")
    show_final(player)

def show_final(player):
    """显示最终统计"""
    print("\n" + "=" * 50)
    print("📊 冒险统计")
    print("=" * 50)
    print(f"❤️  最终生命值：{player['生命值']}")
    print(f"🎒 收集物品：{', '.join(player['背包']) if player['背包'] else '无'}")
    print(f"🏆 解锁成就：{', '.join(player['成就']) if player['成就'] else '无'}")
    print(f"🔢 总选择次数：{player['选择次数']}")
    print("=" * 50)

# ========== 主程序 ==========

def main():
    """游戏主入口"""
    print("=" * 50)
    print("   🏔️  神 秘 洞 穴 探 险  🏔️")
    print("=" * 50)
    print("  一个文字冒险游戏")
    print("  提示：不同的选择会导向不同的结局哦！")
    print("=" * 50)

    while True:
        player = create_player()
        intro(player)

        print("\n" + "-" * 50)
        again = input("🔄 想再玩一次吗？试试不同的选择！(y/n): ").strip().lower()
        if again != 'y':
            slow_print("\n感谢你的冒险！下次再见！👋")
            break
        print("\n" + "=" * 50)
        print("   🔄 开始新的冒险...")
        print("=" * 50)

if __name__ == "__main__":
    main()
