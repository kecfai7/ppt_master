import os
import sys
import soundfile as sf
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

# Import original deck builder logic
import generate_little_prince_deck as lp
from build_presentation_helpers import apply_paperlogy_to_deck

AUDIO_DIR = 'projects/ai_edu_roundtrip/audio'

def build_autoplay_timing_slide1(video_spid, audio_spid, audio_dur_ms):
    return f'''<p:timing xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:tnLst>
    <p:par>
      <p:cTn id="1" dur="indefinite" restart="always" nodeType="tmRoot">
        <p:childTnLst>
          <p:seq concurrent="1" nextAc="seek">
            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
              <p:childTnLst>
                <!-- Video Loop Autoplay -->
                <p:par>
                  <p:cTn id="3" fill="hold">
                    <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                    <p:childTnLst>
                      <p:par>
                        <p:cTn id="4" fill="hold" presetID="1" presetClass="mediacall" presetSubtype="0">
                          <p:childTnLst>
                            <p:cmd type="call" cmd="playFrom(0.0)">
                              <p:cBhvr>
                                <p:cTn id="5" dur="indefinite" fill="hold" repeatCount="indefinite">
                                  <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                                </p:cTn>
                                <p:tgtEl><p:spTgt spid="{video_spid}"/></p:tgtEl>
                              </p:cBhvr>
                            </p:cmd>
                          </p:childTnLst>
                        </p:cTn>
                      </p:par>
                    </p:childTnLst>
                  </p:cTn>
                </p:par>
                <!-- Audio Narration Autoplay -->
                <p:par>
                  <p:cTn id="6" fill="hold">
                    <p:stCondLst><p:cond delay="300"/></p:stCondLst>
                    <p:childTnLst>
                      <p:par>
                        <p:cTn id="7" fill="hold" presetID="1" presetClass="mediacall" presetSubtype="0">
                          <p:childTnLst>
                            <p:cmd type="call" cmd="playFrom(0.0)">
                              <p:cBhvr>
                                <p:cTn id="8" dur="{audio_dur_ms}" fill="hold">
                                  <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                                </p:cTn>
                                <p:tgtEl><p:spTgt spid="{audio_spid}"/></p:tgtEl>
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
          <!-- Media Nodes -->
          <p:video>
            <p:cMediaNode rptCount="indefinite" vol="80000">
              <p:cTn id="9" fill="hold" display="0">
                <p:stCondLst><p:cond delay="0"/></p:stCondLst>
              </p:cTn>
              <p:tgtEl><p:spTgt spid="{video_spid}"/></p:tgtEl>
            </p:cMediaNode>
          </p:video>
          <p:video>
            <p:cMediaNode vol="80000">
              <p:cTn id="10" fill="hold" display="0">
                <p:stCondLst><p:cond delay="300"/></p:stCondLst>
              </p:cTn>
              <p:tgtEl><p:spTgt spid="{audio_spid}"/></p:tgtEl>
            </p:cMediaNode>
          </p:video>
        </p:childTnLst>
      </p:cTn>
    </p:par>
  </p:tnLst>
</p:timing>'''

def build_autoplay_timing_content_slide(audio_spid, audio_dur_ms, anim_shapes):
    # anim_shapes is list of (spid, effect_type)
    # effect_type: 'wipe' or 'fade'
    
    anim_pars = ""
    curr_id = 6
    curr_delay = 200
    for spid, eff in anim_shapes:
        if eff == 'fade':
            preset_id = "10"
            filter_str = "fade"
        else:
            preset_id = "22"
            filter_str = "wipe(down)"
        
        anim_pars += f'''
                <p:par>
                  <p:cTn id="{curr_id}" fill="hold">
                    <p:stCondLst><p:cond delay="{curr_delay}"/></p:stCondLst>
                    <p:childTnLst>
                      <p:par>
                        <p:cTn id="{curr_id+1}" presetID="{preset_id}" presetClass="entr" presetSubtype="0" fill="hold" nodeType="afterEffect">
                          <p:childTnLst>
                            <p:set>
                              <p:cBhvr>
                                <p:cTn id="{curr_id+2}" dur="1" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst></p:cTn>
                                <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
                                <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
                              </p:cBhvr>
                              <p:to><p:strVal val="visible"/></p:to>
                            </p:set>
                            <p:animEffect transition="in" filter="{filter_str}">
                              <p:cBhvr>
                                <p:cTn id="{curr_id+3}" dur="350"/>
                                <p:tgtEl><p:spTgt spid="{spid}"/></p:tgtEl>
                              </p:cBhvr>
                            </p:animEffect>
                          </p:childTnLst>
                        </p:cTn>
                      </p:par>
                    </p:childTnLst>
                  </p:cTn>
                </p:par>'''
        curr_id += 4
        curr_delay += 120

    media_node_id = curr_id + 1

    return f'''<p:timing xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
  <p:tnLst>
    <p:par>
      <p:cTn id="1" dur="indefinite" restart="always" nodeType="tmRoot">
        <p:childTnLst>
          <p:seq concurrent="1" nextAc="seek">
            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
              <p:childTnLst>
                <!-- Audio Narration Autoplay -->
                <p:par>
                  <p:cTn id="3" fill="hold">
                    <p:stCondLst><p:cond delay="100"/></p:stCondLst>
                    <p:childTnLst>
                      <p:par>
                        <p:cTn id="4" fill="hold" presetID="1" presetClass="mediacall" presetSubtype="0">
                          <p:childTnLst>
                            <p:cmd type="call" cmd="playFrom(0.0)">
                              <p:cBhvr>
                                <p:cTn id="5" dur="1" fill="hold">
                                  <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                                </p:cTn>
                                <p:tgtEl><p:spTgt spid="{audio_spid}"/></p:tgtEl>
                              </p:cBhvr>
                            </p:cmd>
                          </p:childTnLst>
                        </p:cTn>
                      </p:par>
                    </p:childTnLst>
                  </p:cTn>
                </p:par>
                {anim_pars}
              </p:childTnLst>
            </p:cTn>
          </p:seq>
          <!-- Audio Media Node -->
          <p:video>
            <p:cMediaNode vol="80000">
              <p:cTn id="{media_node_id}" fill="hold" display="0">
                <p:stCondLst><p:cond delay="100"/></p:stCondLst>
              </p:cTn>
              <p:tgtEl><p:spTgt spid="{audio_spid}"/></p:tgtEl>
            </p:cMediaNode>
          </p:video>
        </p:childTnLst>
      </p:cTn>
    </p:par>
  </p:tnLst>
</p:timing>'''

def build_perfect_autoplay_deck():
    print("Step 1: Reading base presentation 'AI 시대-교육의 문법이 바뀌다-어린왕자.pptx'...")
    prs = Presentation('AI 시대-교육의 문법이 바뀌다-어린왕자.pptx')
    
    print(f"Total slides to process: {len(prs.slides)}")
    
    for idx, slide in enumerate(prs.slides, 1):
        mp3_path = os.path.join(AUDIO_DIR, f"slide_{idx:02d}.mp3")
        if not os.path.exists(mp3_path):
            print(f"Warning: audio {mp3_path} not found!")
            continue
            
        data, sr = sf.read(mp3_path)
        dur_sec = len(data) / float(sr)
        dur_ms = int(dur_sec * 1000)
        adv_tm_ms = dur_ms + 800  # 800ms silence before advance
        
        # 1. Cleanly remove ANY previous timing and transition elements
        for child in list(slide._element):
            if child.tag.endswith('timing') or child.tag.endswith('transition'):
                slide._element.remove(child)
                
        # 2. Add audio shape off-canvas (size 0.1x0.1 inches at -1, -1)
        audio_shape = slide.shapes.add_movie(
            mp3_path,
            Inches(-1), Inches(-1), Inches(0.1), Inches(0.1),
            mime_type='audio/mp3'
        )
        audio_spid = str(audio_shape.shape_id)
        
        # 3. Clean python-pptx default timing that add_movie just added
        for child in list(slide._element):
            if child.tag.endswith('timing'):
                slide._element.remove(child)
                
        # 4. Construct timing node
        if idx == 1:
            # Slide 1 has the video loop (shape 0 which has id 2)
            video_spid = str(slide.shapes[0].shape_id)
            timing_xml = build_autoplay_timing_slide1(video_spid, audio_spid, dur_ms)
        else:
            # Collect content shapes to animate (excluding background image which is shape 0)
            anim_shapes = []
            for shp in slide.shapes:
                sid = str(shp.shape_id)
                if sid == audio_spid or shp == slide.shapes[0]:
                    continue
                name = shp.name
                if "TextBox" in name or "Pill" in name:
                    eff = "wipe"
                else:
                    eff = "fade"
                anim_shapes.append((sid, eff))
            timing_xml = build_autoplay_timing_content_slide(audio_spid, dur_ms, anim_shapes)
            
        slide._element.append(parse_xml(timing_xml))
        
        # 5. Add slide transition with auto-advance timing
        transition_xml = f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" advOn="1" advTm="{adv_tm_ms}"><p:fade dur="500"/></p:transition>'
        slide._element.append(parse_xml(transition_xml))
        
        print(f"Slide {idx:02d}: Narration {dur_sec:.2f}s, Autoplay mediacall configured, Auto-advance at {adv_tm_ms/1000:.2f}s")

    # Save to 어린왕자-자율재생.pptx
    out_pptx = "어린왕자-자율재생.pptx"
    out_ppsx = "어린왕자-자율재생.ppsx"
    
    prs.save(out_pptx)
    prs.save(out_ppsx)
    prs.save("AI 시대-교육의 문법이 바뀌다-어린왕자-자율재생-애니메이션.pptx")
    prs.save("어린왕자.pptx")
    
    print("\n============================================================")
    print(f" [성공] 완벽한 자동 실행 파워포인트 생성 완료!")
    print(f" 1. PPTX: {out_pptx} ({os.path.getsize(out_pptx):,} bytes)")
    print(f" 2. PPSX (쇼 바로 실행): {out_ppsx} ({os.path.getsize(out_ppsx):,} bytes)")
    print("============================================================")

if __name__ == '__main__':
    build_perfect_autoplay_deck()

