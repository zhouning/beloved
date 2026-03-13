"""
第9课示例：学习数据分析器
运行方式：python grade-analyzer.py
功能：分析各科成绩，并生成漂亮的 HTML 报告
"""

import json
import os
import webbrowser
from datetime import datetime

# ========== 示例数据 ==========

SAMPLE_DATA = {
    "姓名": "小明",
    "科目": {
        "语文": [85, 90, 78, 92, 88],
        "数学": [92, 85, 96, 88, 90],
        "英语": [78, 82, 85, 80, 88],
        "物理": [88, 91, 85, 93, 90],
        "历史": [75, 80, 82, 78, 85]
    }
}

DATA_FILE = "grades.json"

# ========== 数据处理 ==========

def analyze_subject(name, scores):
    """分析单科成绩"""
    avg = sum(scores) / len(scores)
    highest = max(scores)
    lowest = min(scores)

    # 趋势分析：比较最近两次和前面的平均
    if len(scores) >= 3:
        recent_avg = sum(scores[-2:]) / 2
        earlier_avg = sum(scores[:-2]) / len(scores[:-2])
        if recent_avg > earlier_avg + 2:
            trend = "↑ 上升"
        elif recent_avg < earlier_avg - 2:
            trend = "↓ 下降"
        else:
            trend = "→ 稳定"
    else:
        trend = "→ 数据不足"

    return {
        "科目": name,
        "平均分": round(avg, 1),
        "最高分": highest,
        "最低分": lowest,
        "趋势": trend,
        "所有成绩": scores
    }

def full_analysis(data):
    """完整分析"""
    results = []
    for subject, scores in data["科目"].items():
        results.append(analyze_subject(subject, scores))

    # 找最强和最弱科目
    results.sort(key=lambda x: x["平均分"], reverse=True)
    strongest = results[0]
    weakest = results[-1]

    # 总平均分
    all_avgs = [r["平均分"] for r in results]
    total_avg = round(sum(all_avgs) / len(all_avgs), 1)

    return {
        "姓名": data["姓名"],
        "各科分析": results,
        "最强科目": strongest["科目"],
        "最弱科目": weakest["科目"],
        "总平均分": total_avg
    }

# ========== 终端输出 ==========

def print_analysis(analysis):
    """在终端打印分析结果"""
    print("\n" + "=" * 55)
    print(f"  📊 {analysis['姓名']} 的成绩分析报告")
    print("=" * 55)

    for item in analysis["各科分析"]:
        print(f"\n📘 {item['科目']}")
        print(f"   平均分：{item['平均分']}  |  最高：{item['最高分']}  |  最低：{item['最低分']}")
        print(f"   趋势：{item['趋势']}")
        bar_len = int(item['平均分'] / 2)
        color = "🟩" if item['平均分'] >= 90 else "🟦" if item['平均分'] >= 60 else "🟥"
        print(f"   {color * bar_len}")

    print(f"\n{'=' * 55}")
    print(f"  🏆 最强科目：{analysis['最强科目']}")
    print(f"  💪 需加油：{analysis['最弱科目']}")
    print(f"  📈 总平均分：{analysis['总平均分']}")
    print(f"{'=' * 55}")

# ========== HTML 报告生成 ==========

def generate_html_report(analysis, data):
    """生成 HTML 报告"""
    subjects = [item["科目"] for item in analysis["各科分析"]]
    averages = [item["平均分"] for item in analysis["各科分析"]]
    highs = [item["最高分"] for item in analysis["各科分析"]]
    lows = [item["最低分"] for item in analysis["各科分析"]]

    # 表格行
    table_rows = ""
    for item in analysis["各科分析"]:
        avg_color = "#10b981" if item["平均分"] >= 90 else "#3b82f6" if item["平均分"] >= 60 else "#ef4444"
        table_rows += f"""
        <tr>
            <td>{item['科目']}</td>
            <td style="color:{avg_color}; font-weight:bold">{item['平均分']}</td>
            <td>{item['最高分']}</td>
            <td>{item['最低分']}</td>
            <td>{item['趋势']}</td>
        </tr>"""

    # 评价
    avg = analysis["总平均分"]
    if avg >= 90:
        comment = "太棒了！各科成绩都很优秀，继续保持！"
    elif avg >= 80:
        comment = "成绩不错！再努努力，争取更上一层楼！"
    elif avg >= 70:
        comment = "成绩中等偏上，重点关注一下薄弱科目。"
    else:
        comment = "还有提升空间，多花时间在薄弱科目上吧！"

    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{analysis['姓名']}的成绩分析报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }}
        h1 {{ color: #1e293b; margin-bottom: 8px; }}
        .subtitle {{ color: #64748b; margin-bottom: 20px; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }}
        .stat-item {{
            background: #f8fafc;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 28px;
            font-weight: bold;
            color: #7c3aed;
        }}
        .stat-label {{ color: #64748b; font-size: 14px; margin-top: 4px; }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 12px;
        }}
        th, td {{
            padding: 12px;
            text-align: center;
            border-bottom: 1px solid #e2e8f0;
        }}
        th {{ background: #f8fafc; color: #475569; font-weight: 600; }}
        .comment {{
            background: linear-gradient(135deg, #f0f9ff, #e0f2fe);
            border-radius: 12px;
            padding: 20px;
            font-size: 16px;
            color: #0369a1;
            text-align: center;
        }}
        .footer {{
            text-align: center;
            color: rgba(255,255,255,0.7);
            padding: 20px;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>📊 {analysis['姓名']}的成绩分析报告</h1>
            <p class="subtitle">生成时间：{now}</p>

            <div class="stats-grid">
                <div class="stat-item">
                    <div class="stat-value">{analysis['总平均分']}</div>
                    <div class="stat-label">总平均分</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">🏆</div>
                    <div class="stat-label">最强：{analysis['最强科目']}</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value">💪</div>
                    <div class="stat-label">加油：{analysis['最弱科目']}</div>
                </div>
            </div>

            <table>
                <tr>
                    <th>科目</th>
                    <th>平均分</th>
                    <th>最高分</th>
                    <th>最低分</th>
                    <th>趋势</th>
                </tr>
                {table_rows}
            </table>
        </div>

        <div class="card">
            <div class="comment">💬 {comment}</div>
        </div>

        <div class="footer">
            由 Python 生成 | AI编程启蒙课 第9课
        </div>
    </div>
</body>
</html>"""

    return html

# ========== 数据输入 ==========

def input_data():
    """手动输入数据"""
    name = input("请输入你的名字：").strip() or "匿名同学"

    subjects_input = input("请输入你的科目（用逗号分隔，如：语文,数学,英语）：").strip()
    subjects = [s.strip() for s in subjects_input.split(",") if s.strip()]

    if not subjects:
        print("没有输入科目，使用示例数据。")
        return SAMPLE_DATA

    data = {"姓名": name, "科目": {}}
    for subject in subjects:
        scores_input = input(f"请输入{subject}的成绩（用空格分隔，如：85 90 78）：").strip()
        scores = []
        for s in scores_input.split():
            try:
                scores.append(int(s))
            except ValueError:
                pass
        if scores:
            data["科目"][subject] = scores
        else:
            print(f"  {subject}没有有效成绩，已跳过。")

    return data if data["科目"] else SAMPLE_DATA

def save_data(data):
    """保存数据到 JSON 文件"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 数据已保存到 {DATA_FILE}")

def load_data():
    """从 JSON 文件加载数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

# ========== 主程序 ==========

def main():
    print("=" * 50)
    print("  📊 学习数据分析器")
    print("=" * 50)

    # 检查是否有已保存的数据
    saved = load_data()
    if saved:
        print(f"\n发现已保存的数据（{saved['姓名']}）")
        choice = input("使用已有数据(1) 还是 输入新数据(2) 还是 使用示例数据(3)？").strip()
        if choice == "1":
            data = saved
        elif choice == "2":
            data = input_data()
            save_data(data)
        else:
            data = SAMPLE_DATA
    else:
        choice = input("\n输入自己的数据(1) 还是 使用示例数据(2)？").strip()
        if choice == "1":
            data = input_data()
            save_data(data)
        else:
            data = SAMPLE_DATA

    # 分析
    analysis = full_analysis(data)

    # 终端输出
    print_analysis(analysis)

    # 生成 HTML
    html = generate_html_report(analysis, data)
    report_file = "report.html"
    with open(report_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n📄 HTML 报告已生成：{report_file}")
    print("正在打开浏览器...")
    webbrowser.open(f"file://{os.path.abspath(report_file)}")

if __name__ == "__main__":
    main()
