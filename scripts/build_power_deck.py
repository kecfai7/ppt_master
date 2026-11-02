import os
import re
import io
import json
import zipfile
import soundfile as sf
from xml.etree import ElementTree as ET

import sys
sys.path.append('ppt-master/skills/ppt-master/scripts/svg_to_pptx')
sys.path.append('ppt-master/skills/ppt-master/scripts')

import pptx_animations as anim
import pptx_package.narration as narr
from pptx_transitions import P14_NS, PML_NS

SOURCE_PPTX = "AI 시대-교육의 문법이 바뀌다-어린왕자.pptx"
OUTPUT_PPTX = "AI 시대-교육의 문법이 바뀌다-어린왕자-자율재생-애니메이션.pptx"
AUDIO_DIR = "projects/ai_edu_roundtrip/audio"

print("Starting build of Little Prince Power Deck...")

# 1. Read audio durations
audio_durations = {}
for i in range(1, 23):
    mp3_file = os.path.join(AUDIO_DIR, f"slide_{i:02d}.mp3")
    if os.path.exists(mp3_file):
        data, sr = sf.read(mp3_file)
        audio_durations[i] = len(data) / float(sr)
    else:
        audio_durations[i] = 10.0
    print(f"Slide {i:02d} audio duration: {audio_durations[i]:.2f}s")

# 2. Process PPTX as zip
with open(SOURCE_PPTX, "rb") as f:
    in_zip_bytes = f.read()

in_zip = zipfile.ZipFile(io.BytesIO(in_zip_bytes), "r")
out_buf = io.BytesIO()
out_zip = zipfile.ZipFile(out_buf, "w", compression=zipfile.ZIP_DEFLATED)

# Copy all files except slides and slide rels which we modify
slide_files = [n for n in in_zip.namelist() if re.match(r"^ppt/slides/slide\d+\.xml$", n)]
slide_files.sort(key=lambda x: int(re.search(r"\d+", x).group()))

print(f"Found {len(slide_files)} slides in {SOURCE_PPTX}")

# Ensure Content_Types has mp3 and wav
content_types_xml = in_zip.read("[Content_Types].xml").decode("utf-8")
if '<Default Extension="mp3"' not in content_types_xml:
    content_types_xml = content_types_xml.replace(
        "</Types>",
        '  <Default Extension="mp3" ContentType="audio/mpeg"/>\n  <Default Extension="wav" ContentType="audio/wav"/>\n</Types>'
    )
out_zip.writestr("[Content_Types].xml", content_types_xml.encode("utf-8"))

# Ensure presentation.xml has useTimings="1"
pres_xml = in_zip.read("ppt/presentation.xml").decode("utf-8")
# Check if <p:showPr> has useTimings
if "<p:showPr" in pres_xml:
    if 'useTimings="0"' in pres_xml:
        pres_xml = pres_xml.replace('useTimings="0"', 'useTimings="1"')
    elif 'useTimings="1"' not in pres_xml:
        pres_xml = pres_xml.replace("<p:showPr", '<p:showPr useTimings="1"')
else:
    pres_xml = pres_xml.replace("</p:presentation>", '  <p:showPr useTimings="1"/>\n</p:presentation>')
out_zip.writestr("ppt/presentation.xml", pres_xml.encode("utf-8"))

# Write audio marker icon into media
audio_marker_part = "ppt/media/narration_marker.png"
out_zip.writestr(audio_marker_part, narr.AUDIO_MARKER_PNG_BYTES)

for idx, slide_path in enumerate(slide_files, 1):
    slide_xml = in_zip.read(slide_path).decode("utf-8")
    rels_path = f"ppt/slides/_rels/{os.path.basename(slide_path)}.rels"
    if rels_path in in_zip.namelist():
        rels_xml = in_zip.read(rels_path).decode("utf-8")
    else:
        rels_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"/>'

    audio_file = os.path.join(AUDIO_DIR, f"slide_{idx:02d}.mp3")
    audio_data = open(audio_file, "rb").read()
    audio_media_name = f"narration_{idx:02d}.mp3"
    audio_media_path = f"ppt/media/{audio_media_name}"
    out_zip.writestr(audio_media_path, audio_data)

    # Add relationships in rels
    root_rels = ET.fromstring(rels_xml)
    rel_ids = [int(re.search(r"\d+", r.get("Id", "0")).group()) for r in root_rels if re.search(r"\d+", r.get("Id", "0"))]
    next_rid = max(rel_ids, default=0) + 1

    rid_audio = f"rId{next_rid}"
    rid_media = f"rId{next_rid + 1}"
    rid_poster = f"rId{next_rid + 2}"

    # Rel for audioFile
    rel_a = ET.SubElement(root_rels, "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship")
    rel_a.set("Id", rid_audio)
    rel_a.set("Type", narr.AUDIO_REL_TYPE)
    rel_a.set("Target", f"../media/{audio_media_name}")

    # Rel for media
    rel_m = ET.SubElement(root_rels, "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship")
    rel_m.set("Id", rid_media)
    rel_m.set("Type", narr.MEDIA_REL_TYPE)
    rel_m.set("Target", f"../media/{audio_media_name}")

    # Rel for poster
    rel_p = ET.SubElement(root_rels, "{http://schemas.openxmlformats.org/package/2006/relationships}Relationship")
    rel_p.set("Id", rid_poster)
    rel_p.set("Type", narr.IMAGE_REL_TYPE)
    rel_p.set("Target", "../media/narration_marker.png")

    rels_updated = ET.tostring(root_rels, encoding="utf-8", xml_declaration=True)
    out_zip.writestr(rels_path, rels_updated)

    # 1. Element animations (for slides 2-22)
    # Slide 1 has the video loop timing; slides 2-22 get wipe/fade object animations!
    if idx > 1:
        # Parse slide_xml to find shapes
        root_sld = narr.parse_source_xml(slide_xml)
        spTree = root_sld.find(f"{narr._qn(PML_NS, 'cSld')}/{narr._qn(PML_NS, 'spTree')}")
        
        # Collect shape IDs excluding background image (first shape or pic)
        content_shape_ids = []
        if spTree is not None:
            for child in spTree:
                cNvPr = child.find(f".//{narr._qn(PML_NS, 'cNvPr')}")
                if cNvPr is not None:
                    sid = int(cNvPr.get("id"))
                    name = cNvPr.get("name", "")
                    # Don't animate background image
                    if sid == 1 or "Picture 1" in name or "bg_" in name:
                        continue
                    content_shape_ids.append((sid, name))
        
        # Build targets: header/pill/title fade, cards fade, bullets wipe
        targets = []
        delay = 0
        for sid, name in content_shape_ids:
            if "TextBox" in name or "Pill" in name:
                effect = "entrance_wipe"
            elif "Rounded Rectangle" in name:
                effect = "entrance_fade"
            else:
                effect = "entrance_wipe"
            targets.append((sid, delay, effect, 0.4))
            delay += 150 # 150ms cascade
        
        if targets:
            anim_timing_xml = anim.create_sequence_timing_xml(targets, duration=0.4, trigger="after-previous")
            # Inject anim_timing_xml into slide_xml
            # Remove any existing timing
            for child in list(root_sld):
                if child.tag == narr._qn(PML_NS, "timing"):
                    root_sld.remove(child)
            # Append timing from anim_timing_xml with namespace
            p_ns_timing = anim_timing_xml.replace('<p:timing>', '<p:timing xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">', 1)
            t_elem = ET.fromstring(p_ns_timing)
            # insert before extLst if present
            extLst = root_sld.find(narr._qn(PML_NS, "extLst"))
            if extLst is not None:
                idx_ext = list(root_sld).index(extLst)
                root_sld.insert(idx_ext, t_elem)
            else:
                root_sld.append(t_elem)
            slide_xml = ET.tostring(root_sld, encoding="unicode")

    # 2. Inject audio narration shape and audio timing
    shape_id = narr.next_shape_id(slide_xml)
    slide_xml = narr.inject_narration(
        slide_xml,
        shape_id=shape_id,
        shape_name=f"narration{idx}.mp3",
        audio_rid=rid_audio,
        media_rid=rid_media,
        poster_rid=rid_poster,
        start_delay=0.4
    )

    # 3. Apply auto-advance timing matching narration duration + 0.8s padding
    duration = audio_durations.get(idx, 10.0)
    advance_after = duration + 0.8
    slide_xml = narr.apply_recorded_timing(
        slide_xml,
        advance_after=advance_after,
        transition_duration=0.5,
        transition_effect="fade"
    )

    out_zip.writestr(slide_path, slide_xml.encode("utf-8"))
    print(f"Processed Slide {idx:02d}: Narration injected ({duration:.2f}s audio), Transition: Fade (0.5s), Advance after: {advance_after:.2f}s")

# Copy all other files from in_zip
for item in in_zip.infolist():
    if item.filename in ["[Content_Types].xml", "ppt/presentation.xml"] or item.filename in slide_files or item.filename.startswith("ppt/slides/_rels/"):
        continue
    out_zip.writestr(item, in_zip.read(item.filename))

out_zip.close()
in_zip.close()

with open(OUTPUT_PPTX, "wb") as f:
    f.write(out_buf.getvalue())

print(f"\n[SUCCESS] Generated Power Deck: {OUTPUT_PPTX}")
print(f"File size: {os.path.getsize(OUTPUT_PPTX):,} bytes")
