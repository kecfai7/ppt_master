import os
import re
import io
import zipfile
import glob

# Master Font Normalizer for all presentations
def normalize_deck_fonts(pptx_path):
    with open(pptx_path, "rb") as f:
        in_bytes = f.read()
    
    in_zip = zipfile.ZipFile(io.BytesIO(in_bytes), "r")
    out_buf = io.BytesIO()
    out_zip = zipfile.ZipFile(out_buf, "w", compression=zipfile.ZIP_DEFLATED)
    
    for fname in in_zip.namelist():
        data = in_zip.read(fname)
        
        # 1. Slides
        if fname.startswith("ppt/slides/slide") and fname.endswith(".xml"):
            xml_str = data.decode("utf-8")
            
            # Normalize latin, ea, and cs typefaces to 'Paperlogy'
            pattern = r'<a:(latin|ea|cs)\s+typeface="(?:Paperlogy[^"]*|페이퍼로지[^"]*|Arial|맑은\s*고딕|Calibri)"'
            xml_str = re.sub(pattern, r'<a:\1 typeface="Paperlogy"', xml_str)
            data = xml_str.encode("utf-8")
            
        # 2. Master & Layouts
        elif (fname.startswith("ppt/slideMasters/") or fname.startswith("ppt/slideLayouts/")) and fname.endswith(".xml"):
            xml_str = data.decode("utf-8")
            pattern = r'<a:(latin|ea|cs)\s+typeface="(?:Paperlogy[^"]*|페이퍼로지[^"]*|Arial|맑은\s*고딕|Calibri)"'
            xml_str = re.sub(pattern, r'<a:\1 typeface="Paperlogy"', xml_str)
            data = xml_str.encode("utf-8")
            
        # 3. Theme
        elif fname.startswith("ppt/theme/theme") and fname.endswith(".xml"):
            xml_str = data.decode("utf-8")
            xml_str = re.sub(r'<a:font\s+script="Hang"\s+typeface="[^"]*"', '<a:font script="Hang" typeface="Paperlogy"', xml_str)
            xml_str = re.sub(r'<a:majorFont>(.*?)<a:latin\s+typeface="[^"]*"', r'<a:majorFont>\1<a:latin typeface="Paperlogy"', xml_str, flags=re.DOTALL)
            xml_str = re.sub(r'<a:majorFont>(.*?)<a:ea\s+typeface="[^"]*"', r'<a:majorFont>\1<a:ea typeface="Paperlogy"', xml_str, flags=re.DOTALL)
            xml_str = re.sub(r'<a:minorFont>(.*?)<a:latin\s+typeface="[^"]*"', r'<a:minorFont>\1<a:latin typeface="Paperlogy"', xml_str, flags=re.DOTALL)
            xml_str = re.sub(r'<a:minorFont>(.*?)<a:ea\s+typeface="[^"]*"', r'<a:minorFont>\1<a:ea typeface="Paperlogy"', xml_str, flags=re.DOTALL)
            data = xml_str.encode("utf-8")
            
        out_zip.writestr(fname, data)
        
    out_zip.close()
    with open(pptx_path, "wb") as f:
        f.write(out_buf.getvalue())
    print(f"Normalized all fonts to Paperlogy in: {os.path.basename(pptx_path)}")

all_decks = glob.glob("presentations/*.pptx") + glob.glob("presentations/*.ppsx")
print(f"Normalizing fonts to Paperlogy across {len(all_decks)} decks...")
for d in all_decks:
    normalize_deck_fonts(d)

print("All decks normalized to canonical 'Paperlogy'!")
