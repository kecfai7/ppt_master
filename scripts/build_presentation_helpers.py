import os
import shutil
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

# -------------------------------------------------------------
# CONSTANTS & PALETTE (Google Education Theme)
# -------------------------------------------------------------
COLOR_GOOGLE_BLUE = RGBColor(66, 133, 244)   # #4285F4
COLOR_GOOGLE_RED = RGBColor(234, 67, 53)     # #EA4335
COLOR_GOOGLE_YELLOW = RGBColor(251, 188, 5)  # #FBBC05
COLOR_GOOGLE_GREEN = RGBColor(52, 168, 83)   # #34A853

COLOR_PRIMARY_BLUE = RGBColor(26, 115, 232)  # #1A73E8
COLOR_BG_LIGHT = RGBColor(248, 250, 252)     # #F8FAFC
COLOR_BG_CARD = RGBColor(255, 255, 255)      # #FFFFFF
COLOR_BORDER = RGBColor(226, 232, 240)       # #E2E8F0
COLOR_TEXT_MAIN = RGBColor(30, 41, 59)       # #1E293B
COLOR_TEXT_MUTED = RGBColor(100, 116, 139)   # #64748B
COLOR_DARK_CARD = RGBColor(15, 23, 42)       # #0F172A
COLOR_PILL_BG = RGBColor(232, 240, 254)      # #E8F0FE

FONT_TITLE = "Paperlogy 8 ExtraBold"
FONT_HEADING = "Paperlogy 7 Bold"
FONT_SUBTITLE = "Paperlogy 6 SemiBold"
FONT_BODY = "Paperlogy 5 Medium"
FONT_REGULAR = "Paperlogy 4 Regular"

# -------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------
def set_font_run(r, font_name):
    rPr = r._r.get_or_add_rPr()
    for tag in ['latin', 'ea', 'cs']:
        for child in list(rPr):
            if child.tag.endswith(tag):
                rPr.remove(child)
    rPr.append(parse_xml(f'<a:latin xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="{font_name}"/>'))
    rPr.append(parse_xml(f'<a:ea xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="{font_name}"/>'))
    rPr.append(parse_xml(f'<a:cs xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="{font_name}"/>'))

def set_font_p(p, font_name):
    p.font.name = font_name
    pPr = p._p.get_or_add_pPr()
    defRPr = pPr.get_or_add_defRPr()
    for tag in ['latin', 'ea', 'cs']:
        for child in list(defRPr):
            if child.tag.endswith(tag):
                defRPr.remove(child)
    defRPr.append(parse_xml(f'<a:latin xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="{font_name}"/>'))
    defRPr.append(parse_xml(f'<a:ea xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="{font_name}"/>'))
    defRPr.append(parse_xml(f'<a:cs xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" typeface="{font_name}"/>'))
    for r in p.runs:
        set_font_run(r, font_name)

def apply_paperlogy_to_deck(prs):
    from pptx.enum.shapes import MSO_SHAPE_TYPE
    def process_text_frame(tf):
        for p in tf.paragraphs:
            if not p.text.strip():
                continue
            is_bold = (p.font.bold is True)
            size = p.font.size.pt if p.font.size else 12.0
            
            # Typographic Hierarchy:
            # 1. Slide & section titles (>= 20pt) -> Paperlogy 8 ExtraBold
            # 2. Card headers, key metric headings (>= 12pt bold) -> Paperlogy 7 Bold
            # 3. Badges, pill tags, category chips (< 12pt bold) -> Paperlogy 6 SemiBold
            # 4. Body bullets, descriptive text -> Paperlogy 5 Medium
            if size >= 20:
                font = FONT_TITLE
            elif is_bold and size >= 12:
                font = FONT_HEADING
            elif is_bold:
                font = FONT_SUBTITLE
            else:
                font = FONT_BODY
            
            set_font_p(p, font)
            for r in p.runs:
                r_size = r.font.size.pt if r.font.size else size
                r_bold = r.font.bold if r.font.bold is not None else is_bold
                if r_size >= 20:
                    r_font = FONT_TITLE
                elif r_bold and r_size >= 12:
                    r_font = FONT_HEADING
                elif r_bold:
                    r_font = FONT_SUBTITLE
                else:
                    r_font = font
                set_font_run(r, r_font)

    def process_shape(shape):
        if shape.has_text_frame:
            process_text_frame(shape.text_frame)
        if shape.has_table:
            for row in shape.table.rows:
                for cell in row.cells:
                    process_text_frame(cell.text_frame)
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            for sub_shape in shape.shapes:
                process_shape(sub_shape)

    for slide in prs.slides:
        for shape in slide.shapes:
            process_shape(shape)
        if slide.has_notes_slide:
            process_text_frame(slide.notes_slide.notes_text_frame)

def set_shape_flat_color(shape, bg_rgb, border_rgb=None, border_width_pt=1.0):
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_rgb
    if border_rgb:
        shape.line.color.rgb = border_rgb
        shape.line.width = Pt(border_width_pt)
    else:
        shape.line.fill.background()

def add_header(slide, category_text, title_text, subtitle_text, accent_color=COLOR_GOOGLE_BLUE):
    # Category Pill (Dynamically sized to fit text on a single line with comfortable padding)
    pill_width = max(2.3, round(len(category_text) * 0.105 + 0.5, 2))
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.7), Inches(0.42), Inches(pill_width), Inches(0.3))
    set_shape_flat_color(pill, COLOR_PILL_BG, border_rgb=COLOR_PRIMARY_BLUE, border_width_pt=0.8)
    tf_p = pill.text_frame
    tf_p.word_wrap = False
    tf_p.margin_left = Inches(0.12)
    tf_p.margin_right = Inches(0.12)
    tf_p.margin_top = Inches(0.02)
    tf_p.margin_bottom = Inches(0.02)
    p0 = tf_p.paragraphs[0]
    p0.text = category_text
    p0.font.size = Pt(10)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_PRIMARY_BLUE
    p0.alignment = PP_ALIGN.CENTER
    set_font_p(p0, FONT_SUBTITLE)

    # Title
    t_box = slide.shapes.add_textbox(Inches(0.68), Inches(0.75), Inches(8.6), Inches(0.55))
    tf_t = t_box.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p1 = tf_t.paragraphs[0]
    p1.text = title_text
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_MAIN
    set_font_p(p1, FONT_TITLE)

    # Subtitle
    if subtitle_text:
        s_box = slide.shapes.add_textbox(Inches(0.7), Inches(1.32), Inches(8.6), Inches(0.35))
        tf_s = s_box.text_frame
        tf_s.word_wrap = True
        tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
        p2 = tf_s.paragraphs[0]
        p2.text = subtitle_text
        p2.font.size = Pt(11.5)
        p2.font.color.rgb = COLOR_TEXT_MUTED
        set_font_p(p2, FONT_BODY)

def add_card(slide, left, top, width, height, bg_rgb=COLOR_BG_CARD, border_rgb=COLOR_BORDER, border_width_pt=1.0, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE):
    card = slide.shapes.add_shape(shape_type, left, top, width, height)
    set_shape_flat_color(card, bg_rgb, border_rgb, border_width_pt)
    return card

def add_indicator_bar(slide, left, top, width, height, bar_color):
    bar = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    set_shape_flat_color(bar, bar_color)
    return bar

def set_speaker_notes(slide, notes_text):
    if not slide.has_notes_slide:
        slide.notes_slide
    tf = slide.notes_slide.notes_text_frame
    tf.text = notes_text.strip()

def configure_video_autoplay_loop(slide, movie_shape):
    spid = str(movie_shape.shape_id)
    
    # 1. Cleanly remove ANY default timing element generated by python-pptx (which defaults to delay="indefinite")
    for child in list(slide._element):
        if child.tag.endswith('timing'):
            slide._element.remove(child)

    # 2. Append the single, standard PowerPoint OpenXML timing node that triggers playback immediately (delay="0") and loops indefinitely
    timing_xml = f'''<p:timing xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:tnLst>
    <p:par>
      <p:cTn id="1" dur="indefinite" restart="always" nodeType="tmRoot">
        <p:childTnLst>
          <p:seq concurrent="1" nextAc="seek">
            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
              <p:childTnLst>
                <p:par>
                  <p:cTn id="3" fill="hold">
                    <p:stCondLst>
                      <p:cond delay="0"/>
                    </p:stCondLst>
                    <p:childTnLst>
                      <p:par>
                        <p:cTn id="4" fill="hold" presetID="1" presetClass="mediacall" presetSubtype="0">
                          <p:childTnLst>
                            <p:cmd type="call" cmd="playFrom(0.0)">
                              <p:cBhvr>
                                <p:cTn id="5" dur="indefinite" fill="hold" repeatCount="indefinite">
                                  <p:stCondLst>
                                    <p:cond delay="0"/>
                                  </p:stCondLst>
                                </p:cTn>
                                <p:tgtEl>
                                  <p:spTgt spid="{spid}"/>
                                </p:tgtEl>
                              </p:cBhvr>
                            </p:cmd>
                          </p:childTnLst>
                        </p:cTn>
                      </p:par>
                    </p:childTnLst>
                  </p:cTn>
                </p:par>
              </p:childTnLst>
            </p:cTn>
          </p:seq>
          <p:video>
            <p:cMediaNode rptCount="indefinite" vol="80000">
              <p:cTn id="6" fill="hold" display="0">
                <p:stCondLst>
                  <p:cond delay="0"/>
                </p:stCondLst>
              </p:cTn>
              <p:tgtEl>
                <p:spTgt spid="{spid}"/>
              </p:tgtEl>
            </p:cMediaNode>
          </p:video>
        </p:childTnLst>
      </p:cTn>
    </p:par>
  </p:tnLst>
</p:timing>'''
    slide._element.append(parse_xml(timing_xml))

print("Helper functions updated with robust single-timing autoplay logic!")
