import os
import json
import urllib.parse
from http.server import HTTPServer, SimpleHTTPRequestHandler

PORT = 5050
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.join(BASE_DIR, "projects", "ai_edu_roundtrip")

# Little Prince dirs
LP_SVG_DIR = os.path.join(BASE_DIR, "projects", "little_prince_svg", "svg")
if not os.path.exists(LP_SVG_DIR):
    LP_SVG_DIR = os.path.join(PROJECT_DIR, "analysis", "roundtrip-svg", "flat")
LP_AUDIO_DIR = os.path.join(PROJECT_DIR, "audio")
LP_NOTES_DIR = os.path.join(PROJECT_DIR, "notes")

# Math dirs
MATH_SVG_DIR = os.path.join(BASE_DIR, "projects", "math_assets", "svg")
MATH_NOTES_DIR = os.path.join(BASE_DIR, "projects", "math_assets", "notes")
MATH_IMG_DIR = os.path.join(BASE_DIR, "projects", "math_assets")
MATH_FONTS_DIR = os.path.join(BASE_DIR, "projects", "math_assets", "fonts")

ANNOTATIONS_FILE = os.path.join(PROJECT_DIR, "annotations.json")

class LivePreviewHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        url_path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)
        deck = query.get("deck", ["math"])[0]
        
        # API: list slides
        if url_path == "/api/slides":
            slides = []
            if deck == "math":
                titles = [
                    "1. 수학의 본질 & 동적 시각화",
                    "2. 이차함수 파라미터와 기하학",
                    "3. 삼각함수 주기와 위상 변환",
                    "4. 미분계수와 접선의 순간변화율",
                    "5. 정적분 리만합과 면적 수렴",
                    "6. 시뮬레이터 수업 활용 매뉴얼"
                ]
                for i in range(1, 7):
                    svg_name = f"slide_{i:02d}.svg"
                    note_name = f"slide_{i:02d}.md"
                    note_content = ""
                    note_path = os.path.join(MATH_NOTES_DIR, note_name)
                    if os.path.exists(note_path):
                        with open(note_path, "r", encoding="utf-8") as f:
                            note_content = f.read()
                    
                    slides.append({
                        "id": i,
                        "title": titles[i-1] if i <= len(titles) else f"Math Slide {i:02d}",
                        "svg_url": f"/svg/math/{svg_name}",
                        "audio_url": "",
                        "notes": note_content,
                        "deck": "math"
                    })
            else:
                for i in range(1, 23):
                    svg_name = f"slide_{i:02d}.svg"
                    mp3_name = f"slide_{i:02d}.mp3"
                    note_name = f"slide_{i:02d}.md"
                    
                    note_content = ""
                    note_path = os.path.join(LP_NOTES_DIR, note_name)
                    if os.path.exists(note_path):
                        with open(note_path, "r", encoding="utf-8") as f:
                            note_content = f.read()
                    
                    slides.append({
                        "id": i,
                        "title": f"Slide {i:02d}",
                        "svg_url": f"/svg/{svg_name}",
                        "audio_url": f"/audio/{mp3_name}",
                        "notes": note_content,
                        "deck": "little_prince"
                    })
            
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(slides, ensure_ascii=False).encode("utf-8"))
            return

        # Serve Anime.js library
        if url_path == "/anime.min.js":
            fpath = os.path.join(BASE_DIR, "anime.min.js")
            if os.path.exists(fpath):
                self.send_response(200)
                self.send_header("Content-Type", "application/javascript")
                self.end_headers()
                with open(fpath, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Serve Math SVG files
        if url_path.startswith("/svg/math/"):
            fname = os.path.basename(url_path)
            fpath = os.path.join(MATH_SVG_DIR, fname)
            if os.path.exists(fpath):
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
                self.end_headers()
                with open(fpath, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Serve Little Prince SVG files
        if url_path.startswith("/svg/"):
            fname = os.path.basename(url_path)
            fpath = os.path.join(LP_SVG_DIR, fname)
            if os.path.exists(fpath):
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
                self.end_headers()
                with open(fpath, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Serve Audio files
        if url_path.startswith("/audio/"):
            fname = os.path.basename(url_path)
            fpath = os.path.join(LP_AUDIO_DIR, fname)
            if os.path.exists(fpath):
                self.send_response(200)
                self.send_header("Content-Type", "audio/mpeg")
                self.end_headers()
                with open(fpath, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Serve Math Image files
        if url_path.startswith("/math_assets/"):
            fname = os.path.basename(url_path)
            fpath = os.path.join(MATH_IMG_DIR, fname)
            if os.path.exists(fpath):
                self.send_response(200)
                self.send_header("Content-Type", "image/png")
                self.end_headers()
                with open(fpath, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Serve Font files
        if url_path.startswith("/fonts/"):
            fname = os.path.basename(url_path)
            fpath = os.path.join(MATH_FONTS_DIR, fname)
            if os.path.exists(fpath):
                self.send_response(200)
                self.send_header("Content-Type", "font/ttf")
                self.end_headers()
                with open(fpath, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Serve Little Prince Image files
        if url_path.startswith("/images/"):
            fname = os.path.basename(url_path)
            fpath = os.path.join(BASE_DIR, "projects", "little_prince_svg", "images", fname)
            if not os.path.exists(fpath):
                IMG_DIR = os.path.join(PROJECT_DIR, "images")
                fpath = os.path.join(IMG_DIR, fname)
            if os.path.exists(fpath):
                ext = os.path.splitext(fname)[1].lower()
                ctype = "image/png" if ext == ".png" else "image/jpeg"
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.end_headers()
                with open(fpath, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Downloads
        if url_path == "/download" or url_path == "/download-prince":
            pptx_path = os.path.join(BASE_DIR, "presentations", "AI 시대-교육의 문법이 바뀌다-어린왕자-자율재생-애니메이션.pptx")
            if not os.path.exists(pptx_path):
                pptx_path = os.path.join(BASE_DIR, "presentations", "어린왕자.pptx")
            if not os.path.exists(pptx_path):
                pptx_path = os.path.join(BASE_DIR, "AI 시대-교육의 문법이 바뀌다-어린왕자-자율재생-애니메이션.pptx")
            if os.path.exists(pptx_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
                self.send_header("Content-Disposition", 'attachment; filename="어린왕자-클릭진행.pptx"')
                self.end_headers()
                with open(pptx_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        if url_path == "/download-math":
            pptx_path = os.path.join(BASE_DIR, "presentations", "수학.pptx")
            if not os.path.exists(pptx_path):
                pptx_path = os.path.join(BASE_DIR, "수학.pptx")
            if os.path.exists(pptx_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
                self.send_header("Content-Disposition", 'attachment; filename="수학.pptx"')
                self.end_headers()
                with open(pptx_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        if url_path == "/download-autoplay":
            pptx_path = os.path.join(BASE_DIR, "presentations", "어린왕자-자율재생.pptx")
            if not os.path.exists(pptx_path):
                pptx_path = os.path.join(BASE_DIR, "어린왕자-자율재생.pptx")
            if os.path.exists(pptx_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/vnd.openxmlformats-officedocument.presentationml.presentation")
                self.send_header("Content-Disposition", 'attachment; filename="어린왕자-자율재생.pptx"')
                self.end_headers()
                with open(pptx_path, "rb") as f:
                    self.wfile.write(f.read())
                return

        # Default: Serve Web UI
        if url_path == "/" or url_path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_UI.encode("utf-8"))
            return

        self.send_error(404, "File not found")

    def do_POST(self):
        url_path = urllib.parse.urlparse(self.path).path
        if url_path == "/api/annotate":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                data = json.loads(body)
                annotations = []
                if os.path.exists(ANNOTATIONS_FILE):
                    try:
                        with open(ANNOTATIONS_FILE, "r", encoding="utf-8") as f:
                            annotations = json.load(f)
                    except:
                        annotations = []
                annotations.append(data)
                with open(ANNOTATIONS_FILE, "w", encoding="utf-8") as f:
                    json.dump(annotations, f, ensure_ascii=False, indent=2)
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b'{"status":"ok"}')
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(str(e).encode("utf-8"))
            return
        self.send_error(404)

HTML_UI = """<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <title>PPT Master Studio - 수학교육 & 어린왕자</title>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/fonts-archive/Paperlogy/Paperlogy.css" type="text/css"/>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css">
  <script src="/anime.min.js"></script>
  <style>
    @font-face {
      font-family: 'Paperlogy';
      src: url('/fonts/Paperlogy-5Medium.ttf') format('truetype');
      font-weight: 500;
      font-style: normal;
    }
    @font-face {
      font-family: 'Paperlogy';
      src: url('/fonts/Paperlogy-6SemiBold.ttf') format('truetype');
      font-weight: 600;
      font-style: normal;
    }
    @font-face {
      font-family: 'Paperlogy';
      src: url('/fonts/Paperlogy-7Bold.ttf') format('truetype');
      font-weight: 700;
      font-style: normal;
    }
    @font-face {
      font-family: 'Paperlogy';
      src: url('/fonts/Paperlogy-8ExtraBold.ttf') format('truetype');
      font-weight: 800;
      font-style: normal;
    }
    :root {
      --bg: #090d16;
      --card: #131b2e;
      --card-border: #1e293b;
      --accent: #38bdf8;
      --gold: #fbbf24;
      --rose: #f43f5e;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Paperlogy', 'Pretendard', sans-serif;
      height: 100vh;
      display: flex;
      flex-direction: column;
      overflow: hidden;
      user-select: none;
    }

    /* Header */
    header {
      height: 60px;
      background: rgba(19, 27, 46, 0.98);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 16px;
      z-index: 100;
    }
    .logo-area { display: flex; align-items: center; gap: 8px; }
    .badge {
      font-size: 11px;
      padding: 3px 8px;
      border-radius: 999px;
      font-weight: 700;
      background: rgba(56, 189, 248, 0.15);
      color: var(--accent);
      border: 1px solid rgba(56, 189, 248, 0.3);
    }
    .badge-gold {
      background: rgba(251, 191, 36, 0.15);
      color: var(--gold);
      border-color: rgba(251, 191, 36, 0.3);
    }

    /* Center Big Deck Navigation Tabs */
    .tab-group {
      display: flex;
      background: #0b1120;
      border: 1.5px solid var(--card-border);
      border-radius: 12px;
      padding: 4px;
      gap: 4px;
    }
    .tab-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 7px 16px;
      font-size: 13px;
      font-weight: 800;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .tab-btn:hover { color: #fff; background: rgba(255,255,255,0.06); }
    .tab-btn.active {
      background: var(--accent);
      color: #090d16;
      box-shadow: 0 3px 12px rgba(56, 189, 248, 0.4);
    }
    .tab-btn.active.gold-tab {
      background: var(--gold);
      color: #090d16;
      box-shadow: 0 3px 12px rgba(251, 191, 36, 0.45);
    }

    /* Buttons */
    .btn {
      background: var(--accent);
      color: #090d16;
      border: none;
      border-radius: 8px;
      padding: 6px 12px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      text-decoration: none;
      transition: all 0.2s;
    }
    .btn:hover { filter: brightness(1.15); transform: translateY(-1px); }
    .btn-secondary {
      background: #1e293b;
      color: var(--text);
      border: 1px solid var(--card-border);
    }
    .btn-secondary:hover { background: #334155; }
    .btn-gold {
      background: var(--gold);
      color: #090d16;
    }

    /* Layout */
    .main-container {
      display: flex;
      flex: 1;
      height: calc(100vh - 60px);
      position: relative;
      overflow: hidden;
    }
    #starsCanvas {
      position: absolute;
      top: 0; left: 0;
      width: 100%; height: 100%;
      pointer-events: none;
      z-index: 1;
    }

    /* Sidebar Thumbs */
    .sidebar {
      width: 185px;
      background: #0b1120;
      border-right: 1px solid var(--card-border);
      overflow-y: auto;
      padding: 10px 8px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      z-index: 10;
    }
    .thumb-item {
      background: var(--card);
      border: 2px solid transparent;
      border-radius: 8px;
      padding: 5px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .thumb-item:hover { border-color: rgba(56,189,248,0.5); transform: scale(1.02); }
    .thumb-item.active { border-color: var(--accent); box-shadow: 0 0 14px rgba(56,189,248,0.3); }
    .thumb-title { font-size: 11px; font-weight: 700; margin-bottom: 4px; color: var(--text); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .thumb-frame {
      width: 100%; height: 90px; background: #000; border-radius: 5px; overflow: hidden; display: flex; align-items: center; justify-content: center;
    }
    .thumb-frame object, .thumb-frame img { width: 100%; height: 100%; pointer-events: none; }

    /* Center Viewport */
    .viewport {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 12px;
      position: relative;
      z-index: 10;
    }
    .canvas-card {
      width: 100%;
      max-width: 960px;
      aspect-ratio: 16 / 9;
      background: #0F172A;
      border-radius: 14px;
      overflow: hidden;
      box-shadow: 0 25px 60px -15px rgba(0,0,0,0.85);
      border: 1px solid rgba(255,255,255,0.08);
      position: relative;
      transition: transform 0.15s ease-out;
    }
    .svg-container { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; }

    .controls-bar {
      margin-top: 10px;
      display: flex;
      align-items: center;
      gap: 12px;
      background: rgba(19, 27, 46, 0.85);
      padding: 6px 16px;
      border-radius: 24px;
      border: 1px solid var(--card-border);
    }

    /* Right Details Panel */
    .details-panel {
      width: 320px;
      background: #0b1120;
      border-left: 1px solid var(--card-border);
      padding: 12px;
      display: flex;
      flex-direction: column;
      gap: 12px;
      overflow-y: auto;
      z-index: 10;
    }
    .panel-section {
      background: var(--card);
      border: 1px solid var(--card-border);
      border-radius: 10px;
      padding: 12px;
    }
    .section-title {
      font-size: 12px; font-weight: 700; color: var(--text); margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;
    }
    .notes-box {
      font-size: 11.5px; line-height: 1.6; color: #cbd5e1; max-height: 220px; overflow-y: auto; white-space: pre-wrap; font-family: monospace; background: rgba(0,0,0,0.25); padding: 8px; border-radius: 6px;
    }
    .audio-visualizer {
      display: flex; align-items: flex-end; justify-content: center; gap: 3px; height: 26px; margin-bottom: 8px; background: rgba(0,0,0,0.3); border-radius: 6px; padding: 3px 6px;
    }
    .wave-bar { width: 4px; height: 4px; background: #38bdf8; border-radius: 2px; transition: height 0.08s ease; }
    .wave-bar.gold { background: #fbbf24; }
    audio { width: 100%; height: 32px; filter: invert(0.9) hue-rotate(180deg); }

    /* Interactive Math Lab Studio View: FIXED FLEXBOX WITH VISIBLE CONTROLS */
    #mathLabStudio {
      display: none;
      width: 100%;
      height: 100%;
      background: #0b1120;
      flex-direction: column;
    }
    .math-lab-toolbar {
      height: 48px;
      background: #131b2e;
      border-bottom: 1px solid var(--card-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 12px;
      flex-shrink: 0;
    }
    .math-mode-btn {
      background: transparent;
      border: 1px solid #334155;
      color: #94a3b8;
      padding: 5px 11px;
      font-size: 11.5px;
      font-weight: 700;
      border-radius: 6px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .math-mode-btn:hover { color: #fff; background: rgba(255,255,255,0.05); }
    .math-mode-btn.active {
      background: rgba(56, 189, 248, 0.2);
      border-color: #38bdf8;
      color: #38bdf8;
    }
    .math-lab-body {
      flex: 1;
      display: flex;
      flex-direction: row;
      overflow: hidden;
      position: relative;
      width: 100%;
      height: calc(100% - 48px);
    }
    .canvas-wrapper {
      flex: 1 1 0;
      min-width: 0;
      height: 100%;
      position: relative;
      overflow: hidden;
      display: flex;
      align-items: center;
      justify-content: center;
      background: #090e1a;
    }
    #mathPlotCanvas {
      width: 100%;
      height: 100%;
      display: block;
      cursor: crosshair;
    }
    .canvas-hint {
      position: absolute;
      bottom: 8px;
      left: 10px;
      font-size: 11px;
      color: rgba(255,255,255,0.5);
      pointer-events: none;
      background: rgba(0,0,0,0.5);
      padding: 3px 8px;
      border-radius: 4px;
    }
    .math-controls-sidebar {
      flex: 0 0 290px;
      width: 290px;
      min-width: 290px;
      max-width: 290px;
      background: #0d1527;
      border-left: 2px solid #1e293b;
      padding: 10px;
      display: flex;
      flex-direction: column;
      gap: 9px;
      overflow-y: auto;
      z-index: 20;
    }
    .slider-row {
      display: flex;
      flex-direction: column;
      gap: 3px;
      background: #162035;
      padding: 6px 8px;
      border-radius: 6px;
      border: 1px solid #23314d;
    }
    .slider-header {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      font-weight: 700;
      color: #38bdf8;
    }
    .slider-control-line {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .btn-step {
      width: 24px;
      height: 24px;
      background: #23314d;
      border: none;
      color: #fff;
      font-weight: bold;
      border-radius: 4px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
    }
    .btn-step:hover { background: #38bdf8; color: #000; }
    input[type=range] {
      flex: 1;
      accent-color: #38bdf8;
      cursor: pointer;
      height: 18px;
    }
    .math-info-card {
      background: #162035;
      border: 1.5px solid #38bdf8;
      border-radius: 6px;
      padding: 8px;
      font-size: 11px;
      color: #e2e8f0;
      line-height: 1.55;
    }
  </style>
</head>
<body>
  <header>
    <div class="logo-area">
      <span style="font-size:20px;">📐</span>
      <h2 style="font-size:15px; font-weight:800;">PPT Master Studio</h2>
      <span class="badge badge-gold" id="deckBadge">수학교육 에디션</span>
    </div>

    <!-- Center Big Deck Selector Tabs -->
    <div class="tab-group">
      <button class="tab-btn active" id="tabMath" onclick="switchDeck('math')">📐 수학.pptx 슬라이드 (6장)</button>
      <button class="tab-btn gold-tab" id="tabMathLab" onclick="openMathLab()">🎛️ Live Math Lab (실시간 시뮬레이터)</button>
      <button class="tab-btn" id="tabPrince" onclick="switchDeck('little_prince')">🌟 어린왕자 에디션 (22장)</button>
    </div>

    <!-- Actions -->
    <div style="display:flex; align-items:center; gap:6px;">
      <button class="btn btn-gold" id="btnAutoPlay" onclick="toggleAutoPlay()" title="오디오 종료 시 다음 슬라이드로 자동 진행">⏸️ 자율재생 ON</button>
      <button class="btn btn-secondary" onclick="toggleFullScreen()" title="전체화면 (단축키: F)">🖥️ 전체화면</button>
      <a class="btn btn-gold" href="/download-math" title="수학.pptx 파일 다운로드">📥 수학.pptx 다운로드</a>
      <a class="btn btn-secondary" href="/download" title="어린왕자 클릭진행 PPTX 다운로드">📥 어린왕자.pptx</a>
    </div>
  </header>

  <div class="main-container">
    <canvas id="starsCanvas"></canvas>

    <!-- Thumbnails Sidebar -->
    <div class="sidebar" id="thumbsList"></div>

    <!-- Center Canvas Viewport -->
    <div class="viewport" id="viewportArea">
      <div class="canvas-card" id="mainCanvas">
        <!-- SVG Slide View -->
        <div id="svgContainer" class="svg-container"></div>
        
        <!-- Live Interactive Math Lab Studio -->
        <div id="mathLabStudio">
          <div class="math-lab-toolbar">
            <div style="display:flex; gap:6px; align-items:center;">
              <span style="font-size:12px; font-weight:800; color:#fbbf24;">⚡ MODE:</span>
              <button class="math-mode-btn active" id="btnM1" onclick="setMathMode(1)">[1] 이차함수 포물선</button>
              <button class="math-mode-btn" id="btnM2" onclick="setMathMode(2)">[2] 삼각함수 파동</button>
              <button class="math-mode-btn" id="btnM3" onclick="setMathMode(3)">[3] 미분 접선 역학</button>
              <button class="math-mode-btn" id="btnM4" onclick="setMathMode(4)">[4] 정적분 리만합</button>
            </div>
            <div style="font-size:11px; color:#38bdf8; font-weight:bold;">🖱️ 그래프를 직접 드래그하거나 우측 슬라이더 조절</div>
          </div>
          <div class="math-lab-body">
            <div class="canvas-wrapper">
              <canvas id="mathPlotCanvas"></canvas>
              <div class="canvas-hint">💡 캔버스 위를 클릭 &amp; 드래그하여 그래프 직접 조작 가능</div>
            </div>
            <div class="math-controls-sidebar" id="mathSlidersPanel">
              <!-- Dynamically populated sliders -->
            </div>
          </div>
        </div>
      </div>

      <div class="controls-bar" id="controlsBar">
        <button class="btn btn-secondary" onclick="prevSlide()">◀ 이전 (Left)</button>
        <span id="pageIndicator" style="font-size:13px; font-weight:bold; letter-spacing:1px; min-width:70px; text-align:center;">1 / 6</span>
        <button class="btn btn-secondary" onclick="nextSlide()">다음 (Right/Click) ▶</button>
      </div>
    </div>

    <!-- Right Details Panel -->
    <div class="details-panel">
      <div class="panel-section">
        <div class="section-title">
          <span>🎙️ 발표자 대본 및 지도 가이드</span>
          <span style="font-size:10px; color:#38bdf8;" id="audioTag">수업 지도 가이드</span>
        </div>
        
        <div class="audio-visualizer" id="waveVisualizer" style="display:none;"></div>
        <audio id="audioPlayer" controls style="display:none;"></audio>
        <div class="notes-box" id="notesBox" style="margin-top:4px;">대본을 불러오는 중...</div>
      </div>

      <div class="panel-section">
        <div class="section-title">
          <span>✏️ 실시간 피드백 및 수업 메모</span>
        </div>
        <textarea id="annotationInput" style="width:100%; height:55px; background:#0b1120; border:1px solid #334155; border-radius:6px; color:#fff; padding:6px; font-size:11px;" placeholder="예: 2번 슬라이드 꼭짓점 설명 보완"></textarea>
        <button class="btn" style="width:100%; margin-top:8px; justify-content:center;" onclick="submitAnnotation()">메모 저장</button>
        <div id="statusMsg" style="display:none; color:#38bdf8; font-size:11px; margin-top:4px;">✓ 저장되었습니다!</div>
      </div>

      <div class="panel-section">
        <div class="section-title"><span>📊 프레젠테이션 스펙</span></div>
        <div id="deckSpecInfo" style="font-size:11.5px; color:var(--text-muted); line-height:1.7;">
          • 모드: 수학교육 &amp; 동적 인터랙티브<br>
          • 슬라이드: 6개 단원 수록<br>
          • 서체: Paperlogy 5~8 전체 패밀리<br>
          • 시뮬레이터: HTML5 Canvas 실시간 렌더러
        </div>
      </div>
    </div>
  </div>

  <script>
    let currentDeck = 'math';
    let isMathLabOpen = false;
    let isAutoPlay = true;
    let slides = [];
    let currentIdx = 0;

    // ─────────────────────────────────────────────────────────────
    // 1. Starfield Particle Background
    // ─────────────────────────────────────────────────────────────
    const starsCanvas = document.getElementById('starsCanvas');
    const ctx = starsCanvas.getContext('2d');
    let stars = [];

    function initStars() {
      starsCanvas.width = window.innerWidth;
      starsCanvas.height = window.innerHeight;
      stars = [];
      const numStars = Math.floor((starsCanvas.width * starsCanvas.height) / 14000);
      for (let i = 0; i < numStars; i++) {
        stars.push({
          x: Math.random() * starsCanvas.width,
          y: Math.random() * starsCanvas.height,
          radius: Math.random() * 1.5 + 0.5,
          color: Math.random() > 0.3 ? '#38bdf8' : (Math.random() > 0.5 ? '#fbbf24' : '#e0e7ff'),
          alpha: Math.random() * 0.8 + 0.2,
          speed: Math.random() * 0.02 + 0.005,
          phase: Math.random() * Math.PI * 2
        });
      }
    }
    window.addEventListener('resize', initStars);

    function drawStars() {
      ctx.clearRect(0, 0, starsCanvas.width, starsCanvas.height);
      const time = Date.now() * 0.001;
      stars.forEach(star => {
        const twinkle = Math.sin(time * 2 + star.phase) * 0.3 + 0.7;
        ctx.beginPath();
        ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = star.color;
        ctx.globalAlpha = star.alpha * twinkle;
        ctx.fill();
      });
      requestAnimationFrame(drawStars);
    }
    initStars();
    drawStars();

    // ─────────────────────────────────────────────────────────────
    // 2. Audio Waveform
    // ─────────────────────────────────────────────────────────────
    const waveContainer = document.getElementById('waveVisualizer');
    for (let i = 0; i < 24; i++) {
      const bar = document.createElement('div');
      bar.className = 'wave-bar' + (i % 6 === 0 ? ' gold' : '');
      waveContainer.appendChild(bar);
    }
    const waveBars = waveContainer.querySelectorAll('.wave-bar');

    function animateWaveform() {
      const audio = document.getElementById('audioPlayer');
      const isPlaying = !audio.paused && !audio.ended && audio.currentTime > 0;
      const time = Date.now() * 0.008;

      waveBars.forEach((bar, i) => {
        if (isPlaying) {
          const noise = Math.sin(time * 3 + i * 0.5) * Math.cos(time * 2 + i * 0.3);
          const h = Math.max(4, Math.abs(noise) * 22 + 4);
          bar.style.height = `${h}px`;
        } else {
          const idle = Math.sin(time * 1.2 + i * 0.25) * 2 + 4;
          bar.style.height = `${Math.max(3, idle)}px`;
        }
      });
      requestAnimationFrame(animateWaveform);
    }
    animateWaveform();

    // ─────────────────────────────────────────────────────────────
    // 3. Deck Switching & Slide Loading
    // ─────────────────────────────────────────────────────────────
    async function switchDeck(deck) {
      currentDeck = deck;
      isMathLabOpen = false;
      document.getElementById('svgContainer').style.display = 'flex';
      document.getElementById('mathLabStudio').style.display = 'none';
      document.getElementById('controlsBar').style.display = 'flex';

      document.getElementById('tabMath').className = 'tab-btn' + (deck === 'math' ? ' active' : '');
      document.getElementById('tabPrince').className = 'tab-btn' + (deck === 'little_prince' ? ' active' : '');
      document.getElementById('tabMathLab').className = 'tab-btn gold-tab';

      const audio = document.getElementById('audioPlayer');
      const wave = document.getElementById('waveVisualizer');

      if (deck === 'math') {
        document.getElementById('deckBadge').innerText = '수학교육 에디션';
        document.getElementById('deckBadge').className = 'badge badge-gold';
        document.getElementById('audioTag').innerText = '수업 지도 가이드';
        audio.style.display = 'none';
        wave.style.display = 'none';
        document.getElementById('deckSpecInfo').innerHTML = '• 모드: 수학교육 &amp; 동적 인터랙티브<br>• 슬라이드: 6개 단원 수록<br>• 서체: Paperlogy 5~8 전체 패밀리<br>• 수식: LaTeX 정밀 수식 &amp; 고해상도 그래프';
      } else {
        document.getElementById('deckBadge').innerText = '어린왕자 에디션';
        document.getElementById('deckBadge').className = 'badge';
        document.getElementById('audioTag').innerText = 'Edge-TTS SunHi';
        audio.style.display = 'block';
        wave.style.display = 'flex';
        document.getElementById('deckSpecInfo').innerHTML = '• 모드: AI 시대 교육의 문법<br>• 슬라이드: 22개 슬라이드 전곡<br>• 서체: Paperlogy 5~8<br>• 오디오: 22개 나레이션 수록';
      }

      const res = await fetch(`/api/slides?deck=${deck}`);
      slides = await res.json();
      renderThumbs();
      await loadSlide(0);
    }

    function renderThumbs() {
      const list = document.getElementById('thumbsList');
      list.innerHTML = '';
      slides.forEach((s, idx) => {
        const item = document.createElement('div');
        item.className = 'thumb-item' + (idx === currentIdx ? ' active' : '');
        item.onclick = () => loadSlide(idx);
        item.innerHTML = `
          <div class="thumb-title">${s.title}</div>
          <div class="thumb-frame">
            <object data="${s.svg_url}" type="image/svg+xml" style="pointer-events:none;"></object>
          </div>
        `;
        list.appendChild(item);
      });
    }

    async function loadSlide(idx) {
      if (idx < 0 || idx >= slides.length) return;
      currentIdx = idx;

      const s = slides[idx];
      document.getElementById('pageIndicator').innerText = `${idx + 1} / ${slides.length}`;
      document.getElementById('notesBox').innerText = s.notes || '(해당 슬라이드 메모 없음)';

      const audio = document.getElementById('audioPlayer');
      if (s.audio_url && currentDeck === 'little_prince') {
        audio.style.display = 'block';
        audio.src = s.audio_url;
        if (isAutoPlay) {
          audio.play().catch(e => console.log('Autoplay audio:', e));
        }
      } else {
        audio.style.display = 'none';
        audio.pause();
      }

      const thumbs = document.querySelectorAll('.thumb-item');
      thumbs.forEach((t, i) => {
        t.className = 'thumb-item' + (i === currentIdx ? ' active' : '');
      });
      if (thumbs[currentIdx]) {
        thumbs[currentIdx].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      }

      const container = document.getElementById('svgContainer');
      try {
        const res = await fetch(s.svg_url);
        const svgContent = await res.text();
        container.innerHTML = svgContent;

        const svgEl = container.querySelector('svg');
        if (svgEl) {
          svgEl.setAttribute('width', '100%');
          svgEl.setAttribute('height', '100%');
          svgEl.style.display = 'block';
        }

        if (typeof anime !== 'undefined') {
          // Slide container smooth transition
          anime({
            targets: container,
            opacity: [0.4, 1],
            scale: [0.99, 1],
            duration: 350,
            easing: 'easeOutCubic'
          });

          // Animate slide internal shapes in sequence
          const shapes = container.querySelectorAll('svg > g[id^="shape-"]');
          if (shapes.length > 0) {
            anime({
              targets: shapes,
              opacity: [0, 1],
              translateY: [12, 0],
              delay: anime.stagger(100, {start: 60}),
              duration: 550,
              easing: 'easeOutCubic'
            });
          }
        }
      } catch (e) {
        console.error(e);
      }
    }

    function toggleAutoPlay() {
      isAutoPlay = !isAutoPlay;
      const btn = document.getElementById('btnAutoPlay');
      if (btn) {
        btn.className = 'btn ' + (isAutoPlay ? 'btn-gold' : 'btn-secondary');
        btn.innerHTML = isAutoPlay ? '⏸️ 자율재생 ON' : '▶️ 자율재생 OFF';
      }
      const audio = document.getElementById('audioPlayer');
      if (isAutoPlay && audio && currentDeck === 'little_prince') {
        audio.play().catch(e => {});
      }
    }

    // Auto advance when narration audio completes
    const audioEl = document.getElementById('audioPlayer');
    if (audioEl) {
      audioEl.onended = () => {
        if (isAutoPlay && currentDeck === 'little_prince') {
          setTimeout(() => {
            if (currentIdx < slides.length - 1) {
              loadSlide(currentIdx + 1);
            }
          }, 800);
        }
      };
    }

    function prevSlide() { if (currentIdx > 0) loadSlide(currentIdx - 1); }
    function nextSlide() { if (currentIdx < slides.length - 1) loadSlide(currentIdx + 1); }

    document.addEventListener('keydown', (e) => {
      if (e.target.tagName === 'TEXTAREA' || e.target.tagName === 'INPUT') return;
      if (e.key === 'ArrowLeft') prevSlide();
      if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); nextSlide(); }
      if (e.key.toLowerCase() === 'f') toggleFullScreen();
      if (isMathLabOpen) {
        if (e.key === '1') setMathMode(1);
        if (e.key === '2') setMathMode(2);
        if (e.key === '3') setMathMode(3);
        if (e.key === '4') setMathMode(4);
      }
    });

    function toggleFullScreen() {
      if (!document.fullscreenElement) {
        document.documentElement.requestFullscreen().catch(() => {});
      } else {
        document.exitFullscreen().catch(() => {});
      }
    }

    // ─────────────────────────────────────────────────────────────
    // 4. Live Interactive Math Lab (HTML5 Canvas Studio)
    // ─────────────────────────────────────────────────────────────
    let mathMode = 1;
    let mathParams = {
      m1: { a: 1.0, b: -2.0, c: -1.0 },
      m2: { A: 1.5, B: 2.0, C: 0.0, D: 0.0 },
      m3: { x0: 1.2 },
      m4: { n: 12, b: 3.0 }
    };

    function openMathLab() {
      isMathLabOpen = true;
      document.getElementById('svgContainer').style.display = 'none';
      document.getElementById('mathLabStudio').style.display = 'flex';
      document.getElementById('controlsBar').style.display = 'none';

      document.getElementById('tabPrince').className = 'tab-btn';
      document.getElementById('tabMath').className = 'tab-btn';
      document.getElementById('tabMathLab').className = 'tab-btn gold-tab active';

      document.getElementById('deckBadge').innerText = 'Live Math Lab';
      document.getElementById('deckBadge').className = 'badge badge-gold';

      document.getElementById('notesBox').innerText = 
`[🎛️ Live Math Lab 조작 가이드]
1. 상단 [1~4] 버튼을 눌러 수학 주제를 전환합니다.
2. 우측 슬라이더와 [-] / [+] 버튼으로 계수를 조절합니다.
3. 캔버스 위를 마우스로 직접 클릭 & 드래그해도 파형과 접선이 실시간 추종합니다!
4. 키보드 숫자키 [1], [2], [3], [4]로도 즉시 전환 가능합니다.`;

      setMathMode(mathMode);
    }

    window.openMathLabMode = function(mode) {
      openMathLab();
      setMathMode(mode);
    };

    function setMathMode(mode) {
      mathMode = mode;
      for (let i = 1; i <= 4; i++) {
        const btn = document.getElementById(`btnM${i}`);
        if (btn) btn.className = 'math-mode-btn' + (i === mode ? ' active' : '');
      }
      renderMathSliders();
      // Wait for layout calculation then draw
      setTimeout(drawMathPlot, 20);
    }

    function renderMathSliders() {
      const panel = document.getElementById('mathSlidersPanel');
      panel.innerHTML = '';

      if (mathMode === 1) {
        panel.innerHTML = `
          <div class="math-info-card" id="m1Info"></div>
          ${createSliderHTML('a', '계수 a (곡률/볼록성)', -3.0, 3.0, 0.1, mathParams.m1.a, 'updateM1Param')}
          ${createSliderHTML('b', '계수 b (대칭축 이동)', -5.0, 5.0, 0.1, mathParams.m1.b, 'updateM1Param')}
          ${createSliderHTML('c', '계수 c (y-절편)', -5.0, 5.0, 0.1, mathParams.m1.c, 'updateM1Param')}
        `;
      } else if (mathMode === 2) {
        panel.innerHTML = `
          <div class="math-info-card" id="m2Info"></div>
          ${createSliderHTML('A', '진폭 A (Amplitude)', 0.2, 3.0, 0.1, mathParams.m2.A, 'updateM2Param')}
          ${createSliderHTML('B', '각주파수 B (주기 압축)', 0.5, 4.0, 0.1, mathParams.m2.B, 'updateM2Param')}
          ${createSliderHTML('C', '위상 C (Phase)', -3.14, 3.14, 0.1, mathParams.m2.C, 'updateM2Param')}
          ${createSliderHTML('D', '중심선 D (Offset)', -2.0, 2.0, 0.1, mathParams.m2.D, 'updateM2Param')}
        `;
      } else if (mathMode === 3) {
        panel.innerHTML = `
          <div class="math-info-card" id="m3Info"></div>
          ${createSliderHTML('x0', '접점 x₀ 위치 (Tangent Point)', -2.2, 2.2, 0.05, mathParams.m3.x0, 'updateM3Param')}
        `;
      } else if (mathMode === 4) {
        panel.innerHTML = `
          <div class="math-info-card" id="m4Info"></div>
          ${createSliderHTML('n', '분할 수 n (리만 직사각형)', 4, 50, 2, mathParams.m4.n, 'updateM4Param')}
          ${createSliderHTML('b', '적분 상한 b', 1.0, 4.0, 0.2, mathParams.m4.b, 'updateM4Param')}
        `;
      }
      updateMathCards();
    }

    function createSliderHTML(key, label, min, max, step, val, callbackName) {
      return `
        <div class="slider-row">
          <div class="slider-header">
            <span>${label}</span>
            <span id="val_${key}">${val.toFixed(1)}</span>
          </div>
          <div class="slider-control-line">
            <button class="btn-step" onclick="stepParam('${key}', -${step}, '${callbackName}')">-</button>
            <input type="range" id="input_${key}" min="${min}" max="${max}" step="${step}" value="${val}" oninput="window['${callbackName}']('${key}', parseFloat(this.value))">
            <button class="btn-step" onclick="stepParam('${key}', ${step}, '${callbackName}')">+</button>
          </div>
        </div>
      `;
    }

    function stepParam(key, delta, callbackName) {
      const input = document.getElementById(`input_${key}`);
      if (input) {
        let newVal = parseFloat(input.value) + delta;
        newVal = Math.max(parseFloat(input.min), Math.min(parseFloat(input.max), newVal));
        input.value = newVal;
        if (typeof window[callbackName] === 'function') {
          window[callbackName](key, newVal);
        }
      }
    }

    window.updateM1Param = function(key, val) {
      mathParams.m1[key] = val;
      const el = document.getElementById(`val_${key}`);
      if (el) el.innerText = val.toFixed(1);
      updateMathCards();
      drawMathPlot();
    };

    window.updateM2Param = function(key, val) {
      mathParams.m2[key] = val;
      const el = document.getElementById(`val_${key}`);
      if (el) el.innerText = val.toFixed(1);
      updateMathCards();
      drawMathPlot();
    };

    window.updateM3Param = function(key, val) {
      mathParams.m3[key] = val;
      const el = document.getElementById(`val_${key}`);
      if (el) el.innerText = val.toFixed(2);
      updateMathCards();
      drawMathPlot();
    };

    window.updateM4Param = function(key, val) {
      mathParams.m4[key] = val;
      const el = document.getElementById(`val_${key}`);
      if (el) el.innerText = (key === 'n' ? val : val.toFixed(1));
      updateMathCards();
      drawMathPlot();
    };

    function updateMathCards() {
      if (mathMode === 1) {
        const { a, b, c } = mathParams.m1;
        const p = -b / (2 * a);
        const q = c - (b * b) / (4 * a);
        const D = b * b - 4 * a * c;
        const dStr = D > 0 ? 'D > 0 (두 실근)' : (Math.abs(D) < 0.001 ? 'D = 0 (중근 접함)' : 'D < 0 (허근)');
        const el = document.getElementById('m1Info');
        if (el) el.innerHTML = `
          <b style="color:#38bdf8;">f(x) = ${a.toFixed(1)}x² + ${b.toFixed(1)}x + ${c.toFixed(1)}</b><br>
          • 꼭짓점: (${p.toFixed(2)}, ${q.toFixed(2)})<br>
          • 대칭축: x = ${p.toFixed(2)}<br>
          • 판별식: D = ${D.toFixed(2)} [${dStr}]
        `;
      } else if (mathMode === 2) {
        const { A, B, C, D } = mathParams.m2;
        const T = (2 * Math.PI) / Math.abs(B);
        const el = document.getElementById('m2Info');
        if (el) el.innerHTML = `
          <b style="color:#38bdf8;">y = ${A.toFixed(1)} sin(${B.toFixed(1)}x - ${C.toFixed(1)}) + ${D.toFixed(1)}</b><br>
          • 진폭: |A| = ${Math.abs(A).toFixed(2)}<br>
          • 주기: T = 2π/B = ${T.toFixed(2)}<br>
          • 위상 이동: ${(C/B).toFixed(2)}
        `;
      } else if (mathMode === 3) {
        const { x0 } = mathParams.m3;
        const y0 = Math.pow(x0, 3) - 3 * x0;
        const m = 3 * Math.pow(x0, 2) - 3;
        const el = document.getElementById('m3Info');
        if (el) el.innerHTML = `
          <b style="color:#38bdf8;">f(x) = x³ - 3x (3차함수)</b><br>
          • 접점 P: (${x0.toFixed(2)}, ${y0.toFixed(2)})<br>
          • 접선 기울기: m = ${m.toFixed(2)}<br>
          • 방정식: y = ${m.toFixed(2)}(x - ${x0.toFixed(2)}) + ${y0.toFixed(2)}
        `;
      } else if (mathMode === 4) {
        const { n, b } = mathParams.m4;
        const dx = b / n;
        let sum = 0;
        for (let i = 0; i < n; i++) {
          const x = i * dx;
          sum += Math.pow(x, 2) * dx;
        }
        const exact = Math.pow(b, 3) / 3;
        const err = Math.abs((sum - exact) / exact) * 100;
        const el = document.getElementById('m4Info');
        if (el) el.innerHTML = `
          <b style="color:#38bdf8;">∫₀^${b.toFixed(1)} x² dx = x³/3 |₀^${b.toFixed(1)}</b><br>
          • 참값(Exact): ${exact.toFixed(3)}<br>
          • 리만합(Sₙ): ${sum.toFixed(3)} (n=${n})<br>
          • 오차율: ${err.toFixed(2)}%
        `;
      }
    }

    function drawMathPlot() {
      const canvas = document.getElementById('mathPlotCanvas');
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      const dpr = window.devicePixelRatio || 1;
      canvas.width = rect.width * dpr;
      canvas.height = rect.height * dpr;

      const pctx = canvas.getContext('2d');
      const W = canvas.width;
      const H = canvas.height;

      pctx.fillStyle = '#090e1a';
      pctx.fillRect(0, 0, W, H);

      let xMin = -5, xMax = 5, yMin = -5, yMax = 5;
      if (mathMode === 2) { xMin = -1; xMax = 12; yMin = -4; yMax = 4; }
      if (mathMode === 3) { xMin = -3.5; xMax = 3.5; yMin = -4; yMax = 4; }
      if (mathMode === 4) { xMin = -0.5; xMax = 4.5; yMin = -1; yMax = 16; }

      const toScreenX = (x) => ((x - xMin) / (xMax - xMin)) * W;
      const toScreenY = (y) => H - ((y - yMin) / (yMax - yMin)) * H;

      // Draw Grid
      pctx.strokeStyle = '#1e293b';
      pctx.lineWidth = 1;
      for (let x = Math.ceil(xMin); x <= Math.floor(xMax); x++) {
        pctx.beginPath();
        pctx.moveTo(toScreenX(x), 0);
        pctx.lineTo(toScreenX(x), H);
        pctx.stroke();
      }
      for (let y = Math.ceil(yMin); y <= Math.floor(yMax); y++) {
        pctx.beginPath();
        pctx.moveTo(0, toScreenY(y));
        pctx.lineTo(W, toScreenY(y));
        pctx.stroke();
      }

      // Main Axes
      pctx.strokeStyle = '#64748b';
      pctx.lineWidth = 2 * dpr;
      pctx.beginPath();
      pctx.moveTo(0, toScreenY(0));
      pctx.lineTo(W, toScreenY(0));
      pctx.moveTo(toScreenX(0), 0);
      pctx.lineTo(toScreenX(0), H);
      pctx.stroke();

      // Plot curves based on mode
      if (mathMode === 1) {
        const { a, b, c } = mathParams.m1;
        pctx.strokeStyle = '#38bdf8';
        pctx.lineWidth = 3.5 * dpr;
        pctx.beginPath();
        for (let px = 0; px <= W; px += 2) {
          const x = xMin + (px / W) * (xMax - xMin);
          const y = a * x * x + b * x + c;
          const py = toScreenY(y);
          if (px === 0) pctx.moveTo(px, py); else pctx.lineTo(px, py);
        }
        pctx.stroke();

        // Vertex Point
        const p = -b / (2 * a);
        const q = c - (b * b) / (4 * a);
        pctx.fillStyle = '#fbbf24';
        pctx.beginPath();
        pctx.arc(toScreenX(p), toScreenY(q), 6 * dpr, 0, Math.PI * 2);
        pctx.fill();
      } else if (mathMode === 2) {
        const { A, B, C, D } = mathParams.m2;
        pctx.strokeStyle = '#38bdf8';
        pctx.lineWidth = 3.5 * dpr;
        pctx.beginPath();
        for (let px = 0; px <= W; px += 2) {
          const x = xMin + (px / W) * (xMax - xMin);
          const y = A * Math.sin(B * x - C) + D;
          const py = toScreenY(y);
          if (px === 0) pctx.moveTo(px, py); else pctx.lineTo(px, py);
        }
        pctx.stroke();
      } else if (mathMode === 3) {
        const { x0 } = mathParams.m3;
        pctx.strokeStyle = '#38bdf8';
        pctx.lineWidth = 3.5 * dpr;
        pctx.beginPath();
        for (let px = 0; px <= W; px += 2) {
          const x = xMin + (px / W) * (xMax - xMin);
          const y = Math.pow(x, 3) - 3 * x;
          const py = toScreenY(y);
          if (px === 0) pctx.moveTo(px, py); else pctx.lineTo(px, py);
        }
        pctx.stroke();

        // Tangent line
        const y0 = Math.pow(x0, 3) - 3 * x0;
        const m = 3 * Math.pow(x0, 2) - 3;
        pctx.strokeStyle = '#f43f5e';
        pctx.lineWidth = 2.5 * dpr;
        pctx.beginPath();
        const tLen = 2.5;
        pctx.moveTo(toScreenX(x0 - tLen), toScreenY(y0 - m * tLen));
        pctx.lineTo(toScreenX(x0 + tLen), toScreenY(y0 + m * tLen));
        pctx.stroke();

        // Point P
        pctx.fillStyle = '#fbbf24';
        pctx.beginPath();
        pctx.arc(toScreenX(x0), toScreenY(y0), 6 * dpr, 0, Math.PI * 2);
        pctx.fill();
      } else if (mathMode === 4) {
        const { n, b } = mathParams.m4;
        const dx = b / n;
        pctx.fillStyle = 'rgba(56, 189, 248, 0.25)';
        pctx.strokeStyle = '#38bdf8';
        pctx.lineWidth = 1.5 * dpr;
        for (let i = 0; i < n; i++) {
          const rx = i * dx;
          const ry = Math.pow(rx, 2);
          const sx = toScreenX(rx);
          const sw = toScreenX(rx + dx) - sx;
          const sy = toScreenY(ry);
          const base = toScreenY(0);
          pctx.fillRect(sx, sy, sw, base - sy);
          pctx.strokeRect(sx, sy, sw, base - sy);
        }

        // Curve y = x^2
        pctx.strokeStyle = '#fbbf24';
        pctx.lineWidth = 3.5 * dpr;
        pctx.beginPath();
        for (let px = 0; px <= W; px += 2) {
          const x = xMin + (px / W) * (xMax - xMin);
          const y = Math.pow(x, 2);
          const py = toScreenY(y);
          if (px === 0) pctx.moveTo(px, py); else pctx.lineTo(px, py);
        }
        pctx.stroke();
      }
    }

    // Direct Mouse Click & Drag Interaction on Canvas
    let isCanvasDragging = false;
    const plotCanvas = document.getElementById('mathPlotCanvas');
    
    function handleCanvasInteraction(e) {
      const rect = plotCanvas.getBoundingClientRect();
      const mx = Math.max(0, Math.min(1, (e.clientX - rect.left) / rect.width));
      const my = Math.max(0, Math.min(1, 1 - (e.clientY - rect.top) / rect.height));
      
      let xMin = -5, xMax = 5, yMin = -5, yMax = 5;
      if (mathMode === 2) { xMin = -1; xMax = 12; yMin = -4; yMax = 4; }
      if (mathMode === 3) { xMin = -3.5; xMax = 3.5; yMin = -4; yMax = 4; }
      if (mathMode === 4) { xMin = -0.5; xMax = 4.5; yMin = -1; yMax = 16; }
      
      const mathX = xMin + mx * (xMax - xMin);
      const mathY = yMin + my * (yMax - yMin);
      
      if (mathMode === 1) {
        // Drag vertex (p, q) directly
        const a = mathParams.m1.a;
        const p = mathX;
        const q = mathY;
        mathParams.m1.b = -2 * a * p;
        mathParams.m1.c = q + a * p * p;
        renderMathSliders();
        drawMathPlot();
      } else if (mathMode === 2) {
        // Drag amplitude & phase
        mathParams.m2.A = Math.max(0.2, Math.min(3.0, Math.abs(mathY)));
        mathParams.m2.C = Math.max(-3.14, Math.min(3.14, (mathX - 3) * 0.5));
        renderMathSliders();
        drawMathPlot();
      } else if (mathMode === 3) {
        // Drag tangent point x0
        mathParams.m3.x0 = Math.max(-2.2, Math.min(2.2, mathX));
        renderMathSliders();
        drawMathPlot();
      } else if (mathMode === 4) {
        // Drag upper bound b
        mathParams.m4.b = Math.max(1.0, Math.min(4.0, mathX));
        renderMathSliders();
        drawMathPlot();
      }
    }
    
    plotCanvas.addEventListener('mousedown', (e) => {
      isCanvasDragging = true;
      handleCanvasInteraction(e);
    });
    window.addEventListener('mousemove', (e) => {
      if (isCanvasDragging) handleCanvasInteraction(e);
    });
    window.addEventListener('mouseup', () => {
      isCanvasDragging = false;
    });

    async function submitAnnotation() {
      const input = document.getElementById('annotationInput');
      const val = input.value.trim();
      if (!val) return;
      const res = await fetch('/api/annotate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ slide_idx: currentIdx + 1, deck: currentDeck, note: val, timestamp: new Date().toISOString() })
      });
      if (res.ok) {
        document.getElementById('statusMsg').style.display = 'block';
        input.value = '';
        setTimeout(() => { document.getElementById('statusMsg').style.display = 'none'; }, 3000);
      }
    }

    // Check URL parameters for initial load
    const urlParams = new URLSearchParams(window.location.search);
    const initMode = urlParams.get('mode');
    const initDeck = urlParams.get('deck') || 'math';

    if (initMode === 'lab') {
      openMathLab();
    } else {
      switchDeck(initDeck);
    }
  </script>
</body>
</html>
"""

def run():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, LivePreviewHandler)
    print(f"============================================================")
    print(f"  PPT Master Live Preview & Interactive Studio Server")
    print(f"  Serving on http://localhost:{PORT}")
    print(f"============================================================")
    httpd.serve_forever()

if __name__ == '__main__':
    run()
