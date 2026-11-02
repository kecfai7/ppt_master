import os
import re
import io
import zipfile
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# Import Paperlogy font styling from helpers
from build_presentation_helpers import (
    apply_paperlogy_to_deck,
    FONT_TITLE, FONT_HEADING, FONT_SUBTITLE, FONT_BODY,
    set_font_p, set_font_run
)

# Colors
C_BG = RGBColor(15, 23, 42)          # #0F172A Deep Slate
C_CARD = RGBColor(30, 41, 59)        # #1E293B Card Slate
C_BORDER = RGBColor(51, 65, 85)      # #334155
C_ACCENT = RGBColor(56, 189, 248)    # #38BDF8 Sky Blue
C_GOLD = RGBColor(251, 191, 36)      # #FBBF24 Amber
C_ROSE = RGBColor(244, 63, 94)       # #F43F5E Rose
C_TEXT = RGBColor(248, 250, 252)     # #F8FAFC White
C_MUTED = RGBColor(148, 163, 184)    # #94A3B8 Gray
C_NAV_BG = RGBColor(30, 58, 95)      # #1E3A5F Nav Button BG

def set_native_background(slide):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = C_BG

def add_header(slide, badge_text, title_text, subtitle_text):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.32), Inches(8.4), Inches(1.05))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p0 = tf.paragraphs[0]
    p0.text = f"●  {badge_text.upper()}"
    p0.font.size = Pt(10.5)
    p0.font.bold = True
    p0.font.color.rgb = C_ACCENT
    p0.space_after = Pt(2)
    
    p1 = tf.add_paragraph()
    p1.text = title_text
    p1.font.size = Pt(20)
    p1.font.bold = True
    p1.font.color.rgb = C_TEXT
    p1.space_after = Pt(2)
    
    p2 = tf.add_paragraph()
    p2.text = subtitle_text
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_MUTED

def add_card(slide, left, top, width, height, title, items, border_color=C_BORDER):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = C_CARD
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)
    
    tb = slide.shapes.add_textbox(left + Inches(0.18), top + Inches(0.14), width - Inches(0.36), height - Inches(0.28))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    if title:
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.size = Pt(12.5)
        p0.font.bold = True
        p0.font.color.rgb = C_ACCENT
        p0.space_after = Pt(5)
    
    for i, itm in enumerate(items):
        p = tf.add_paragraph() if (title or i > 0) else tf.paragraphs[0]
        p.text = itm
        p.font.size = Pt(10.5)
        p.font.color.rgb = C_TEXT
        p.space_after = Pt(3.5)

def add_action_button(slide, left, top, width, height, text, target_url, bg_color=C_CARD, border_color=C_ACCENT, text_color=C_ACCENT):
    btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    btn.fill.solid()
    btn.fill.fore_color.rgb = bg_color
    btn.line.color.rgb = border_color
    btn.line.width = Pt(1.5)
    btn.click_action.hyperlink.address = target_url
    
    tf = btn.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = text_color
    p.alignment = PP_ALIGN.CENTER
    return btn

def set_speaker_notes(slide, notes_text):
    if not slide.has_notes_slide:
        slide.notes_slide
    tf = slide.notes_slide.notes_text_frame
    tf.text = notes_text.strip()

def build_math_deck():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    blank_layout = prs.slide_layouts[6]
    
    slides = []

    # =========================================================================
    # SLIDE 1: Title & Hero
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_native_background(s1)
    slides.append(s1)
    
    tb1 = s1.shapes.add_textbox(Inches(0.8), Inches(0.9), Inches(8.4), Inches(2.6))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "● MATHEMATICS EDUCATION & DYNAMIC VISUALIZATION"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_GOLD
    p.space_after = Pt(12)
    
    p = tf1.add_paragraph()
    p.text = "수학의 본질을 꿰뚫는\nLaTeX 수식 & 동적 그래프 시뮬레이션"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = C_TEXT
    p.space_after = Pt(12)
    
    p = tf1.add_paragraph()
    p.text = "수학교사를 위한 인터랙티브 시각화, 마우스 & 키보드 조절 파라미터 수업 설계"
    p.font.size = Pt(13)
    p.font.color.rgb = C_MUTED
    
    # Hero Info Card
    add_card(
        s1, Inches(0.8), Inches(3.6), Inches(8.4), Inches(0.65),
        None,
        ["⚡ 마우스 클릭 진행  |  📐 LaTeX 수식 정밀 렌더링  |  🎛️ 실시간 동적 GUI 시뮬레이터 수록"]
    )
    
    # Action Launch Buttons on Cover
    add_action_button(
        s1, Inches(0.8), Inches(4.35), Inches(4.1), Inches(0.55),
        "🎛️ Python GUI 시뮬레이터 실행하기 (클릭)",
        "수학_시뮬레이터_실행.bat",
        bg_color=RGBColor(35, 25, 15), border_color=C_GOLD, text_color=C_GOLD
    )
    add_action_button(
        s1, Inches(5.1), Inches(4.35), Inches(4.1), Inches(0.55),
        "🌐 웹 인터랙티브 랩 바로 열기 (클릭)",
        "http://localhost:5050",
        bg_color=RGBColor(15, 35, 55), border_color=C_ACCENT, text_color=C_ACCENT
    )
    
    set_speaker_notes(
        s1,
        "[도입] 선생님 여러분 안녕하십니까. 정적인 칠판 수식에서 벗어나 파라미터의 변화에 따라 "
        "살아 움직이는 함수의 거동과 기하학적 의미를 시각적으로 직관화하는 수업 모델입니다. "
        "슬라이드 쇼(F5) 중 화면의 [시뮬레이터 실행] 버튼을 클릭하시면 실시간 조작창이 열립니다."
    )

    # =========================================================================
    # SLIDE 2: 이차함수
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_native_background(s2)
    slides.append(s2)
    add_header(s2, "Algebra & Geometry", "이차함수의 파라미터 변화와 기하학적 거동", "f(x) = a(x - p)² + q 에서 계수 a, p, q의 변화가 궤적에 미치는 영향")
    
    add_card(
        s2, Inches(0.8), Inches(1.45), Inches(4.2), Inches(3.45),
        "핵심 개념 및 지도 포인트",
        [
            "• 표준형 수식:  f(x) = a(x - p)² + q",
            "• 일반형 수식:  f(x) = ax² + bx + c",
            "• 꼭짓점의 좌표:  (p, q) = (-b/2a,  -(b²-4ac)/4a)",
            "• 대칭축의 방정식:  x = p (좌우 완전 대칭성)",
            "• 판별식 D = b² - 4ac:",
            "   - D > 0: x축과 서로 다른 두 실근 교차",
            "   - D = 0: x축에 접함 (중근)",
            "   - D < 0: x축과 만나지 않음 (허근)",
            "💡 [실시간 조작]: 우측 하단 [🎛️ GUI] 또는 [🌐 웹 랩] 버튼을",
            "   클릭하면 a, b, c 계수를 마우스/키보드로 직접 조절합니다."
        ]
    )
    plot2 = os.path.join('projects', 'math_assets', 'graph_quadratic.png')
    if os.path.exists(plot2):
        pic2 = s2.shapes.add_picture(plot2, Inches(5.2), Inches(1.45), Inches(4.0), Inches(2.85))
        pic2.click_action.hyperlink.address = "http://localhost:5050"
    
    add_action_button(s2, Inches(5.2), Inches(4.38), Inches(1.95), Inches(0.48), "🎛️ GUI 시뮬레이터", "수학_시뮬레이터_실행.bat", bg_color=C_CARD, border_color=C_GOLD, text_color=C_GOLD)
    add_action_button(s2, Inches(7.25), Inches(4.38), Inches(1.95), Inches(0.48), "🌐 웹 실시간 랩", "http://localhost:5050", bg_color=C_CARD, border_color=C_ACCENT, text_color=C_ACCENT)
        
    set_speaker_notes(
        s2,
        "[수업 가이드] 꼭짓점 p가 바뀔 때 포물선 축 전체가 평행이동하고, a의 절댓값이 커질수록 곡선 폭이 급격히 좁아지는 기하학적 직관을 제시합니다. "
        "우측 버튼을 눌러 a 슬라이더를 음수로 옮기며 즉각적인 상하 반전을 관찰시킵니다."
    )

    # =========================================================================
    # SLIDE 3: 삼각함수
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_native_background(s3)
    slides.append(s3)
    add_header(s3, "Periodic Functions", "삼각함수의 진폭, 주기와 위상 변환", "y = A sin(Bx - C) + D 파동 모델링과 단위원을 통한 해석")
    
    add_card(
        s3, Inches(0.8), Inches(1.45), Inches(4.2), Inches(3.45),
        "파동 수식 모델 분석",
        [
            "• 일반형 수식:  y = A sin(Bx - C) + D",
            "• 진폭(Amplitude):  |A|  (파동의 수직 진동 폭)",
            "• 주기(Period):  T = 2π / |B|  (1회 파동 완결 길이)",
            "• 위상 이동(Phase Shift):  x 방향으로 C/B 만큼 이동",
            "• 수직 중심선 이동:  y = D 만큼 축 이동",
            "• 최댓값 M = |A| + D,  최솟값 m = -|A| + D",
            "💡 [오개념 방지]: B가 커질수록 주기가 1/B로 압축되는",
            "   파동 현상을 우측 [🎛️ 시뮬레이터] 버튼으로 직접 검증합니다."
        ]
    )
    plot3 = os.path.join('projects', 'math_assets', 'graph_trig.png')
    if os.path.exists(plot3):
        pic3 = s3.shapes.add_picture(plot3, Inches(5.2), Inches(1.45), Inches(4.0), Inches(2.85))
        pic3.click_action.hyperlink.address = "http://localhost:5050"
        
    add_action_button(s3, Inches(5.2), Inches(4.38), Inches(1.95), Inches(0.48), "🎛️ GUI 시뮬레이터", "수학_시뮬레이터_실행.bat", bg_color=C_CARD, border_color=C_GOLD, text_color=C_GOLD)
    add_action_button(s3, Inches(7.25), Inches(4.38), Inches(1.95), Inches(0.48), "🌐 웹 실시간 랩", "http://localhost:5050", bg_color=C_CARD, border_color=C_ACCENT, text_color=C_ACCENT)
        
    set_speaker_notes(
        s3,
        "[오개념 교정] 파란색 실선(B=2)과 회색 점선(B=1)을 대조하여 B가 커질수록 같은 2π 구간 안에 파동이 2배 촘촘하게 채워짐을 명확히 보여주십시오."
    )

    # =========================================================================
    # SLIDE 4: 미분계수
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_native_background(s4)
    slides.append(s4)
    add_header(s4, "Differential Calculus", "평균변화율에서 순간변화율(접선)로의 수렴", "h → 0 일 때 두 점을 잇는 할선이 한 점에서의 접선으로 극한 수렴")
    
    add_card(
        s4, Inches(0.8), Inches(1.45), Inches(4.2), Inches(3.45),
        "미분의 기하학적 정의",
        [
            "• 평균변화율:  Δy / Δx = [f(a + h) - f(a)] / h",
            "• 순간변화율 / 미분계수 (접선의 기울기):",
            "   f'(a) = lim [f(a + h) - f(a)] / h  (h → 0)",
            "• 접선의 방정식:  y - f(a) = f'(a)(x - a)",
            "• 기하학적 의미: 곡선 상의 점 P에서의 순간 진행 방향",
            "💡 [실시간 역학]: 우측 [🎛️ GUI] 버튼을 눌러 접점 x₀를",
            "   움직이면, 접선이 곡선을 따라 살아 숨쉬듯 회전 추종합니다."
        ]
    )
    plot4 = os.path.join('projects', 'math_assets', 'graph_derivative.png')
    if os.path.exists(plot4):
        pic4 = s4.shapes.add_picture(plot4, Inches(5.2), Inches(1.45), Inches(4.0), Inches(2.85))
        pic4.click_action.hyperlink.address = "http://localhost:5050"
        
    add_action_button(s4, Inches(5.2), Inches(4.38), Inches(1.95), Inches(0.48), "🎛️ GUI 시뮬레이터", "수학_시뮬레이터_실행.bat", bg_color=C_CARD, border_color=C_GOLD, text_color=C_GOLD)
    add_action_button(s4, Inches(7.25), Inches(4.38), Inches(1.95), Inches(0.48), "🌐 웹 실시간 랩", "http://localhost:5050", bg_color=C_CARD, border_color=C_ACCENT, text_color=C_ACCENT)
        
    set_speaker_notes(
        s4,
        "[기하학적 직관 유도] 기울기 m이 극값에서 0이 되고, 변곡점에서 접선의 기울기가 극대가 되는 곡선 역학을 함께 보여주십시오."
    )

    # =========================================================================
    # SLIDE 5: 정적분
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_native_background(s5)
    slides.append(s5)
    add_header(s5, "Integral Calculus", "구분구적법(리만합)과 정적분의 기하학적 면적", "곡선 아래의 넓이를 무수히 많은 직사각형의 극한합으로 완성하는 정적분")
    
    add_card(
        s5, Inches(0.8), Inches(1.45), Inches(4.2), Inches(3.45),
        "구분구적법과 미적분의 기본정리",
        [
            "• 리만합 (직사각형 근사):  Sₙ = ∑ f(xₖ*) Δx",
            "• 정적분의 정의:  ∫[a to b] f(x) dx = lim [∑ f(xₖ*) Δx]",
            "• 미적분의 기본정리:  ∫[a to b] f(x) dx = F(b) - F(a)",
            "• 분할 수 n 증가 (n=4 → 16 → 50):",
            "   직사각형 오차 틈새가 사라지며 완벽한 곡면 넓이로 수렴",
            "💡 [실시간 수렴]: 우측 [🎛️ GUI] 버튼에서 분할 수 n을 늘려가며",
            "   오차(Error)가 0으로 사라지는 극한을 시각적으로 확인합니다."
        ]
    )
    plot5 = os.path.join('projects', 'math_assets', 'graph_integral.png')
    if os.path.exists(plot5):
        pic5 = s5.shapes.add_picture(plot5, Inches(5.2), Inches(1.45), Inches(4.0), Inches(2.85))
        pic5.click_action.hyperlink.address = "http://localhost:5050"
        
    add_action_button(s5, Inches(5.2), Inches(4.38), Inches(1.95), Inches(0.48), "🎛️ GUI 시뮬레이터", "수학_시뮬레이터_실행.bat", bg_color=C_CARD, border_color=C_GOLD, text_color=C_GOLD)
    add_action_button(s5, Inches(7.25), Inches(4.38), Inches(1.95), Inches(0.48), "🌐 웹 실시간 랩", "http://localhost:5050", bg_color=C_CARD, border_color=C_ACCENT, text_color=C_ACCENT)
        
    set_speaker_notes(
        s5,
        "[적분의 시각화] 직사각형들을 쪼갤수록 오차 면적이 눈에 띄게 줄어드는 과정을 보여줍니다. "
        "우측 시뮬레이터 버튼을 눌러 슬라이더 n을 늘려가며 학생들이 극한의 실체적 의미를 바로 납득하게 합니다."
    )

    # =========================================================================
    # SLIDE 6: Simulator Manual & Big Buttons
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_native_background(s6)
    slides.append(s6)
    add_header(s6, "Interactive Classroom Tool", "마우스 & 키보드 조절 수학 시뮬레이터 실행 안내", "교실 프로젝터 및 학생 태블릿에서 실시간으로 수식과 그래프를 탐구하는 GUI 도구")
    
    add_card(
        s6, Inches(0.8), Inches(1.45), Inches(4.1), Inches(2.8),
        "🎮 마우스 & 키보드 조절 가이드",
        [
            "• 모드 즉시 전환 키:",
            "   [1] 이차함수   [2] 삼각함수",
            "   [3] 미분 접선   [4] 정적분 리만합",
            "• 마우스 조작:  하단 슬라이더 or [-] [+] 클릭",
            "• 키보드 조작:",
            "   - [↑ / ↓] : 조절할 파라미터 선택",
            "   - [← / →] : 0.05 단위 정밀 수치 조절",
            "   - [R]     : 기본 수치 초기화 (Reset)"
        ],
        border_color=C_GOLD
    )
    add_action_button(
        s6, Inches(0.8), Inches(4.35), Inches(4.1), Inches(0.52),
        "🎛️ 데스크톱 GUI 시뮬레이터 즉시 실행 (클릭)",
        "수학_시뮬레이터_실행.bat",
        bg_color=RGBColor(35, 25, 15), border_color=C_GOLD, text_color=C_GOLD
    )
    
    add_card(
        s6, Inches(5.1), Inches(1.45), Inches(4.1), Inches(2.8),
        "💡 수업 현장 활용 시나리오",
        [
            "1. 교사의 발문 & 학생 예측 유도",
            "   'a 계수가 음수가 되면 그래프는 어떻게 변할까?'",
            "2. 마우스 드래그 & 즉각 검증",
            "   슬라이더를 움직여 학생들이 화면 변화를 즉각 목격",
            "3. 수학적 성질 실시간 디스플레이",
            "   우측 패널에 꼭짓점, 판별식, 접선 방정식이 실시간 갱신",
            "4. 자기주도 탐구 과제 연계"
        ],
        border_color=C_ACCENT
    )
    add_action_button(
        s6, Inches(5.1), Inches(4.35), Inches(4.1), Inches(0.52),
        "🌐 웹 브라우저 실시간 랩 바로 열기 (클릭)",
        "http://localhost:5050",
        bg_color=RGBColor(15, 35, 55), border_color=C_ACCENT, text_color=C_ACCENT
    )
    
    set_speaker_notes(
        s6,
        "[마무리 및 실습] 오늘 프레젠테이션과 연동되는 '수학_시뮬레이터_실행.bat'은 설치 없이 바로 실행됩니다. "
        "키보드 방향키만으로 슬라이더를 부드럽게 조절하면서 학생들과 상호작용하는 역동적인 수학 수업을 만드시기 바랍니다."
    )

    # =========================================================================
    # Navigation Buttons (Prev, Guide Text, Next) on all slides
    # =========================================================================
    for idx, s in enumerate(slides):
        # Prev Button
        if idx > 0:
            btn_prev = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(5.08), Inches(1.3), Inches(0.38))
            btn_prev.fill.solid()
            btn_prev.fill.fore_color.rgb = C_CARD
            btn_prev.line.color.rgb = C_BORDER
            btn_prev.click_action.target_slide = slides[idx - 1]
            tf = btn_prev.text_frame
            tf.word_wrap = False
            p = tf.paragraphs[0]
            p.text = "◀ 이전 (Left)"
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = C_MUTED
            p.alignment = PP_ALIGN.CENTER
            
        # Middle Help Guide Banner
        tb_guide = s.shapes.add_textbox(Inches(2.2), Inches(5.08), Inches(5.9), Inches(0.38))
        tf_g = tb_guide.text_frame
        tf_g.word_wrap = False
        tf_g.margin_left = tf_g.margin_top = tf_g.margin_right = tf_g.margin_bottom = 0
        p_g = tf_g.paragraphs[0]
        p_g.text = "💡 슬라이드 쇼(F5) 중 [🎛️ GUI] 또는 [🌐 웹 랩] 버튼을 클릭하면 실시간 시뮬레이터가 열립니다"
        p_g.font.size = Pt(8.5)
        p_g.font.color.rgb = RGBColor(100, 116, 139)
        p_g.alignment = PP_ALIGN.CENTER
            
        # Next Button
        if idx < len(slides) - 1:
            btn_next = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.3), Inches(5.08), Inches(1.3), Inches(0.38))
            btn_next.fill.solid()
            btn_next.fill.fore_color.rgb = C_NAV_BG
            btn_next.line.color.rgb = C_ACCENT
            btn_next.click_action.target_slide = slides[idx + 1]
            tf = btn_next.text_frame
            tf.word_wrap = False
            p = tf.paragraphs[0]
            p.text = "다음 ▶ (Right)"
            p.font.size = Pt(9.5)
            p.font.bold = True
            p.font.color.rgb = C_ACCENT
            p.alignment = PP_ALIGN.CENTER

    # Apply Paperlogy Font Family across the entire deck
    print("Applying Paperlogy 5~8 typography hierarchy...")
    apply_paperlogy_to_deck(prs)

    out_file = '수학.pptx'
    prs.save(out_file)
    print(f"Presentation saved: {out_file}")
    return out_file

if __name__ == '__main__':
    build_math_deck()
