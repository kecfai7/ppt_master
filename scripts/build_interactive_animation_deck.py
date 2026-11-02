import os
import re
import io
import zipfile

SOURCE_PPTX = "어린왕자-자율재생.pptx"
TARGET_PPTX = "AI 시대-교육의 문법이 바뀌다-어린왕자-자율재생-애니메이션.pptx"

print("======================================================================")
print("Restoring Complete Animations + Configuring Click Advance + Controllable Audio")
print(f"Base Template with Valid Animations: {SOURCE_PPTX}")
print(f"Target Deck: {TARGET_PPTX}")
print("======================================================================")

if not os.path.exists(SOURCE_PPTX):
    raise FileNotFoundError(f"Cannot find source {SOURCE_PPTX}")

with open(SOURCE_PPTX, "rb") as f:
    in_bytes = f.read()

in_zip = zipfile.ZipFile(io.BytesIO(in_bytes), "r")
out_buf = io.BytesIO()
out_zip = zipfile.ZipFile(out_buf, "w", compression=zipfile.ZIP_DEFLATED)

# 1. Update [Content_Types].xml
ct_xml = in_zip.read("[Content_Types].xml").decode("utf-8")
if '<Default Extension="mp3"' not in ct_xml:
    ct_xml = ct_xml.replace(
        "</Types>",
        '  <Default Extension="mp3" ContentType="audio/mpeg"/>\n  <Default Extension="wav" ContentType="audio/wav"/>\n</Types>'
    )
out_zip.writestr("[Content_Types].xml", ct_xml.encode("utf-8"))

# 2. Update presentation.xml: remove useTimings="1"
pres_xml = in_zip.read("ppt/presentation.xml").decode("utf-8")
pres_xml = re.sub(r'<p:showPr\b[^>]*>', '<p:showPr/>', pres_xml)
out_zip.writestr("ppt/presentation.xml", pres_xml.encode("utf-8"))

# 3. Process each slide
slide_files = [n for n in in_zip.namelist() if re.match(r"^ppt/slides/slide\d+\.xml$", n)]

AUDIO_X = 8046720
AUDIO_Y = 4343400
AUDIO_CX = 457200
AUDIO_CY = 457200

for fname in in_zip.namelist():
    if fname in ["[Content_Types].xml", "ppt/presentation.xml"]:
        continue
    
    if fname in slide_files:
        slide_xml = in_zip.read(fname).decode("utf-8")
        
        # A. Transition: Change from auto-advance (advOn="1" advTm="...") to manual click advance (advClick="1")
        if "<p:transition" in slide_xml:
            def repl_trans(m):
                inner = m.group(1)
                return f'<p:transition advClick="1">{inner}</p:transition>'
            slide_xml = re.sub(r'<p:transition\b[^>]*>(.*?)</p:transition>', repl_trans, slide_xml, flags=re.DOTALL)
        else:
            slide_xml = slide_xml.replace('</p:sld>', '<p:transition advClick="1"><p:fade dur="500"/></p:transition></p:sld>')
            
        # B. Make Audio visible & controllable: remove display="0" from <p:cMediaNode>
        slide_xml = re.sub(r'(<p:cMediaNode\b[^>]*>.*?<p:cTn\b[^>]*)\s+display="0"', r'\1', slide_xml, flags=re.DOTALL)
        
        # C. Resize and reposition the audio shape so it doesn't cover the entire slide
        media_spids = re.findall(r'<p:spTgt spid="(\d+)"/></p:tgtEl></p:cMediaNode>', slide_xml)
        for spid in media_spids:
            if fname == "ppt/slides/slide1.xml" and spid == "2":
                continue # video
            
            pattern = rf'(<p:pic\b[^>]*>.*?<p:cNvPr\b[^>]*\bid="{spid}".*?)(<a:xfrm>)(.*?)(</a:xfrm>)(.*?</p:pic>)'
            def repl_xfrm(m):
                prefix = m.group(1)
                suffix = m.group(5)
                new_xfrm = f'<a:xfrm><a:off x="{AUDIO_X}" y="{AUDIO_Y}"/><a:ext cx="{AUDIO_CX}" cy="{AUDIO_CY}"/></a:xfrm>'
                return prefix + new_xfrm + suffix
            
            slide_xml = re.sub(pattern, repl_xfrm, slide_xml, flags=re.DOTALL)
            
        out_zip.writestr(fname, slide_xml.encode("utf-8"))
    else:
        out_zip.writestr(fname, in_zip.read(fname))

out_zip.close()
final_data = out_buf.getvalue()

with open(TARGET_PPTX, "wb") as f:
    f.write(final_data)

with open("어린왕자.pptx", "wb") as f:
    f.write(final_data)

print(f"[성공] {TARGET_PPTX} ({len(final_data):,} bytes) 복구 및 최적화 완료!")
