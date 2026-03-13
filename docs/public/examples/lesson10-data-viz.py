"""
第10课示例：我的一周数据可视化
运行方式：python data-viz.py
功能：分析一周的时间数据，生成带 Chart.js 图表的 HTML 报告
"""

import json
import os
import webbrowser
from datetime import datetime

# ========== 示例数据 ==========

SAMPLE_DATA = {
    "日期范围": "2026年3月7日 - 3月13日",
    "天数": ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
    "学习": [3, 4, 2, 3.5, 4, 5, 2.5],
    "运动": [1, 0.5, 1.5, 1, 0.5, 2, 1.5],
    "娱乐": [2, 1.5, 3, 2, 1.5, 3, 4],
    "睡眠": [8, 8, 7.5, 8, 8.5, 9, 9]
}

# ========== 数据分析 ==========

def analyze_data(data):
    """分析一周数据"""
    days = data["天数"]
    study = data["学习"]
    exercise = data["运动"]
    fun = data["娱乐"]
    sleep = data["睡眠"]

    analysis = {
        "总学习": round(sum(study), 1),
        "总运动": round(sum(exercise), 1),
        "总娱乐": round(sum(fun), 1),
        "总睡眠": round(sum(sleep), 1),
        "日均学习": round(sum(study) / len(study), 1),
        "日均运动": round(sum(exercise) / len(exercise), 1),
        "日均睡眠": round(sum(sleep) / len(sleep), 1),
        "学习最多日": days[study.index(max(study))],
        "学习最少日": days[study.index(min(study))],
        "运动达标天数": sum(1 for e in exercise if e >= 1),
    }

    return analysis

# ========== HTML 生成 ==========

def generate_html(data, analysis):
    """生成带 Chart.js 图表的 HTML"""
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>我的一周数据分析</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #e2e8f0;
            min-height: 100vh;
            padding: 20px;
        }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{
            text-align: center;
            font-size: 28px;
            margin-bottom: 4px;
            background: linear-gradient(135deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        .subtitle {{ text-align: center; color: #94a3b8; margin-bottom: 24px; }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
            margin-bottom: 24px;
        }}
        .stat-card {{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }}
        .stat-icon {{ font-size: 24px; }}
        .stat-value {{ font-size: 24px; font-weight: bold; color: #60a5fa; margin: 4px 0; }}
        .stat-label {{ font-size: 12px; color: #94a3b8; }}
        .chart-card {{
            background: rgba(255,255,255,0.05);
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 20px;
        }}
        .chart-title {{
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 16px;
            color: #f1f5f9;
        }}
        .chart-desc {{
            color: #94a3b8;
            font-size: 14px;
            margin-top: 12px;
            line-height: 1.6;
        }}
        canvas {{ max-height: 350px; }}
        .footer {{
            text-align: center;
            color: #475569;
            padding: 20px;
            font-size: 13px;
        }}
        .toggle-btn {{
            position: fixed;
            top: 16px;
            right: 16px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
            padding: 8px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 14px;
        }}
        body.light {{
            background: linear-gradient(135deg, #f0f4ff 0%, #e8ecf4 100%);
            color: #1e293b;
        }}
        body.light .stat-card, body.light .chart-card {{
            background: white;
            border-color: #e2e8f0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}
        body.light .stat-label {{ color: #64748b; }}
        body.light .chart-title {{ color: #1e293b; }}
        body.light .chart-desc {{ color: #475569; }}
    </style>
</head>
<body>
    <button class="toggle-btn" onclick="document.body.classList.toggle('light')">🌓 切换主题</button>
    <div class="container">
        <h1>📊 我的一周数据分析</h1>
        <p class="subtitle">{data['日期范围']} | 生成于 {now}</p>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📚</div>
                <div class="stat-value">{analysis['总学习']}h</div>
                <div class="stat-label">总学习时间</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🏃</div>
                <div class="stat-value">{analysis['运动达标天数']}/7</div>
                <div class="stat-label">运动达标天数</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⭐</div>
                <div class="stat-value">{analysis['学习最多日']}</div>
                <div class="stat-label">最勤奋的一天</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">😴</div>
                <div class="stat-value">{analysis['日均睡眠']}h</div>
                <div class="stat-label">日均睡眠</div>
            </div>
        </div>

        <div class="chart-card">
            <div class="chart-title">📊 每日时间分配对比</div>
            <canvas id="barChart"></canvas>
            <div class="chart-desc">
                柱状图展示了每天学习、运动和娱乐的时间分配。
                {analysis['学习最多日']}学习时间最多，{analysis['学习最少日']}最少。
            </div>
        </div>

        <div class="chart-card">
            <div class="chart-title">🥧 一周时间总体分配</div>
            <canvas id="pieChart"></canvas>
            <div class="chart-desc">
                饼图展示了这一周时间的整体分配比例。
                学习占总活动时间的 {round(analysis['总学习'] / (analysis['总学习'] + analysis['总运动'] + analysis['总娱乐']) * 100, 1)}%。
            </div>
        </div>

        <div class="chart-card">
            <div class="chart-title">📈 学习时间变化趋势</div>
            <canvas id="lineChart"></canvas>
            <div class="chart-desc">
                折线图展示了每天学习时间的变化。日均学习 {analysis['日均学习']} 小时。
            </div>
        </div>

        <div class="footer">
            由 Python + Chart.js 生成 | AI编程启蒙课 第10课
        </div>
    </div>

    <script>
        const labels = {json.dumps(data['天数'], ensure_ascii=False)};
        const studyData = {json.dumps(data['学习'])};
        const exerciseData = {json.dumps(data['运动'])};
        const funData = {json.dumps(data['娱乐'])};

        // 柱状图
        new Chart(document.getElementById('barChart'), {{
            type: 'bar',
            data: {{
                labels: labels,
                datasets: [
                    {{
                        label: '学习',
                        data: studyData,
                        backgroundColor: 'rgba(96, 165, 250, 0.7)',
                        borderRadius: 4
                    }},
                    {{
                        label: '运动',
                        data: exerciseData,
                        backgroundColor: 'rgba(52, 211, 153, 0.7)',
                        borderRadius: 4
                    }},
                    {{
                        label: '娱乐',
                        data: funData,
                        backgroundColor: 'rgba(251, 146, 60, 0.7)',
                        borderRadius: 4
                    }}
                ]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{ display: true, text: '小时', color: '#94a3b8' }},
                        ticks: {{ color: '#94a3b8' }},
                        grid: {{ color: 'rgba(148,163,184,0.1)' }}
                    }},
                    x: {{
                        ticks: {{ color: '#94a3b8' }},
                        grid: {{ color: 'rgba(148,163,184,0.1)' }}
                    }}
                }}
            }}
        }});

        // 饼图
        new Chart(document.getElementById('pieChart'), {{
            type: 'doughnut',
            data: {{
                labels: ['学习', '运动', '娱乐', '睡眠'],
                datasets: [{{
                    data: [{analysis['总学习']}, {analysis['总运动']}, {analysis['总娱乐']}, {analysis['总睡眠']}],
                    backgroundColor: [
                        'rgba(96, 165, 250, 0.8)',
                        'rgba(52, 211, 153, 0.8)',
                        'rgba(251, 146, 60, 0.8)',
                        'rgba(167, 139, 250, 0.8)'
                    ],
                    borderWidth: 0
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }}
            }}
        }});

        // 折线图
        new Chart(document.getElementById('lineChart'), {{
            type: 'line',
            data: {{
                labels: labels,
                datasets: [{{
                    label: '学习时间',
                    data: studyData,
                    borderColor: '#60a5fa',
                    backgroundColor: 'rgba(96, 165, 250, 0.1)',
                    fill: true,
                    tension: 0.3,
                    pointRadius: 5,
                    pointBackgroundColor: '#60a5fa'
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{ legend: {{ labels: {{ color: '#94a3b8' }} }} }},
                scales: {{
                    y: {{
                        beginAtZero: true,
                        title: {{ display: true, text: '小时', color: '#94a3b8' }},
                        ticks: {{ color: '#94a3b8' }},
                        grid: {{ color: 'rgba(148,163,184,0.1)' }}
                    }},
                    x: {{
                        ticks: {{ color: '#94a3b8' }},
                        grid: {{ color: 'rgba(148,163,184,0.1)' }}
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>"""

    return html

# ========== 数据输入 ==========

def input_week_data():
    """手动输入一周数据"""
    days = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    data = {
        "日期范围": input("请输入日期范围（如：3月7日-3月13日）：").strip() or "本周",
        "天数": days,
        "学习": [],
        "运动": [],
        "娱乐": [],
        "睡眠": []
    }

    for day in days:
        print(f"\n--- {day} ---")
        for category in ["学习", "运动", "娱乐", "睡眠"]:
            while True:
                try:
                    hours = float(input(f"  {category}时间（小时）：").strip() or "0")
                    data[category].append(hours)
                    break
                except ValueError:
                    print("  请输入数字！")

    return data

# ========== 主程序 ==========

def main():
    print("=" * 50)
    print("  📊 我的一周数据可视化")
    print("=" * 50)

    choice = input("\n输入自己的数据(1) 还是 使用示例数据(2)？").strip()

    if choice == "1":
        data = input_week_data()
    else:
        data = SAMPLE_DATA
        print("\n使用示例数据...")

    # 分析数据
    analysis = analyze_data(data)

    # 打印摘要
    print(f"\n📊 数据摘要：")
    print(f"  总学习时间：{analysis['总学习']} 小时")
    print(f"  日均运动：{analysis['日均运动']} 小时")
    print(f"  最勤奋的一天：{analysis['学习最多日']}")
    print(f"  运动达标天数：{analysis['运动达标天数']}/7")

    # 生成 HTML
    html = generate_html(data, analysis)
    output_file = "week_report.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n✅ 可视化报告已生成：{output_file}")
    print("正在打开浏览器...")
    webbrowser.open(f"file://{os.path.abspath(output_file)}")

if __name__ == "__main__":
    main()
