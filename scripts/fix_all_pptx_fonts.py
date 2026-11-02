import os
import re
import io
import zipfile
import glob

FONT_MAP = {
    "Paperlogy 8 ExtraBold": "페이퍼로지 8 ExtraBold",
    "Paperlogy 7 Bold": "페이퍼로지 7 Bold",
    "Paperlogy 6 SemiBold": "페이퍼로지 6 SemiBold",
    "Paperlogy 5 Medium": "페이퍼로지 5 Medium",
    "Paperlogy 4 Regular": "페이퍼로지 4 Regular",
    "Paperlogy 3 Light": "페이퍼로지 3 Light",
    "Paperlogy 2 ExtraLight": "페이퍼로지 2 ExtraLight",
    "Paperlogy 1 Thin": "페이퍼로지 1 Thin",
    "Paperlogy 9 Black": "페이퍼로지 9 Black",
    "Paperlogy": "페이퍼로지 6 SemiBold",
}

def fix_deck_fonts(pptx_path):
    with open(pptx_path, "rb") as f:
        in_bytes = f.read()
    
    in_zip = zipfile.ZipFile(io.BytesIO(in_bytes), "r")
    out_buf = io.BytesIO()
    out_zip = zipfile.ZipFile(out_buf, "w", compression=zipfile.ZIP_DEFLATED)
    
    modified = False
    
    for fname in in_zip.namelist():
        data = in_zip.read(fname)
        
        # 1. Slide files: fix <a:ea typeface="..."> and <a:cs typeface="...">
        if fname.startswith("ppt/slides/slide") and fname.endswith(".xml"):
            xml_text = data.decode("utf-8")
            old_xml = xml_text
            
            # Map ea typeface to Korean font name
            for eng, kor in FONT_MAP.items():
                xml_text = re.sub(rf'<a:ea\s+typeface="{re.escape(eng)}"', f'<a:ea typeface="{kor}"', xml_text)
                xml_text = re.sub(rf'<a:cs\s+typeface="{re.escape(eng)}"', f'<a:cs typeface="{kor}"', xml_text)
            
            if xml_text != old_xml:
                modified = True
                data = xml_text.encode("utf-8")
                
        # 2. Slide Master & Layouts
        elif (fname.startswith("ppt/slideMasters/") or fname.startswith("ppt/slideLayouts/")) and fname.endswith(".xml"):
            xml_text = data.decode("utf-8")
            old_xml = xml_text
            for eng, kor in FONT_MAP.items():
                xml_text = re.sub(rf'<a:ea\s+typeface="{re.escape(eng)}"', f'<a:ea typeface="{kor}"', xml_text)
                xml_text = re.sub(rf'<a:cs\s+typeface="{re.escape(eng)}"', f'<a:cs typeface="{kor}"', xml_text)
            if xml_text != old_xml:
                modified = True
                data = xml_text.encode("utf-8")
                
        # 3. Theme file: replace Malgun Gothic with Paperlogy
        elif fname.startswith("ppt/theme/theme") and fname.endswith(".xml"):
            xml_text = data.decode("utf-8")
            xml_text = re.sub(r'<a:font\s+script="Hang"\s+typeface="[^"]*"', '<a:font script="Hang" typeface="페이퍼로지 7 Bold"', xml_text)
            xml_text = re.sub(r'<a:majorFont>(\s*)<a:latin\s+typeface="[^"]*"', r'<a:majorFont>\1<a:latin typeface="Paperlogy 8 ExtraBold"', xml_text)
            xml_text = re.sub(r'<a:majorFont>(.*?)<a:ea\s+typeface="[^"]*"', r'<a:majorFont>\1<a:ea typeface="페이퍼로지 8 ExtraBold"', xml_text, flags=re.DOTALL)
            xml_text = re.sub(r'<a:minorFont>(\s*)<a:latin\s+typeface="[^"]*"', r'<a:minorFont>\1<a:latin typeface="Paperlogy 5 Medium"', xml_text)
            xml_text = re.sub(r'<a:minorFont>(.*?)<a:ea\s+typeface="[^"]*"', r'<a:minorFont>\1<a:ea typeface="페이퍼로지 5 Medium"', xml_text, flags=re.DOTALL)
            modified = True
            data = xml_text.encode("utf-8")
            
        out_zip.writestr(fname, data)
        
    out_zip.close()
    
    with open(pptx_path, "wb") as f:
        f.write(out_buf.getvalue())
    print(f"Fixed fonts in: {os.path.basename(pptx_path)}")

# Apply to all decks in presentations/
all_decks = glob.glob("presentations/*.pptx") + glob.glob("presentations/*.ppsx")
print(f"Applying Paperlogy Korean FaceName mapping to {len(all_decks)} decks...")
for d in all_decks:
    fix_deck_fonts(d)

print("All decks updated with exact Windows GDI Paperlogy FaceNames!")

