import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

from build_presentation_helpers import (
    COLOR_GOOGLE_BLUE, COLOR_GOOGLE_RED, COLOR_GOOGLE_YELLOW, COLOR_GOOGLE_GREEN,
    COLOR_PRIMARY_BLUE, COLOR_BG_LIGHT, COLOR_BG_CARD, COLOR_BORDER,
    COLOR_TEXT_MAIN, COLOR_TEXT_MUTED, COLOR_DARK_CARD, COLOR_PILL_BG,
    FONT_TITLE, FONT_HEADING, FONT_SUBTITLE, FONT_BODY,
    set_shape_flat_color, add_header, add_card, add_indicator_bar,
    set_speaker_notes, configure_video_autoplay_loop, apply_paperlogy_to_deck
)

SUBTLE_BG_IMAGE = 'projects/ai_edu_roundtrip/images/bg_3d_subtle_80.png'

SLIDE_BACKGROUNDS = {
    2: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_stars.png',
    3: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_birds.png',
    4: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_b612.png',
    5: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_birds.png',
    6: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_b612.png',
    7: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_b612.png',
    8: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_b612.png',
    9: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_stars.png',
    10: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_well.png',
    11: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_stars.png',
    12: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_fox.png',
    13: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_stars.png',
    14: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_fox.png',
    15: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_well.png',
    16: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_fox.png',
    17: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_stars.png',
    18: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_b612.png',
    19: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_fox.png',
    20: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_birds.png',
    21: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_well.png',
    22: 'projects/ai_edu_roundtrip/images/bg_lp_subtle_stars.png',
}

def add_slide_with_subtle_bg(prs, blank_layout, slide_num=2):
    slide = prs.slides.add_slide(blank_layout)
    bg_img = SLIDE_BACKGROUNDS.get(slide_num, 'projects/ai_edu_roundtrip/images/bg_lp_subtle_stars.png')
    slide.shapes.add_picture(bg_img, 0, 0, Inches(10), Inches(5.625))
    return slide

def build_education_deck():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(5.625)
    blank_layout = prs.slide_layouts[6]

    # =========================================================================
    # SLIDE 1: COVER (3D MOVING BACKGROUND VIDEO - AUTOPLAY & LOOP)
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    
    # 1. Background Video (Full Screen)
    video_path = 'projects/ai_edu_roundtrip/images/bg_little_prince_loop.mp4'
    poster_path = 'projects/ai_edu_roundtrip/images/bg_little_prince_poster.png'
    movie_shape = s1.shapes.add_movie(
        video_path,
        0, 0, Inches(10), Inches(5.625),
        poster_frame_image=poster_path,
        mime_type='video/mp4'
    )
    configure_video_autoplay_loop(s1, movie_shape)

    # 2. Glassmorphism Container Card on top of video
    card_bg = add_card(s1, Inches(0.6), Inches(0.45), Inches(5.6), Inches(4.7), bg_rgb=COLOR_DARK_CARD, border_rgb=COLOR_PRIMARY_BLUE, border_width_pt=1.5)
    
    # Pill Tag
    tag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.85), Inches(0.68), Inches(2.6), Inches(0.32))
    set_shape_flat_color(tag, RGBColor(30, 41, 59), border_rgb=COLOR_GOOGLE_BLUE, border_width_pt=1.0)
    tf_tag = tag.text_frame
    tf_tag.word_wrap = False
    tf_tag.margin_left = tf_tag.margin_right = tf_tag.margin_top = tf_tag.margin_bottom = 0
    p = tf_tag.paragraphs[0]
    p.text = "✦ LE PETIT PRINCE & AI EDUCATION ✦"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(0, 229, 255) # Electric cyan
    p.alignment = PP_ALIGN.CENTER

    # Main Title Box
    t_box = s1.shapes.add_textbox(Inches(0.85), Inches(1.15), Inches(5.1), Inches(1.2))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p1 = tf_t.paragraphs[0]
    p1.text = "AI 시대, 교육의 문법이 바뀌다"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = RGBColor(255, 255, 255)
    
    p1_sub = tf_t.add_paragraph()
    p1_sub.text = "\"가장 중요한 것은 눈에 보이지 않아\" — 어린왕자와 교사가 함께 그리는 미래 교실"
    p1_sub.font.name = FONT_BODY
    p1_sub.font.size = Pt(12)
    p1_sub.font.color.rgb = RGBColor(148, 163, 184)
    p1_sub.space_before = Pt(8)

    # Card 1: KEY FOCUS
    c1 = add_card(s1, Inches(0.85), Inches(2.55), Inches(5.1), Inches(1.05), bg_rgb=RGBColor(30, 41, 59), border_rgb=RGBColor(51, 65, 85))
    add_indicator_bar(s1, Inches(0.85), Inches(2.55), Inches(0.08), Inches(1.05), COLOR_GOOGLE_BLUE)
    tf_c1 = s1.shapes.add_textbox(Inches(1.05), Inches(2.65), Inches(4.7), Inches(0.85)).text_frame
    tf_c1.word_wrap = True
    tf_c1.margin_left = tf_c1.margin_right = tf_c1.margin_top = tf_c1.margin_bottom = 0
    p_c1_h = tf_c1.paragraphs[0]
    p_c1_h.text = "KEY FOCUS"
    p_c1_h.font.name = FONT_HEADING
    p_c1_h.font.size = Pt(10)
    p_c1_h.font.bold = True
    p_c1_h.font.color.rgb = COLOR_GOOGLE_BLUE
    p_c1_b = tf_c1.add_paragraph()
    p_c1_b.text = "\"네 장미가 소중한 것은 네가 바친 시간 때문이야\" — 행정을 줄이고 아이들과 만나는 시간"
    p_c1_b.font.name = FONT_BODY
    p_c1_b.font.size = Pt(13.5)
    p_c1_b.font.bold = True
    p_c1_b.font.color.rgb = RGBColor(241, 245, 249)
    p_c1_b.space_before = Pt(4)

    # Card 2: OUR MISSION
    c2 = add_card(s1, Inches(0.85), Inches(3.75), Inches(5.1), Inches(1.15), bg_rgb=RGBColor(30, 41, 59), border_rgb=RGBColor(51, 65, 85))
    add_indicator_bar(s1, Inches(0.85), Inches(3.75), Inches(0.08), Inches(1.15), COLOR_GOOGLE_GREEN)
    tf_c2 = s1.shapes.add_textbox(Inches(1.05), Inches(3.85), Inches(4.7), Inches(0.95)).text_frame
    tf_c2.word_wrap = True
    tf_c2.margin_left = tf_c2.margin_right = tf_c2.margin_top = tf_c2.margin_bottom = 0
    p_c2_h = tf_c2.paragraphs[0]
    p_c2_h.text = "OUR MISSION"
    p_c2_h.font.name = FONT_HEADING
    p_c2_h.font.size = Pt(10)
    p_c2_h.font.bold = True
    p_c2_h.font.color.rgb = COLOR_GOOGLE_GREEN
    p_c2_b = tf_c2.add_paragraph()
    p_c2_b.text = "\"오늘 우리는 단순한 기술 도구가 아닌, 우리 아이들의 미래를 이야기하려 모였습니다.\""
    p_c2_b.font.name = FONT_BODY
    p_c2_b.font.size = Pt(12)
    p_c2_b.font.color.rgb = RGBColor(226, 232, 240)
    p_c2_b.space_before = Pt(4)

    # Right floating glass tags over 3D wave
    tags = ["✦ 3D Neural Space", "✦ Multimodal AI", "✦ High-Touch Teaching"]
    for i, tag_text in enumerate(tags):
        rtag = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.5 + (i * 0.2)), Inches(1.0 + (i * 1.3)), Inches(2.6), Inches(0.7))
        set_shape_flat_color(rtag, RGBColor(15, 23, 42), border_rgb=RGBColor(56, 189, 248), border_width_pt=1.0)
        tf_rt = rtag.text_frame
        tf_rt.margin_left = tf_rt.margin_right = tf_rt.margin_top = tf_rt.margin_bottom = 0
        prt = tf_rt.paragraphs[0]
        prt.text = tag_text
        prt.font.name = FONT_HEADING
        prt.font.size = Pt(12)
        prt.font.bold = True
        prt.font.color.rgb = RGBColor(240, 249, 255)
        prt.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s1, """[발표자 대본]
선생님 여러분, 안녕하십니까? 
오늘 'AI 시대, 교육의 문법이 바뀌다'라는 주제로 여러분과 귀한 시간을 함께하게 된 강사입니다.
지금 보고 계시는 첫 슬라이드의 움직이는 3차원 신경망처럼, 우리 교육 현장에도 눈에 보이지 않던 거대한 기술의 파도가 밀려오고 있습니다.
하지만 오늘 이 자리는 복잡한 컴퓨터 공학 기술을 배우기 위한 자리가 아닙니다.
기술을 우리의 든든한 조력자로 삼아, 어떻게 하면 과중한 업무에서 벗어나 우리 아이들의 눈빛을 한 번 더 마주하고 참된 교육의 본질을 회복할 수 있을 것인가에 대한 이야기를 나누고자 합니다.
오늘 강연을 통해 교실의 문법을 바꾸는 기분 좋은 여정을 함께 시작해 보겠습니다.""")

    # =========================================================================
    # SLIDE 2: 생각의 전환 (MOTIVATION)
    # =========================================================================
    s2 = add_slide_with_subtle_bg(prs, blank_layout, 2)
    add_header(s2, "MOTIVATION & MINDSET", "생각의 전환: 기술을 대하는 교사의 태도", "두려움과 거부감을 넘어, 교육의 본질을 회복하는 도구로서의 AI")

    q_card = add_card(s2, Inches(0.7), Inches(1.85), Inches(4.3), Inches(3.2), bg_rgb=COLOR_DARK_CARD, border_rgb=COLOR_PRIMARY_BLUE, border_width_pt=1.5)
    add_indicator_bar(s2, Inches(0.7), Inches(1.85), Inches(0.08), Inches(3.2), COLOR_GOOGLE_YELLOW)
    tf_q = s2.shapes.add_textbox(Inches(0.95), Inches(2.1), Inches(3.8), Inches(2.7)).text_frame
    tf_q.word_wrap = True
    tf_q.margin_left = tf_q.margin_right = tf_q.margin_top = tf_q.margin_bottom = 0
    
    pq_tag = tf_q.paragraphs[0]
    pq_tag.text = "KEY MESSAGE"
    pq_tag.font.name = FONT_HEADING
    pq_tag.font.size = Pt(11)
    pq_tag.font.bold = True
    pq_tag.font.color.rgb = COLOR_GOOGLE_YELLOW
    
    pq_main = tf_q.add_paragraph()
    pq_main.text = "\"AI는 교사를 대체하지 않습니다.\n\n단, AI를 능숙하게 활용하는 교사가 그렇지 않은 교사를 대체할 것입니다.\""
    pq_main.font.name = FONT_HEADING
    pq_main.font.size = Pt(17)
    pq_main.font.bold = True
    pq_main.font.color.rgb = RGBColor(255, 255, 255)
    pq_main.space_before = Pt(14)

    rc1 = add_card(s2, Inches(5.2), Inches(1.85), Inches(4.1), Inches(1.5), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_BORDER)
    add_indicator_bar(s2, Inches(5.2), Inches(1.85), Inches(0.06), Inches(1.5), COLOR_GOOGLE_BLUE)
    tf_rc1 = s2.shapes.add_textbox(Inches(5.4), Inches(1.95), Inches(3.7), Inches(1.3)).text_frame
    tf_rc1.word_wrap = True
    tf_rc1.margin_left = tf_rc1.margin_right = tf_rc1.margin_top = tf_rc1.margin_bottom = 0
    p_rc1_h = tf_rc1.paragraphs[0]
    p_rc1_h.text = "PERSPECTIVE | 관점의 전환"
    p_rc1_h.font.name = FONT_HEADING
    p_rc1_h.font.size = Pt(11)
    p_rc1_h.font.bold = True
    p_rc1_h.font.color.rgb = COLOR_GOOGLE_BLUE
    p_rc1_b = tf_rc1.add_paragraph()
    p_rc1_b.text = "변화를 막연한 두려움이 아닌 기회로 보는 시각: 교실 속 단순 반복 행정을 덜어내고 진정한 교육의 본질로 돌아갈 절호의 기회입니다."
    p_rc1_b.font.name = FONT_BODY
    p_rc1_b.font.size = Pt(11)
    p_rc1_b.font.color.rgb = COLOR_TEXT_MAIN
    p_rc1_b.space_before = Pt(6)

    rc2 = add_card(s2, Inches(5.2), Inches(3.55), Inches(4.1), Inches(1.5), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_BORDER)
    add_indicator_bar(s2, Inches(5.2), Inches(3.55), Inches(0.06), Inches(1.5), COLOR_GOOGLE_GREEN)
    tf_rc2 = s2.shapes.add_textbox(Inches(5.4), Inches(3.65), Inches(3.7), Inches(1.3)).text_frame
    tf_rc2.word_wrap = True
    tf_rc2.margin_left = tf_rc2.margin_right = tf_rc2.margin_top = tf_rc2.margin_bottom = 0
    p_rc2_h = tf_rc2.paragraphs[0]
    p_rc2_h.text = "ROLE SHIFT | 교사 역할의 재정의"
    p_rc2_h.font.name = FONT_HEADING
    p_rc2_h.font.size = Pt(11)
    p_rc2_h.font.bold = True
    p_rc2_h.font.color.rgb = COLOR_GOOGLE_GREEN
    p_rc2_b = tf_rc2.add_paragraph()
    p_rc2_b.text = "일방적인 지식 전달자(Lecturer)에서 학생의 잠재력을 이끌어내는 학습 촉진자(Facilitator)이자 정서적 멘토로 도약합니다."
    p_rc2_b.font.name = FONT_BODY
    p_rc2_b.font.size = Pt(11)
    p_rc2_b.font.color.rgb = COLOR_TEXT_MAIN
    p_rc2_b.space_before = Pt(6)

    set_speaker_notes(s2, """[발표자 대본]
연수를 시작하며 가장 먼저 드리고 싶은 말씀은 '생각의 전환'입니다.
많은 분들이 'AI가 발전하면 교사라는 직업이 사라지는 것 아니냐'는 두려움을 말씀하십니다.
하지만 교육학자와 미래학자들의 공통된 결론은 분명합니다. AI는 결코 살아 숨 쉬는 인간 교사를 대체할 수 없습니다. 
다만, AI라는 강력한 날개를 달고 자신의 수업과 행정을 혁신하는 교사가 그렇지 않은 교사보다 훨씬 앞서 나갈 것은 분명합니다.
우리가 기술을 바라보는 관점을 '경쟁'이 아닌 '협력'으로 바꾸는 순간, 교직 생활의 피로감은 놀라운 보람으로 바뀌기 시작합니다.""")

    # =========================================================================
    # SLIDE 3: 2024 AI의 현주소 (MULTIMODAL)
    # =========================================================================
    s3 = add_slide_with_subtle_bg(prs, blank_layout, 3)
    add_header(s3, "TECHNOLOGY TREND", "AI 대전환: 멀티모달(Multimodal)의 시대", "텍스트 입력을 넘어 보고, 듣고, 말하며 실시간으로 추론하는 지능의 진화")

    cards_data = [
        ("시각 (Vision)", "교과서 도표, 손글씨 풀이, 학생 필기를 사진으로 찍어 올리면 즉각 오류를 진단하고 맞춤 해설 생성", COLOR_GOOGLE_BLUE),
        ("청각 (Audio)", "방대한 교육청 연구 보고서나 논문을 팟캐스트 형태의 대화형 음성으로 요약하여 출퇴근길 청취", COLOR_GOOGLE_RED),
        ("음성 (Voice)", "ChatGPT 보이스 및 Gemini Live를 통해 기계적이지 않은 자연스러운 실시간 음성 질의응답 및 외국어 회화", COLOR_GOOGLE_YELLOW),
        ("추론 (Reasoning)", "수백 페이지의 2022 개정 교육과정 총론을 단번에 파악하고, 복합 문제의 단계적 해결 전략 도출", COLOR_GOOGLE_GREEN),
    ]

    for idx, (head, body, color) in enumerate(cards_data):
        row = idx // 2
        col = idx % 2
        l = Inches(0.7 + col * 4.4)
        t = Inches(1.85 + row * 1.55)
        w = Inches(4.2)
        h = Inches(1.4)

        card = add_card(s3, l, t, w, h)
        add_indicator_bar(s3, l, t, Inches(0.06), h, color)
        tf = s3.shapes.add_textbox(l + Inches(0.18), t + Inches(0.12), w - Inches(0.3), h - Inches(0.24)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        ph = tf.paragraphs[0]
        ph.text = head
        ph.font.name = FONT_HEADING
        ph.font.size = Pt(12.5)
        ph.font.bold = True
        ph.font.color.rgb = color
        
        pb = tf.add_paragraph()
        pb.text = body
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10)
        pb.font.color.rgb = COLOR_TEXT_MAIN
        pb.space_before = Pt(4)

    bot_card = add_card(s3, Inches(0.7), Inches(5.0), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b = bot_card.text_frame
    tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
    pb_text = tf_b.paragraphs[0]
    pb_text.text = "✦ 이제 AI는 단순 텍스트 챗봇이 아니라, 교사의 오감을 보조하는 살아있는 협업 파트너입니다."
    pb_text.font.name = FONT_HEADING
    pb_text.font.size = Pt(10.5)
    pb_text.font.bold = True
    pb_text.font.color.rgb = COLOR_PRIMARY_BLUE
    pb_text.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s3, """[발표자 대본]
불과 1~2년 전만 해도 우리는 AI에게 키보드로 글자를 쳐서 물어보고 글자로 답변을 받았습니다.
하지만 지금의 AI는 완전히 다른 차원으로 도약했습니다. 바로 '멀티모달'입니다.
인간이 눈으로 보고, 귀로 듣고, 입으로 말하며 생각하듯, AI 역시 복잡한 수학 도표를 사진으로 찍으면 바로 인식하고, 음성으로 대화하며, 수백 페이지의 공문서를 단 몇 초 만에 심층 분석합니다.
특히 교실 현장에서는 아이들의 손글씨 풀이 노트를 카메라로 비추기만 해도 취약점을 진단해 주는 엄청난 교육적 활용이 가능해졌습니다.""")

    # =========================================================================
    # SLIDE 4: 학교 현장의 3대 고민
    # =========================================================================
    s4 = add_slide_with_subtle_bg(prs, blank_layout, 4)
    add_header(s4, "CURRENT CHALLENGES", "학교 현장의 3대 고민: 우리가 매일 마주하는 현실", "교육의 이상과 교실의 현실 사이에서 교사들을 지치게 만드는 3대 장벽")

    cols_data = [
        ("01. 맞춤형 교육의 한계", "다양한 학습 속도와 격차", [
            "한 교실 25~30명의 극단적인 수준 차이",
            "기초학력 지원 대상과 심화 학습자 동시 만족 불가",
            "1:1 개별 피드백 제공을 위한 물리적 시간 부족"
        ], COLOR_GOOGLE_RED),
        ("02. 과중한 행정 업무 부담", "수업을 잠식하는 서류 작업", [
            "연간 수백 건의 공문, 가정통신문, 주간안내",
            "방과후/체험학습 기안 및 정산 서류 압박",
            "정작 소중한 수업 연구와 학생 상담 시간 잠식"
        ], COLOR_GOOGLE_YELLOW),
        ("03. 디지털 격차 & 윤리 이슈", "새로운 혼란과 위험성", [
            "학생 간 기기 활용 능력 및 접근성 편차 심화",
            "생성형 AI 표절, 딥페이크, 저작권, 개인정보 우려",
            "학교 단위의 체계적인 가이드라인 부재"
        ], COLOR_GOOGLE_BLUE),
    ]

    for idx, (title, subtitle, bullets, color) in enumerate(cols_data):
        l = Inches(0.7 + idx * 2.95)
        t = Inches(1.85)
        w = Inches(2.75)
        h = Inches(3.05)

        card = add_card(s4, l, t, w, h)
        add_indicator_bar(s4, l, t, w, Inches(0.08), color)
        
        tf = s4.shapes.add_textbox(l + Inches(0.15), t + Inches(0.18), w - Inches(0.3), h - Inches(0.3)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = color
        
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(9.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(3)
        p_sub.space_after = Pt(8)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = "• " + b
            pb.font.name = FONT_BODY
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = COLOR_TEXT_MAIN
            pb.space_before = Pt(4)

    bot4 = add_card(s4, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b4 = bot4.text_frame
    tf_b4.margin_left = tf_b4.margin_right = tf_b4.margin_top = tf_b4.margin_bottom = 0
    pb4 = tf_b4.paragraphs[0]
    pb4.text = "✦ 선생님의 에너지가 행정에 소진되지 않고 아이들의 마음에 닿으려면 도구의 혁신이 필요합니다."
    pb4.font.name = FONT_HEADING
    pb4.font.size = Pt(10.5)
    pb4.font.bold = True
    pb4.font.color.rgb = COLOR_PRIMARY_BLUE
    pb4.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s4, """[발표자 대본]
선생님들께서 학교에서 매일 마주하시는 현실은 참으로 무겁습니다.
첫째, 한 반에 25명에서 30명의 아이들이 앉아 있는데, 영어를 원어민처럼 구사하는 아이부터 알파벳을 겨우 읽는 아이까지 스펙트럼이 너무나 넓습니다. 교사 한 사람이 이 모든 아이를 개별화 지도하는 것은 물리적으로 불가능에 가깝습니다.
둘째, 아침에 출근하자마자 쌓여있는 미결 공문, 품의서, 가정통신문... 수업 준비를 하기도 전에 파김치가 됩니다.
셋째, AI가 좋다는 건 알지만 혹시 아이들이 과제를 표절하지는 않을까, 윤리적 사고는 어떻게 가르쳐야 할까 고민이 깊어집니다.
오늘 이 세 가지 난제를 구글 AI 도구로 어떻게 해결할 수 있는지 구체적으로 살펴보겠습니다.""")

    # =========================================================================
    # SLIDE 5: 왜 Google인가? (ECO-SYSTEM)
    # =========================================================================
    s5 = add_slide_with_subtle_bg(prs, blank_layout, 5)
    add_header(s5, "GOOGLE WORKSPACE FOR EDUCATION", "왜 Google인가? 끊김 없는 올인원(All-in-One) 생태계", "별도의 도구 전환 없이, 내가 일하던 업무 공간 그대로 AI가 유기적으로 스며듭니다")

    g_cards = [
        ("Google Docs & Sheets", "문서 및 데이터 일체화", [
            "문서 작성 중 사이드 패널에서 Gemini 즉시 호출",
            "가정통신문 초안을 '구글 문서로 내보내기' 원클릭 연동",
            "학생 설문 결과 및 학업 통계를 스프레드시트로 즉각 분석"
        ], COLOR_GOOGLE_BLUE),
        ("Google Drive", "학교 자료의 중앙 지식고", [
            "지난 수년간 축적된 교사용 학습 자료와 공문서 보관",
            "파일을 일일이 업로드할 필요 없이 드라이브에서 직접 AI 연동",
            "교육청 계정 기반의 강력한 보안 및 용량 지원"
        ], COLOR_GOOGLE_YELLOW),
        ("Google Classroom", "과제 및 개별 피드백 자동화", [
            "수업별 수준에 맞춘 형성평가 및 루브릭 자동 생성",
            "학생 과제에 대한 1:1 맞춤형 피드백 초안 작성 지원",
            "학생 개인정보 유출 걱정 없는 안전한 공교육 환경"
        ], COLOR_GOOGLE_GREEN),
    ]

    for idx, (title, subtitle, bullets, color) in enumerate(g_cards):
        l = Inches(0.7 + idx * 2.95)
        t = Inches(1.85)
        w = Inches(2.75)
        h = Inches(3.05)

        card = add_card(s5, l, t, w, h)
        add_indicator_bar(s5, l, t, w, Inches(0.08), color)
        
        tf = s5.shapes.add_textbox(l + Inches(0.15), t + Inches(0.18), w - Inches(0.3), h - Inches(0.3)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = color
        
        p_sub = tf.add_paragraph()
        p_sub.text = subtitle
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(9.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(3)
        p_sub.space_after = Pt(8)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = "• " + b
            pb.font.name = FONT_BODY
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = COLOR_TEXT_MAIN
            pb.space_before = Pt(4)

    bot5 = add_card(s5, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b5 = bot5.text_frame
    tf_b5.margin_left = tf_b5.margin_right = tf_b5.margin_top = tf_b5.margin_bottom = 0
    pb5 = tf_b5.paragraphs[0]
    pb5.text = "✦ 도구의 분절이 없는 하나의 생태계(All-in-One)가 교사의 업무 피로도를 획기적으로 낮춥니다."
    pb5.font.name = FONT_HEADING
    pb5.font.size = Pt(10.5)
    pb5.font.bold = True
    pb5.font.color.rgb = COLOR_PRIMARY_BLUE
    pb5.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s5, """[발표자 대본]
시중에 정말 수많은 AI 서비스가 나와 있습니다. 그런데 왜 우리는 '구글 생태계'에 주목해야 할까요?
선생님들께서 새로운 AI 사이트에 가입하고, 복사해서 다른 프로그램에 붙여넣고, 서식이 깨져서 다시 수정하는 과정 자체가 또 다른 업무 스트레스가 되기 때문입니다.
구글 워크스페이스는 우리가 이미 친숙하게 사용하고 있는 구글 문서, 드라이브, 클래스룸 안에 제미나이(Gemini)가 물 흐르듯 결합되어 있습니다.
문서를 쓰다가 오른쪽 패널에서 제미나이를 불러 초안을 잡고, 버튼 하나로 바로 문서에 삽입하는 이 자연스러운 연속성이야말로 구글 생태계의 가장 큰 무기입니다.""")

    # =========================================================================
    # SLIDE 6: Google App for Desktop
    # =========================================================================
    s6 = add_slide_with_subtle_bg(prs, blank_layout, 6)
    add_header(s6, "INFRASTRUCTURE & SETUP", "Google App for Desktop: 내 컴퓨터와 AI의 연결", "내 PC 폴더 속 잠자던 문서들이 AI의 살아있는 지식이 되는 가장 쉬운 출발점")

    steps_data = [
        ("STEP 01", "데스크톱 드라이브 설치", "컴퓨터 탐색기 안에 가상 하드 드라이브(G 드라이브) 자동 마운트\nUSB나 외장하드처럼 편리하게 내 PC 파일 관리", COLOR_GOOGLE_BLUE),
        ("STEP 02", "수업 및 업무 폴더 자동 동기화", "평소처럼 내 컴퓨터 폴더에 파일을 저장하면 실시간 클라우드 자동 백업\nHWP, PDF, PPT, Excel 등 모든 형식 완벽 지원", COLOR_GOOGLE_RED),
        ("STEP 03", "AI 지식화 즉시 완료", "Gemini 및 NotebookLM에서 내 컴퓨터의 최신 문서를 즉각 검색 및 인용\n\"내 드라이브의 2학기 안전 계획 찾아줘\" 한마디로 해결", COLOR_GOOGLE_GREEN),
    ]

    for idx, (step_tag, title, desc, color) in enumerate(steps_data):
        l = Inches(0.7 + idx * 2.95)
        t = Inches(1.85)
        w = Inches(2.75)
        h = Inches(3.0)

        card = add_card(s6, l, t, w, h)
        add_indicator_bar(s6, l, t, Inches(0.06), h, color)
        
        tf = s6.shapes.add_textbox(l + Inches(0.18), t + Inches(0.18), w - Inches(0.3), h - Inches(0.3)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p_tag = tf.paragraphs[0]
        p_tag.text = step_tag
        p_tag.font.name = FONT_HEADING
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = color
        
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_MAIN
        p_t.space_before = Pt(6)
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_TEXT_MUTED
        p_d.space_before = Pt(8)

    bot6 = add_card(s6, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b6 = bot6.text_frame
    tf_b6.margin_left = tf_b6.margin_right = tf_b6.margin_top = tf_b6.margin_bottom = 0
    pb6 = tf_b6.paragraphs[0]
    pb6.text = "✦ 파일 업로드의 번거로움 없이, 내 컴퓨터 폴더 전체가 AI의 브레인으로 변신합니다."
    pb6.font.name = FONT_HEADING
    pb6.font.size = Pt(10.5)
    pb6.font.bold = True
    pb6.font.color.rgb = COLOR_PRIMARY_BLUE
    pb6.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s6, """[발표자 대본]
선생님들께서 AI를 쓰실 때 가장 귀찮아하시는 부분이 무엇일까요? 바로 '파일 업로드'입니다.
웹 브라우저를 열고, 로그인하고, 파일 찾기를 눌러 내 컴퓨터 구석에 있는 문서를 찾는 번거로운 과정이죠.
'데스크톱용 구글 드라이브'를 설치하시면 이 문제가 단번에 해결됩니다.
내 컴퓨터 바탕화면이나 탐색기 안에 마치 일반 폴더처럼 구글 드라이브가 연결되어, 평소처럼 문서를 저장하기만 하면 그 즉시 구글 클라우드와 동기화됩니다.
그리고 제미나이나 노트북LM에서 내 컴퓨터에 있는 파일명을 말하기만 하면 바로 내용을 찾아 대화할 수 있게 됩니다.""")

    # =========================================================================
    # SLIDE 7: Gemini - 내 책상 위의 행정 비서
    # =========================================================================
    s7 = add_slide_with_subtle_bg(prs, blank_layout, 7)
    add_header(s7, "PRACTICAL WORKFLOW", "Gemini: 내 책상 위의 지능형 행정 비서", "\"올해 체험학습 안내문 초안 써줘\" → 단 10초 만에 완벽한 공문 기안 완성")

    lp = add_card(s7, Inches(0.7), Inches(1.85), Inches(4.3), Inches(3.1), bg_rgb=COLOR_DARK_CARD, border_rgb=COLOR_PRIMARY_BLUE)
    add_indicator_bar(s7, Inches(0.7), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_YELLOW)
    tf_lp = s7.shapes.add_textbox(Inches(0.92), Inches(2.0), Inches(3.9), Inches(2.8)).text_frame
    tf_lp.word_wrap = True
    tf_lp.margin_left = tf_lp.margin_right = tf_lp.margin_top = tf_lp.margin_bottom = 0
    
    plp_h = tf_lp.paragraphs[0]
    plp_h.text = "✦ 실전 프롬프트 입력창 (Prompt)"
    plp_h.font.name = FONT_HEADING
    plp_h.font.size = Pt(11)
    plp_h.font.bold = True
    plp_h.font.color.rgb = COLOR_GOOGLE_YELLOW
    
    plp_b = tf_lp.add_paragraph()
    plp_b.text = "\"대상: 초등학교 4학년 학부모님\n장소: 국립과천과학관 (상설전시관 및 천문대)\n일시: 2026년 5월 15일(금) 09:00 ~ 15:30\n준비물: 도시락, 물, 필기도구, 간편한 복장\n주의사항: 버스 탑승 안전 수칙, 비상 연락망 포함\n\n학부모님께 신뢰를 주고 다정하며 품격 있는 어조로 가정통신문 초안을 표와 함께 정갈하게 작성해 줘.\""
    plp_b.font.name = FONT_BODY
    plp_b.font.size = Pt(10.5)
    plp_b.font.color.rgb = RGBColor(241, 245, 249)
    plp_b.space_before = Pt(8)

    rp = add_card(s7, Inches(5.2), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_BORDER)
    tf_rp = s7.shapes.add_textbox(Inches(5.4), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_rp.word_wrap = True
    tf_rp.margin_left = tf_rp.margin_right = tf_rp.margin_top = tf_rp.margin_bottom = 0
    
    prp_h = tf_rp.paragraphs[0]
    prp_h.text = "KEY WORKFLOW FEATURES"
    prp_h.font.name = FONT_HEADING
    prp_h.font.size = Pt(11)
    prp_h.font.bold = True
    prp_h.font.color.rgb = COLOR_PRIMARY_BLUE
    
    bullets7 = [
        ("01. 원클릭 구글 문서(Docs) 내보내기", "답변 하단의 [내보내기] 버튼 클릭 시 표와 서식이 깨지지 않고 구글 문서로 바로 생성"),
        ("02. 복사/붙여넣기 없는 업무 연속성", "형식이 흐트러지는 스트레스 제로, 바로 학교 양식에 맞춰 인쇄 및 전자결재 기안 가능"),
        ("03. 교사의 최종 검증과 교육적 터치", "AI가 초안의 90%를 완성하고, 교사는 학급 특이사항만 10% 검토하여 시간 대폭 절감")
    ]
    for b_title, b_desc in bullets7:
        p_bt = tf_rp.add_paragraph()
        p_bt.text = "• " + b_title
        p_bt.font.name = FONT_HEADING
        p_bt.font.size = Pt(11)
        p_bt.font.bold = True
        p_bt.font.color.rgb = COLOR_TEXT_MAIN
        p_bt.space_before = Pt(8)
        
        p_bd = tf_rp.add_paragraph()
        p_bd.text = "   " + b_desc
        p_bd.font.name = FONT_BODY
        p_bd.font.size = Pt(9.5)
        p_bd.font.color.rgb = COLOR_TEXT_MUTED
        p_bd.space_before = Pt(2)

    bot7 = add_card(s7, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b7 = bot7.text_frame
    tf_b7.margin_left = tf_b7.margin_right = tf_b7.margin_top = tf_b7.margin_bottom = 0
    pb7 = tf_b7.paragraphs[0]
    pb7.text = "✦ AI에게 완벽한 정답을 요구하는 대신, '훌륭한 초안'을 작성하게 하는 것이 생산성의 핵심입니다."
    pb7.font.name = FONT_HEADING
    pb7.font.size = Pt(10.5)
    pb7.font.bold = True
    pb7.font.color.rgb = COLOR_PRIMARY_BLUE
    pb7.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s7, """[발표자 대본]
실제 교무실에서 가장 많이 쓰이는 실전 사례입니다. 바로 '가정통신문 및 공문 기안'입니다.
우리가 체험학습 안내문을 하나 쓰려면 예전 양식을 찾고 날짜 고치고 안전 수칙을 검색하느라 30분~1시간이 훌쩍 지나갑니다.
하지만 슬라이드 왼쪽에 보시는 것처럼, 제미나이에게 핵심 팩트(일시, 장소, 준비물, 어조)만 툭 던져주면 단 10초 만에 완벽한 격식을 갖춘 안내문 초안이 작성됩니다.
더 놀라운 것은 답변 아래의 [문서로 내보내기] 버튼을 누르면 구글 문서로 깔끔한 표 서식 그대로 열린다는 점입니다.
선생님께서는 오탈자와 세부 사항만 확인하시고 결재를 올리시면 됩니다.""")

    # =========================================================================
    # SLIDE 8: [실전 사례] 업무 효율화
    # =========================================================================
    s8 = add_slide_with_subtle_bg(prs, blank_layout, 8)
    add_header(s8, "CASE STUDY: TIME SAVING", "[실전 사례] 주간학습안내 & 가정통신문 제작의 혁신", "기존 75분 이상 걸리던 매주 반복 업무가 10분 이내로 단축되는 기적")

    b_card = add_card(s8, Inches(0.7), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=RGBColor(241, 245, 249), border_rgb=COLOR_BORDER)
    add_indicator_bar(s8, Inches(0.7), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_RED)
    tf_bc = s8.shapes.add_textbox(Inches(0.92), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_bc.word_wrap = True
    tf_bc.margin_left = tf_bc.margin_right = tf_bc.margin_top = tf_bc.margin_bottom = 0
    pbc_h = tf_bc.paragraphs[0]
    pbc_h.text = "과거의 업무 방식 (총 75분 소요)"
    pbc_h.font.name = FONT_HEADING
    pbc_h.font.size = Pt(12)
    pbc_h.font.bold = True
    pbc_h.font.color.rgb = COLOR_GOOGLE_RED
    
    b_steps = [
        "1. 지난주/작년 파일 찾아 복사본 만들기 (10분)",
        "2. 나이스 교육과정 진도표와 시간표 대조 (30분)",
        "3. 준비물 및 행사 안내 문구 수동 재작성 (20분)",
        "4. 오탈자 및 결재 양식 서식 수동 정렬 (15분)"
    ]
    for bs in b_steps:
        pbs = tf_bc.add_paragraph()
        pbs.text = bs
        pbs.font.name = FONT_BODY
        pbs.font.size = Pt(10)
        pbs.font.color.rgb = COLOR_TEXT_MUTED
        pbs.space_before = Pt(8)

    a_card = add_card(s8, Inches(5.2), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_GOOGLE_BLUE, border_width_pt=1.5)
    add_indicator_bar(s8, Inches(5.2), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_BLUE)
    tf_ac = s8.shapes.add_textbox(Inches(5.42), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_ac.word_wrap = True
    tf_ac.margin_left = tf_ac.margin_right = tf_ac.margin_top = tf_ac.margin_bottom = 0
    pac_h = tf_ac.paragraphs[0]
    pac_h.text = "AI 협업 방식 (총 10분 소요 / 85% 감축)"
    pac_h.font.name = FONT_HEADING
    pac_h.font.size = Pt(12)
    pac_h.font.bold = True
    pac_h.font.color.rgb = COLOR_PRIMARY_BLUE
    
    a_steps = [
        "1. 주간 단원명과 주요 학급 행사 Gemini에 입력 (1분)",
        "2. 요일별/교시별 표 형태의 주간안내 초안 생성 (10초)",
        "3. 우리 반 학생 맞춤 알림 사항 2~3줄 수정 (5분)",
        "4. 구글 닥스 즉시 내보내기 및 학부모 앱 공유 (2분)"
    ]
    for as_step in a_steps:
        pas = tf_ac.add_paragraph()
        pas.text = as_step
        pas.font.name = FONT_BODY
        pas.font.size = Pt(10)
        pas.font.color.rgb = COLOR_TEXT_MAIN
        pas.space_before = Pt(8)

    bot8 = add_card(s8, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b8 = bot8.text_frame
    tf_b8.margin_left = tf_b8.margin_right = tf_b8.margin_top = tf_b8.margin_bottom = 0
    pb8 = tf_b8.paragraphs[0]
    pb8.text = "✦ 절약된 65분의 여유는 우리 반 아이들과 눈을 맞추고 깊이 있게 대화하는 시간으로 돌아옵니다."
    pb8.font.name = FONT_HEADING
    pb8.font.size = Pt(10.5)
    pb8.font.bold = True
    pb8.font.color.rgb = COLOR_PRIMARY_BLUE
    pb8.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s8, """[발표자 대본]
이 슬라이드는 실제 초등학교 담임선생님의 주간학습안내 제작 전후를 비교한 데이터입니다.
매주 금요일마다 주간학습안내를 만들기 위해 진도표를 확인하고, 시간표를 맞추고, 준비물을 적다 보면 퇴근 시간이 훌쩍 지나기 일쑤였습니다.
하지만 AI를 활용하면, 이번 주에 나갈 단원명만 넣고 표 형태로 구성해 달라고 하면 10초 만에 서식이 완성됩니다.
절약된 1시간 남짓의 시간... 이것이 단순한 시간 절약일까요?
아닙니다. 교사의 방전된 에너지를 충전하고, 방과 후에 고민이 있는 학생과 진심 어린 상담을 나눌 수 있는 소중한 교육적 시간이 확보되는 것입니다.""")

    # =========================================================================
    # SLIDE 9: NotebookLM - 지식 관리 혁명
    # =========================================================================
    s9 = add_slide_with_subtle_bg(prs, blank_layout, 9)
    add_header(s9, "GROUNDED KNOWLEDGE BASE", "NotebookLM: 지식 관리의 새로운 패러다임", "\"인터넷의 불확실한 지식이 아닌, '우리 학교'의 검증된 문서로만 답변합니다\"")

    c9_l = add_card(s9, Inches(0.7), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=RGBColor(241, 245, 249), border_rgb=COLOR_BORDER)
    add_indicator_bar(s9, Inches(0.7), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_RED)
    tf_9l = s9.shapes.add_textbox(Inches(0.92), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_9l.word_wrap = True
    tf_9l.margin_left = tf_9l.margin_right = tf_9l.margin_top = tf_9l.margin_bottom = 0
    p9l_h = tf_9l.paragraphs[0]
    p9l_h.text = "일반 생성형 AI (Open Web LLM)"
    p9l_h.font.name = FONT_HEADING
    p9l_h.font.size = Pt(12)
    p9l_h.font.bold = True
    p9l_h.font.color.rgb = COLOR_GOOGLE_RED
    
    p9l_items = [
        "전 세계 인터넷의 방대한 공개 데이터 학습",
        "우리 학교의 학칙, 교육과정, 내부 규정 모름",
        "자신 있게 거짓 정보를 생성하는 할루시네이션(환각) 위험",
        "출처 확인이 어려워 공식 업무에 즉각 활용 불안"
    ]
    for it in p9l_items:
        p = tf_9l.add_paragraph()
        p.text = "• " + it
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(8)

    c9_r = add_card(s9, Inches(5.2), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_PRIMARY_BLUE, border_width_pt=1.5)
    add_indicator_bar(s9, Inches(5.2), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_PRIMARY_BLUE)
    tf_9r = s9.shapes.add_textbox(Inches(5.42), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_9r.word_wrap = True
    tf_9r.margin_left = tf_9r.margin_right = tf_9r.margin_top = tf_9r.margin_bottom = 0
    p9r_h = tf_9r.paragraphs[0]
    p9r_h.text = "NotebookLM (Grounded AI)"
    p9r_h.font.name = FONT_HEADING
    p9r_h.font.size = Pt(12)
    p9r_h.font.bold = True
    p9r_h.font.color.rgb = COLOR_PRIMARY_BLUE
    
    p9r_items = [
        "내가 직접 업로드한 공식 문서(PDF, 웹, Docs)만 기반",
        "우리 학교 교육계획서, 학사일정 완벽 학습",
        "모든 답변에 원문 각주(Citation) 번호 100% 표기",
        "각주를 클릭하면 해당 문서의 원문 문단으로 즉시 이동 확인"
    ]
    for it in p9r_items:
        p = tf_9r.add_paragraph()
        p.text = "✦ " + it
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(8)

    bot9 = add_card(s9, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b9 = bot9.text_frame
    tf_b9.margin_left = tf_b9.margin_right = tf_b9.margin_top = tf_b9.margin_bottom = 0
    pb9 = tf_b9.paragraphs[0]
    pb9.text = "✦ 할루시네이션(환각) 0%에 도전하는 가장 신뢰할 수 있는 교사용 지식 베이스입니다."
    pb9.font.name = FONT_HEADING
    pb9.font.size = Pt(10.5)
    pb9.font.bold = True
    pb9.font.color.rgb = COLOR_PRIMARY_BLUE
    pb9.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s9, """[발표자 대본]
오늘 제가 가장 힘주어 소개해 드리고 싶은 도구가 바로 '노트북LM(NotebookLM)'입니다.
기존의 챗GPT나 제미나이는 전 세계 웹 데이터를 학습했기 때문에 우리 학교 규칙이나 2026학년도 학교 교육계획서에 대해 물어보면 엉뚱한 답변을 지어내곤 했습니다. 이를 '할루시네이션(환각 현상)'이라고 하죠.
하지만 노트북LM은 철저하게 '내가 업로드한 문서'만을 근거로 답변합니다.
학교 규정집, 교육과정 해설서, 연간 학사일정 PDF를 올려두면, 오직 그 문서 안에서만 팩트를 찾아 답변하고, 모든 문장마다 각주 번호를 달아줍니다.
각주를 클릭하면 원본 문서의 몇 페이지 몇 번째 줄에서 가져왔는지 노란색으로 하이라이트해 주기 때문에, 공문서 처리나 연구 수업 준비에 100% 안심하고 활용할 수 있습니다.""")

    # =========================================================================
    # SLIDE 10: 자료의 재구성 (SOURCE INSIGHT)
    # =========================================================================
    s10 = add_slide_with_subtle_bg(prs, blank_layout, 10)
    add_header(s10, "DOCUMENT INTELLIGENCE", "자료의 재구성: 수백 장의 문서를 단 3초 만에", "방대한 교육과정 해설서, 교원 매뉴얼, 학급 회의록을 교사 맞춤형 포맷으로 즉각 재구성")

    s10_cards = [
        ("핵심 요약 & 스터디 가이드", "200페이지의 해설서도 1페이지로", "수백 페이지의 2022 개정 교육과정 총론에서 교과별 핵심 성취기준 및 이전 대비 변경점만 일목요연하게 축약 및 구조화", COLOR_GOOGLE_BLUE),
        ("자동성장형 퀴즈 & 형성평가", "수업 교재 본문 기반 문항 생성", "업로드된 수업 지문을 기반으로 5지선다형 객관식, 빈칸 채우기, 서술형 토론 논제 및 정답 해설 루브릭까지 원클릭 출제", COLOR_GOOGLE_YELLOW),
        ("FAQ 및 체크리스트 자동화", "복잡한 업무 매뉴얼의 질의응답화", "학교생활기록부 기재요령, 교원 복무규정 등 두꺼운 책자 속에서 교사들이 가장 헷갈려하는 핵심 Q&A 자동 도출", COLOR_GOOGLE_GREEN)
    ]

    for idx, (title, sub, body, color) in enumerate(s10_cards):
        l = Inches(0.7 + idx * 2.95)
        t = Inches(1.85)
        w = Inches(2.75)
        h = Inches(3.05)

        card = add_card(s10, l, t, w, h)
        add_indicator_bar(s10, l, t, w, Inches(0.08), color)
        
        tf = s10.shapes.add_textbox(l + Inches(0.15), t + Inches(0.18), w - Inches(0.3), h - Inches(0.3)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = color
        
        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(9.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(3)
        p_sub.space_after = Pt(8)

        pb = tf.add_paragraph()
        pb.text = body
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10)
        pb.font.color.rgb = COLOR_TEXT_MAIN
        pb.space_before = Pt(4)

    bot10 = add_card(s10, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b10 = bot10.text_frame
    tf_b10.margin_left = tf_b10.margin_right = tf_b10.margin_top = tf_b10.margin_bottom = 0
    pb10 = tf_b10.paragraphs[0]
    pb10.text = "✦ 읽고 정리하느라 밤새우던 문서 업무를, 이제 AI와 대화하며 전략적 판단만 내리세요."
    pb10.font.name = FONT_HEADING
    pb10.font.size = Pt(10.5)
    pb10.font.bold = True
    pb10.font.color.rgb = COLOR_PRIMARY_BLUE
    pb10.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s10, """[발표자 대본]
선생님들, 교육과정 개정 시기나 새 학기가 되면 몇백 페이지짜리 두꺼운 해설서와 매뉴얼을 받고 한숨 쉬신 적 있으시죠?
노트북LM에 그 두꺼운 PDF를 올려두면 마법 같은 일이 일어납니다.
[스터디 가이드 만들기] 버튼 하나만 누르면 전체 핵심 요약과 질문 리스트가 3초 만에 정리됩니다.
또한 수업 지문을 올려두고 '이 지문을 바탕으로 5지선다형 문제 3개와 토론 질문 1개를 만들어줘'라고 하면, 원문에 딱 맞춘 형성평가 시험지가 즉시 출력됩니다.
두꺼운 매뉴얼을 처음부터 끝까지 정독하는 시대에서, 필요한 정보만 똑똑하게 추출해 수업에 적용하는 시대로 바뀐 것입니다.""")

    # =========================================================================
    # SLIDE 11: [하이라이트] 오디오 오버뷰 (AUDIO OVERVIEW)
    # =========================================================================
    s11 = add_slide_with_subtle_bg(prs, blank_layout, 11)
    add_header(s11, "FEATURE SPOTLIGHT", "[하이라이트] 오디오 오버뷰: 문서가 팟캐스트로", "읽지 말고 들으세요 — 학교 운영계획서가 2인의 유쾌한 팟캐스트 토론으로 변신합니다")

    c11_l = add_card(s11, Inches(0.7), Inches(1.85), Inches(4.3), Inches(3.1), bg_rgb=COLOR_DARK_CARD, border_rgb=COLOR_GOOGLE_YELLOW)
    add_indicator_bar(s11, Inches(0.7), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_YELLOW)
    tf_11l = s11.shapes.add_textbox(Inches(0.95), Inches(2.05), Inches(3.9), Inches(2.7)).text_frame
    tf_11l.word_wrap = True
    tf_11l.margin_left = tf_11l.margin_right = tf_11l.margin_top = tf_11l.margin_bottom = 0
    
    p11l_h = tf_11l.paragraphs[0]
    p11l_h.text = "🎙️ AI Audio Overview (Deep Dive Podcast)"
    p11l_h.font.name = FONT_HEADING
    p11l_h.font.size = Pt(12)
    p11l_h.font.bold = True
    p11l_h.font.color.rgb = COLOR_GOOGLE_YELLOW
    
    p11l_b = tf_11l.add_paragraph()
    p11l_b.text = "• 2인의 남녀 AI 호스트가 업로드된 문서를 바탕으로 생생한 대화형 오디오 자동 생성\n\n• 단순한 기계음 읽기(TTS)가 아닌, 맞장구와 감탄사, 유머가 섞인 고품질 라디오 토크쇼 형식\n\n• 문서의 핵심 쟁점과 교육적 가치를 서로 질문하고 토론하며 입체적으로 청각화"
    p11l_b.font.name = FONT_BODY
    p11l_b.font.size = Pt(10.5)
    p11l_b.font.color.rgb = RGBColor(241, 245, 249)
    p11l_b.space_before = Pt(10)

    c11_r = add_card(s11, Inches(5.2), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_BORDER)
    tf_11r = s11.shapes.add_textbox(Inches(5.4), Inches(2.05), Inches(3.7), Inches(2.7)).text_frame
    tf_11r.word_wrap = True
    tf_11r.margin_left = tf_11r.margin_right = tf_11r.margin_top = tf_11r.margin_bottom = 0
    
    p11r_h = tf_11r.paragraphs[0]
    p11r_h.text = "EDUCATIONAL APPLICATIONS"
    p11r_h.font.name = FONT_HEADING
    p11r_h.font.size = Pt(11)
    p11r_h.font.bold = True
    p11r_h.font.color.rgb = COLOR_PRIMARY_BLUE
    
    app_list = [
        ("01. 출퇴근길 업무 파악", "차 안이나 대중교통 이동 중 학교 교육계획서나 공문을 10분짜리 팟캐스트로 들으며 사전 파악"),
        ("02. 수업 도입 오디오 프리뷰", "새로운 단원 진도 전 학생들에게 5분 분량의 흥미진진한 팟캐스트를 사전 청취 과제로 부여"),
        ("03. 포용적 교육 지원", "긴 글 읽기에 부담을 느끼는 난독 학생이나 다문화 학생을 위한 훌륭한 청각 학습 도구 제공")
    ]
    for atitle, adesc in app_list:
        pa = tf_11r.add_paragraph()
        pa.text = "• " + atitle
        pa.font.name = FONT_HEADING
        pa.font.size = Pt(11)
        pa.font.bold = True
        pa.font.color.rgb = COLOR_TEXT_MAIN
        pa.space_before = Pt(8)
        
        pad = tf_11r.add_paragraph()
        pad.text = "   " + adesc
        pad.font.name = FONT_BODY
        pad.font.size = Pt(9.5)
        pad.font.color.rgb = COLOR_TEXT_MUTED
        pad.space_before = Pt(2)

    bot11 = add_card(s11, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b11 = bot11.text_frame
    tf_b11.margin_left = tf_b11.margin_right = tf_b11.margin_top = tf_b11.margin_bottom = 0
    pb11 = tf_b11.paragraphs[0]
    pb11.text = "✦ '읽는 문서'에서 '듣는 경험'으로의 전환: 오디오 오버뷰가 교실의 접근성을 넓힙니다."
    pb11.font.name = FONT_HEADING
    pb11.font.size = Pt(10.5)
    pb11.font.bold = True
    pb11.font.color.rgb = COLOR_PRIMARY_BLUE
    pb11.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s11, """[발표자 대본]
전 세계 교육자들을 가장 열광시킨 노트북LM의 킬러 기능, 바로 '오디오 오버뷰(Audio Overview)'입니다.
문서를 올려놓고 [오디오 생성] 버튼을 누르면, 남녀 두 명의 AI 아나운서가 등장해 그 문서를 가지고 마치 라디오 팟캐스트처럼 토론을 시작합니다.
"어, 이번 우리 학교 교육계획서 보니까 창의융합 프로젝트가 강조됐네? 맞아, 특히 2학기 현장체험학습이랑 연계된 점이 흥미롭더라고!" 하면서 농담도 섞고 서로 맞장구를 칩니다.
선생님들 출퇴근길 운전하실 때 라디오처럼 켜두시면 교내 연수 자료가 귀로 쏙쏙 들어옵니다.
뿐만 아니라 학생들에게 수업 전에 이 오디오 파일을 들려주면 배경지식을 형성하는 데 최고의 동기유발 자료가 됩니다.""")

    # =========================================================================
    # SLIDE 12: 개인별 맞춤 학습 튜터
    # =========================================================================
    s12 = add_slide_with_subtle_bg(prs, blank_layout, 12)
    add_header(s12, "PERSONALIZED LEARNING", "개인별 맞춤 학습 튜터: 1:1 개별화 교육의 실현", "하나의 공통 지문으로 학생 수준에 최적화된 3단계 '수준별 맞춤 학습지' 자동 생성")

    tiers_data = [
        ("LEVEL 1 : 기초 다지기", "기초학력 지원 대상", [
            "어려운 한자어 및 생소한 어휘 각주 풀이 수록",
            "복잡한 만연체 문장을 짧고 직관적인 문장으로 변환",
            "내용 일치 여부 확인형 O/X 및 핵심 단어 빈칸 채우기"
        ], COLOR_GOOGLE_GREEN),
        ("LEVEL 2 : 표준 역량", "교육과정 표준 도달", [
            "교과서 표준 수준의 원문 지문과 핵심 어휘 유지",
            "문맥 추론 및 문단별 중심 생각 파악 문항",
            "단원 성취기준에 부합하는 서술형 형성평가 2문항"
        ], COLOR_GOOGLE_BLUE),
        ("LEVEL 3 : 심화 탐구", "심화 탐구 및 영재", [
            "관련 시사 이슈 및 심화 학술 칼럼 연계 제시",
            "저자의 주장을 비판적 시각에서 반박하는 토론 논제",
            "자신의 논리를 종합하여 작성하는 에세이형 탐구 과제"
        ], COLOR_GOOGLE_RED),
    ]

    for idx, (title, sub, bullets, color) in enumerate(tiers_data):
        l = Inches(0.7 + idx * 2.95)
        t = Inches(1.85)
        w = Inches(2.75)
        h = Inches(3.05)

        card = add_card(s12, l, t, w, h)
        add_indicator_bar(s12, l, t, w, Inches(0.08), color)
        
        tf = s12.shapes.add_textbox(l + Inches(0.15), t + Inches(0.18), w - Inches(0.3), h - Inches(0.3)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(11.5)
        p0.font.bold = True
        p0.font.color.rgb = color
        
        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(9.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(3)
        p_sub.space_after = Pt(8)

        for b in bullets:
            pb = tf.add_paragraph()
            pb.text = "• " + b
            pb.font.name = FONT_BODY
            pb.font.size = Pt(9.5)
            pb.font.color.rgb = COLOR_TEXT_MAIN
            pb.space_before = Pt(4)

    bot12 = add_card(s12, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b12 = bot12.text_frame
    tf_b12.margin_left = tf_b12.margin_right = tf_b12.margin_top = tf_b12.margin_bottom = 0
    pb12 = tf_b12.paragraphs[0]
    pb12.text = "✦ 한 명의 교사가 30명의 학습 속도를 맞추는 기적이 AI를 통해 현실이 됩니다."
    pb12.font.name = FONT_HEADING
    pb12.font.size = Pt(10.5)
    pb12.font.bold = True
    pb12.font.color.rgb = COLOR_PRIMARY_BLUE
    pb12.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s12, """[발표자 대본]
공교육 교실에서 가장 가슴 아픈 순간은 한 수업 안에서 누구는 지루해서 하품하고, 누구는 어려워서 엎드려 잘 때입니다.
선생님들도 수준별 학습지를 만들어주고 싶지만, 매 차시마다 3단계로 학습지를 만들 시간이 도저히 없었습니다.
하지만 제미나이를 활용하면 원문 기사나 문학 작품 하나를 넣고,
'1단계는 어휘 각주와 짧은 문장으로 변환해 주고, 2단계는 표준 문제로, 3단계는 심화 비판적 토론 과제로 3단 분할해줘'라고 프롬프트를 넣으면 20초 만에 3종의 학습지가 생성됩니다.
단 한 명의 아이도 수업에서 소외되지 않도록 돕는 진정한 의미의 '포용적 맞춤 교육'이 실현되는 것입니다.""")

    # =========================================================================
    # SLIDE 13: Google AI Studio - 나만의 AI 제작
    # =========================================================================
    s13 = add_slide_with_subtle_bg(prs, blank_layout, 13)
    add_header(s13, "NO-CODE PROMPT ENGINEERING", "Google AI Studio: 우리 교실 전용 챗봇 제작", "단 한 줄의 코딩 없이 5분 만에 완성하는 '우리 반 전담 AI 소크라테스 튜터'")

    steps13 = [
        ("STEP 01", "System Instruction 설정", "\"너는 초등학교 5학년 학생의 눈높이에 맞춰 친절하고 자상하게 대화하는 수학 멘토야. 정답을 바로 알려주지 말고, 질문을 통해 학생이 스스로 답을 찾도록 유도해.\"", COLOR_GOOGLE_BLUE),
        ("STEP 02", "Few-shot Examples 주입", "학생: \"분수 덧셈 어떻게 해요?\"\nAI: \"분수의 덧셈이군요! 분모가 서로 다를 때는 먼저 어떤 작업을 해야 크기를 비교할 수 있을까요?\" (모범 대화 학습)", COLOR_GOOGLE_YELLOW),
        ("STEP 03", "클래스룸 배포 & 즉시 참여", "완성된 AI 챗봇의 웹 링크를 구글 클래스룸에 공유\n학생들은 태블릿으로 접속하여 안전한 가이드라인 속에서 1:1 탐구 대화 수행", COLOR_GOOGLE_GREEN),
    ]

    for idx, (step_tag, title, desc, color) in enumerate(steps13):
        l = Inches(0.7 + idx * 2.95)
        t = Inches(1.85)
        w = Inches(2.75)
        h = Inches(3.0)

        card = add_card(s13, l, t, w, h)
        add_indicator_bar(s13, l, t, Inches(0.06), h, color)
        
        tf = s13.shapes.add_textbox(l + Inches(0.18), t + Inches(0.18), w - Inches(0.3), h - Inches(0.3)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p_tag = tf.paragraphs[0]
        p_tag.text = step_tag
        p_tag.font.name = FONT_HEADING
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = color
        
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_MAIN
        p_t.space_before = Pt(6)
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_TEXT_MUTED
        p_d.space_before = Pt(8)

    bot13 = add_card(s13, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b13 = bot13.text_frame
    tf_b13.margin_left = tf_b13.margin_right = tf_b13.margin_top = tf_b13.margin_bottom = 0
    pb13 = tf_b13.paragraphs[0]
    pb13.text = "✦ 교사가 설계한 철학대로 학생과 상호작용하는 안전한 교실 챗봇을 누구나 만들 수 있습니다."
    pb13.font.name = FONT_HEADING
    pb13.font.size = Pt(10.5)
    pb13.font.bold = True
    pb13.font.color.rgb = COLOR_PRIMARY_BLUE
    pb13.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s13, """[발표자 대본]
학생들에게 상용 챗봇을 그대로 쓰게 하면 가장 큰 문제가 무엇일까요?
아이들이 '선생님 숙제 다 해줘'라고 물어보면 AI가 정답을 그냥 다 알려줘 버린다는 점입니다. 사고력이 자랄 틈이 없죠.
구글 AI 스튜디오(Google AI Studio)를 활용하면, 코딩을 전혀 몰라도 '시스템 지침(System Instruction)'에 '너는 정답을 주지 말고 소크라테스처럼 반문하며 학생이 생각하게 만들어'라고 교사의 교육 철학을 입력해 둘 수 있습니다.
이렇게 만든 링크를 학생들에게 주면, 아무리 정답을 달라고 졸라도 친절하게 생각의 실마리만 던져주는 우리 반 전담 튜터가 완성됩니다.""")

    # =========================================================================
    # SLIDE 14: [사례] 생기부 & 상담 어시스턴트
    # =========================================================================
    s14 = add_slide_with_subtle_bg(prs, blank_layout, 14)
    add_header(s14, "ETHICAL CLASSROOM USE", "[사례] 학교생활기록부 & 학생 상담 어시스턴트", "교사의 교육 철학과 일상 관찰 기록을 공공 기록물 문체로 정교하게 다듬는 과정")

    c14_l = add_card(s14, Inches(0.7), Inches(1.85), Inches(4.1), Inches(2.5), bg_rgb=RGBColor(241, 245, 249), border_rgb=COLOR_BORDER)
    add_indicator_bar(s14, Inches(0.7), Inches(1.85), Inches(0.06), Inches(2.5), COLOR_GOOGLE_YELLOW)
    tf_14l = s14.shapes.add_textbox(Inches(0.92), Inches(2.0), Inches(3.7), Inches(2.2)).text_frame
    tf_14l.word_wrap = True
    tf_14l.margin_left = tf_14l.margin_right = tf_14l.margin_top = tf_14l.margin_bottom = 0
    p14l_h = tf_14l.paragraphs[0]
    p14l_h.text = "교사의 날것 관찰 메모 (Observation Notes)"
    p14l_h.font.name = FONT_HEADING
    p14l_h.font.size = Pt(11)
    p14l_h.font.bold = True
    p14l_h.font.color.rgb = COLOR_GOOGLE_YELLOW
    p14l_b = tf_14l.add_paragraph()
    p14l_b.text = "\"민우가 과학 시간 실험할 때 조원들 의견 잘 조율하고, 회로 연결 실패했을 때 끝까지 포기하지 않고 원인 찾아서 결국 전구 켬. 끈기 있고 책임감 강함.\""
    p14l_b.font.name = FONT_BODY
    p14l_b.font.size = Pt(11)
    p14l_b.font.color.rgb = COLOR_TEXT_MUTED
    p14l_b.space_before = Pt(8)

    c14_r = add_card(s14, Inches(5.2), Inches(1.85), Inches(4.1), Inches(2.5), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_GOOGLE_BLUE, border_width_pt=1.5)
    add_indicator_bar(s14, Inches(5.2), Inches(1.85), Inches(0.06), Inches(2.5), COLOR_PRIMARY_BLUE)
    tf_14r = s14.shapes.add_textbox(Inches(5.42), Inches(2.0), Inches(3.7), Inches(2.2)).text_frame
    tf_14r.word_wrap = True
    tf_14r.margin_left = tf_14r.margin_right = tf_14r.margin_top = tf_14r.margin_bottom = 0
    p14r_h = tf_14r.paragraphs[0]
    p14r_h.text = "정제된 NEIS 기재용 공식 문체 (Refined Output)"
    p14r_h.font.name = FONT_HEADING
    p14r_h.font.size = Pt(11)
    p14r_h.font.bold = True
    p14r_h.font.color.rgb = COLOR_PRIMARY_BLUE
    p14r_b = tf_14r.add_paragraph()
    p14r_b.text = "\"과학 탐구 실험에서 모둠원 간의 이견을 경청하며 합리적으로 조율하는 의사소통 역량을 발휘함. 회로 결선 오류 상황에서도 과제를 포기하지 않고 가설 검증을 끈기 있게 반복하여 성공적으로 해결해 내는 과제 집착력이 매우 우수함.\""
    p14r_b.font.name = FONT_BODY
    p14r_b.font.size = Pt(10.5)
    p14r_b.font.color.rgb = COLOR_TEXT_MAIN
    p14r_b.space_before = Pt(8)

    w_card = add_card(s14, Inches(0.7), Inches(4.5), Inches(8.6), Inches(0.95), bg_rgb=RGBColor(254, 242, 242), border_rgb=COLOR_GOOGLE_RED, border_width_pt=1.2)
    tf_w = w_card.text_frame
    tf_w.word_wrap = True
    tf_w.margin_left = tf_w.margin_right = tf_w.margin_top = tf_w.margin_bottom = 0
    pw0 = tf_w.paragraphs[0]
    pw0.text = "⚠️ 개인정보 보호 및 법적 준수 수칙 (CRITICAL PRIVACY SHIELD)"
    pw0.font.name = FONT_HEADING
    pw0.font.size = Pt(10)
    pw0.font.bold = True
    pw0.font.color.rgb = COLOR_GOOGLE_RED
    pw1 = tf_w.add_paragraph()
    pw1.text = "• 학생의 실명, 주민번호, 생년월일, 사진 등 개인 식별 정보는 절대로 프롬프트에 입력하지 않습니다. (학생 A, 학생 B 가명 사용)\n• AI는 어휘와 문장 다듬기 보조 도구일 뿐이며, 최종 기록 내용의 진실성과 법적 책임은 오직 담당 교사의 직접 확인과 검증에 있습니다."
    pw1.font.name = FONT_BODY
    pw1.font.size = Pt(9.5)
    pw1.font.color.rgb = RGBColor(153, 27, 27)
    pw1.space_before = Pt(3)

    set_speaker_notes(s14, """[발표자 대본]
학기 말이면 생활기록부 작성 때문에 수많은 선생님들께서 극심한 스트레스를 겪으십니다.
교사가 아이의 행동을 관찰하고 칭찬해 주고 싶은 핵심 포인트는 명확한데, 교육부 기재요령에 맞는 정형화된 공공 문체로 바꾸는 작업이 많은 에너지를 소모시키기 때문입니다.
왼쪽에 보시는 것처럼 선생님께서 수첩에 적어둔 솔직하고 거친 관찰 메모를 넣고, '생기부 기재요령에 맞는 품격 있는 문체로 다듬어줘'라고 요청하면 오른쪽처럼 정교한 표현으로 다듬어집니다.
단, 여기서 가장 중요한 철칙이 있습니다. 학생의 이름이나 주민번호 같은 개인정보는 절대 입력해서는 안 되며, '학생 A'처럼 익명화해야 합니다. 그리고 최종 문구는 반드시 교사가 직접 확인하고 교직의 양심으로 기재해야 합니다.""")

    # =========================================================================
    # SLIDE 15: Google Vids - 영상 제작의 미래
    # =========================================================================
    s15 = add_slide_with_subtle_bg(prs, blank_layout, 15)
    add_header(s15, "NEXT-GEN MULTIMEDIA", "Google Vids: 영상 제작의 새로운 미래", "텍스트 입력만으로 수업 도입 영상과 프로젝트 안내 영상이 완성되는 시대")

    v_cards = [
        ("01. 스토리보드 자동 구성", "수업 기획의 완전 자동화", "단원명과 핵심 학습 목표를 입력하면 도입-전개-정리에 적합한 최적의 씬(Scene) 구성안 및 나레이션 스크립트 자동 생성", COLOR_GOOGLE_BLUE),
        ("02. 라이선스 안전 스톡 미디어", "저작권 걱정 없는 고화질 클립", "공교육 현장에서 안심하고 쓸 수 있는 고화질 비디오 클립과 테마별 배경음악이 텍스트 내용에 맞춰 자동 매칭", COLOR_GOOGLE_RED),
        ("03. 스튜디오급 AI 보이스오버", "전문 성우 수준의 음성 더빙", "교사가 마이크로 직접 녹음할 필요 없이, 감정과 톤 조절이 가능한 또렷한 한국어 나레이션 자동 합성", COLOR_GOOGLE_GREEN),
    ]

    for idx, (title, sub, body, color) in enumerate(v_cards):
        l = Inches(0.7 + idx * 2.95)
        t = Inches(1.85)
        w = Inches(2.75)
        h = Inches(3.05)

        card = add_card(s15, l, t, w, h)
        add_indicator_bar(s15, l, t, w, Inches(0.08), color)
        
        tf = s15.shapes.add_textbox(l + Inches(0.15), t + Inches(0.18), w - Inches(0.3), h - Inches(0.3)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = FONT_HEADING
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = color
        
        p_sub = tf.add_paragraph()
        p_sub.text = sub
        p_sub.font.name = FONT_BODY
        p_sub.font.size = Pt(9.5)
        p_sub.font.color.rgb = COLOR_TEXT_MUTED
        p_sub.space_before = Pt(3)
        p_sub.space_after = Pt(8)

        pb = tf.add_paragraph()
        pb.text = body
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10)
        pb.font.color.rgb = COLOR_TEXT_MAIN
        pb.space_before = Pt(4)

    bot15 = add_card(s15, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b15 = bot15.text_frame
    tf_b15.margin_left = tf_b15.margin_right = tf_b15.margin_top = tf_b15.margin_bottom = 0
    pb15 = tf_b15.paragraphs[0]
    pb15.text = "✦ 복잡한 영상 편집 툴을 배울 필요 없이, 프롬프트 한 줄로 수업 도입 영상이 제작됩니다."
    pb15.font.name = FONT_HEADING
    pb15.font.size = Pt(10.5)
    pb15.font.bold = True
    pb15.font.color.rgb = COLOR_PRIMARY_BLUE
    pb15.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s15, """[발표자 대본]
선생님들께서 수업 도입 단계에서 학생들의 주의를 집중시키기 위해 유튜브 영상을 찾느라 고생하신 경험이 많으실 겁니다.
하지만 딱 우리 단원 내용에 들어맞는 영상을 찾기란 하늘의 별 따기였죠.
구글 워크스페이스의 차세대 영상 제작 도구인 'Google Vids'는 프롬프트 몇 줄로 교실 전용 비디오를 만들어줍니다.
'조선 시대의 대동법 시행 배경에 대한 2분짜리 수업 도입 영상을 만들어줘'라고 하면, AI가 스토리보드를 짜고, 저작권 문제가 없는 스톡 영상과 배경음악을 깔고, 전문 성우 톤의 목소리까지 입혀서 하나의 완성된 영상 클립을 만들어냅니다.
영상 제작에 들던 수많은 시간이 단 몇 분으로 압축됩니다.""")

    # =========================================================================
    # SLIDE 16: 멀티미디어와 교육의 결합
    # =========================================================================
    s16 = add_slide_with_subtle_bg(prs, blank_layout, 16)
    add_header(s16, "CREATIVE EXPRESSION", "멀티미디어와 교육의 결합: 상상력의 시각화", "Imagen 3와 음향 AI를 활용해 교과서 너머의 생생한 몰입형 학습 경험 제공")

    c16_l = add_card(s16, Inches(0.7), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_BORDER)
    add_indicator_bar(s16, Inches(0.7), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_BLUE)
    tf_16l = s16.shapes.add_textbox(Inches(0.92), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_16l.word_wrap = True
    tf_16l.margin_left = tf_16l.margin_right = tf_16l.margin_top = tf_16l.margin_bottom = 0
    p16l_h = tf_16l.paragraphs[0]
    p16l_h.text = "역사 & 사회과: 시대상의 생생한 복원"
    p16l_h.font.name = FONT_HEADING
    p16l_h.font.size = Pt(12)
    p16l_h.font.bold = True
    p16l_h.font.color.rgb = COLOR_GOOGLE_BLUE
    p16l_b = tf_16l.add_paragraph()
    p16l_b.text = "• \"조선 시대 한양 육의전 저잣거리에서 비단을 파는 시전 상인들과 장터 풍경을 실사 화풍으로 재현해 줘\"\n\n• 교과서의 낡은 흑백 삽화나 작은 사진의 한계를 뛰어넘어, 학생들이 당시 역사 현장에 서 있는 듯한 시각적 몰입감 제공\n\n• 고증 자료와 AI 시각화를 비교하는 비판적 사료 비판 수업 설계 가능"
    p16l_b.font.name = FONT_BODY
    p16l_b.font.size = Pt(10)
    p16l_b.font.color.rgb = COLOR_TEXT_MAIN
    p16l_b.space_before = Pt(8)

    c16_r = add_card(s16, Inches(5.2), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_BORDER)
    add_indicator_bar(s16, Inches(5.2), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_GREEN)
    tf_16r = s16.shapes.add_textbox(Inches(5.42), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_16r.word_wrap = True
    tf_16r.margin_left = tf_16r.margin_right = tf_16r.margin_top = tf_16r.margin_bottom = 0
    p16r_h = tf_16r.paragraphs[0]
    p16r_h.text = "국어 & 예술: 문학과 상상의 시각화"
    p16r_h.font.name = FONT_HEADING
    p16r_h.font.size = Pt(12)
    p16r_h.font.bold = True
    p16r_h.font.color.rgb = COLOR_GOOGLE_GREEN
    p16r_b = tf_16r.add_paragraph()
    p16r_b.text = "• 학생들이 직접 창작한 동시나 단편 소설의 주요 장면을 프롬프트로 묘사하여 AI 삽화집 완성\n\n• 자신의 언어적 묘사가 어떻게 시각적 이미지로 변환되는지 관찰하며 형용사 및 비유적 표현력 증진\n\n• 그림을 그리지 못해 위축되던 학생들도 자신만의 독창적인 아이디어로 예술 프로젝트에 당당히 참여"
    p16r_b.font.name = FONT_BODY
    p16r_b.font.size = Pt(10)
    p16r_b.font.color.rgb = COLOR_TEXT_MAIN
    p16r_b.space_before = Pt(8)

    bot16 = add_card(s16, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b16 = bot16.text_frame
    tf_b16.margin_left = tf_b16.margin_right = tf_b16.margin_top = tf_b16.margin_bottom = 0
    pb16 = tf_b16.paragraphs[0]
    pb16.text = "✦ AI 이미지 생성은 단순 감상이 아니라, 학생들의 상상력을 구체화하는 표현 도구가 됩니다."
    pb16.font.name = FONT_HEADING
    pb16.font.size = Pt(10.5)
    pb16.font.bold = True
    pb16.font.color.rgb = COLOR_PRIMARY_BLUE
    pb16.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s16, """[발표자 대본]
멀티미디어 생성 AI는 수업을 지루한 활자에서 살아 움직이는 시각적 경험으로 바꿉니다.
역사 수업에서 '삼국시대 장터의 모습'을 가르칠 때, 구글의 최신 이미지 모델 Imagen 3를 활용해 사실적인 고화질 그림을 생성해 보여주면 아이들의 눈이 반짝입니다.
또한 국어 시간에 시나 소설을 쓸 때, 자신이 쓴 글을 묘사 프롬프트로 바꿔서 AI 삽화집을 만들어보는 활동을 해보세요.
평소 그림 솜씨가 없어 위축되었던 아이들도 자신의 상상력을 마음껏 발휘하며 훌륭한 그림책 작가가 될 수 있습니다.
기술이 예술적 표현의 문턱을 낮추어 모든 아이에게 창작의 기쁨을 주는 것입니다.""")

    # =========================================================================
    # SLIDE 17: 평가 패러다임의 변화
    # =========================================================================
    s17 = add_slide_with_subtle_bg(prs, blank_layout, 17)
    add_header(s17, "EVALUATION PARADIGM", "평가 패러다임의 변화: 지식 암기에서 질문 역량으로", "\"무엇을 기억하는가?\"에서 \"AI를 활용해 어떤 가치 있는 질문을 던지는가?\"로의 전환")

    c17_l = add_card(s17, Inches(0.7), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=RGBColor(241, 245, 249), border_rgb=COLOR_BORDER)
    add_indicator_bar(s17, Inches(0.7), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_RED)
    tf_17l = s17.shapes.add_textbox(Inches(0.92), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_17l.word_wrap = True
    tf_17l.margin_left = tf_17l.margin_right = tf_17l.margin_top = tf_17l.margin_bottom = 0
    p17l_h = tf_17l.paragraphs[0]
    p17l_h.text = "과거의 지식 암기식 평가 (Past)"
    p17l_h.font.name = FONT_HEADING
    p17l_h.font.size = Pt(12)
    p17l_h.font.bold = True
    p17l_h.font.color.rgb = COLOR_GOOGLE_RED
    
    p17l_items = [
        "단편적인 사실 기억 및 공식 암기력 측정",
        "정답이 하나로 정해진 5지선다형 일제식 지필평가",
        "결과로서의 점수 산출 및 학생 서열화",
        "⚠️ AI가 3초 만에 100점 맞을 수 있는 시험의 한계"
    ]
    for it in p17l_items:
        p = tf_17l.add_paragraph()
        p.text = "• " + it
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(8)

    c17_r = add_card(s17, Inches(5.2), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_PRIMARY_BLUE, border_width_pt=1.5)
    add_indicator_bar(s17, Inches(5.2), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_PRIMARY_BLUE)
    tf_17r = s17.shapes.add_textbox(Inches(5.42), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_17r.word_wrap = True
    tf_17r.margin_left = tf_17r.margin_right = tf_17r.margin_top = tf_17r.margin_bottom = 0
    p17r_h = tf_17r.paragraphs[0]
    p17r_h.text = "미래의 과정 중심 역량 평가 (Future)"
    p17r_h.font.name = FONT_HEADING
    p17r_h.font.size = Pt(12)
    p17r_h.font.bold = True
    p17r_h.font.color.rgb = COLOR_PRIMARY_BLUE
    
    p17r_items = [
        "문제 상황을 정의하고 프롬프트를 설계하는 질문력",
        "AI가 출력한 결과물의 오류를 찾아내는 비판적 검증력",
        "해결 과정을 기록하고 성찰하는 포트폴리오 수행평가",
        "✦ 오직 인간 교사만이 평가할 수 있는 사고의 깊이"
    ]
    for it in p17r_items:
        p = tf_17r.add_paragraph()
        p.text = "✦ " + it
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(8)

    bot17 = add_card(s17, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b17 = bot17.text_frame
    tf_b17.margin_left = tf_b17.margin_right = tf_b17.margin_top = tf_b17.margin_bottom = 0
    pb17 = tf_b17.paragraphs[0]
    pb17.text = "✦ AI 시대의 인재는 '정답을 외우는 사람'이 아니라 '새로운 질문을 생성하는 사람'입니다."
    pb17.font.name = FONT_HEADING
    pb17.font.size = Pt(10.5)
    pb17.font.bold = True
    pb17.font.color.rgb = COLOR_PRIMARY_BLUE
    pb17.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s17, """[발표자 대본]
선생님들, AI가 등장하면서 학교 시험과 평가에 가장 큰 지각변동이 일어났습니다.
단순히 교과서 몇 페이지에 나오는 사실을 외워서 정답 번호를 고르는 시험은 이제 아무런 의미가 없어졌습니다. AI에게 물어보면 3초 만에 만점을 받기 때문입니다.
그렇다면 우리는 무엇을 평가해야 할까요?
첫째, 복잡한 문제 상황에서 AI에게 어떤 정교한 질문(프롬프트)을 던져 해결책을 이끌어내는가?
둘째, AI가 내놓은 그럴듯한 답변에서 오류를 찾아내고 팩트를 검증할 수 있는가?
셋째, 그 결과를 바탕으로 친구들과 어떻게 소통하고 협력하는가?
즉, '지식의 암기'에서 '질문하는 역량과 비판적 사고력'으로 평가의 무게중심이 완전히 이동한 것입니다.""")

    # =========================================================================
    # SLIDE 18: 안전한 AI 활용 (ETHICS)
    # =========================================================================
    s18 = add_slide_with_subtle_bg(prs, blank_layout, 18)
    add_header(s18, "DIGITAL CITIZENSHIP & ETHICS", "안전한 AI 활용을 위한 윤리 가이드라인", "기술의 편리함 뒤에 반드시 갖추어야 할 교사와 학생의 디지털 시민의식 4대 원칙")

    eth_cards = [
        ("01. 개인정보 보호 (Privacy)", "식별 정보 절대 입력 금지", "학생 및 교직원의 이름, 주민번호, 성적, 사진 등 민감한 개인정보를 프롬프트에 입력하지 않기", COLOR_GOOGLE_RED),
        ("02. 출처 표기 & 저작권 준수", "투명한 도구 활용 공시", "과제나 보고서 작성 시 사용한 AI 도구와 프롬프트 명시, 타인의 창작물에 대한 저작권 존중", COLOR_GOOGLE_YELLOW),
        ("03. 비판적 검증 (Fact-Check)", "할루시네이션 교차 검증", "AI 답변을 맹신하지 않고 공인 기관 통계 및 1차 출처 문서를 통해 사실 여부를 검증하는 태도", COLOR_GOOGLE_GREEN),
        ("04. 딥페이크 & 윤리적 분별력", "책임감 있는 기술 사용", "인공지능을 이용한 타인의 이미지 합성, 악의적 왜곡, 차별과 혐오 콘텐츠 생성에 대한 단호한 경계", COLOR_GOOGLE_BLUE),
    ]

    for idx, (head, sub, body, color) in enumerate(eth_cards):
        row = idx // 2
        col = idx % 2
        l = Inches(0.7 + col * 4.4)
        t = Inches(1.85 + row * 1.55)
        w = Inches(4.2)
        h = Inches(1.4)

        card = add_card(s18, l, t, w, h)
        add_indicator_bar(s18, l, t, Inches(0.06), h, color)
        tf = s18.shapes.add_textbox(l + Inches(0.18), t + Inches(0.12), w - Inches(0.3), h - Inches(0.24)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        ph = tf.paragraphs[0]
        ph.text = head
        ph.font.name = FONT_HEADING
        ph.font.size = Pt(12)
        ph.font.bold = True
        ph.font.color.rgb = color
        
        ps = tf.add_paragraph()
        ps.text = sub
        ps.font.name = FONT_BODY
        ps.font.size = Pt(9.5)
        ps.font.color.rgb = COLOR_TEXT_MUTED
        ps.space_before = Pt(2)

        pb = tf.add_paragraph()
        pb.text = body
        pb.font.name = FONT_BODY
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = COLOR_TEXT_MAIN
        pb.space_before = Pt(4)

    bot18 = add_card(s18, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b18 = bot18.text_frame
    tf_b18.margin_left = tf_b18.margin_right = tf_b18.margin_top = tf_b18.margin_bottom = 0
    pb18 = tf_b18.paragraphs[0]
    pb18.text = "✦ 자동차의 발전이 브레이크와 신호등을 낳았듯, AI 활용의 성숙도는 윤리적 브레이크에 있습니다."
    pb18.font.name = FONT_HEADING
    pb18.font.size = Pt(10.5)
    pb18.font.bold = True
    pb18.font.color.rgb = COLOR_PRIMARY_BLUE
    pb18.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s18, """[발표자 대본]
선생님들, 자동차의 속도가 빨라질수록 가장 중요해지는 부품이 무엇일까요? 바로 '브레이크'입니다.
AI라는 강력한 엔진을 장착할 때, 우리는 아이들에게 반드시 안전한 브레이크를 쥐어주어야 합니다.
첫째, 우리 반 아이들의 소중한 개인정보는 절대 웹상의 공개 AI에 입력하지 않도록 철저히 가르쳐야 합니다.
둘째, 과제를 할 때 AI를 썼다면 '어떤 도구를 써서 어떻게 수정했는지' 투명하게 밝히는 출처 표기의 정직성을 지도해야 합니다.
셋째, AI가 제시한 정보라도 늘 의심하고 공식 문서로 확인하는 팩트체크 습관입니다.
넷째, 최근 심각한 사회 문제가 되고 있는 딥페이크나 합성물 등 타인에게 상처를 주는 행위에 대해 단호한 윤리적 기준을 세워주어야 합니다.""")

    # =========================================================================
    # SLIDE 19: 하이터치(High-Touch)의 시대
    # =========================================================================
    s19 = add_slide_with_subtle_bg(prs, blank_layout, 19)
    add_header(s19, "PHILOSOPHY OF EDUCATION", "하이터치(High-Touch)의 시대: 교사의 존재 이유", "하이테크(High-Tech)가 고도화될수록, 아이들의 마음을 어루만지는 인간적 교감은 더욱 빛납니다")

    c19_l = add_card(s19, Inches(0.7), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_BORDER)
    add_indicator_bar(s19, Inches(0.7), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_BLUE)
    tf_19l = s19.shapes.add_textbox(Inches(0.92), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_19l.word_wrap = True
    tf_19l.margin_left = tf_19l.margin_right = tf_19l.margin_top = tf_19l.margin_bottom = 0
    p19l_h = tf_19l.paragraphs[0]
    p19l_h.text = "High-Tech : AI가 맡아줄 영역"
    p19l_h.font.name = FONT_HEADING
    p19l_h.font.size = Pt(12)
    p19l_h.font.bold = True
    p19l_h.font.color.rgb = COLOR_PRIMARY_BLUE
    
    p19l_items = [
        "수준별 반복 학습 및 맞춤형 문제 풀이 훈련",
        "행정 공문 초안, 안내문, 주간학습안내 자동화",
        "방대한 교육 데이터 분석 및 학업 성취도 진단",
        "외국어 발음 피드백 및 단순 질의응답 튜터링"
    ]
    for it in p19l_items:
        p = tf_19l.add_paragraph()
        p.text = "• " + it
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.color.rgb = COLOR_TEXT_MUTED
        p.space_before = Pt(8)

    c19_r = add_card(s19, Inches(5.2), Inches(1.85), Inches(4.1), Inches(3.1), bg_rgb=COLOR_DARK_CARD, border_rgb=COLOR_GOOGLE_YELLOW, border_width_pt=1.5)
    add_indicator_bar(s19, Inches(5.2), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_YELLOW)
    tf_19r = s19.shapes.add_textbox(Inches(5.42), Inches(2.0), Inches(3.7), Inches(2.8)).text_frame
    tf_19r.word_wrap = True
    tf_19r.margin_left = tf_19r.margin_right = tf_19r.margin_top = tf_19r.margin_bottom = 0
    p19r_h = tf_19r.paragraphs[0]
    p19r_h.text = "High-Touch : 오직 선생님만의 영역"
    p19r_h.font.name = FONT_HEADING
    p19r_h.font.size = Pt(12)
    p19r_h.font.bold = True
    p19r_h.font.color.rgb = COLOR_GOOGLE_YELLOW
    
    p19r_items = [
        "교실 문을 열고 들어오는 아이의 그늘진 표정을 읽고 안아주는 일",
        "친구와의 갈등 속에서 경청과 배려, 화해의 미덕을 가르치는 일",
        "도전에 실패했을 때 등을 두드려 주며 믿음을 건네는 따뜻한 사랑",
        "한 영혼의 가치를 발견하고 꿈을 심어주는 전인적 인생 멘토링"
    ]
    for it in p19r_items:
        p = tf_19r.add_paragraph()
        p.text = "✦ " + it
        p.font.name = FONT_BODY
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = RGBColor(254, 243, 199)
        p.space_before = Pt(8)

    bot19 = add_card(s19, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b19 = bot19.text_frame
    tf_b19.margin_left = tf_b19.margin_right = tf_b19.margin_top = tf_b19.margin_bottom = 0
    pb19 = tf_b19.paragraphs[0]
    pb19.text = "✦ AI가 지식을 전담해 주기에, 선생님은 비로소 한 아이의 마음을 어루만지는 참된 스승이 됩니다."
    pb19.font.name = FONT_HEADING
    pb19.font.size = Pt(10.5)
    pb19.font.bold = True
    pb19.font.color.rgb = COLOR_PRIMARY_BLUE
    pb19.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s19, """[발표자 대본]
선생님 여러분, 오늘 강연 중 가장 마음에 담아 가셨으면 하는 슬라이드입니다.
우리가 왜 AI라는 고도의 하이테크(High-Tech)를 익혀야 할까요?
역설적이게도 가장 인간적인 하이터치(High-Touch)를 지켜내기 위해서입니다.
지식을 전달하고, 문제를 채점하고, 안내문을 작성하는 일은 AI에게 맡기십시오. AI가 훨씬 빠르고 지치지 않고 잘합니다.
그 대신 아침에 교실 문을 열고 들어올 때 유난히 어깨가 처진 아이의 등을 토닥여 주는 일, 친구와 다투고 우는 아이의 눈물을 닦아주며 용서와 공감을 가르치는 일... 
이것은 전 세계의 어떤 최첨단 슈퍼컴퓨터도 절대 대신할 수 없는 교사만의 신성한 영역입니다.
기술이 발전할수록 인간 교사의 온기는 더욱 귀해집니다.""")

    # =========================================================================
    # SLIDE 20: [Action Plan] 당장 내일 시도해볼 것
    # =========================================================================
    s20 = add_slide_with_subtle_bg(prs, blank_layout, 20)
    add_header(s20, "IMMEDIATE ACTION PLAN", "[Action Plan] 당장 내일 교실에서 시작하는 실천 3단계", "거창한 준비는 필요 없습니다. 내일 아침 출근해서 바로 시도해 볼 수 있는 작지만 확실한 3가지 액션")

    act_steps = [
        ("ACTION 01", "NotebookLM에 문서 1개 올리기", "이번 학기 교육과정 계획서나 수업 지도안 PDF를 노트북LM에 올려두고 핵심 요약 요청해 보기", COLOR_GOOGLE_BLUE),
        ("ACTION 02", "Gemini에게 공문 초안 부탁하기", "이번 주 나갈 가정통신문이나 행사 기안문 초안을 10초 만에 작성해 달라고 요청해 보기", COLOR_GOOGLE_YELLOW),
        ("ACTION 03", "수업 도입 흥미 질문 3개 뽑기", "내일 수업할 교과 단원명을 넣고 학생들의 눈빛을 반짝이게 할 흥미로운 도입 질문 3가지 추천받기", COLOR_GOOGLE_GREEN),
    ]

    for idx, (step_tag, title, desc, color) in enumerate(act_steps):
        l = Inches(0.7 + idx * 2.95)
        t = Inches(1.85)
        w = Inches(2.75)
        h = Inches(3.0)

        card = add_card(s20, l, t, w, h)
        add_indicator_bar(s20, l, t, Inches(0.06), h, color)
        
        tf = s20.shapes.add_textbox(l + Inches(0.18), t + Inches(0.18), w - Inches(0.3), h - Inches(0.3)).text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
        
        p_tag = tf.paragraphs[0]
        p_tag.text = step_tag
        p_tag.font.name = FONT_HEADING
        p_tag.font.size = Pt(11)
        p_tag.font.bold = True
        p_tag.font.color.rgb = color
        
        p_t = tf.add_paragraph()
        p_t.text = title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(12)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_MAIN
        p_t.space_before = Pt(6)
        
        p_d = tf.add_paragraph()
        p_d.text = desc
        p_d.font.name = FONT_BODY
        p_d.font.size = Pt(10)
        p_d.font.color.rgb = COLOR_TEXT_MUTED
        p_d.space_before = Pt(8)

    bot20 = add_card(s20, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b20 = bot20.text_frame
    tf_b20.margin_left = tf_b20.margin_right = tf_b20.margin_top = tf_b20.margin_bottom = 0
    pb20 = tf_b20.paragraphs[0]
    pb20.text = "✦ 거창한 변화보다, 내일 아침 커피 한 잔과 함께 시도하는 작은 5분이 교실의 공기를 바꿉니다."
    pb20.font.name = FONT_HEADING
    pb20.font.size = Pt(10.5)
    pb20.font.bold = True
    pb20.font.color.rgb = COLOR_PRIMARY_BLUE
    pb20.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s20, """[발표자 대본]
연수가 끝나고 나면 '좋은 내용이었지만 학교 가면 바빠서 언제 해보나...' 하고 잊어버리기 쉽습니다.
그래서 딱 세 가지만 당장 내일 아침에 해보시기를 강력하게 권합니다.
첫째, 출근하셔서 노트북LM 사이트를 열고, 이번 학기 교육과정 계획서 PDF 하나만 업로드해 보세요. 그리고 '이번 학기 4학년 과학 주요 성취기준 요약해줘'라고 딱 한 번 물어보십시오.
둘째, 이번 주 나갈 가정통신문 초안을 제미나이에게 써달라고 해보세요. 10초 만에 나오는 결과물을 보며 무릎을 치시게 될 겁니다.
셋째, 내일 수업할 단원명을 넣고 '아이들이 흥미를 느낄 만한 깜짝 질문 3개만 추천해줘'라고 해보세요.
이 세 가지 작은 실천이 선생님의 교직 생활을 완전히 바꾸어 놓을 것입니다.""")

    # =========================================================================
    # SLIDE 21: QR 코드 & 리소스 공유
    # =========================================================================
    s21 = add_slide_with_subtle_bg(prs, blank_layout, 21)
    add_header(s21, "RESOURCES & CONNECT", "QR 코드 & 실전 리소스 공유", "오늘 강연에 활용된 실전 프롬프트 템플릿과 추천 AI 도구 모음집을 지금 다운로드하세요")

    c21_l = add_card(s21, Inches(0.7), Inches(1.85), Inches(5.1), Inches(3.1), bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_BORDER)
    add_indicator_bar(s21, Inches(0.7), Inches(1.85), Inches(0.06), Inches(3.1), COLOR_GOOGLE_BLUE)
    tf_21l = s21.shapes.add_textbox(Inches(0.95), Inches(2.05), Inches(4.7), Inches(2.7)).text_frame
    tf_21l.word_wrap = True
    tf_21l.margin_left = tf_21l.margin_right = tf_21l.margin_top = tf_21l.margin_bottom = 0
    p21l_h = tf_21l.paragraphs[0]
    p21l_h.text = "DOWNLOADABLE TEACHER TOOLKIT"
    p21l_h.font.name = FONT_HEADING
    p21l_h.font.size = Pt(11)
    p21l_h.font.bold = True
    p21l_h.font.color.rgb = COLOR_PRIMARY_BLUE
    
    r_items = [
        ("01. 교사용 실전 프롬프트 치트시트 50선", "가정통신문, 체험학습, 생기부 문체 변환, 수업 도입 질문 등 구글 닥스 링크"),
        ("02. 초·중·고 교과별 NotebookLM 소스 모음", "2022 개정 교육과정 주요 과목별 핵심 요약 및 형성평가 프롬프트 세트"),
        ("03. 교실 AI 윤리 서약서 & 학부모 안내 서식", "학기 초 학급에서 바로 인쇄하여 활용할 수 있는 학생용 서약서 한글/PDF"),
        ("04. 오늘 발표 슬라이드 전체 PDF & 발표 대본", "교내 동료 장학 및 자율 연수 전달 강연용 전체 강의안 패키지")
    ]
    for rtitle, rdesc in r_items:
        p = tf_21l.add_paragraph()
        p.text = "• " + rtitle
        p.font.name = FONT_HEADING
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_MAIN
        p.space_before = Pt(6)
        
        pd = tf_21l.add_paragraph()
        pd.text = "   " + rdesc
        pd.font.name = FONT_BODY
        pd.font.size = Pt(9)
        pd.font.color.rgb = COLOR_TEXT_MUTED
        pd.space_before = Pt(2)

    c21_r = add_card(s21, Inches(6.0), Inches(1.85), Inches(3.3), Inches(3.1), bg_rgb=COLOR_DARK_CARD, border_rgb=COLOR_GOOGLE_BLUE, border_width_pt=1.5)
    tf_21r = s21.shapes.add_textbox(Inches(6.2), Inches(2.05), Inches(2.9), Inches(2.7)).text_frame
    tf_21r.word_wrap = True
    tf_21r.margin_left = tf_21r.margin_right = tf_21r.margin_top = tf_21r.margin_bottom = 0
    
    pqr_h = tf_21r.paragraphs[0]
    pqr_h.text = "SCAN FOR RESOURCES"
    pqr_h.font.name = FONT_HEADING
    pqr_h.font.size = Pt(11)
    pqr_h.font.bold = True
    pqr_h.font.color.rgb = COLOR_GOOGLE_YELLOW
    pqr_h.alignment = PP_ALIGN.CENTER
    
    pqr_b = tf_21r.add_paragraph()
    pqr_b.text = "📱 [QR CODE AREA]\n\n스마트폰 카메라로\nQR 코드를 스캔하시면\n자료실로 즉시 연결됩니다."
    pqr_b.font.name = FONT_HEADING
    pqr_b.font.size = Pt(12)
    pqr_b.font.bold = True
    pqr_b.font.color.rgb = RGBColor(255, 255, 255)
    pqr_b.alignment = PP_ALIGN.CENTER
    pqr_b.space_before = Pt(24)

    bot21 = add_card(s21, Inches(0.7), Inches(5.02), Inches(8.6), Inches(0.42), bg_rgb=COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE)
    tf_b21 = bot21.text_frame
    tf_b21.margin_left = tf_b21.margin_right = tf_b21.margin_top = tf_b21.margin_bottom = 0
    pb21 = tf_b21.paragraphs[0]
    pb21.text = "✦ 스마트폰 카메라를 켜고 화면의 QR 코드를 비추시면 모든 자료를 평생 무료로 열람하실 수 있습니다."
    pb21.font.name = FONT_HEADING
    pb21.font.size = Pt(10.5)
    pb21.font.bold = True
    pb21.font.color.rgb = COLOR_PRIMARY_BLUE
    pb21.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s21, """[발표자 대본]
오늘 강의에 사용된 모든 프롬프트와 자료를 선생님들께 아낌없이 공유해 드립니다.
화면 우측의 QR 코드를 스마트폰 카메라로 비추시면 구글 드라이브 폴더로 바로 연결됩니다.
그 안에는 학교에서 바로 복사해 쓰실 수 있는 프롬프트 50선 문서, 학급용 AI 윤리 서약서 서식, 그리고 오늘 보여드린 슬라이드 전체 파일이 들어있습니다.
학교에 돌아가셔서 동료 선생님들과 함께 나누어 보시고, 교내 자율 연수나 연구회 모임에서도 자유롭게 활용하시기 바랍니다.""")

    # =========================================================================
    # SLIDE 22: 마무리: 교육의 미래
    # =========================================================================
    s22 = add_slide_with_subtle_bg(prs, blank_layout, 22)
    add_header(s22, "CONCLUSION & VISION", "마무리: 교육의 미래, 우리가 함께 만들어갑니다", "\"미래는 이미 와 있습니다. 단지 널리 퍼져 있지 않을 뿐입니다.\" - 윌리엄 깁슨")

    c22_c = add_card(s22, Inches(0.7), Inches(1.85), Inches(8.6), Inches(2.9), bg_rgb=COLOR_DARK_CARD, border_rgb=COLOR_PRIMARY_BLUE, border_width_pt=1.5)
    add_indicator_bar(s22, Inches(0.7), Inches(1.85), Inches(8.6), Inches(0.08), COLOR_GOOGLE_YELLOW)
    
    tf_22c = s22.shapes.add_textbox(Inches(1.1), Inches(2.1), Inches(7.8), Inches(2.4)).text_frame
    tf_22c.word_wrap = True
    tf_22c.margin_left = tf_22c.margin_right = tf_22c.margin_top = tf_22c.margin_bottom = 0
    
    p22_q = tf_22c.paragraphs[0]
    p22_q.text = "\"미래는 이미 우리 곁에 와 있습니다. 단지 널리 퍼지지 않았을 뿐입니다.\""
    p22_q.font.name = FONT_HEADING
    p22_q.font.size = Pt(18)
    p22_q.font.bold = True
    p22_q.font.color.rgb = COLOR_GOOGLE_YELLOW
    p22_q.alignment = PP_ALIGN.CENTER
    
    p22_body = tf_22c.add_paragraph()
    p22_body.text = "기술에 휘둘리지 않고, 기술의 어깨 위에 올라타 아이들의 더 큰 미래를 열어주는 사람.\n오늘 이 자리에 함께하신 선생님 여러분이 바로 대한민국 미래 교육의 주인공입니다."
    p22_body.font.name = FONT_BODY
    p22_body.font.size = Pt(13)
    p22_body.font.color.rgb = RGBColor(241, 245, 249)
    p22_body.alignment = PP_ALIGN.CENTER
    p22_body.space_before = Pt(16)

    bot22 = add_card(s22, Inches(0.7), Inches(4.9), Inches(8.6), Inches(0.55), bg_rgb=COLOR_GOOGLE_BLUE)
    tf_b22 = bot22.text_frame
    tf_b22.margin_left = tf_b22.margin_right = tf_b22.margin_top = tf_b22.margin_bottom = 0
    pb22 = tf_b22.paragraphs[0]
    pb22.text = "경청해 주셔서 대단히 감사합니다! | Q&A 질의응답"
    pb22.font.name = FONT_HEADING
    pb22.font.size = Pt(14)
    pb22.font.bold = True
    pb22.font.color.rgb = RGBColor(255, 255, 255)
    pb22.alignment = PP_ALIGN.CENTER

    set_speaker_notes(s22, """[발표자 대본]
공상과학 소설가 윌리엄 깁슨은 말했습니다. "미래는 이미 와 있다. 단지 널리 퍼지지 않았을 뿐이다."
오늘 우리가 나눈 이야기들은 먼 미래의 공상과학이 아닙니다. 지금 이 순간에도 수많은 교실에서 실현되고 있는 현재의 이야기입니다.
기술이 아무리 눈부시게 발전해도, 교실의 진짜 기적은 아이들의 손을 잡아주고 눈을 맞춰주는 선생님의 따뜻한 손길에서 시작됩니다.
기술에 압도당하는 교사가 아니라, 기술의 어깨 위에 당당히 올라타 아이들에게 더 넓은 세상을 보여주는 멋진 선생님들이 되시기를 진심으로 응원합니다.
오랜 시간 경청해 주셔서 대단히 감사합니다. 질문 있으신 분은 자유롭게 말씀해 주시기 바랍니다.""")

    # Apply Paperlogy font family across all slides and runs
    print("Applying Paperlogy typography hierarchy across all slides...")
    apply_paperlogy_to_deck(prs)

    # SAVE TO SEPARATE FILE (교육용)
    output_path = 'AI 시대-교육의 문법이 바뀌다-어린왕자.pptx'
    prs.save('AI 시대-교육의 문법이 바뀌다_어린왕자.pptx')
    prs.save(output_path)
    print(f"Little Prince presentation generated successfully: {output_path} and AI 시대-교육의 문법이 바뀌다_어린왕자.pptx")

if __name__ == '__main__':
    build_education_deck()
