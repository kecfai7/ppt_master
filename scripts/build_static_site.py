import os
import shutil
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC_DIR = os.path.join(BASE_DIR, "public")

print("Building Static Web Assets for Vercel & GitHub Pages...")

# 1. Clean / create public directory
os.makedirs(PUBLIC_DIR, exist_ok=True)
os.makedirs(os.path.join(PUBLIC_DIR, "svg", "math"), exist_ok=True)
os.makedirs(os.path.join(PUBLIC_DIR, "audio"), exist_ok=True)
os.makedirs(os.path.join(PUBLIC_DIR, "images"), exist_ok=True)
os.makedirs(os.path.join(PUBLIC_DIR, "fonts"), exist_ok=True)
os.makedirs(os.path.join(PUBLIC_DIR, "api"), exist_ok=True)
os.makedirs(os.path.join(PUBLIC_DIR, "presentations"), exist_ok=True)

# 2. Copy Math SVGs
math_svg_src = os.path.join(BASE_DIR, "projects", "math_assets", "svg")
if os.path.exists(math_svg_src):
    for f in os.listdir(math_svg_src):
        if f.endswith(".svg"):
            shutil.copy2(os.path.join(math_svg_src, f), os.path.join(PUBLIC_DIR, "svg", "math", f))
print("Copied Math SVGs")

# 3. Copy Little Prince SVGs
lp_svg_src = os.path.join(BASE_DIR, "projects", "little_prince_svg", "svg")
if not os.path.exists(lp_svg_src):
    lp_svg_src = os.path.join(BASE_DIR, "projects", "ai_edu_roundtrip", "analysis", "roundtrip-svg", "flat")
if os.path.exists(lp_svg_src):
    for f in os.listdir(lp_svg_src):
        if f.endswith(".svg"):
            shutil.copy2(os.path.join(lp_svg_src, f), os.path.join(PUBLIC_DIR, "svg", f))
print("Copied Little Prince SVGs")

# 4. Copy Audios
audio_src = os.path.join(BASE_DIR, "projects", "ai_edu_roundtrip", "audio")
if os.path.exists(audio_src):
    for f in os.listdir(audio_src):
        if f.endswith(".mp3"):
            shutil.copy2(os.path.join(audio_src, f), os.path.join(PUBLIC_DIR, "audio", f))
print("Copied Audio MP3s")

# 5. Copy Images
img_src = os.path.join(BASE_DIR, "projects", "little_prince_svg", "images")
if os.path.exists(img_src):
    for f in os.listdir(img_src):
        shutil.copy2(os.path.join(img_src, f), os.path.join(PUBLIC_DIR, "images", f))
print("Copied Images")

# 6. Copy Fonts
font_src = os.path.join(BASE_DIR, "projects", "math_assets", "fonts")
if os.path.exists(font_src):
    for f in os.listdir(font_src):
        if f.endswith(".ttf"):
            shutil.copy2(os.path.join(font_src, f), os.path.join(PUBLIC_DIR, "fonts", f))
print("Copied Fonts")

# 7. Copy Anime.js
if os.path.exists(os.path.join(BASE_DIR, "anime.min.js")):
    shutil.copy2(os.path.join(BASE_DIR, "anime.min.js"), os.path.join(PUBLIC_DIR, "anime.min.js"))

# 8. Copy Key Presentations for direct web download
pres_src = os.path.join(BASE_DIR, "presentations")
if os.path.exists(pres_src):
    for p_name in ["수학.pptx", "AI 시대-교육의 문법이 바뀌다-어린왕자-자율재생-애니메이션.pptx", "어린왕자-자율재생.pptx", "어린왕자.pptx"]:
        src_file = os.path.join(pres_src, p_name)
        if os.path.exists(src_file):
            shutil.copy2(src_file, os.path.join(PUBLIC_DIR, "presentations", p_name))
print("Copied Presentations for Web Download")

# 9. Generate Static JSON Data
MATH_NOTES_DIR = os.path.join(BASE_DIR, "projects", "math_assets", "notes")
LP_NOTES_DIR = os.path.join(BASE_DIR, "projects", "ai_edu_roundtrip", "notes")

math_titles = [
    "1. 수학의 본질 & 동적 시각화",
    "2. 이차함수 파라미터와 기하학",
    "3. 삼각함수 주기와 위상 변환",
    "4. 미분계수와 접선의 순간변화율",
    "5. 정적분 리만합과 면적 수렴",
    "6. 시뮬레이터 수업 활용 매뉴얼"
]
math_slides = []
for i in range(1, 7):
    note_path = os.path.join(MATH_NOTES_DIR, f"slide_{i:02d}.md")
    notes = open(note_path, encoding="utf-8").read() if os.path.exists(note_path) else ""
    math_slides.append({
        "id": i,
        "title": math_titles[i-1],
        "svg_url": f"/svg/math/slide_{i:02d}.svg",
        "audio_url": "",
        "notes": notes,
        "deck": "math"
    })

prince_slides = []
for i in range(1, 23):
    note_path = os.path.join(LP_NOTES_DIR, f"slide_{i:02d}.md")
    notes = open(note_path, encoding="utf-8").read() if os.path.exists(note_path) else ""
    prince_slides.append({
        "id": i,
        "title": f"Slide {i:02d}",
        "svg_url": f"/svg/slide_{i:02d}.svg",
        "audio_url": f"/audio/slide_{i:02d}.mp3",
        "notes": notes,
        "deck": "little_prince"
    })

with open(os.path.join(PUBLIC_DIR, "api", "slides_math.json"), "w", encoding="utf-8") as f:
    json.dump(math_slides, f, ensure_ascii=False, indent=2)

with open(os.path.join(PUBLIC_DIR, "api", "slides_prince.json"), "w", encoding="utf-8") as f:
    json.dump(prince_slides, f, ensure_ascii=False, indent=2)

print("Generated API Static JSON files")

# 10. Generate index.html from HTML_UI in live_preview_server.py
server_path = os.path.join(BASE_DIR, "scripts", "live_preview_server.py")
with open(server_path, "r", encoding="utf-8") as f:
    server_code = f.read()

s_idx = server_code.find('HTML_UI = """')
e_idx = server_code.find('"""\n\ndef run():')
if s_idx != -1 and e_idx != -1:
    html_content = server_code[s_idx + len('HTML_UI = """'):e_idx]
    
    # Update fetch call in switchDeck to support static hosting fallback:
    # const res = await fetch(`/api/slides?deck=${deck}`); -> fetch static json
    old_fetch = "const res = await fetch(`/api/slides?deck=${deck}`);"
    new_fetch = """let res;
      try {
        res = await fetch(`/api/slides?deck=${deck}`);
        if (!res.ok) throw new Error('API fallback');
      } catch (err) {
        const jsonFile = deck === 'math' ? '/api/slides_math.json' : '/api/slides_prince.json';
        res = await fetch(jsonFile);
      }"""
    html_content = html_content.replace(old_fetch, new_fetch)
    
    # Also adjust download links for static hosting
    html_content = html_content.replace('href="/download-math"', 'href="/presentations/수학.pptx" download')
    html_content = html_content.replace('href="/download"', 'href="/presentations/AI 시대-교육의 문법이 바뀌다-어린왕자-자율재생-애니메이션.pptx" download')

    # Save to public/index.html and root index.html
    with open(os.path.join(PUBLIC_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    with open(os.path.join(BASE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Exported updated index.html to public/ and root!")

print("Static Web Assets Build Complete!")

