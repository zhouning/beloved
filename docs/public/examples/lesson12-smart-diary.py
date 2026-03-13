"""
第12课示例：智能日记本
运行方式：python smart-diary.py
功能：记录每天的日记和心情，提供情绪分析，运行网页版在浏览器中使用
"""

import json
import os
import webbrowser
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

DATA_FILE = "diary.json"
PORT = 8000

# ========== 数据管理 ==========

def load_diary():
    """加载日记数据"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_diary(entries):
    """保存日记数据"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def analyze_mood(entries):
    """分析情绪统计"""
    if not entries:
        return {"total": 0}

    mood_count = {}
    for entry in entries:
        mood = entry.get("mood", "平静")
        mood_count[mood] = mood_count.get(mood, 0) + 1

    most_common = max(mood_count, key=mood_count.get) if mood_count else "平静"
    return {
        "total": len(entries),
        "mood_count": mood_count,
        "most_common": most_common
    }

# ========== HTML 页面 ==========

def get_html():
    """生成聊天界面的 HTML"""
    return """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能日记本</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: linear-gradient(135deg, #fef3c7 0%, #fde68a 50%, #fbbf24 100%);
            min-height: 100vh;
        }
        .app {
            max-width: 600px;
            margin: 0 auto;
            min-height: 100vh;
            background: #fffbeb;
        }
        .header {
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
            padding: 20px;
            text-align: center;
        }
        .header h1 { font-size: 22px; }
        .tabs {
            display: flex;
            background: #fef3c7;
            border-bottom: 2px solid #fde68a;
        }
        .tab {
            flex: 1;
            padding: 12px;
            text-align: center;
            cursor: pointer;
            font-size: 14px;
            color: #92400e;
            transition: all 0.2s;
        }
        .tab.active {
            background: white;
            font-weight: bold;
            border-bottom: 3px solid #f59e0b;
        }
        .page { display: none; padding: 20px; }
        .page.active { display: block; }

        /* 写日记页面 */
        .mood-selector { display: flex; gap: 8px; margin: 12px 0; flex-wrap: wrap; }
        .mood-btn {
            padding: 8px 16px;
            border: 2px solid #fde68a;
            border-radius: 20px;
            background: white;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.2s;
        }
        .mood-btn.selected { border-color: #f59e0b; background: #fef3c7; }
        textarea {
            width: 100%;
            min-height: 150px;
            padding: 12px;
            border: 2px solid #fde68a;
            border-radius: 12px;
            font-size: 15px;
            resize: vertical;
            font-family: inherit;
        }
        textarea:focus { outline: none; border-color: #f59e0b; }
        .save-btn {
            width: 100%;
            padding: 14px;
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            margin-top: 12px;
        }
        .save-btn:hover { opacity: 0.9; }

        /* 日记列表 */
        .entry-card {
            background: white;
            border-radius: 12px;
            padding: 16px;
            margin-bottom: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .entry-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            font-size: 14px;
            color: #92400e;
        }
        .entry-mood { font-size: 20px; }
        .entry-content { color: #44403c; line-height: 1.6; }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #a8a29e;
        }

        /* 统计页面 */
        .stat-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 20px;
        }
        .stat-item {
            background: white;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .stat-value { font-size: 28px; font-weight: bold; color: #d97706; }
        .stat-label { font-size: 13px; color: #78716c; margin-top: 4px; }
        .chart-container {
            background: white;
            border-radius: 12px;
            padding: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }

        .toast {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #065f46;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            display: none;
            z-index: 100;
        }
        .toast.show { display: block; animation: fadeInUp 0.3s; }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateX(-50%) translateY(10px); }
            to { opacity: 1; transform: translateX(-50%) translateY(0); }
        }

        label { display: block; font-weight: 600; color: #78716c; margin: 12px 0 6px; }
    </style>
</head>
<body>
    <div class="app">
        <div class="header">
            <h1>📔 智能日记本</h1>
        </div>

        <div class="tabs">
            <div class="tab active" onclick="showPage('write')">✏️ 写日记</div>
            <div class="tab" onclick="showPage('list')">📖 我的日记</div>
            <div class="tab" onclick="showPage('stats')">📊 心情统计</div>
        </div>

        <!-- 写日记 -->
        <div id="page-write" class="page active">
            <label>📅 日期</label>
            <input type="date" id="diary-date" style="width:100%;padding:10px;border:2px solid #fde68a;border-radius:8px;font-size:15px;">

            <label>你今天的心情</label>
            <div class="mood-selector">
                <button class="mood-btn" onclick="selectMood(this, '开心')">😄 开心</button>
                <button class="mood-btn" onclick="selectMood(this, '平静')">😌 平静</button>
                <button class="mood-btn" onclick="selectMood(this, '难过')">😢 难过</button>
                <button class="mood-btn" onclick="selectMood(this, '生气')">😠 生气</button>
                <button class="mood-btn" onclick="selectMood(this, '兴奋')">🤩 兴奋</button>
            </div>

            <label>写下今天的故事</label>
            <textarea id="diary-content" placeholder="今天发生了什么有趣的事？"></textarea>

            <button class="save-btn" onclick="saveDiary()">💾 保存日记</button>
        </div>

        <!-- 日记列表 -->
        <div id="page-list" class="page">
            <div id="diary-list"></div>
        </div>

        <!-- 统计页面 -->
        <div id="page-stats" class="page">
            <div id="stats-content"></div>
        </div>
    </div>

    <div class="toast" id="toast"></div>

    <script>
        let currentMood = '平静';
        const MOOD_EMOJI = { '开心': '😄', '平静': '😌', '难过': '😢', '生气': '😠', '兴奋': '🤩' };

        // 设置默认日期为今天
        document.getElementById('diary-date').valueAsDate = new Date();

        function showPage(name) {
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.getElementById('page-' + name).classList.add('active');
            event.target.classList.add('active');
            if (name === 'list') loadDiaryList();
            if (name === 'stats') loadStats();
        }

        function selectMood(btn, mood) {
            document.querySelectorAll('.mood-btn').forEach(b => b.classList.remove('selected'));
            btn.classList.add('selected');
            currentMood = mood;
        }

        function showToast(msg) {
            const toast = document.getElementById('toast');
            toast.textContent = msg;
            toast.classList.add('show');
            setTimeout(() => toast.classList.remove('show'), 2000);
        }

        async function saveDiary() {
            const date = document.getElementById('diary-date').value;
            const content = document.getElementById('diary-content').value.trim();
            if (!content) { showToast('请写点什么再保存哦~'); return; }

            const res = await fetch('/api/save', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ date, mood: currentMood, content })
            });
            const data = await res.json();
            if (data.ok) {
                showToast('✅ 日记保存成功！');
                document.getElementById('diary-content').value = '';
            }
        }

        async function loadDiaryList() {
            const res = await fetch('/api/list');
            const entries = await res.json();
            const container = document.getElementById('diary-list');

            if (entries.length === 0) {
                container.innerHTML = '<div class="empty-state">📝 还没有日记，快去写一篇吧！</div>';
                return;
            }

            container.innerHTML = entries.map(e => `
                <div class="entry-card">
                    <div class="entry-header">
                        <span>📅 ${e.date}</span>
                        <span class="entry-mood">${MOOD_EMOJI[e.mood] || '😌'} ${e.mood}</span>
                    </div>
                    <div class="entry-content">${e.content}</div>
                </div>
            `).join('');
        }

        async function loadStats() {
            const res = await fetch('/api/stats');
            const stats = await res.json();
            const container = document.getElementById('stats-content');

            if (stats.total === 0) {
                container.innerHTML = '<div class="empty-state">📊 写几篇日记后就能看到统计啦！</div>';
                return;
            }

            const moods = stats.mood_count || {};
            const labels = Object.keys(moods);
            const values = Object.values(moods);

            container.innerHTML = `
                <div class="stat-grid">
                    <div class="stat-item">
                        <div class="stat-value">${stats.total}</div>
                        <div class="stat-label">总日记数</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${MOOD_EMOJI[stats.most_common] || '😌'}</div>
                        <div class="stat-label">最常见心情：${stats.most_common}</div>
                    </div>
                </div>
                <div class="chart-container">
                    <canvas id="moodChart"></canvas>
                </div>
            `;

            new Chart(document.getElementById('moodChart'), {
                type: 'doughnut',
                data: {
                    labels: labels.map(l => MOOD_EMOJI[l] + ' ' + l),
                    datasets: [{
                        data: values,
                        backgroundColor: ['#fbbf24', '#60a5fa', '#f87171', '#ef4444', '#a78bfa'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: { legend: { position: 'bottom' } }
                }
            });
        }
    </script>
</body>
</html>"""

# ========== HTTP 服务器 ==========

class DiaryHandler(BaseHTTPRequestHandler):
    """处理 HTTP 请求"""

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(get_html().encode('utf-8'))

        elif self.path == '/api/list':
            entries = load_diary()
            entries.reverse()  # 最新的在前
            self.send_json(entries)

        elif self.path == '/api/stats':
            entries = load_diary()
            stats = analyze_mood(entries)
            self.send_json(stats)

        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == '/api/save':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)

            entries = load_diary()
            entries.append({
                "date": data.get("date", datetime.now().strftime("%Y-%m-%d")),
                "mood": data.get("mood", "平静"),
                "content": data.get("content", ""),
                "timestamp": datetime.now().isoformat()
            })
            save_diary(entries)

            self.send_json({"ok": True})
        else:
            self.send_response(404)
            self.end_headers()

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))

    def log_message(self, format, *args):
        pass  # 不在终端输出每个请求日志

# ========== 主程序 ==========

def main():
    print("=" * 50)
    print("  📔 智能日记本")
    print("=" * 50)
    print(f"\n  服务器启动在 http://localhost:{PORT}")
    print("  请在浏览器中打开上面的地址")
    print("  按 Ctrl+C 停止服务器")
    print("=" * 50)

    webbrowser.open(f"http://localhost:{PORT}")

    server = HTTPServer(('localhost', PORT), DiaryHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止。日记数据保存在 diary.json 中。")
        server.server_close()

if __name__ == "__main__":
    main()
